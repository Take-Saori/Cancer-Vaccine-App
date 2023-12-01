import pandas as pd

# Load the DataFrame
peptide_matches_df = pd.read_csv("IEDB_utils/peptide_matches.csv")

column_categories = {
    # General Information
    "Peptide": "General",
    "Assay ID_IEDB IRI": "General",
    "Reference_IEDB IRI": "General",
    "Reference_Type": "General",
    "Reference_PMID": "General",
    "Reference_Submission ID": "General",
    "Reference_Authors": "General",
    "Reference_Journal": "General",
    "Reference_Date": "General",
    "Reference_Title": "General",

    # Epitope Information
    "Epitope_IEDB IRI": "Epitope Information",
    "Epitope_Object Type": "Epitope Information",
    "Epitope_Name": "Epitope Information",
    "Epitope_Reference Name": "Epitope Information",
    "Epitope_Modified residues": "Epitope Information",
    "Epitope_Modifications": "Epitope Information",
    "Epitope_Starting Position": "Epitope Information",
    "Epitope_Ending Position": "Epitope Information",
    "Epitope_IRI": "Epitope Information",
    "Epitope_Synonyms": "Epitope Information",
    "Epitope_Source Molecule": "Epitope Information",
    "Epitope_Source Molecule IRI": "Epitope Information",
    "Epitope_Molecule Parent": "Epitope Information",
    "Epitope_Molecule Parent IRI": "Epitope Information",
    "Epitope_Source Organism": "Epitope Information",
    "Epitope_Source Organism IRI": "Epitope Information",
    "Epitope_Species": "Epitope Information",
    "Epitope_Species IRI": "Epitope Information",
    "Epitope_Epitope Comments": "Epitope Information",

    # Related Object Details
    "Related Object_Epitope Relation": "Related Object",
    "Related Object_Object Type": "Related Object",
    "Related Object_Name": "Related Object",
    "Related Object_Starting Position": "Related Object",
    "Related Object_Ending Position": "Related Object",
    "Related Object_IRI": "Related Object",
    "Related Object_Synonyms": "Related Object",
    "Related Object_Source Molecule": "Related Object",
    "Related Object_Source Molecule IRI": "Related Object",
    "Related Object_Molecule Parent": "Related Object",
    "Related Object_Molecule Parent IRI": "Related Object",
    "Related Object_Source Organism": "Related Object",
    "Related Object_Source Organism IRI": "Related Object",
    "Related Object_Species": "Related Object",
    "Related Object_Species IRI": "Related Object",

    # Host Data
    "Host_Name": "Host Data",
    "Host_IRI": "Host Data",
    "Host_Geolocation": "Host Data",
    "Host_Geolocation IRI": "Host Data",
    "Host_Sex": "Host Data",
    "Host_Age": "Host Data",
    "Host_MHC Present": "Host Data",

    # In vivo Process Information
    "1st in vivo Process_Process Type": "In vivo Process",
    "1st in vivo Process_Disease": "In vivo Process",
    "1st in vivo Process_Disease IRI": "In vivo Process",
    "1st in vivo Process_Disease Stage": "In vivo Process",

    # Immunogen Information
    "1st immunogen_Epitope Relation": "Immunogen",
    "1st immunogen_Object Type": "Immunogen",
    "1st immunogen_Name": "Immunogen",
    "1st immunogen_Reference Name": "Immunogen",
    "1st immunogen_Starting Position": "Immunogen",
    "1st immunogen_Ending Position": "Immunogen",
    "1st immunogen_IRI": "Immunogen",
    "1st immunogen_Source Molecule": "Immunogen",
    "1st immunogen_Source Molecule IRI": "Immunogen",
    "1st immunogen_Molecule Parent": "Immunogen",
    "1st immunogen_Molecule Parent IRI": "Immunogen",
    "1st immunogen_Source Organism": "Immunogen",
    "1st immunogen_Source Organism IRI": "Immunogen",
    "1st immunogen_Species": "Immunogen",
    "1st immunogen_Species IRI": "Immunogen",
    "1st immunogen_Adjuvants": "Immunogen",
    "1st immunogen_Route": "Immunogen",
    "1st immunogen_Dose Schedule": "Immunogen",

    # Second In vivo Process
    "2nd in vivo Process_Process Type": "Second In vivo Process",
    "2nd in vivo Process_Disease": "Second In vivo Process",
    "2nd in vivo Process_Disease IRI": "Second In vivo Process",
    "2nd in vivo Process_Disease Stage": "Second In vivo Process",

    # Second Immunogen Information
    "2nd immunogen_Epitope Relation": "Second Immunogen",
    "2nd immunogen_Object Type": "Second Immunogen",
    "2nd immunogen_Name": "Second Immunogen",
    "2nd immunogen_Reference Name": "Second Immunogen",
    "2nd immunogen_Starting Position": "Second Immunogen",
    "2nd immunogen_Ending Position": "Second Immunogen",
    "2nd immunogen_IRI": "Second Immunogen",
    "2nd immunogen_Source Molecule": "Second Immunogen",
    "2nd immunogen_Source Molecule IRI": "Second Immunogen",
    "2nd immunogen_Molecule Parent": "Second Immunogen",
    "2nd immunogen_Molecule Parent IRI": "Second Immunogen",
    "2nd immunogen_Source Organism": "Second Immunogen",
    "2nd immunogen_Source Organism IRI": "Second Immunogen",
    "2nd immunogen_Species": "Second Immunogen",
    "2nd immunogen_Species IRI": "Second Immunogen",
    "2nd immunogen_Adjuvants": "Second Immunogen",
    "2nd immunogen_Route": "Second Immunogen",
    "2nd immunogen_Dose Schedule": "Second Immunogen",

    # In vitro Process Information
    "In vitro Process_Process Type": "In vitro Process",
    "in vitro Responder Cell_Name": "In vitro Process",
    "in vitro Responder Cell_IRI": "In vitro Process",
    "in vitro Stimulator Cell_Name": "In vitro Process",
    "in vitro Stimulator Cell_IRI": "In vitro Process",
    "in vitro immunogen_Epitope Relation": "In vitro Process",
    "in vitro immunogen_Object Type": "In vitro Process",
    "in vitro immunogen_Name": "In vitro Process",
    "in vitro immunogen_Reference Name": "In vitro Process",
    "in vitro immunogen_Starting Position": "In vitro Process",
    "in vitro immunogen_Ending Position": "In vitro Process",
    "in vitro immunogen_IRI": "In vitro Process",
    "in vitro immunogen_Source Molecule": "In vitro Process",
    "in vitro immunogen_Source Molecule IRI": "In vitro Process",
    "in vitro immunogen_Molecule Parent": "In vitro Process",
    "in vitro immunogen_Molecule Parent IRI": "In vitro Process",
    "in vitro immunogen_Source Organism": "In vitro Process",
    "in vitro immunogen_Source Organism IRI": "In vitro Process",
    "in vitro immunogen_Species": "In vitro Process",
    "in vitro immunogen_Species IRI": "In vitro Process",

    # Adoptive Transfer Information
    "Adoptive Transfer_Flag": "Adoptive Transfer",
    "Adoptive Transfer_Comments": "Adoptive Transfer",

    # Immunization Information
    "Immunization_Comments": "Immunization",

    # Assay Information
    "Assay_Location of Assay Data in Reference": "Assay",
    "Assay_Method": "Assay",
    "Assay_Response measured": "Assay",
    "Assay_Units": "Assay",
    "Assay_IRI": "Assay",
    "Assay_Qualitative Measurement": "Assay",
    "Assay_Measurement Inequality": "Assay",
    "Assay_Quantitative measurement": "Assay",
    "Assay_Number of Subjects Tested": "Assay",
    "Assay_Number of Subjects Positive": "Assay",
    "Assay_Response Frequency (%)": "Assay",
    "Assay_Comments": "Assay",

    # Effector Cell Information
    "Effector Cell_Source Tissue": "Effector Cell",
    "Effector Cell_Source Tissue IRI": "Effector Cell",
    "Effector Cell_Name": "Effector Cell",
    "Effector Cell_IRI": "Effector Cell",
    "Effector Cell_Culture Condition": "Effector Cell",
    "Effector Cell_TCR Name": "Effector Cell",

    # Antigen Presenting Cell Information
    "Antigen Presenting Cell_Source Tissue": "Antigen Presenting Cell",
    "Antigen Presenting Cell_Source Tissue IRI": "Antigen Presenting Cell",
    "Antigen Presenting Cell_Name": "Antigen Presenting Cell",
    "Antigen Presenting Cell_IRI": "Antigen Presenting Cell",
    "Antigen Presenting Cell_Culture Condition": "Antigen Presenting Cell",

    # MHC Restriction Data
    "MHC Restriction_Name": "MHC Restriction",
    "MHC Restriction_IRI": "MHC Restriction",
    "MHC Restriction_Evidence Code": "MHC Restriction",
    "MHC Restriction_Class": "MHC Restriction",

    # Assay Antigen Details
    "Assay Antigen_Epitope Relation": "Assay Antigen",
    "Assay Antigen_Object Type": "Assay Antigen",
    "Assay Antigen_Name": "Assay Antigen",
    "Assay Antigen_Reference Name": "Assay Antigen",
    "Assay Antigen_Starting Position": "Assay Antigen",
    "Assay Antigen_Ending Position": "Assay Antigen",
    "Assay Antigen_IRI": "Assay Antigen",
    "Assay Antigen_Source Molecule": "Assay Antigen",
    "Assay Antigen_Source Molecule IRI": "Assay Antigen",
    "Assay Antigen_Molecule Parent": "Assay Antigen",
    "Assay Antigen_Molecule Parent IRI": "Assay Antigen",
    "Assay Antigen_Source Organism": "Assay Antigen",
    "Assay Antigen_Source Organism IRI": "Assay Antigen",
    "Assay Antigen_Species": "Assay Antigen",
    "Assay Antigen_Species IRI": "Assay Antigen"
}


def get_peptide_data(peptide):
    # Check if the peptide is in the DataFrame
    if peptide in peptide_matches_df['Peptide'].values:
        # Extract the row corresponding to the peptide
        row = peptide_matches_df[peptide_matches_df['Peptide'] == peptide].iloc[0]

        # Create a dictionary to hold categorized data
        categorized_data = {category: [] for category in set(column_categories.values())}

        # Group data by categories
        for col in peptide_matches_df.columns:
            if pd.notna(row[col]) and col in column_categories:
                category = column_categories[col]
                categorized_data[category].append(f"{col}: {row[col]}")

        # Print data by category
        for category, data in categorized_data.items():
            if data:  # Check if category has data
                print(f"\n{category}")
                for item in data:
                    print(item)
    else:
        print(f"No data found for peptide: {peptide}")

    return categorized_data