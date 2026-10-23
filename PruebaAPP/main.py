import customtkinter as ctk
from src.views.inicial import Ventana_inicial

def main():
    # Configuración de CustomTkinter
    ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

    ventana = ctk.CTk()
    ventana.title("DrugApp - Sistema de Análisis Farmacogenético")
    ventana.geometry("950x650")
    ventana.minsize(800, 500)
    
    # Inicializar la vista
    app = Ventana_inicial(ventana)
    
    ventana.mainloop()    

if __name__ == "__main__":
    main()
