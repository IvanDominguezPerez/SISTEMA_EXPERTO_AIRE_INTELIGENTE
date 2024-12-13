import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import webbrowser
from PIL import Image, ImageTk

# Archivo donde se almacenará la información
data_file = "aire_data.json"

# Inicializar archivo JSON si no existe
def init_data_file():
    try:
        with open(data_file, "r") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(data_file, "w") as f: 
            json.dump({}, f)

# Guardar datos en el archivo JSON
def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

# Cargar datos del archivo JSON
def load_data():
    with open(data_file, "r") as f:
        return json.load(f)

# Crear la aplicación principal
class AireInteligenteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AIRE INTELIGENTE")
        self.root.geometry("800x600")

        self.current_frame = None
        self.background_image = ImageTk.PhotoImage(Image.open("background.jpg"))
        self.switch_frame(self.main_menu)

    def switch_frame(self, frame_function):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        background_label = tk.Label(self.current_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)
        frame_function()

    def main_menu(self):
        tk.Label(self.current_frame, text="BIENVENIDO A AIRE INTELIGENTE", font=("Arial", 24), bg="white").pack(pady=50)

        user_button = tk.Button(self.current_frame, text="Usuario", command=lambda: self.switch_frame(self.user_menu), width=20, height=2)
        user_button.pack(pady=10)

        admin_button = tk.Button(self.current_frame, text="Administrador", command=self.admin_login, width=20, height=2)
        admin_button.pack(pady=10)

        exit_button = tk.Button(self.current_frame, text="Salir", command=self.exit_program, width=20, height=2)
        exit_button.pack(pady=10)

    def exit_program(self):
        self.root.destroy()

    def admin_login(self):
        password = simpledialog.askstring("Administrador", "Ingrese la contraseña:", show='*')
        if password == "0243":
            self.switch_frame(self.admin_menu)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def admin_menu(self):
        tk.Label(self.current_frame, text="Menú de Administrador", font=("Arial", 18), bg="white").pack(pady=20)

        buttons = [
            ("Marcas de Aire", lambda: self.manage_info("Marcas de Aire")),
            ("Tipos de Equipos", lambda: self.manage_info("Tipos de Equipos")),
            ("Mantenimientos", lambda: self.manage_info("Mantenimientos")),
            ("Cómo Seleccionar Mi Aire", lambda: self.manage_info("Cómo Seleccionar Mi Aire")),
            ("Comprar Aire", lambda: self.manage_info("Comprar Aire")),
            ("Regresar", lambda: self.switch_frame(self.main_menu))
        ]

        for text, command in buttons:
            tk.Button(self.current_frame, text=text, command=command, width=25, height=2).pack(pady=5)

    def manage_info(self, category):
        data = load_data()
        if category not in data:
            data[category] = []

        def add_info():
            name_label = "Modelo:" if category == "Comprar Aire" else ("Tipo de Equipo:" if category == "Mantenimientos" else "Nombre:")
            name = name_entry.get()
            description = description_entry.get()
            link = link_entry.get() if category == "Comprar Aire" else None
            cost = cost_entry.get() if category == "Comprar Aire" else None

            if name and description:
                entry = {"name": name, "description": description}
                if link:
                    entry["link"] = link
                if cost:
                    entry["cost"] = cost
                data[category].append(entry)
                save_data(data)
                messagebox.showinfo("Éxito", "Información agregada correctamente")
                self.switch_frame(lambda: self.manage_info(category))

        self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        background_label = tk.Label(self.current_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        tk.Label(self.current_frame, text=f"Gestionar {category}", font=("Arial", 18), bg="white").pack(pady=20)

        frame_container = tk.Frame(self.current_frame, bg="white")
        frame_container.pack(fill="both", expand=True, pady=10)

        canvas = tk.Canvas(frame_container, bg="white")
        scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for info in data[category]:
            frame = tk.Frame(scrollable_frame, pady=5, padx=10, relief="groove", borderwidth=1, bg="white")
            frame.pack(fill="x", pady=5, padx=10)

            label_type = "Tipo de Equipo:" if category == "Mantenimientos" else "Modelo:" if category == "Comprar Aire" else "Nombre:"
            tk.Label(frame, text=f"{label_type} {info['name']}", font=("Arial", 12, "bold"), anchor="w", bg="white").pack(fill="x")

            if category == "Mantenimientos" and info['description'].startswith("http"):
                link_label = tk.Label(frame, text="Ver video", fg="blue", cursor="hand2", bg="white")
                link_label.pack()
                link_label.bind("<Button-1>", lambda e, url=info['description']: webbrowser.open(url))
            else:
                tk.Label(frame, text=f"Descripción: {info['description']}", anchor="w", wraplength=700, justify="left", bg="white").pack(fill="x")

            if category == "Comprar Aire" and "cost" in info:
                tk.Label(frame, text=f"Costo: {info['cost']}", anchor="w", wraplength=700, justify="left", bg="white").pack(fill="x")

        name_label = "Modelo:" if category == "Comprar Aire" else ("Tipo de Equipo:" if category == "Mantenimientos" else "Nombre:")
        tk.Label(self.current_frame, text=name_label, bg="white").pack()
        name_entry = tk.Entry(self.current_frame, width=50)
        name_entry.pack(pady=5)

        tk.Label(self.current_frame, text="Descripción:", bg="white").pack()
        description_entry = tk.Entry(self.current_frame, width=50)
        description_entry.pack(pady=5)

        if category == "Comprar Aire":
            tk.Label(self.current_frame, text="Enlace:", bg="white").pack()
            link_entry = tk.Entry(self.current_frame, width=50)
            link_entry.pack(pady=5)

            tk.Label(self.current_frame, text="Costo:", bg="white").pack()
            cost_entry = tk.Entry(self.current_frame, width=50)
            cost_entry.pack(pady=5)

        if category == "Mantenimientos":
            tk.Label(self.current_frame, text="(Ingrese un enlace a un video en la descripción si aplica)", bg="white", font=("Arial", 10, "italic")).pack(pady=5)

        tk.Button(self.current_frame, text="Agregar Información", command=add_info).pack(pady=5)
        tk.Button(self.current_frame, text="Regresar", command=lambda: self.switch_frame(self.admin_menu)).pack(pady=5)

    def user_menu(self):
        tk.Label(self.current_frame, text="Menú de Usuario", font=("Arial", 18), bg="white").pack(pady=20)

        buttons = [
            ("Marcas de Aire", lambda: self.view_info("Marcas de Aire")),
            ("Tipos de Equipos", lambda: self.view_info("Tipos de Equipos")),
            ("Mantenimientos", lambda: self.view_info("Mantenimientos")),
            ("Cómo Seleccionar Mi Aire", lambda: self.view_info("Cómo Seleccionar Mi Aire")),
            ("Comprar Aire", lambda: self.view_info("Comprar Aire")),
            ("Regresar", lambda: self.switch_frame(self.main_menu))
        ]

        for text, command in buttons:
            tk.Button(self.current_frame, text=text, command=command, width=25, height=2).pack(pady=5)

    def view_info(self, category):
        data = load_data()
        if category not in data:
            data[category] = []

        self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        background_label = tk.Label(self.current_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        tk.Label(self.current_frame, text=f"{category}", font=("Arial", 18), bg="white").pack(pady=20)

        if category == "Cómo Seleccionar Mi Aire":
            tk.Label(self.current_frame, text="Dimensiones y Tonelaje Sugerido", font=("Arial", 16), bg="white").pack(pady=10)

            labels = [
                "Hasta 20 m²: 1 Tonelada",
                "De 20 m² a 40 m²: 1.5 Toneladas",
                "De 40 m² a 60 m²: 2 Toneladas",
                "Más de 60 m²: Consultar con un especialista"
            ]

            for label in labels:
                tk.Label(self.current_frame, text=label, font=("Arial", 12), bg="white", anchor="w").pack(pady=2)

        frame_container = tk.Frame(self.current_frame, bg="white")
        frame_container.pack(fill="both", expand=True, pady=10)

        canvas = tk.Canvas(frame_container, bg="white")
        scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for info in data[category]:
            frame = tk.Frame(scrollable_frame, pady=5, padx=10, relief="groove", borderwidth=1, bg="white")
            frame.pack(fill="x", pady=5, padx=10)

            label_type = "Tipo de Equipo:" if category == "Mantenimientos" else "Modelo:" if category == "Comprar Aire" else "Nombre:"
            tk.Label(frame, text=f"{label_type} {info['name']}", font=("Arial", 12, "bold"), anchor="w", bg="white").pack(fill="x")

            if category == "Mantenimientos" and info['description'].startswith("http"):
                link_label = tk.Label(frame, text="Ver video", fg="blue", cursor="hand2", bg="white")
                link_label.pack()
                link_label.bind("<Button-1>", lambda e, url=info['description']: webbrowser.open(url))
            else:
                tk.Label(frame, text=f"Descripción: {info['description']}", anchor="w", wraplength=700, justify="left", bg="white").pack(fill="x")

            if category == "Comprar Aire" and "cost" in info:
                tk.Label(frame, text=f"Costo: {info['cost']}", anchor="w", wraplength=700, justify="left", bg="white").pack(fill="x")

        tk.Button(self.current_frame, text="Regresar", command=lambda: self.switch_frame(self.user_menu)).pack(pady=20)

if __name__ == "__main__":
    init_data_file()
    root = tk.Tk()
    app = AireInteligenteApp(root)
    root.mainloop()
