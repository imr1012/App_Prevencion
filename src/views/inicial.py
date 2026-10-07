
import tkinter as tk
from tkinter import filedialog

class Ventana_inicial():
    def __init__(self, ventana):
        self.ventana = ventana

    def inicializar(self):
        # Paso 1: Crear un texto (Label)
        texto = tk.Label(self.ventana, text="Suba el CSV")
        # Paso 2: Colocarlo en la ventana
        texto.pack(pady=10)
        # 4. Etiqueta para mostrar la ruta del archivo elegido
        etiqueta_resultado = tk.Label(
            self.ventana, 
            text="No has seleccionado ningún archivo", 
            wraplength=400  # Hace que el texto salte de línea si la ruta es muy larga
        )
        # 3. Botón para cargar el archivo
        boton_cargar = tk.Button(
            self.ventana, 
            text="Seleccionar archivo", 
            command=self.seleccionar_archivo(etiqueta_resultado)
        )
        boton_cargar.pack(pady=15)

        
        etiqueta_resultado.pack(pady=10)

    def seleccionar_archivo(et, self):
        # Abre la ventana del explorador para elegir un archivo
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
        )
        
        # Si el usuario eligió un archivo (no canceló)
        if ruta:
            # Mostramos la ruta seleccionada en la etiqueta de texto
            et.config(text=f"Archivo:\n{ruta}")

