import pandas as pd

def generar_recomendaciones(solucion):
    tablita = []

    for paciente, metabolizador in solucion.items():
        for gen, datos in metabolizador.items():
            fenotipo = datos.get("Phenotype", "")
            medicacion = ""
            recomendacion = ""

            if gen == "CYP2D6":
                medicacion = "Tamoxifeno"
                if fenotipo == "Poor Metabolizer":
                    recomendacion = "Considerar cambio de tratamiento"
                elif fenotipo == "Intermediate Metabolizer":
                    recomendacion = "Considerar reducción de la dosis"
                else:
                    recomendacion = "Dosis estándar"

            elif gen == "DPYD":
                medicacion = "Fluoropirimidinas"
                if fenotipo == "Poor Metabolizer":
                    recomendacion = "Contraindicado. Iniciar con dosis muy reducidas"
                elif fenotipo == "Intermediate Metabolizer":
                    recomendacion = "50% dosis estándar, aumentando si es tolerado"
                else:
                    recomendacion = "Dosis estándar"

            elif gen == "UGT1A1":
                medicacion = "Irinotecán"
                if fenotipo in ("Poor Metabolizer", "Intermediate Metabolizer"):
                    recomendacion = "Reducción de la dosis"
                else:
                    recomendacion = "Dosis estándar"

            tablita.append({
                "Identificador paciente": str(paciente),
                "Gen": gen,
                "Nombre medicación": medicacion,
                "Recomendaciones": recomendacion,
            })

    return pd.DataFrame(tablita)