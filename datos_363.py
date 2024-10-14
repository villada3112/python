import pandas as pd
from tkinter import Tk, Menu, messagebox, simpledialog, filedialog
from statistics import mean, mode, StatisticsError

class MenuApp:
    def __init__(self, master):
        self.master = master
        self.estudiantes = None  
        self.create_menu()

    def create_menu(self):
        barra_menus = Menu(self.master)

        menu_excel = Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Excel", menu=menu_excel)
        menu_excel.add_command(label="Cargar Datos", command=self.load_data)
        menu_excel.add_command(label="Mostrar Todos", command=self.show_all)
        menu_excel.add_command(label="Nombre", command=self.show_name)
        menu_excel.add_command(label="Mayores de 18", command=self.show_over_18)

        menu_calculo = Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Cálculo", menu=menu_calculo)
        menu_calculo.add_command(label="Promedio", command=self.calculate_average)
        menu_calculo.add_command(label="Medida", command=self.show_height)
        menu_calculo.add_command(label="Moda", command=self.calculate_mode)

        self.master.config(menu=barra_menus)

    def load_data(self):
        nombreArchivo = filedialog.askopenfilename(title="Selecciona un archivo de Excel", filetypes=[("Archivos Excel", ".xls;.xlsx")])
        if not nombreArchivo:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
            return

        try:
            self.estudiantes = pd.read_excel(nombreArchivo)
        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo no fue encontrado: {nombreArchivo}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {e}")
            return

        required_columns = ["nombreApellido", "edad", "catHermanos"]
        for col in required_columns:
            if col not in self.estudiantes.columns:
                messagebox.showerror("Error", f"Falta la columna: {col}")
                return

        messagebox.showinfo("Éxito", "Datos cargados correctamente.")

    def show_all(self):
        if self.estudiantes is not None:
            messagebox.showinfo("Datos de Estudiantes", str(self.estudiantes))
        else:
            messagebox.showwarning("Advertencia", "No hay datos cargados.")

    def show_name(self):
        name = simpledialog.askstring("Nombre", "Introduce tu nombre:")
        if name:
            messagebox.showinfo("Nombre ingresado", f"Tu nombre es: {name}")

    def show_over_18(self):
        age = simpledialog.askinteger("Edad", "Introduce tu edad:")
        if age is not None:
            if age >= 18:
                messagebox.showinfo("Acceso permitido", "Eres mayor de 18 años.")
            else:
                messagebox.showwarning("Acceso denegado", "Eres menor de 18 años.")

    def calculate_average(self):
        notas = simpledialog.askstring("Promedio", "Introduce una lista de notas separadas por comas:")
        if notas:
            try:
                notas = list(map(float, notas.split(','))) 
                if not notas:  # Check if the list is empty
                    raise ValueError("La lista de notas no puede estar vacía.")
                promedio = mean(notas) 
                if promedio >= 6:
                    messagebox.showinfo("Resultado", f"Promedio: {promedio:.2f}. ¡Aprobaste!")
                else:
                    messagebox.showinfo("Resultado", f"Promedio: {promedio:.2f}. Desaprobaste.")
            except ValueError:
                messagebox.showerror("Error", "Entrada inválida. Por favor ingresa una lista de números.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def show_height(self):
        height = simpledialog.askfloat("Medida", "Introduce tu altura en metros:")
        if height is not None:  # Check for None
            messagebox.showinfo("Altura ingresada", f"Tu altura es: {height:.2f} metros")

    def calculate_mode(self):
        numeros = simpledialog.askstring("Moda", "Introduce una lista de números separados por comas:")
        if numeros:
            try:
                numeros = list(map(float, numeros.split(',')))  
                if not numeros:  # Check if the list is empty
                    raise ValueError("La lista de números no puede estar vacía.")
                moda = mode(numeros) 
                messagebox.showinfo("Moda", f"La moda es: {moda}")
            except StatisticsError:
                messagebox.showerror("Error", "No existe una moda única.")
            except ValueError:
                messagebox.showerror("Error", "Entrada inválida. Por favor ingresa una lista de números.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Aplicación con Menú Excel y Cálculo")
        
        self.menu_app = MenuApp(self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
