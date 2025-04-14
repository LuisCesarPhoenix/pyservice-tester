from fpdf import FPDF

def generate_pdf_report(data, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Relatório de Processamento de Dados", ln=True, align="C")

    for row in data[:10]:  # Apenas uma amostra dos dados
        pdf.cell(200, 10, str(row), ln=True)

    pdf.output(output_file)
    return output_file
