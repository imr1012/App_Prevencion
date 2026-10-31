import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
from src.logic.processor import procesar_genotipos
from src.logic.pdf_generator import generar_pdf_paciente, generar_pdf_manual, informe_pdf
from src.logic.generar_recomendaciones import generar_recomendaciones



ctk.set_appearance_mode("Light")
class Ventana_inicial:
    def __init__(self, master):
        self.master = master
        self.df_resultados = None
        self.df_recomendaciones = None


        self.COLOR_BG = "#FFF0F5"      
        self.COLOR_CARD = "#FFFFFF"       
        self.COLOR_PRIMARY = "#D84B75"    
        self.COLOR_HOVER = "#C23863"      
        self.COLOR_ACCENT = "#E77298"     
        self.COLOR_FILA_PAR = "#FFFFFF"   
        self.COLOR_FILA_IMPAR = "#FDF0F4" 
        self.COLOR_TEXT = "#4A2835"       

        
        self.master.configure(bg=self.COLOR_BG)

        # --- ESTILOS PARA LA TABLA (Integración de ttk con modo oscuro) ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=self.COLOR_FILA_PAR,
                        foreground=self.COLOR_TEXT,
                        rowheight=32,
                        fieldbackground=self.COLOR_FILA_PAR,
                        bordercolor="#F5C2D2",
                        borderwidth=1,
                        font=('Helvetica', 10))
        style.map('Treeview', 
                  background=[('selected', self.COLOR_ACCENT)],
                  foreground=[('selected', 'white')])
        style.configure("Treeview.Heading",
                        background=self.COLOR_PRIMARY,
                        foreground="white",
                        relief="flat",
                        padding=6,
                        font=('Helvetica', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', self.COLOR_HOVER)])
        # --- CONTENEDOR PRINCIPAL ---
        main_frame = ctk.CTkScrollableFrame(
            self.master, 
            corner_radius=18, 
            fg_color=self.COLOR_CARD,
            border_color="#F8B4C9",
            border_width=2
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- SECCIÓN SUPERIOR ---
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=(10, 10), padx=10)

        titulo = ctk.CTkLabel(header_frame, text="💊 DrugApp: Reportes de Farmacogenética",
                      text_color=self.COLOR_PRIMARY,
                      font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"))
        
        titulo.pack(side=tk.LEFT)

        self.btn_cargar = ctk.CTkButton(header_frame, text="📂 Cargar CSV", command=self.cargar_csv,
                                font=ctk.CTkFont(weight="bold"),
                                fg_color=self.COLOR_PRIMARY,
                                hover_color=self.COLOR_HOVER,
                                text_color="white")
        self.btn_cargar.pack(side=tk.RIGHT)

        self.lbl_estado = ctk.CTkLabel(header_frame, text="Esperando archivo...", 
                                       text_color="gray", font=ctk.CTkFont(slant="italic"))
        self.lbl_estado.pack(side=tk.RIGHT, padx=15)

        # --- SECCIÓN MEDIA (Tabla) ---
        table_frame = ctk.CTkFrame(main_frame, corner_radius=10,
                           fg_color=self.COLOR_CARD,
                           border_color="#F8B4C9", border_width=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)

        self.tree = ttk.Treeview(table_frame, show='headings', selectmode="browse")
        
        # Barras de desplazamiento
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)

        #style.configure("Vertical.TScrollbar", background=self.COLOR_ACCENT,
                #troughcolor=self.COLOR_BG, bordercolor=self.COLOR_BG,
                #arrowcolor="white")
        #style.configure("Horizontal.TScrollbar", background=self.COLOR_ACCENT,
                        #troughcolor=self.COLOR_BG, bordercolor=self.COLOR_BG,
                        #arrowcolor="white")
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar_x.pack(side=tk.TOP, fill=tk.X, padx=20)

        # --- SECCIÓN INFERIOR ---
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill=tk.X, pady=(20, 10), padx=10)

        '''
        self.btn_pdf = ctk.CTkButton(footer_frame, text="📄 Generar PDF del Paciente", command=self.exportar_pdf,
                             state="disabled",
                             fg_color="#E8B9C8",
                             hover_color=self.COLOR_HOVER,
                             text_color="white",
                             text_color_disabled="white",
                             font=ctk.CTkFont(weight="bold"))
        self.btn_pdf.pack(side=tk.RIGHT)

        '''
        self.btn_previ = ctk.CTkButton(footer_frame, text="Previsualizar recomendaciones", command=self.previsualizacion,
                             state="disabled",
                             fg_color="#E8B9C8",
                             hover_color=self.COLOR_HOVER,
                             text_color="white",
                             text_color_disabled="white",
                             font=ctk.CTkFont(weight="bold"))
        self.btn_previ.pack(side=tk.RIGHT, padx=10)
    
        
        self.btn_paciente = ctk.CTkButton(footer_frame, text="Añadir datos de paciente", command=self.datos_paciente,
                             state="disabled",
                             fg_color="#E8B9C8",
                             hover_color=self.COLOR_HOVER,
                             text_color="white",
                             text_color_disabled="white",
                             font=ctk.CTkFont(weight="bold"))
        self.btn_paciente.pack(side=tk.RIGHT, padx=10)
        
        instrucciones = ctk.CTkLabel(footer_frame,
                             text="* Selecciona un paciente de la tabla para exportar su informe.",
                             text_color=self.COLOR_TEXT)
        instrucciones.pack(side=tk.LEFT)

        '''
        # Línea divisoria
        separador = ctk.CTkFrame(main_frame, height=2, fg_color="#F8B4C9")
        separador.pack(fill=tk.X, padx=20, pady=25)
        '''



    # --- LÓGICA DE LA INTERFAZ ---
    def cargar_csv(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if ruta_archivo:
            try:
                self.lbl_estado.configure(text="Procesando datos...", text_color="#E67E22")
                self.master.update()
                
                # Llamada a la lógica procesadora
                self.df_resultados, solucion = procesar_genotipos(ruta_archivo)              
                self.actualizar_tabla(self.df_resultados)
                # Recomendaciones para la previsualización
                self.df_recomendaciones = generar_recomendaciones(solucion)
                # Rehabilitar botón con su color original
                #self.btn_pdf.configure(state="normal", fg_color=self.COLOR_PRIMARY)
                self.btn_previ.configure(state="normal", fg_color=self.COLOR_PRIMARY)
                self.btn_paciente.configure(state="normal", fg_color=self.COLOR_PRIMARY)
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
            
        self.tree.tag_configure("impar", background=self.COLOR_FILA_IMPAR, foreground=self.COLOR_TEXT)
        self.tree.tag_configure("par", background=self.COLOR_FILA_PAR, foreground=self.COLOR_TEXT)

    '''
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

    '''

    def datos_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, haz clic sobre un paciente de la lista primero.")
            return

        valores = self.tree.item(seleccion[0], 'values')
        datos_paciente = dict(zip(self.tree["columns"], valores))
        id_paciente = str(datos_paciente.get("Paciente", ""))

        #Construcción de ventana
        # Ventana emergente
        win = ctk.CTkToplevel(self.master)
        win.title(f"Paciente {id_paciente}")
        win.geometry("720x500")
        win.configure(fg_color=self.COLOR_BG)
        win.after(100, win.lift)   # evita que quede detrás en algunos sistemas
        win.grab_set()

        ctk.CTkLabel(win, text=f"Paciente: {id_paciente}",
                    text_color=self.COLOR_PRIMARY,
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        #Ingreso manual del usuario de los datos
        lbl_manual = ctk.CTkLabel(win, text="📝 Ingreso Manual de Paciente Individual",
                                  text_color=self.COLOR_PRIMARY,
                                  font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"))
        lbl_manual.pack(anchor="w", padx=20, pady=(0, 15))

        datos_frame = ctk.CTkFrame(win, fg_color="transparent")
        datos_frame.pack(fill=tk.X, padx=20)

        # Fila 1: Nombre, Apellido, DNI
        self.ent_nombre = ctk.CTkEntry(datos_frame, placeholder_text="Nombre", width=200, border_color="#F8B4C9")
        self.ent_nombre.grid(row=0, column=0, padx=(0, 15), pady=10)
        self.ent_apellido = ctk.CTkEntry(datos_frame, placeholder_text="Apellidos", width=200, border_color="#F8B4C9")
        self.ent_apellido.grid(row=0, column=1, padx=15, pady=10)
        self.ent_dni = ctk.CTkEntry(datos_frame, placeholder_text="DNI (Opcional)", width=150, border_color="#F8B4C9")
        self.ent_dni.grid(row=0, column=2, padx=15, pady=10)

        # Fila 2: Sexo, Fecha de Nacimiento
        self.cbx_sexo = ctk.CTkComboBox(datos_frame, values=["Seleccionar Sexo", "Masculino", "Femenino", "Otro"], width=200, border_color="#F8B4C9", button_color=self.COLOR_PRIMARY)
        self.cbx_sexo.grid(row=1, column=0, padx=(0, 15), pady=10)
        self.ent_fecha = ctk.CTkEntry(datos_frame, placeholder_text="Fecha Nacimiento (DD/MM/AAAA)", width=200, border_color="#F8B4C9")
        self.ent_fecha.grid(row=1, column=1, padx=15, pady=10)

        # Fila 3: Patologías
        ctk.CTkLabel(datos_frame, text="Patologías actuales (Opcional):", text_color=self.COLOR_TEXT, font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=3, sticky="w", pady=(15, 5))
        self.txt_enferm = ctk.CTkTextbox(datos_frame, height=60, width=580, border_color="#F8B4C9", border_width=2, fg_color=self.COLOR_FILA_PAR)
        self.txt_enferm.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 15))

        # Fila 4: Tratamientos
        ctk.CTkLabel(datos_frame, text="Tratamiento habitual (Opcional):", text_color=self.COLOR_TEXT, font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, columnspan=3, sticky="w", pady=(15, 5))
        self.txt_tto = ctk.CTkTextbox(datos_frame, height=60, width=580, border_color="#F8B4C9", border_width=2, fg_color=self.COLOR_FILA_PAR)
        self.txt_tto.grid(row=5, column=0, columnspan=3, sticky="w", pady=(0, 15))        

        '''
        # Fila 4: Cuadro Genético
        ctk.CTkLabel(datos_frame, text="Cuadro Genético Conocido:", text_color=self.COLOR_PRIMARY, font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, columnspan=3, sticky="w", pady=(10, 5))
        
        gen_frame = ctk.CTkFrame(datos_frame, fg_color="transparent")
        gen_frame.grid(row=5, column=0, columnspan=3, sticky="w")

        self.ent_gen = ctk.CTkEntry(gen_frame, placeholder_text="Gen (ej. CYP2D6)", width=130, border_color="#F8B4C9")
        self.ent_gen.pack(side=tk.LEFT, padx=(0, 10))
        self.ent_alelo1 = ctk.CTkEntry(gen_frame, placeholder_text="Alelo 1 (ej. *1)", width=90, border_color="#F8B4C9")
        self.ent_alelo1.pack(side=tk.LEFT, padx=10)
        self.ent_alelo2 = ctk.CTkEntry(gen_frame, placeholder_text="Alelo 2 (ej. *4)", width=90, border_color="#F8B4C9")
        self.ent_alelo2.pack(side=tk.LEFT, padx=10)
        
        btn_add_gen = ctk.CTkButton(gen_frame, text="➕ Añadir Gen", command=self.add_gen_manual, 
                                    fg_color=self.COLOR_PRIMARY, hover_color=self.COLOR_HOVER, font=ctk.CTkFont(weight="bold"))
        btn_add_gen.pack(side=tk.LEFT, padx=15)

        # Tabla Manual de Genes
        self.tree_manual = ttk.Treeview(datos_frame, columns=("Gen", "Alelo 1", "Alelo 2", "Diplotipo"), show='headings', height=4)
        for col in ("Gen", "Alelo 1", "Alelo 2", "Diplotipo"):
            self.tree_manual.heading(col, text=col)
            self.tree_manual.column(col, width=130, anchor=tk.CENTER)
        self.tree_manual.grid(row=6, column=0, columnspan=3, sticky="we", pady=15)
        '''

        # Botón final Manual
        btn_pdf_manual = ctk.CTkButton(win, text="📄 Generar PDF del Paciente", command=self.exportar_pdf_manual, 
                                       fg_color=self.COLOR_PRIMARY, hover_color=self.COLOR_HOVER, font=ctk.CTkFont(weight="bold"))
        btn_pdf_manual.pack(side=tk.RIGHT, padx=20, pady=(0, 20))
        
    
    def previsualizacion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, haz clic sobre un paciente de la lista primero.")
            return

        valores = self.tree.item(seleccion[0], 'values')
        datos_paciente = dict(zip(self.tree["columns"], valores))
        id_paciente = str(datos_paciente.get("Paciente", ""))

        df = self.df_recomendaciones
        df_paciente = df[df["Identificador paciente"] == id_paciente]

        if df_paciente.empty:
            messagebox.showinfo("Sin datos", f"No hay recomendaciones para el paciente {id_paciente}.")
            return

        # Ventana emergente
        win = ctk.CTkToplevel(self.master)
        win.title(f"Recomendaciones - {id_paciente}")
        win.geometry("800x300")
        win.configure(fg_color=self.COLOR_BG)
        win.after(100, win.lift)   # evita que quede detrás en algunos sistemas
        win.grab_set()

        ctk.CTkLabel(win, text=f"Paciente: {id_paciente}",
                    text_color=self.COLOR_PRIMARY,
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        frame = ctk.CTkFrame(win, fg_color=self.COLOR_CARD, corner_radius=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        columnas = list(df_paciente.columns.drop("Identificador paciente"))
        tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="none")

        anchos = {"Gen": 90, "Nombre medicación": 180, "Recomendaciones": 380}
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=anchos.get(col, 120), anchor=tk.CENTER)

        for i, (_, fila) in enumerate(df_paciente.iterrows()):
            tag = "par" if i % 2 == 0 else "impar"
            tree.insert("", "end", values=[fila[c] for c in columnas], tags=(tag,))

        tree.tag_configure("par", background=self.COLOR_FILA_PAR)
        tree.tag_configure("impar", background=self.COLOR_FILA_IMPAR)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
    def add_gen_manual(self):
        gen = self.ent_gen.get().strip().upper()
        a1 = self.ent_alelo1.get().strip()
        a2 = self.ent_alelo2.get().strip()
        if gen and a1 and a2:
            diplotipo = f"{a1}/{a2}"
            
            # Etiquetado para intercalar colores
            num_items = len(self.tree_manual.get_children())
            tag = "par" if num_items % 2 == 0 else "impar"
            
            self.tree_manual.insert("", "end", values=(gen, a1, a2, diplotipo), tags=(tag,))
            self.tree_manual.tag_configure("impar", background=self.COLOR_FILA_IMPAR, foreground=self.COLOR_TEXT)
            self.tree_manual.tag_configure("par", background=self.COLOR_FILA_PAR, foreground=self.COLOR_TEXT)
            
            self.ent_gen.delete(0, tk.END)
            self.ent_alelo1.delete(0, tk.END)
            self.ent_alelo2.delete(0, tk.END)
        else:
            messagebox.showwarning("Faltan datos", "Por favor rellena el Gen y ambos alelos.")

    def exportar_pdf_manual(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, haz clic sobre un paciente de la lista primero.")
            return

        valores = self.tree.item(seleccion[0], 'values')
        datos_paciente = dict(zip(self.tree["columns"], valores))
        id_paciente = str(datos_paciente.get("Paciente", ""))

            
        df_resultados = self.df_resultados
        df_res = df_resultados[df_resultados["Paciente"] == id_paciente]


        df = self.df_recomendaciones
        df_paciente = df[df["Identificador paciente"] == id_paciente]

        nombre = self.ent_nombre.get().strip()
        apellido = self.ent_apellido.get().strip()
        
        if not nombre or not apellido:
            messagebox.showwarning("Faltan datos", "El Nombre y los Apellidos son obligatorios.")
            return
            
        genes = []
        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            genes.append({"Gen": valores[0], "Diplotipo": valores[3]})

        datos = {
            "Nombre": f"{nombre} {apellido}",
            "DNI": self.ent_dni.get().strip() or "No especificado",
            "Sexo": self.cbx_sexo.get() if self.cbx_sexo.get() != "Seleccionar Sexo" else "No especificado",
            "Fecha Nacimiento": self.ent_fecha.get().strip() or "No especificada",
            "Enfermedades": self.txt_enferm.get("1.0", tk.END).strip() or "Ninguna",
            "Tratamientos": self.txt_tto.get("1.0", tk.END).strip() or "Ninguno",
            "Genes": genes
        }

        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"Informe_{nombre}_{apellido}.pdf")
        if ruta:
            informe_pdf(id_paciente, datos, df_res, df_paciente, ruta)
            messagebox.showinfo("Éxito", "Informe del paciente generado correctamente.")