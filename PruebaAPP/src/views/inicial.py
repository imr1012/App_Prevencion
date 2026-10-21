import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
from src.logic.processor import procesar_genotipos
from src.logic.pdf_generator import generar_pdf_paciente

class Ventana_inicial:
    def __init__(self, master):
        self.master = master
        self.df_resultados = None

        # --- ESTILOS PARA LA TABLA (Integración de ttk con modo oscuro) ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#2b2b2b",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=('Helvetica', 10))
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        font=('Helvetica', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        # --- CONTENEDOR PRINCIPAL ---
        main_frame = ctk.CTkFrame(self.master, corner_radius=15)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- SECCIÓN SUPERIOR ---
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=(10, 20), padx=10)

        titulo = ctk.CTkLabel(header_frame, text="💊 DrogApp: Reportes de Farmacogenética", 
                              font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"))
        titulo.pack(side=tk.LEFT)

        self.btn_cargar = ctk.CTkButton(header_frame, text="📂 Cargar CSV", command=self.cargar_csv, 
                                        font=ctk.CTkFont(weight="bold"))
        self.btn_cargar.pack(side=tk.RIGHT)

        self.lbl_estado = ctk.CTkLabel(header_frame, text="Esperando archivo...", 
                                       text_color="gray", font=ctk.CTkFont(slant="italic"))
        self.lbl_estado.pack(side=tk.RIGHT, padx=15)

        # --- SECCIÓN MEDIA (Tabla) ---
        table_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)

        self.tree = ttk.Treeview(table_frame, show='headings', selectmode="browse")
        
        # Barras de desplazamiento
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar_x.pack(side=tk.TOP, fill=tk.X, padx=20)

        # --- SECCIÓN INFERIOR ---
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill=tk.X, pady=(20, 10), padx=10)

        self.btn_pdf = ctk.CTkButton(footer_frame, text="📄 Generar PDF del Paciente", command=self.exportar_pdf, 
                                     state="disabled", fg_color="gray", font=ctk.CTkFont(weight="bold"))
        self.btn_pdf.pack(side=tk.RIGHT)
        
        instrucciones = ctk.CTkLabel(footer_frame, text="* Selecciona un paciente de la tabla para exportar su informe.", 
                                     text_color="gray")
        instrucciones.pack(side=tk.LEFT)

    # --- LÓGICA DE LA INTERFAZ ---
    def cargar_csv(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if ruta_archivo:
            try:
                self.lbl_estado.configure(text="Procesando datos...", text_color="#E67E22")
                self.master.update()
                
                # Llamada a la lógica procesadora
                self.df_resultados = procesar_genotipos(ruta_archivo)
                self.actualizar_tabla(self.df_resultados)
                
                # Rehabilitar botón con su color original
                self.btn_pdf.configure(state="normal", fg_color=['#3B8ED0', '#1F6AA5']) 
                self.lbl_estado.configure(text="✅ Datos cargados", text_color="#27AE60")
                
            except Exception as e:
                self.lbl_estado.configure(text="❌ Error al cargar", text_color="#E74C3C")
                messagebox.showerror("Error", f"Ocurrió un error procesando el archivo:\n{e}")

    def actualizar_tabla(self, df):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        columnas = list(df.columns)
        self.tree["columns"] = columnas
        
        for col in columnas:
            self.tree.heading(col, text=col)
            ancho = 180 if "Fenotipo" in col or "Diplotipo" in col else 100
            self.tree.column(col, width=ancho, anchor=tk.CENTER)

        # Alternar colores en las filas (modo oscuro)
        for index, row in df.iterrows():
            valores = list(row)
            tag = "par" if index % 2 == 0 else "impar"
            self.tree.insert("", "end", values=valores, tags=(tag,))
            
        self.tree.tag_configure("impar", background="#333333")
        self.tree.tag_configure("par", background="#2b2b2b")

    def exportar_pdf(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, haz clic sobre un paciente de la lista primero.")
            return
            
        valores = self.tree.item(seleccion[0], 'values')
        columnas = self.tree["columns"]
        datos_paciente = dict(zip(columnas, valores))

        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            initialfile=f"Informe_{datos_paciente.get('Paciente', 'Paciente')}.pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar informe PDF como..."
        )
        
        if ruta_guardado:
            try:
                generar_pdf_paciente(datos_paciente, ruta_guardado)
                messagebox.showinfo("Éxito", f"¡PDF generado correctamente!\n\nSe ha guardado en:\n{ruta_guardado}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el PDF:\n{e}")