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

def generar_pdf_manual(datos, ruta_guardado):
    """Genera el PDF desde el ingreso manual de datos (Pestaña 2)"""
    pdf = FPDF()
    pdf.add_page()
    
    # Título principal
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Informe Farmacogenético Personalizado", ln=True, align='C')
    pdf.ln(10)

    # Datos del paciente
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, " 1. Datos Personales", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    
    pdf.ln(2)
    pdf.cell(100, 8, f"Paciente: {datos['Nombre']}", ln=False)
    pdf.cell(90, 8, f"DNI: {datos['DNI']}", ln=True)
    pdf.cell(100, 8, f"Sexo: {datos['Sexo']}", ln=False)
    pdf.cell(90, 8, f"Fecha de Nac.: {datos['Fecha Nacimiento']}", ln=True)
    pdf.ln(5)
    
    # Historial y Patologías
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, " 2. Patologías y Tratamientos Actuales", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.ln(2)
    
    # Usar multi_cell por si el texto médico es largo y ocupa varias líneas
    pdf.multi_cell(0, 8, datos['Notas'])
    pdf.ln(5)

    # Perfil Genético
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, " 3. Perfil Genético Conocido", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.ln(5)

    if not datos["Genes"]:
        pdf.cell(0, 8, "No se han registrado genes para este paciente.", ln=True)
    else:
        # Dibujar una pequeña tabla para los genes
        pdf.set_font("Arial", "B", 11)
        pdf.cell(95, 8, "Gen", border=1, align='C')
        pdf.cell(95, 8, "Diplotipo Combinado", border=1, align='C', ln=True)
        
        pdf.set_font("Arial", "", 11)
        for gen_info in datos["Genes"]:
            pdf.cell(95, 8, gen_info["Gen"], border=1, align='C')
            pdf.cell(95, 8, gen_info["Diplotipo"], border=1, align='C', ln=True)

    # Guardar documento
    pdf.output(ruta_guardado)