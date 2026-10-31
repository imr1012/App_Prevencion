from Bio import Entrez

Entrez.email=""
Entrez.api_key=""

# Polimorfismos de estudio

variants = {"DPYD*2A": "rs3918290", "DPYD*13": "rs55886062", "DPYD_D949V": "rs67376798", "DPYD_HapB3": "rs56038477", "CYP2D6*3": "rs35742686", 
            "CYP2D6*4": "rs3892097", "CYP2D6*17": "rs28371706", "CYP2D6*41": "rs28371725", "UGT1A1*80": "rs887826"}


# Modificación para hacerlo para todas las variantes
import pandas as pd

# Diccionario que tomaremos como final
genes = []
base_og = []
variantes = []

for k, v in variants.items():
    # Tomamos los datos del polimorfismo de la base de datos dbSNP
    fetch_handle = Entrez.esummary(db = "snp", id = v[2:], retmode = "xml")
    datos = Entrez.read(fetch_handle)
    fetch_handle.close()

    # Extraemos las distintas mutaciones que pueden causar esta variante
    resumen = datos["DocumentSummarySet"]["DocumentSummary"][0]
    gen = resumen["GENES"][0]
    genes.append(gen["NAME"])
    
    mutaciones = resumen["SPDI"].split(",")
    bases = list(map(lambda x: (x[-2], "-") if resumen["SNP_CLASS"] == "del" else (x[-3], x[-1]) , mutaciones))

    # Bases original y mutadas
    base_og.append(bases[0][0])

    gen_mut = []
    for b in bases:
        gen_mut.append(b[1]) 

    variantes.append(gen_mut)
    

    
df_resumen = pd.DataFrame({"Gen": genes, "Polimorfismo": variants.keys(), "Identificador RS": variants.values(), "Base ancestral": base_og, "Mutaciones": variantes})
pd.display(df_resumen)

df_resumen.to_csv("tabla_mutaciones", sep = ",", index = False)

lectura = pd.read_csv("tabla_mutaciones")