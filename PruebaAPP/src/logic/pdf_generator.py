from fpdf import FPDF

def generar_pdf_paciente(datos_paciente, ruta_guardado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título principal
    pdf.cell(200, 10, "Informe Farmacogenético", ln=True, align='C')
    pdf.ln(10)

    # Datos del paciente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, f"ID Paciente: {datos_paciente.get('Paciente', 'N/A')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 11)
    
    # Configuración de los genes a mostrar
    genes = ["CYP2D6", "DPYD", "UGT1A1"]
    
    for gen in genes:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Resultados para el gen {gen}", ln=True)
        pdf.set_font("Arial", "", 11)
        
        diplotipo = datos_paciente.get(f"{gen}_Diplotipo", "N/A")
        fenotipo = datos_paciente.get(f"{gen}_Fenotipo", "N/A")
        score = datos_paciente.get(f"{gen}_Score", "N/A")
        
        pdf.cell(200, 8, f"- Diplotipo: {diplotipo}", ln=True)
        if gen == "CYP2D6":
            pdf.cell(200, 8, f"- Activity Score: {score}", ln=True)
        pdf.cell(200, 8, f"- Fenotipo inferido: {fenotipo}", ln=True)
        pdf.ln(5)

    # Guardar documento
    pdf.output(ruta_guardado)