import logging
import pandas as pd
from tqdm import tqdm
import mhcflurry
import streamlit as st

@st.cache_resource
def reformat_allele_names(alleles_list, prefix):
    formatted_alleles = [f'{prefix}*{allele.split(":")[0]}:{allele.split(":")[1]}' 
                         if '*' not in allele else allele for allele in alleles_list if pd.notna(allele)]
    formatted_alleles = [f'HLA-{allele.split(":")[0]}:{allele.split(":")[1]}' 
                         if not allele.startswith('HLA-') else allele for allele in formatted_alleles]
    return formatted_alleles

@st.cache_resource
def run_batch(_predictor, batch, predictions_list, problematic_alleles, problematic_data):
    filtered_batch = [(pep, allele) for pep, allele in batch if allele not in problematic_alleles]
    if not filtered_batch:
        return problematic_data
    peptides, alleles = zip(*filtered_batch)
    try:
        prediction_batch = _predictor.predict_to_dataframe(peptides, alleles)
        predictions_list.append(prediction_batch)
    except (KeyError, ValueError) as e:
        logging.error(f"Exception caught: {str(e)}")
        
        # Extract allele from error message; if that fails, log the failure
        try:
            problematic_allele = str(e).split("'")[1]
        except IndexError:
            logging.error("Failed to extract allele from exception message.")
            return problematic_data
        
        for peptide, allele in filtered_batch:
            if allele == problematic_allele:
                problematic_entry = {'allele': allele, 'peptide': peptide, 'prediction_percentile': None}
                problematic_data.append(problematic_entry)
                problematic_alleles.add(problematic_allele)
        
        if problematic_data:
            logging.info(f"Added to problematic_data: {problematic_data[-1]}")
    return problematic_data

@st.cache_resource
def get_binding_prediction(peptides_df, cell_lines_df):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize a list for problematic alleles
    problematic_data = []

    # Load data and predictor
    # peptides_df = pd.read_excel('Peptide Lists.xlsx')
    # cell_lines_df = pd.read_excel('Cell Lines.xlsx')
    predictor = mhcflurry.Class1AffinityPredictor.load()

    # Initialize variables
    unique_pairs = []
    pair_info = {}
    filtered_pairs = []
    unsupported_pairs = []
    predictions_list = []
    batch_size = 100

    # Process cell lines and peptides
    cell_lines_records = cell_lines_df.to_dict('records')
    peptides_records = peptides_df.to_dict('records')

    for row in tqdm(cell_lines_records, desc='Processing Cell Lines', leave=True, position = 0):
        cell_line = row['Name']
        alleles_a = reformat_allele_names(str(row['HLA-A']).split(','), 'A') if pd.notna(row['HLA-A']) else []
        alleles_b = reformat_allele_names(str(row['HLA-B']).split(','), 'B') if pd.notna(row['HLA-B']) else []
        alleles_c = reformat_allele_names(str(row['HLA-C']).split(','), 'C') if pd.notna(row['HLA-C']) else []
        all_alleles = alleles_a + alleles_b + alleles_c

        for peptide_row in peptides_records:
            peptide = peptide_row['Sequence']
            for allele in all_alleles:
                pair = (peptide, allele)
                if pair not in unique_pairs:
                    unique_pairs.append(pair)
                    pair_info[pair] = {'Cell Line': [cell_line], 'Mutation': [row['Mutation']]}
                else:
                    pair_info[pair]['Cell Line'].append(cell_line)
                    pair_info[pair]['Mutation'].append(row['Mutation'])

    # Filter pairs
    supported_alleles = set(predictor.supported_alleles)
    for peptide, allele in unique_pairs:
        if allele in supported_alleles:
            filtered_pairs.append((peptide, allele))
        else:
            unsupported_pairs.append((peptide, allele))

    # Run batches
    problematic_alleles = set()
    temp_batch = []
    for peptide, allele in tqdm(filtered_pairs, desc='Processing Filtered Pairs', leave=True, position=0):
        temp_batch.append((peptide, allele))
        if len(temp_batch) == batch_size:
            problematic_data = run_batch(predictor, temp_batch, predictions_list, problematic_alleles, problematic_data)
            temp_batch = []

    # Process remaining batch if it's not empty
    if temp_batch:
        problematic_data = run_batch(predictor, temp_batch, predictions_list, problematic_alleles, problematic_data)

    # Compile results
    predictions_df = pd.concat(predictions_list, ignore_index=True)
    if problematic_data:
        problematic_df = pd.DataFrame(problematic_data)
        logging.info(f"Problematic DataFrame created with {len(problematic_df)} entries.")
    else:
        logging.warning("Problematic DataFrame is empty.")
        problematic_df = pd.DataFrame()

    # Add 'Cell Line' and 'Mutation' columns
    predictions_df['Cell Line'] = predictions_df.apply(lambda row: list(set(pair_info[(row['peptide'], row['allele'])]['Cell Line'])), axis=1)
    predictions_df['Mutation'] = predictions_df.apply(lambda row: list(set(pair_info[(row['peptide'], row['allele'])]['Mutation'])), axis=1)

    # Initialize unsupported_df
    unsupported_df = pd.DataFrame(unsupported_pairs, columns=['peptide', 'allele'])
    logging.info(f"Unsupported DataFrame created with {len(unsupported_df)} entries.")

    # Create DataFrame from unique_pairs
    unique_pairs_df = pd.DataFrame(unique_pairs, columns=['peptide', 'allele'])

    # Concatenate all DataFrames to create all_predictions_df
    all_predictions_df = pd.concat([predictions_df, unsupported_df, problematic_df], ignore_index=True)

    # Find missing pairs
    missing_pairs = unique_pairs_df.loc[~unique_pairs_df.set_index(['peptide', 'allele']).index.isin(all_predictions_df.set_index(['peptide', 'allele']).index)]
    missing_pairs['prediction'] = None
    missing_pairs['prediction_low'] = None
    missing_pairs['prediction_high'] = None
    missing_pairs['prediction_percentile'] = None

    # Concatenate missing pairs to all_predictions_df
    all_predictions_df = pd.concat([all_predictions_df, missing_pairs], ignore_index=True)

    # Save to Excel
    return all_predictions_df
    # all_predictions_df.to_excel('predictions_all_combinations_batched_with_unsupported.xlsx', index=False)