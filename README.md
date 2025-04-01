This repo contains code to generate the impact factor spreadsheet. 

Steps: 
1. Go to WoS and query for paper information.
2. Download to endnote & run checks.
3. Export to .xlsx, and format so the spreadsheet has the following columns:
  - ['Authors', 'Journal', 'Title', 'Year', 'PMCID', 'PMID', 'URL']
  - This is spreadsheetA
4. Find the latest version of the JCR report. An example is here: https://www.researchgate.net/publication/381580823_Journal_Citation_Reports_JCR_Impact_Factor_2024_PDF_Web_of_Science
  - This is the Journal Citation Report, which includes the Journal name, abbreviated name, and their impact factors.
  - This is spreadsheetB
5. Go to beta.genepattern.org and find the "CitationStats" module, drag and drop the WoS processed query result + JCR spreadsheet into the inputs, specify output name and click "run".
6. Download the .xlsx file, color, format, sort by descending impact factor or year if requested by Jill.


Notes: 
- If impact factor is 0, it means that that journal either has no impact factor or is not included in the JCR report.
- On WoS, if looking for papers that cite a specific paper, make sure that you aren't looking for papers that cite the paper that cite the specific paper.
