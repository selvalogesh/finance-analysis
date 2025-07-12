import pdfplumber
import pandas as pd

def pdf_to_excel(pdf_path, excel_path='output.xlsx', csv_path=None):
    """
    Extract tables from a PDF file containing bank transaction data
    and save them as an Excel or CSV file with row-type data.
    
    :param pdf_path: Path to the input PDF file
    :param excel_path: Path to the output Excel file
    :param csv_path: Path to the output CSV file (if specified, CSV is saved instead of Excel)
    """
    all_tables = []
    col =[]
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                # Convert table to DataFrame
                if page.layout.pageid == 1:
                    col = table[0]
                    df = pd.DataFrame(table[1:], columns=col)
                else:
                    df = pd.DataFrame(table[0:1], columns=col)
                all_tables.append(df)
    
    if all_tables:
        # Concatenate all tables into one DataFrame
        result_df = pd.concat(all_tables, ignore_index=True)
        # Save to CSV or Excel
        if csv_path:
            result_df.to_csv(csv_path, index=False)
            print(f"Data successfully extracted to {csv_path}")
        else:
            result_df.to_excel(excel_path, index=False)
            print(f"Data successfully extracted to {excel_path}")
    else:
        print("No tables found in the PDF.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert bank transaction PDF to Excel or CSV")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--excel_path", default="output.xlsx", help="Path to save the Excel file")
    parser.add_argument("--csv", dest="csv_path", help="Path to save the CSV file")
    args = parser.parse_args()
    pdf_to_excel(args.pdf_path, args.excel_path, args.csv_path)
