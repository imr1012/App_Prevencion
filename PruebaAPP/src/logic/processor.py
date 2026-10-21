import csv
import pandas as pd
from src.logic.generador_tabla import generador_tabla
import os

def procesar_genotipos(ruta_csv):
    # Cargar las bases de datos de referencia
    # Asume que los archivos están en la carpeta raíz del proyecto
    if not os.path.isfile("tabla_mutaciones.csv"): #no existe aún una tabla de transformaciones
        generador_tabla()
    df_resumen = pd.read_csv('tabla_mutaciones.csv')
    CPIC = pd.read_excel('CYP2D6_Diplotype_Phenotype_Table.xlsx')
    
    ancestral = dict(zip(df_resumen["Polimorfismo"], df_resumen["Base ancestral"]))

    #Sacar nombre del alelo mutado
    def etiqueta_mutada(polimorfismo):
        """ Convierte p.ej "CYP2D6*17" a "*17" """
        if "*" in polimorfismo: return "*" + polimorfismo.split("*")[1]
        return "*" + polimorfismo.split("_")[1] #HapB3 p.ej tiene _ en vez de *

    #Función para convertir genotipo a números
    def letras_a_nums(polimorfismo, genotipo):
        wild_type = ancestral[polimorfismo]
        mut = etiqueta_mutada(polimorfismo)
        alelos = ["*1" if b == wild_type else mut for b in genotipo.split("/")]
        alelos.sort(key=lambda a: a != "*1") #Para que el alelo siempre sea con la estructura *1/*17
        return alelos[0] + "/" + alelos[1]

    #Sacar el nombre del gen
    def gen_sin_alelo(polimorfismo):
        """ Convierte p.ej "G/A" a "*1/*17" """
        if "*" in polimorfismo: return polimorfismo.split("*")[0]
        return polimorfismo.split("_")[0]

    # Para leer el CSV del paciente
    with open(ruta_csv, mode="r") as file:
        lector = csv.reader(file, delimiter=";")
        pacientes = {}
        cabecera = next(lector) #Para saltar el encabezado
        for fila in lector:
            cod_paciente = fila[0]
            pacientes[cod_paciente] = {} #Por cada paciente se crea un diccionario
            for columna, elemento in zip(cabecera, fila):
                if columna != "Sample/Assay":#Para no guardar el ID del paciente ya que ya es la clave
                    pacientes[cod_paciente][columna] = elemento

    # Conversión a diplotipos
    pacientes_conv = {} #Creación de diccionario con pacientes como clave y valor diccioanrio con su información
    for paciente, genotipos in pacientes.items():
        alelos_paciente = {}
        for polimorfismo, genotipo in genotipos.items():
            alelos_paciente[polimorfismo] = letras_a_nums(polimorfismo, genotipo)
        pacientes_conv[paciente] = alelos_paciente

    diplotiposPacientes = {}
    for paciente, genotipo in pacientes_conv.items():
        fenotipo = {}
        for polimorfismo, alelo in genotipo.items():
            gen = gen_sin_alelo(polimorfismo)
            fenotipo.setdefault(gen, alelo)
            if fenotipo[gen] != alelo and alelo != "*1/*1":#En caso de que el alelo tambén sea *1/*1 o para evitar la redundancia de comparar en caso de que el propio alelo sea el valor con el que se creó el diccionario
                if fenotipo[gen] == "*1/*1": #Si lo que hay en el diccinario es que no hay mutaciones aún, entonces solo sustituyo el valor por el nuevo alelo
                    fenotipo[gen] = alelo
                else: #Si ya hay una mutación para ese gen en el diccionario
                    variacionAleloGen = fenotipo[gen].split("/")
                    variacionAleloNuevo = alelo.split("/")
                    listaVariaciones = (variacionAleloGen + variacionAleloNuevo)
                    for i in range(len(listaVariaciones)):
                        if listaVariaciones[i] != "*1":
                            fenotipo[gen] += listaVariaciones[i] + "/"
                        fenotipo[gen] = fenotipo[gen][:-1] #Para quitar la última barra
        diplotiposPacientes[paciente] = fenotipo

    # Asignación de Fenotipos
    def fenotipo_asignar(diplotipo):
        if diplotipo in CPIC["CYP2D6 Diplotype"].values:
            fenotipo = CPIC.loc[CPIC["CYP2D6 Diplotype"] == diplotipo, "Coded Diplotype/Phenotype Summary"].values[0]
            score = CPIC.loc[CPIC["CYP2D6 Diplotype"] == diplotipo, "Activity Score"].values[0]
        else:
            fenotipo = "Unknown"
            score = "Unknown"
        return score, fenotipo

    filas_df = []
    solucion = {}
    for paciente, genes in diplotiposPacientes.items():
        fila = {"Paciente": paciente}
        solucion[paciente] = {}
        for gen, diplotipo in genes.items():
            if gen == "CYP2D6":
                score, fenotipo = fenotipo_asignar(diplotipo)
                fila[f"{gen}_Diplotipo"] = diplotipo
                fila[f"{gen}_Score"] = score
                fila[f"{gen}_Fenotipo"] = fenotipo
            elif gen == "DPYD":
                fenotipo = "Poor Metabolizer" if diplotipo == "*1/*HapB3" else "Normal Metabolizer"
                fila[f"{gen}_Diplotipo"] = diplotipo
                fila[f"{gen}_Fenotipo"] = fenotipo
            else: # UGT1A1
                if diplotipo == "*1/*80": fenotipo = "Intermediate Metabolizer"
                elif diplotipo == "*80/*80": fenotipo = "Poor Metabolizer"
                else: fenotipo = "Normal Metabolizer"
                fila[f"{gen}_Diplotipo"] = diplotipo
                fila[f"{gen}_Fenotipo"] = fenotipo
            solucion[paciente][gen] = {"Phenotype": fenotipo}
        filas_df.append(fila)

    return pd.DataFrame(filas_df), solucion