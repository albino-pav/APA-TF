import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import customtkinter
import os
from PIL import Image
import json
import os
from datetime import datetime, timedelta

# Tema y colores

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DelePrestecs Release v1.0")
        self.iconbitmap('img/dele.ico')
        self.geometry("700x450")
        self.resizable(False, False) # Width, Height

        # Cargamos los datos
        self.usuarios = self.cargar_usuarios()
        self.materiales = self.cargar_materiales()
        self.prestecs = self.cargar_prestamos()

        # Creamos un grid 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargamos las imágenes
        self.logo_img = customtkinter.CTkImage(Image.open('img/dele.png'), size=(26, 26))
        self.deleprestecs_img = customtkinter.CTkImage(Image.open("img/deleprestecs.png"), size=(500, 150))
        self.prestec_img = customtkinter.CTkImage(Image.open("img/prestec.png"), size=(20, 20))
        self.material_img = customtkinter.CTkImage(Image.open("img/material.png"), size=(20, 20))
        self.usuaris_img = customtkinter.CTkImage(Image.open("img/usuaris.png"), size=(20, 20))

        # Creamos el frame de navegación
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="DELESEIAAT", image=self.logo_img, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.prestecs_button = customtkinter.CTkButton(self.navigation_frame, 
                                                       corner_radius=0, 
                                                       height=40, 
                                                       border_spacing=10, 
                                                       text="Prestecs",
                                                       fg_color="transparent", 
                                                       text_color=("gray10", "gray90"), 
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.prestec_img, 
                                                       anchor="w",
                                                       command=self.prestecs_button_event)
        self.prestecs_button.grid(row=1, column=0, sticky="ew")

        self.materials_button = customtkinter.CTkButton(self.navigation_frame, 
                                                       corner_radius=0, 
                                                       height=40, 
                                                       border_spacing=10, 
                                                       text="Materials",
                                                       fg_color="transparent", 
                                                       text_color=("gray10", "gray90"), 
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.material_img, 
                                                       anchor="w",
                                                       command=self.materials_button_event)
        self.materials_button.grid(row=2, column=0, sticky="ew")

        self.usuaris_button = customtkinter.CTkButton(self.navigation_frame, 
                                                       corner_radius=0, 
                                                       height=40, 
                                                       border_spacing=10, 
                                                       text="Usuaris",
                                                       fg_color="transparent", 
                                                       text_color=("gray10", "gray90"), 
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.usuaris_img, 
                                                       anchor="w",
                                                       command=self.usuaris_button_event)
        self.usuaris_button.grid(row=3, column=0, sticky="ew")

         # create frame prestecs
        self.prestecs_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.prestecs_frame.grid_columnconfigure(0, weight=1)

        self.prestecs_frame_img = customtkinter.CTkLabel(self.prestecs_frame, text="", image=self.deleprestecs_img)
        self.prestecs_frame_img.grid(row=0, column=0, padx=20, pady=10)
        self.prestecs_frame_prestecs_list_button = customtkinter.CTkButton(self.prestecs_frame, text="Llista de prestecs",height=50, width=250, font = ("Helvetica", 24), command=self.prestecs_frame_prestecs_list_button_event)
        self.prestecs_frame_prestecs_list_button.grid(row=1, column=0, padx=20, pady=10)
        self.prestecs_frame_prestec_button = customtkinter.CTkButton(self.prestecs_frame, text="Nou prestec",height=50, width=250, font = ("Helvetica", 24), command=self.prestecs_frame_prestec_button_event)
        self.prestecs_frame_prestec_button.grid(row=2, column=0, padx=20, pady=10)
        self.prestecs_frame_retornament_button = customtkinter.CTkButton(self.prestecs_frame, text="Retornament",height=50, width=250, font = ("Helvetica", 24), command=self.prestecs_frame_retornament_button_event)
        self.prestecs_frame_retornament_button.grid(row=3, column=0, padx=20, pady=10)
    

        

        # create frame materials
        self.materials_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.materials_frame.grid_columnconfigure(0, weight=1)

        self.materials_frame_img = customtkinter.CTkLabel(self.materials_frame, text="", image=self.deleprestecs_img)
        self.materials_frame_img.grid(row=0, column=0, padx=20, pady=10)
        self.materials_frame_material_list_button = customtkinter.CTkButton(self.materials_frame, text="Llista de materials",height=50, width=250, font = ("Helvetica", 24), command=self.materials_frame_material_list_button_event)
        self.materials_frame_material_list_button.grid(row=1, column=0, padx=20, pady=10)
        self.materials_frame_material_new_button = customtkinter.CTkButton(self.materials_frame, text="Afegir material",height=50, width=250, font = ("Helvetica", 24), command=self.materials_frame_material_new_button_event)
        self.materials_frame_material_new_button.grid(row=2, column=0, padx=20, pady=10)
        self.materials_frame_material_delete_button = customtkinter.CTkButton(self.materials_frame, text="Eliminar material",height=50, width=250, font = ("Helvetica", 24), command=self.materials_frame_material_delete_button_event)
        self.materials_frame_material_delete_button.grid(row=3, column=0, padx=20, pady=10)


        # create frame usuaris
        self.usuaris_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.usuaris_frame.grid_columnconfigure(0, weight=1)

        self.usuaris_frame_img = customtkinter.CTkLabel(self.usuaris_frame, text="", image=self.deleprestecs_img)
        self.usuaris_frame_img.grid(row=0, column=0, padx=20, pady=10)
        self.usuaris_frame_user_list_button = customtkinter.CTkButton(self.usuaris_frame, text="Llista de usuaris",height=50, width=250, font = ("Helvetica", 24), command=self.usuaris_frame_user_list_button_event)
        self.usuaris_frame_user_list_button.grid(row=1, column=0, padx=20, pady=10)
        self.usuaris_frame_user_new_button = customtkinter.CTkButton(self.usuaris_frame, text="Usuari nou",height=50, width=250, font = ("Helvetica", 24), command=self.usuaris_frame_user_new_button_event)
        self.usuaris_frame_user_new_button.grid(row=2, column=0, padx=20, pady=10)
        self.usuaris_frame_user_delete_button = customtkinter.CTkButton(self.usuaris_frame, text="Esborrar usuari",height=50, width=250, font = ("Helvetica", 24), command=self.usuaris_frame_user_delete_button_event)
        self.usuaris_frame_user_delete_button.grid(row=3, column=0, padx=20, pady=10)

        # Seleccionamos el frame de inicio
        self.select_frame_by_name("prestecs")

    # Select by frame
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.prestecs_button.configure(fg_color=("gray75", "gray25") if name == "prestecs" else "transparent")
        self.materials_button.configure(fg_color=("gray75", "gray25") if name == "materials" else "transparent")
        self.usuaris_button.configure(fg_color=("gray75", "gray25") if name == "usuaris" else "transparent")

        # show selected frame
        if name == "prestecs":
            self.prestecs_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.prestecs_frame.grid_forget()
        if name == "materials":
            self.materials_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.materials_frame.grid_forget()
        if name == "usuaris":
            self.usuaris_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.usuaris_frame.grid_forget()
    
    # Aqui van las funciones de los botones
    def prestecs_button_event(self):
        self.select_frame_by_name("prestecs")

    def materials_button_event(self):
        self.select_frame_by_name("materials")

    def usuaris_button_event(self):
        self.select_frame_by_name("usuaris")

    # Funciones de prestamos
    def prestecs_frame_prestecs_list_button_event(self):
        # Crear una nueva ventana Toplevel
        top = customtkinter.CTkToplevel(self)
        top.title("Llista de prestecs")
        top.geometry("1200x600")
        top.iconbitmap('img/dele.ico')

        # Crear un frame de CustomTkinter dentro del Toplevel
        frame = customtkinter.CTkFrame(top, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Crear un Treeview dentro del frame
        treeview = ttk.Treeview(frame, columns=("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"), show="headings", height=10)
        treeview.pack(pady=20, padx=20, fill="both", expand=True)

        # Definir los encabezados de columna
        treeview.heading("A", text="Data Prestec")
        treeview.heading("B", text="Data Retornament")
        treeview.heading("C", text="Nom")
        treeview.heading("D", text="Cognom")
        treeview.heading("E", text="DNI")
        treeview.heading("F", text="Correu")
        treeview.heading("G", text="Telèfon")
        treeview.heading("H", text="Material")
        treeview.heading("I", text="ID")
        treeview.heading("J", text="Estat")

        # Definir el tamaño de las columnas
        treeview.column("A", width=100)
        treeview.column("B", width=100)
        treeview.column("C", width=50)
        treeview.column("D", width=50)
        treeview.column("E", width=50)
        treeview.column("F", width=150)
        treeview.column("G", width=100)
        treeview.column("H", width=100)
        treeview.column("I", width=100)
        treeview.column("J", width=100)

        # Agregar algunos datos
        
        for item in self.prestecs:
            treeview.insert("", tk.END, values=(item["Data Prestec"], item["Data Retornament"], item["Nom"], item["Cognom"], item["DNI"], item["Correu"], item["Telefon"], item["Tipo"], item["ID"], item["Estado"]))

    def prestecs_frame_retornament_button_event(self):
        top = customtkinter.CTkToplevel(self)
        top.title("Retornament")
        top.geometry("300x150")
        top.iconbitmap('img/dele.ico')

        def retornar():
            ID = ID_entry.get()
            # estat = estado_entrada.get()
            trobat, prestec = self.buscar_prestamo_por_id(ID)
            if not trobat:
                messagebox.showerror("Error", f"No existeix cap préstec per al material amb l'ID '{ID}'.")
                return

            self.prestecs.remove(prestec)
            messagebox.showinfo("Éxito", f"Préstec del material amb l'ID '{ID}' retornat correctament.")
            self.guardar_prestamos()
            top.destroy()
        
        ID_entry = customtkinter.CTkEntry(top, placeholder_text="ID")
        ID_entry.pack(pady=10)

        # estado_entrada = customtkinter.CTkEntry(top, placeholder_text="Estat")
        # estado_entrada.pack(pady=10)

        retornar_button = customtkinter.CTkButton(top, text="Retornar", command=retornar)
        retornar_button.pack(pady=10)
    
    def prestecs_frame_prestec_button_event(self):
        finestra_prestec = customtkinter.CTkToplevel(self)
        finestra_prestec.title("Nou Préstec")
        finestra_prestec.geometry("300x200")
        finestra_prestec.resizable(False, False) # Width, Height

        def tancar():
            finestra_prestec.destroy()
            finestra_prestec.update()

        def enviar():
            dni = dni_entrada.get()
            material_id = material_entrada.get()

            # Comprobar si el usuario existe
            usuario = next((u for u in self.usuarios if u['DNI'] == dni), None)
            if usuario is None:
                messagebox.showerror("Error", "L'usuari no existeix.")
                return

            # Comprobar si el material existe
            material = next((m for m in self.materiales if m['ID'] == material_id), None)
            if material is None:
                messagebox.showerror("Error", "El material no existeix.")
                return

            # Comprobar si el material ya está prestado
            prestamo_existente = next((p for p in self.prestecs if p['ID'] == material_id), None)
            if prestamo_existente is not None:
                messagebox.showerror("Error", "El material ja està prestat.")
                return

            # Añadir el nuevo préstamo
            hoy = datetime.now()
            data_prestec = hoy.strftime("%Y-%m-%d")
            data_retornament = (hoy + timedelta(weeks=1)).strftime("%Y-%m-%d")
        
            nuevo_prestamo = {
                "Data Prestec": data_prestec,
                "Data Retornament": data_retornament,
                "Nom": usuario["Nombre"],
                "Cognom": usuario["Apellido"],
                "DNI": usuario["DNI"],
                "Correu": usuario["Correo"],
                "Telefon": usuario["Telefono"],
                "Tipo": material["Tipo"],
                "ID": material["ID"],
                "Estado": material["Estado"]
            }

            self.prestecs.append(nuevo_prestamo)
            messagebox.showinfo("Èxit", "Préstec realitzat amb èxit.")
            # Actualitzar les dades guardades
            self.guardar_prestamos()
            tancar()

        dni_entrada = customtkinter.CTkEntry(finestra_prestec, placeholder_text="DNI")
        dni_entrada.pack(pady=10)
    
        material_entrada = customtkinter.CTkEntry(finestra_prestec, placeholder_text="ID del material")
        material_entrada.pack(pady=10) 

        okay_button = customtkinter.CTkButton(finestra_prestec, text="OK", command=enviar)
        okay_button.pack(pady=10)
    
        tancar_button = customtkinter.CTkButton(finestra_prestec, text="Tancar", command=tancar)
        tancar_button.pack(pady=10)

    # Botones de materiales
    def materials_frame_material_list_button_event(self):
        # Crear una nueva ventana Toplevel
        top = customtkinter.CTkToplevel(self)
        top.title("Llista de Materials")
        top.geometry("800x600")
        top.iconbitmap('img/dele.ico')

        # Crear un frame de CustomTkinter dentro del Toplevel
        frame = customtkinter.CTkFrame(top, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Crear un Treeview dentro del frame
        treeview = ttk.Treeview(frame, columns=("Tipo", "ID", "Estado", "Disponibilidad"), show="headings", height=10)
        treeview.pack(pady=20, padx=20, fill="both", expand=True)

        # Definir los encabezados de columna
        treeview.heading("Tipo", text="Tipo")
        treeview.heading("ID", text="ID")
        treeview.heading("Estado", text="Estado")
        treeview.heading("Disponibilidad", text="Disponibilidad")

        # Definir el tamaño de las columnas/
        treeview.column("Tipo", width=150)
        treeview.column("ID", width=150)
        treeview.column("Estado", width=100)
        treeview.column("Disponibilidad", width=200)

        # Agregar los datos de los usuarios al Treeview
        for material in self.materiales:
            disponibilidad, prestamo = self.buscar_prestamo_por_id(material["ID"])
            if disponibilidad:
                disponibilidad = "No disponible"
            else:
                disponibilidad = "Disponible"
                
            treeview.insert("", tk.END, values=(material["Tipo"], material["ID"], material["Estado"], disponibilidad))
    def materials_frame_material_new_button_event(self):
        top = customtkinter.CTkToplevel(self)
        top.title("Nuevo material")
        top.geometry("250x300")
        top.iconbitmap('img/dele.ico')

        def agregar_material():
            tipo = tipo_entry.get()
            ID = ID_entry.get()
            estado = estado_entry.get()

            trobat, _ = self.buscar_material_por_id(ID)
            if trobat:
                messagebox.showerror("Error", "Ya existe ese ID de material.")
                return

            nuevo_material = {
                "Tipo": tipo,
                "ID": ID,
                "Estado": estado,
            }
            
            self.materiales.append(nuevo_material)
            # guardar_usuarios(self.usuarios)
            messagebox.showinfo("Éxito", "Material agregado con éxito.")
            self.guardar_materiales()
            top.destroy()

        tipo_entry = customtkinter.CTkEntry(top, placeholder_text="Tipo")
        tipo_entry.pack(pady=10)
        ID_entry = customtkinter.CTkEntry(top, placeholder_text="ID")
        ID_entry.pack(pady=10)
        estado_entry = customtkinter.CTkEntry(top, placeholder_text="Estado")
        estado_entry.pack(pady=10)

        boton_agregar = customtkinter.CTkButton(top, text="Enviar", command=agregar_material)
        boton_agregar.pack(pady=10)
    def materials_frame_material_delete_button_event(self):
        top = customtkinter.CTkToplevel(self)
        top.title("Eliminar material")
        top.geometry("250x150")
        top.iconbitmap('img/dele.ico')

        def eliminar_material():
            ID = ID_entry.get()
            trobat, material = self.buscar_material_por_id(ID)
            if not trobat:
                messagebox.showerror("Error", "El material no existe.")
                return

            self.materiales.remove(material)
            # guardar_usuarios(self.usuarios)
            messagebox.showinfo("Éxito", "Material eliminado con éxito.")
            self.guardar_materiales()
            top.destroy()

        ID_entry = customtkinter.CTkEntry(top, placeholder_text="ID")
        ID_entry.pack(pady=10)

        boton_eliminar = customtkinter.CTkButton(top, text="Eliminar", command=eliminar_material)
        boton_eliminar.pack(pady=10)

    # Botones de usuarios
    def usuaris_frame_user_list_button_event(self):
        # Crear una nueva ventana Toplevel
        top = customtkinter.CTkToplevel(self)
        top.title("Llista de usuaris")
        top.geometry("800x600")
        top.iconbitmap('img/dele.ico')

        # Crear un frame de CustomTkinter dentro del Toplevel
        frame = customtkinter.CTkFrame(top, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Crear un Treeview dentro del frame
        treeview = ttk.Treeview(frame, columns=("Nombre", "Apellido", "DNI", "Correo", "Telefono"), show="headings", height=10)
        treeview.pack(pady=20, padx=20, fill="both", expand=True)

        # Definir los encabezados de columna
        treeview.heading("Nombre", text="Nom")
        treeview.heading("Apellido", text="Cognom")
        treeview.heading("DNI", text="DNI")
        treeview.heading("Correo", text="Correu Electrònic")
        treeview.heading("Telefono", text="Telèfon")

        # Definir el tamaño de las columnas/
        treeview.column("Nombre", width=150)
        treeview.column("Apellido", width=150)
        treeview.column("DNI", width=100)
        treeview.column("Correo", width=200)
        treeview.column("Telefono", width=100)

        # Agregar los datos de los usuarios al Treeview
        for usuario in self.usuarios:
            treeview.insert("", tk.END, values=(usuario["Nombre"], usuario["Apellido"], usuario["DNI"], usuario["Correo"], usuario["Telefono"]))
    def usuaris_frame_user_new_button_event(self):
        top = customtkinter.CTkToplevel(self)
        top.title("Nou usuari")
        top.geometry("250x300")
        top.iconbitmap('img/dele.ico')

        def agregar_usuario():
            nombre = nombre_entry.get()
            apellido = apellido_entry.get()
            dni = dni_entry.get()
            correo = correo_entry.get()
            telefono = telefono_entry.get()

            trobat, _ = self.buscar_usuario_por_dni(dni)
            if trobat:
                messagebox.showerror("Error", "Usuari amb aquest DNI ja existeix.")
                return

            nuevo_usuario = {
                "Nombre": nombre,
                "Apellido": apellido,
                "DNI": dni,
                "Correo": correo,
                "Telefono": telefono
            }
            self.usuarios.append(nuevo_usuario)
            # guardar_usuarios(self.usuarios)
            messagebox.showinfo("Èxit", "Usuari afegit amb èxit.")
            self.guardar_usuarios()
            top.destroy()

        nombre_entry = customtkinter.CTkEntry(top, placeholder_text="Nom")
        nombre_entry.pack(pady=10)
        apellido_entry = customtkinter.CTkEntry(top, placeholder_text="Cognom")
        apellido_entry.pack(pady=10)
        dni_entry = customtkinter.CTkEntry(top, placeholder_text="DNI")
        dni_entry.pack(pady=10)
        correo_entry = customtkinter.CTkEntry(top, placeholder_text="Correu Electrònic")
        correo_entry.pack(pady=10)
        telefono_entry = customtkinter.CTkEntry(top, placeholder_text="Telèfon")
        telefono_entry.pack(pady=10)

        boton_agregar = customtkinter.CTkButton(top, text="Enviar", command=agregar_usuario)
        boton_agregar.pack(pady=10)    
    def usuaris_frame_user_delete_button_event(self):
        top = customtkinter.CTkToplevel(self)
        top.title("Eliminar usuari")
        top.geometry("300x150")
        top.iconbitmap('img/dele.ico')

        def eliminar_usuario():
            dni = dni_entry.get()
            trobat, usuario = self.buscar_usuario_por_dni(dni)
            if not trobat:
                messagebox.showerror("Error", "El usuario no existe.")
                return

            self.usuarios.remove(usuario)
            # guardar_usuarios(self.usuarios)
            messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
            self.guardar_usuarios()
            top.destroy()

        dni_entry = customtkinter.CTkEntry(top, placeholder_text="DNI")
        dni_entry.pack(pady=10)

        boton_eliminar = customtkinter.CTkButton(top, text="Eliminar", command=eliminar_usuario)
        boton_eliminar.pack(pady=10)


    # Funciones de carga y guardado de datos
    def cargar_prestamos(self):
        archivo = "data/prestamos.json"
        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding="utf-8") as prestamoFile:
                json.dump([], prestamoFile, indent=4)
        with open(archivo, 'r', encoding="utf-8") as prestamoFile:
            prestamos = json.load(prestamoFile)
        return prestamos
    
    def buscar_prestamo_por_id(self, material_id):
        for prestamo in self.prestecs:
            if prestamo["ID"] == material_id:
                return True, prestamo
        return False, None

    def guardar_prestamos(self):
        with open("data/prestamos.json", "w", encoding="utf-8") as prestamoFile:
            json.dump(self.prestecs, prestamoFile, indent=4)
    
    def cargar_usuarios(self):
        archivo = "data/usuarios.json"
        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding="utf-8") as userFile:
                json.dump([], userFile, indent=4)
        with open(archivo, 'r', encoding="utf-8") as userFile:
            usuarios = json.load(userFile)
        return usuarios 
    
    def buscar_usuario_por_dni(self, dni):
        for usuario in self.usuarios:
            if usuario["DNI"] == dni:
                return True, usuario
        return False, None
    
    def guardar_usuarios(self):
        with open("data/usuarios.json", "w", encoding="utf-8") as userFile:
            json.dump(self.usuarios, userFile, indent=4)
    
    def cargar_materiales(self):
        archivo = "data/materiales.json"
        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding="utf-8") as materialFile:
                json.dump([], materialFile, indent=4)
        with open(archivo, 'r', encoding="utf-8") as materialFile:
            materiales = json.load(materialFile)
        return materiales
    
    def buscar_material_por_id(self, id):
        for material in self.materiales:
            if material["ID"] == id:
                return True, material
        return False, None

    def guardar_materiales(self):
        with open("data/materiales.json", "w", encoding="utf-8") as materialFile:
            json.dump(self.materiales, materialFile, indent=4)
    
if __name__ == "__main__":
    app = App()
    app.mainloop()