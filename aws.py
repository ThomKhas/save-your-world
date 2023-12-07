import os
import shutil
import tkinter as tk
from tkinter import filedialog
from git import Repo, GitCommandError, cmd
from PIL import Image, ImageTk
from threading import Thread
from git.exc import InvalidGitRepositoryError

def seleccionar_carpeta_src(entry_widget):
    # Carpeta predeterminada
    initial_folder = entry_widget.get()
    # Abre el cuadro de diálogo para seleccionar una carpeta
    src_folder = filedialog.askdirectory(initialdir=initial_folder)

    # Imprime el contenido de la carpeta seleccionada para conocer su formato
    print(f"El contenido seleccionado proviene de: {src_folder}")

    # Actualiza el campo de entrada con la carpeta seleccionada
    entry_widget.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
    entry_widget.insert(0, src_folder)  # Inserta la nueva carpeta seleccionada

    return src_folder

def seleccionar_carpeta_repo(entry_widget):
    # Carpeta predeterminada
    initial_folder = entry_widget.get()
    # Abre el cuadro de diálogo para seleccionar una carpeta
    repo_folder = filedialog.askdirectory(initialdir=initial_folder)

    # Imprime el contenido de la carpeta seleccionada para conocer su formato
    print(f"El contenido seleccionado proviene de: {repo_folder}")

    # Actualiza el campo de entrada con la carpeta seleccionada
    entry_widget.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
    entry_widget.insert(0, repo_folder)  # Inserta la nueva carpeta seleccionada

    return repo_folder

def commit_push(src_folder, repo_folder):
    # Define la ruta de la carpeta que se va a copiar
    src_folder = r"{}".format(src_folder)  # Aplica notación de cadena sin procesar
    # Imprime el contenido de src_folder para conocer su formato
    print("Mundo a Guardar:", src_folder)
    # Define la ruta del repositorio clonado de GitHub en tu sistema local
    repo_folder = r"{}".format(repo_folder)  # Aplica notación de cadena sin procesar
    # Imprime el contenido de repo_folder para conocer su formato
    print("Carpeta Clon:", repo_folder)
    
    
    # Verifica si el repositorio ya ha sido clonado
    if not os.path.exists(repo_folder):
        # Si no, clona el repositorio de GitHub
        # ACÁ DEBES CAMBIAR EL LINK DEL REPOSITORIO A UNO PROPIO
        Repo.clone_from("https://github.com/monitosfullmax/WORLD.git", repo_folder)
    else:
        print("La carpeta ya existe.")
        try:
            repo = Repo(repo_folder)
            print("La carpeta existe y es un repositorio Git válido.")
        except InvalidGitRepositoryError:
            print("La carpeta no es un repositorio Git válido. Se clonará nuevamente.")
            git = cmd.Git()
            # ACÁ DEBES CAMBIAR EL LINK DEL REPOSITORIO A UNO PROPIO
            git.clone("https://github.com/monitosfullmax/WORLD.git", repo_folder)

    # Obtén el nombre de la carpeta de origen
    src_folder_name = os.path.basename(src_folder)

    # Copia la carpeta al repositorio clonado
    dst_folder = os.path.join(repo_folder, src_folder_name)
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)
    shutil.copytree(src_folder, dst_folder)

    # Crea un repositorio de Git Python en la carpeta del repositorio
    repo = Repo(repo_folder)

    # Agrega todos los archivos al staging area
    repo.git.add(A=True)

    # Verifica si hay cambios en el repositorio
    if repo.is_dirty():
        # Si hay cambios, haz un commit
        repo.git.commit(m='Añade la carpeta modificada')

        # Haz un pull del repositorio remoto
        origin = repo.remote(name='origin')
        origin.pull()

        # Haz un push al repositorio remoto
        try: 
            repo.git.push()
            # Si el push fue exitoso, actualiza el mensaje de estado
            status_label.config(text="Guardado exitosamente", fg="green")
        except Exception as e:
            # Si hay algún error, actualiza el mensaje de estado con el mensaje de error
            status_label.config(text=f"Error: {str(e)}", fg="red")
    
    
    
# Crea una ventana de Tkinter
root = tk.Tk()
root.geometry("500x330")  
root.title("SaveYourWorld")  # Establece el título de la ventana
# Cambia el ícono de la ventana (reemplaza "icono.ico" con la ruta de tu propio ícono)
root.iconbitmap("saeico.ico")
# Carga la imagen
logo_path = "sae_logo.png"
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((350, 140))  # Ajusta el tamaño de la imagen si es necesario
logo_image = ImageTk.PhotoImage(logo_image)

# Crea una etiqueta para mostrar la imagen del logo
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()


# Crea un marco para cada conjunto de etiqueta, campo de entrada y botón "Examinar"
src_frame = tk.Frame(root)
src_frame.pack(pady=0)  
repo_frame = tk.Frame(root)
repo_frame.pack(pady=0)  

# Crea una etiqueta con el título en negrita 
titulo_font = ("Helvetica", 14, "bold")
src_label = tk.Label(src_frame, text="🚨Bienvenido a Auto World Save🚨", font=titulo_font)
src_label.pack(pady=0)

# Crea una etiqueta, un campo de entrada y un botón "Examinar" para src_folder
src_label = tk.Label(src_frame, text="Seleccione su mundo")
src_label.pack()
src_entry = tk.Entry(src_frame, width=50)
# Establece la carpeta predeterminada en el primer campo de entrada
src_entry.insert(0, os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft"))
src_entry.pack(side=tk.LEFT)
src_boton = tk.Button(src_frame, text="Examinar", command=lambda: seleccionar_carpeta_src(src_entry))
src_boton.pack(side=tk.LEFT)

# Crea una etiqueta, un campo de entrada y un botón "Examinar" para repo_folder
repo_label = tk.Label(repo_frame, text="Seleccione carpeta 'Clon' en la carpeta SaveYourWorld")
repo_label.pack()
repo_entry = tk.Entry(repo_frame, width=50)
# Establece la carpeta predeterminada en la carpeta del script o ejecutable
repo_entry.insert(0, os.path.dirname(os.path.abspath(__file__)))
repo_entry.pack(side=tk.LEFT)
repo_boton = tk.Button(repo_frame, text="Examinar", command=lambda: seleccionar_carpeta_repo(repo_entry))
repo_boton.pack(side=tk.LEFT)

# Crea un marco para mostrar el estado del push
status_frame = tk.Frame(root)
status_frame.pack(pady=1)

# Crea un Label para mostrar el estado del push
status_label = tk.Label(status_frame, text="", fg="black")
status_label.pack()

# Crea un botón que llame a la función ejecutar cuando se presione
submit_boton = tk.Button(root, text="Guardar", command=lambda: commit_push(src_entry.get(), repo_entry.get()))
submit_boton.pack(pady=0)

# Muestra la ventana
root.mainloop()    