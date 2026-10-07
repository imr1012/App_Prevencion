import tkinter as tk
from tkinter import filedialog
from src.views.inicial import Ventana_inicial

def main():
    ventana = tk.Tk()
    ventana.title("DrogApp")
    ventana.geometry("500x750")  # Ancho x Alto en píxeles
    ventana_inicial = Ventana_inicial(ventana)
    ventana.mainloop()    




# 1. Crear la ventana base





if __name__ == "__main__":
    main()
    

