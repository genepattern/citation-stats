import pandas as pd
import numpy as np
import re
import os
import argparse

def load_wos_query_spreadsheet(fp):
    """
    Loads the web of science spreadsheet from query, and adds a new column "Impact Factor" to it.
    Supports .csv, .tsv, and .xlsx files.
    
    Assuming columns are 
    ['Authors', 'Journal', 'Title', 'Year', 'PMCID', 'PMID', 'URL']
    
    
    """
    columns = ['Authors', 'Journal', 'Title', 'Year', 'PMCID', 'PMID', 'URL']
    ext = os.path.splitext(fp)[1].lower()

    if ext == '.csv':
        gsea = pd.read_csv(fp, encoding='utf-8')
    elif ext == '.tsv':
        gsea = pd.read_csv(fp, sep='\t', encoding='utf-8')
    elif ext == '.xlsx':
        gsea = pd.read_excel(fp, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format. Please provide a .csv, .tsv, or .xlsx file.")
    if len(gsea.columns) > 7:
        raise ValueError(f'Spreadsheet should have only 7 columns, in this order: {columns}')
    gsea.columns = columns
    gsea['Impact Factor'] = None
    return gsea

def load_JCR_citation_stats(fp):
    '''
    Loads a spreadsheet containing citation information. 
    Must have these columns: 
        ['Name', 'Abbr Name', 'ISSN', 'EISSN', 'JIF', 'JIF5Years', 'Category']
    Supports .csv, .tsv, and .xlsx file formats.
    '''
    required_columns = ['Name', 'Abbr Name', 'ISSN', 'EISSN', 'JIF', 'JIF5Years', 'Category']
    ext = os.path.splitext(fp)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(fp, encoding='utf-8')
    elif ext == '.tsv':
        df = pd.read_csv(fp, sep='\t', encoding='utf-8')
    elif ext == '.xlsx':
        df = pd.read_excel(fp, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format. Please provide a .csv, .tsv, or .xlsx file.")
    
    # Ensure required columns are present
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Missing one or more required columns: {required_columns}")
    
    return df

mapping = {'Cancers (Basel)': 'Cancers',
 'Aging (Albany NY)': 'Aging',
 'Adv Sci (Weinh)': 'Advanced Science',
 'J Cancer Res Clin Oncol': 'Journal of Cancer Research and Clinical Oncology',
 'Medicine (Baltimore)': 'Medicine',
 'Cell Oncol (Dordr)': 'Cell Oncology',
 'Cancer Immunol Immunother': 'Cancer Immunology, Immunotherapy',
 'Proc Natl Acad Sci U S A': 'Proceedings of the National Academy of Sciences of the United States of America',
 'Br J Cancer': 'British Journal of Cancer',
 'Breast Cancer Res Treat': 'Breast Cancer Research and Treatment',
 'Front Endocrinol (Lausanne)': 'Frontiers in Endocrinology',
 'J Exp Clin Cancer Res': 'Journal of Experimental & Clinical Cancer Research',
 'Biochim Biophys Acta Mol Basis Dis': 'Biochimica et Biophysica Acta',
 'Technol Cancer Res Treat': 'Technology in Cancer Research & Treatment',
 'Comput Struct Biotechnol J': 'Computational and Structural Biotechnology Journal',
 'Front Biosci (Landmark Ed)': 'Frontiers in Bioscience',
 'Cancer Med': 'Cancer Medicine',
 'Neuro Oncol': 'Neuro-Oncology',
 'Funct Integr Genomics': 'Functional & Integrative Genomics',
 'Nat Aging': 'Nature Aging',
 'Comb Chem High Throughput Screen': 'Combinatorial Chemistry & High Throughput Screening',
 'Recent Pat Anticancer Drug Discov': 'Recent Patents on Anti-Cancer Drug Discovery',
 'J Hepatocell Carcinoma': 'Journal of Hepatocellular Carcinoma',
 'Biomol Biomed': 'Biomolecules and Biomedicine',
 'Prostate Cancer Prostatic Dis': 'Prostate Cancer and Prostatic Diseases',
 'Br J Haematol': 'British Journal of Haematology',
 'Mod Pathol': 'Modern Pathology',
 'Genes (Basel)': 'Genes',
 'Acta Neuropathol Commun': 'Acta Neuropathologica Communications',
 'Signal Transduct Target Ther': 'Signal Transduction and Targeted Therapy',
 'Cancer Rep (Hoboken)': 'Cancer Reports',
 'Mol Carcinog': 'Molecular Carcinogenesis',
 'Commun Med (Lond)': 'Communications Medicine',
 'Cancer Genomics Proteomics': 'Cancer Genomics & Proteomics',
 'J Steroid Biochem Mol Biol': 'Journal of Steroid Biochemistry & Molecular Biology',
 'Neurooncol Adv': 'Neuro-Oncology Advances',
 'Mol Ther Oncol': 'Molecular Therapy - Oncolytics',
 'Acta Biochim Biophys Sin (Shanghai)': 'Acta Biochimica et Biophysica Sinica',
 'Viruses': 'Viruses',
 'J Clin Endocrinol Metab': 'Journal of Clinical Endocrinology & Metabolism',
 'World J Gastrointest Oncol': 'World Journal of Gastrointestinal Oncology',
 'Biochim Biophys Acta Mol Cell Res': 'Biochimica et Biophysica Acta',
 'Pharmaceuticals (Basel)': 'Pharmaceuticals',
 'J Biochem Mol Toxicol': 'Journal of Biochemical and Molecular Toxicology',
 'Biochem Biophys Res Commun': 'Biochemical and Biophysical Research Communications',
 'Mil Med Res': 'Military Medical Research',
 'Hematol Transfus Cell Ther': 'Hematology, Transfusion and Cell Therapy',
 'Arterioscler Thromb Vasc Biol': 'Arteriosclerosis, Thrombosis, and Vascular Biology',
 'J Mammary Gland Biol Neoplasia': 'Journal of Mammary Gland Biology and Neoplasia',
 'Mol Ther Nucleic Acids': 'Molecular Therapy - Nucleic Acids'}



def journal_if_5yr(impact_factor, journal):
    """
    Given a journal name, find, using the impact factor DF, the impact factor 
    look through 'name' and 'ABBR name'
    """
    ## check type:
    if type(journal) != type('str'):
        return ""

    query = impact_factor[impact_factor['Name'].str.upper() == journal.upper()]
    if len(query) == 0: ## query by abbr name
        query = impact_factor[impact_factor['Abbr Name'].str.upper() == journal.upper()]

    if len(query) == 0:
        return 'Journal has no impact factor yet.'
    else: 
        return float(query['JIF5Years'].values[0])


def journal_if_yr(impact_factor, journal):
    """
    Given a journal name, find, using the impact factor DF, the impact factor 
    look through 'name' and 'ABBR name'
    """
    ## check type:
    if type(journal) != type('str'):
        return ""

    query = impact_factor[impact_factor['Name'].str.upper() == journal.upper()]
    if len(query) == 0: ## query by abbr name
        query = impact_factor[impact_factor['Abbr Name'].str.upper() == journal.upper()]

    if len(query) == 0:
        return 'Journal has no impact factor yet.'
    else: 
        return float(query['JIF'].values[0])
    
    
if __name__ == "__main__":
    

    parser = argparse.ArgumentParser(description="Load a WoS query spreadsheet and add Impact Factor column.")
    parser.add_argument("--fp", type=str, required=True, help="Path to the input WoS spreadsheet file (.csv, .tsv, .xlsx)")
    parser.add_argument("--jcr", type=str, required=True, help="Path to the JCR citation stats file (.csv, .tsv, .xlsx)")
    parser.add_argument("--out", type=str, default="Impact_factor", help="Output Excel file name")
    args = parser.parse_args()

    df = load_wos_query_spreadsheet(args.fp)
    print(df.columns)
    print(df.head())
    jif = load_JCR_citation_stats(args.jcr)
    print(jif.columns)
    
    print('-------------------Performing test on "nat commun"---------------')
    
    journal = 'nat commun'
    print(f'5 yr impact score: {journal_if_5yr(jif, journal)}')
    print(f'Current year impact score: {journal_if_yr(jif, journal)}')


    print('-----------------------------------------------------------------')
    
    print('\n')
    
    print('-----------Performing lookup----------------------')
    # gsea_if = pd.concat([gsea_if1, gsea_if2], axis = 0)
    gsea_if = df
    gsea_if['Impact Factor'] = gsea_if['Journal'].apply(lambda x: journal_if_yr(jif, x))
    unknowns = gsea_if[gsea_if['Impact Factor'] == 'Journal has no impact factor yet.'].Journal.value_counts()
    unknown_journals = unknowns.index.values.tolist()
    for j in unknown_journals:
        try:
            real_name = mapping[j]
            print(f'{j} stands for {real_name} \n')
            print(f'is {real_name} in impact factors spreadsheet? ')
            print(real_name.upper() in jif['Name'].values.tolist())
            impact_factor_yr = journal_if_yr(jif, real_name)
            gsea_if.loc[gsea_if['Journal'].str.upper() == j.upper(), 'Impact Factor'] = impact_factor_yr
            
        except:
            gsea_if.loc[gsea_if['Journal'].str.upper() == j.upper(), 'Impact Factor'] = 0
            print(f'{j} not found in mapping ... ')
            
    gsea_if['Impact Factor'] = gsea_if['Impact Factor'].apply(lambda x: 0 if x == "Journal has no impact factor yet." else x)
    
    
    print('-----------------------------------------------------------------')

    
    
    print('-----------------------Exporting to CSV ------------------------------')
    gsea_if.dropna(axis = 0).sort_values(by = 'Impact Factor', ascending = False)
    gsea_if.to_excel(args.out+'.xlsx', index=False)
