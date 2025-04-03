import pandas as pd
import statistics
from fpdf import FPDF

def read_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def analyze_data(df):
    """Performs basic statistical analysis on numerical columns."""
    analysis = {}
    for column in df.select_dtypes(include=['number']).columns:
        data = df[column].dropna()
        analysis[column] = {
            'Mean': round(statistics.mean(data), 2),
            'Median': round(statistics.median(data), 2),
            'Std Dev': round(statistics.stdev(data), 2) if len(data) > 1 else 0
        }
    return analysis

def generate_pdf(report_data, output_file):
    """Generates a formatted PDF report."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Data Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for column, stats in report_data.items():
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, column, ln=True)
        pdf.set_font("Arial", size=12)
        for key, value in stats.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)
        pdf.ln(5)
    
    pdf.output(output_file)
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    file_path = "data.csv"  
    df = read_data(file_path)
    if df is not None:
        report_data = analyze_data(df)
        generate_pdf(report_data, "report.pdf")
