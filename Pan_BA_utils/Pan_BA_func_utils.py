import requests
import time
import pandas as pd
import streamlit as st

@st.cache_resource
def get_result_df(sequenceInput, alleleInput):
    peptide_length_min = 8
    peptide_length_max = 12
    sleepNum = (peptide_length_max-peptide_length_min)*6

    # Define the API endpoint
    url = "https://api-nextgen-tools.iedb.org/api/v1/pipeline"

    # Define the headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # Define the payload
    # Define the payload
    payload = {
        "pipeline_id": "",
        "run_stage_range": [1,1],
        "stages": [
            {
                "stage_number": 1,
                "tool_group": "mhci",
                "input_sequence_text": sequenceInput,
                "input_parameters": {
                    "alleles": alleleInput,
                    "peptide_length_range": [peptide_length_min,peptide_length_max],
                    "predictors": [
                        {
                            "type": "binding",
                            "method": "netmhcpan"
                        }
                    ]
                }
            }
        ]
    }




    response = requests.post(url, json=payload)

    # Extract the response content as JSON
    response_json = response.json()

    # Extract the relevant information from the response JSON
    result_id = response_json["result_id"]
    results_uri = response_json["results_uri"]
    pipeline_id = response_json["pipeline_id"]
    pipeline_uri = response_json["pipeline_uri"]
    pipeline_spec_id = response_json["pipeline_spec_id"]
    pipeline_spec_uri = response_json["pipeline_spec_uri"]
    warnings = response_json["warnings"]
    input_sequence_text_id = response_json["input_sequence_text_id"]
    input_sequence_text_uri = response_json["input_sequence_text_uri"]

    # # Print the relevant information
    # print("result_id:", result_id)
    # print("results_uri:", results_uri)

    time.sleep(sleepNum)
    response = requests.get(results_uri)

    # Parse the response content as JSON
    data = response.json()

    # Extract data from the JSON response
    results = data['data']['results']

    # Create an empty list to store each result as a dictionary
    rows = []

    for result in results:
        if result['type'] == 'peptide_table':
            # Extract data from peptide table
            table_data = result['table_data']
            for row in table_data[1:]:
                # Create a dictionary for each row in the peptide table
                data = {
                    'sequence_number': row[0],
                    'peptide': row[1],
                    'length': row[2],
                    'start': row[3],
                    'end': row[4],
                    'allele': row[5],
                    'peptide_index': row[6],
                    'core': row[7],
                    'icore': row[8],
                    'score': row[9],
                    'percentile': row[10]
                }
                # Append the row dictionary to the list of rows
                rows.append(data)

    # score: binding prediction score which indicates binding affinity

    # Create a DataFrame from the list of rows
    df = pd.DataFrame(rows)

    # Sort the DataFrame by percentile rank
    df = df.sort_values('percentile')

    df = df.round(6)

    # filter out rows where 'Core' does not contain 'R'
    df = df[df['peptide'].str.contains('R')]

    return df