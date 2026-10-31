from fpdf import FPDF
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable

import pandas as pd
import datetime as dt

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



def informe_pdf(id, datos_personales, df_resultados, df_datos, ruta):
    archivo_pdf = ruta
    logo = "PruebaAPP/logo_DrugApp.jpeg"

    df_resumen = pd.read_csv("PruebaAPP/mutaciones_entrez.csv")

    doc = SimpleDocTemplate(
        archivo_pdf,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm,
        title="Informe Farmacogenético"
    )

    contenido = []

    estilos = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "TituloPersonalizado",
        parent=estilos["Title"],
        fontName="Times-Bold",
        fontSize=15,
        leading=27,
        alignment=TA_CENTER,
        spaceAfter = 20
    )

    subtitulo_style = ParagraphStyle(
        "SubtituloPersonalizado",
        parent=estilos["Normal"],
        fontName="Times-Bold",
        fontSize=13,
        leading=15,
        alignment = TA_CENTER,
        spaceAfter=5
    )

    parrafo_style = ParagraphStyle(
        "ParrafoPersonalizado",
        parent=estilos["BodyText"],
        fontName="Times-Roman",
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )

    seccion_style = ParagraphStyle(
        "SeccionPersonalizada",
        parent=estilos["Heading2"],
        fontName="Times-Bold",
        fontSize=11,
        leading=18,
        alignment = TA_LEFT,
        spaceBefore=12,
        spaceAfter=8
    )

    logo = Image(logo, width=2.2*cm, height=2*cm)

    cabecera_texto = [
        Spacer(1, 0.6*cm),
        Paragraph("INFORME FARMACOGENÉTICO - PERFIL ONCOLOGÍA", titulo_style),
        Paragraph(f"Código de Muestra {id}", subtitulo_style) # SE PUEDE PONER EL SUBTÍTULO POR SEPARADO EN VEZ DE METERLO EN LISTA
    ]

    cabecera = Table([[logo], [cabecera_texto]])

    cabecera.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))


    contenido.append(cabecera)

    contenido.append(HRFlowable(
        width="100%",
        thickness=0.5,
        color=colors.black,
        spaceBefore=1,
        spaceAfter=0.5*cm
    ))

    hoy = str(dt.date.today()).split("-")
    dia, mes, ano = hoy[2], hoy[1], hoy[0]

    datos_tabla_pers = [
        [f"Paciente: {datos_personales["Nombre"]}", f"DNI: {datos_personales["DNI"]}"],
        [f"Fecha de nacimiento: {datos_personales["Fecha Nacimiento"]}", f"Fecha solicitud: {f"{dia}/{mes}/{ano}"}"]
    ]

    tabla_datos = Table(
        datos_tabla_pers,
        colWidths=[10*cm, 6.5*cm],
        repeatRows=1,
        hAlign="LEFT"
    )

    tabla_datos.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11)
    ]))

    contenido.append(tabla_datos)
    contenido.append(Spacer(1, 0.5*cm))

    tabla_antecedentes = []

    enfermedades = datos_personales["Enfermedades"]
    tratamientos = datos_personales["Tratamientos"]

    if enfermedades == None or enfermedades == "":
        enfermedades = []

    elif isinstance(enfermedades, str):
        enfermedades = [
            e.strip() for e in enfermedades.splitlines()
            if e.strip()
        ]


    if tratamientos == None or tratamientos == "":
        tratamientos = []

    elif isinstance(tratamientos, str):
        tratamientos = [
            t.strip() for t in tratamientos.splitlines()
            if t.strip()
        ]
    
    

    for i, enferm in enumerate(enfermedades):
        if i == 0:
            seccion = Paragraph("<b>Enfermedades actuales: </b>", parrafo_style)
        else:
            seccion = ""

        enf = Paragraph(str(enferm), parrafo_style)
        tabla_antecedentes.append([seccion, enf])

    tabla_antecedentes.append(["", ""])
    
    for i, tto in enumerate(tratamientos):
        if i == 0:
            seccion = Paragraph("<b>Tratamiento habitual: </b>", parrafo_style)
        else:
            seccion = ""

        ttos = Paragraph(str(tto), parrafo_style)
        tabla_antecedentes.append([seccion, ttos])


    tabla_antec = Table(
        tabla_antecedentes,
        colWidths=[4.5*cm, 12*cm],
        repeatRows=1,
        hAlign="LEFT"
    )

    tabla_antec.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11)
    ]))

    contenido.append(tabla_antec)
    contenido.append(Spacer(1, 0.5*cm))
    

    contenido.append(HRFlowable(
        width="100%",
        thickness=0.5,
        color=colors.black,
        spaceBefore=2,
        spaceAfter=0.5*cm
    ))

    contenido.append(Paragraph("Los siguientes polimorfismos se han analizado mediante PCR a tiempo real con tarjeta de genotipado customizada para el Servicio de Oncología en un equipo ViiA7, con el uso de sondas de hibridación TaqMan (Thermofisher).", 
                            parrafo_style))

    contenido.append(Spacer(1, 0.2*cm))



    # Tabla polimorfismos

    datos_tabla1 = [
        ["Gen", f"Polimorfismos analizados\ncon relevancia funcional conocida", "Fármaco de interés"]
    ]

    genes_tabla = df_datos["Gen"].unique()
    polimorfismos = {}
    medicamentos = {"DPYD": "Fluorouracilo", "CYP2D6": "Tamoxifeno", "UGT1A1": "Irinotecán"}

    for i in range(len(df_resumen)):
        fila = df_resumen.iloc[i]
        if fila["Gen"] not in polimorfismos:
            if fila["Gen"] == "UGT1A10":
                fila["Gen"] = "UGT1A1"
            polimorfismos[fila["Gen"]] = []
        
        polimorfismos[fila["Gen"]].append(f"{fila["Polimorfismo"]} ({fila["Identificador RS"]})")


    for gen in genes_tabla:
        polim = polimorfismos[gen]
        datos_tabla1.append([gen, "\n".join(polim), medicamentos[gen]])


    tabla1 = Table(
        datos_tabla1,
        colWidths=[3*cm, 7.5*cm, 6*cm],
        repeatRows=1
    )

    tabla1.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    contenido.append(tabla1)
    contenido.append(Spacer(1, 0.5*cm))

    contenido.append(Paragraph("RESULTADOS:", seccion_style))

    datos_tabla2 = [
        ["Gen", "Fenotipo", "Fármaco de interés", "Recomendación terapéutica"]
    ]

    for i in range(len(genes_tabla)):
        fila = df_datos.iloc[i]
        gen = fila["Gen"]
        datos_tabla2.append([f"{gen}\n{df_resultados[f"{gen}_Diplotipo"].iloc[0]}", 
                            df_resultados[f"{gen}_Fenotipo"].iloc[0], 
                            fila["Nombre medicación"], 
                            fila["Recomendaciones"]])


    tabla2 = Table(
        datos_tabla2,
        colWidths=[2.5*cm, 4.5*cm, 4*cm, 5.5*cm],
        repeatRows=1
    )

    colores = {
        "Poor Metabolizer": colors.HexColor("#f8a4a4"),
        "Intermediate Metabolizer": colors.HexColor("#f9ddb5"),
        "Normal Metabolizer": colors.HexColor("#ddf4a2")
    }


    estilo_tabla2 = [
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 1), (-1, -1), "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]

    for i, metab in enumerate(datos_tabla2[1:], start = 1):
        fenotipo = metab[1]
        color = colores[fenotipo]

        estilo_tabla2.append(
            ("BACKGROUND", (0, i), (-1, i), color)
        )

    tabla2.setStyle(TableStyle(estilo_tabla2))

    contenido.append(tabla2)

    doc.build(contenido)
