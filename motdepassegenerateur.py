import random
import string
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip


def generate_password():
    length = length_var.get()
    use_special_chars = special_chars_var.get()
    use_numbers = numbers_var.get()

    characters = string.ascii_letters
    if use_special_chars:
        characters += string.punctuation
    if use_numbers:
        characters += string.digits

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(tk.END, password)


def save_password():
    password = password_entry.get()
    site = site_entry.get()
    login = login_entry.get()

    if password and site and login:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS passwords (site TEXT, login TEXT, password TEXT)")
        cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (site, login, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sauvegarde", "Mot de passe enregistré avec succès !")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")


def show_passwords():
    password_window = tk.Toplevel(window)
    password_window.title("Mots de passe enregistrés")
    password_window.geometry("600x300")
    password_window.configure(background="#D3D3D3")

    style = ttk.Style(password_window)
    style.theme_use("clam")
    style.configure("Treeview", background="#D3D3D3", foreground="black", fieldbackground="#D3D3D3")
    style.configure("Treeview.Heading", font=(None, 10, "bold"))

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT site, login, password FROM passwords")
    passwords = cursor.fetchall()
    conn.close()

    if passwords:
        tree = ttk.Treeview(password_window, columns=("Site", "Login", "Mot de passe"), show="headings",style="Treeview")
        tree.heading("Site", text="Site")
        tree.heading("Login", text="Login")
        tree.heading("Mot de passe", text="Mot de passe")

        for password in passwords:
            tree.insert("", tk.END, values=password)

        tree.pack(expand=True, fill=tk.BOTH)

        def delete_password():
            selected_item = tree.selection()
            if selected_item:
                result = messagebox.askquestion("Supprimer", "Êtes-vous sûr de vouloir supprimer ce mot de passe ?")
                if result == 'yes':
                    conn = sqlite3.connect("passwords.db")
                    cursor = conn.cursor()
                    for item in selected_item:
                        values = tree.item(item, "values")
                        site = values[0]
                        login = values[1]
                        password = values[2]
                        cursor.execute("DELETE FROM passwords WHERE site=? AND login=? AND password=?", (site, login, password))
                        tree.delete(item)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Suppression", "Mot de passe supprimé avec succès !")
            else:
                messagebox.showinfo("Aucune sélection", "Veuillez sélectionner une ligne à supprimer.")

        def copy_password():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item[0], "values")
                password = values[2]
                pyperclip.copy(password)
                messagebox.showinfo("Copie", "Mot de passe copié dans le presse-papiers !")
            else:
                messagebox.showinfo("Aucune sélection", "Veuillez sélectionner une ligne à copier.")

        delete_button = tk.Button(password_window, text="Supprimer", command=delete_password)
        delete_button.pack()

        copy_button = tk.Button(password_window, text="Copier le mot de passe", command=copy_password)
        copy_button.pack()

    else:
        messagebox.showinfo("Aucun mot de passe", "Aucun mot de passe enregistré.")


window = tk.Tk()
window.title("Générateur de mots de passe")
window.geometry("270x300")

length_label = tk.Label(window, text="Longueur du mot de passe :")
length_label.pack()

length_var = tk.IntVar()
length_entry = tk.Entry(window, textvariable=length_var)
length_entry.pack()

special_chars_var = tk.BooleanVar()
special_chars_checkbox = tk.Checkbutton(window, text="Caractères spéciaux", variable=special_chars_var)
special_chars_checkbox.pack()

numbers_var = tk.BooleanVar()
numbers_checkbox = tk.Checkbutton(window, text="Chiffres", variable=numbers_var)
numbers_checkbox.pack()

generate_button = tk.Button(window, text="Générer", command=generate_password)
generate_button.pack()

site_label = tk.Label(window, text="Site :")
site_label.pack()

site_entry = tk.Entry(window)
site_entry.pack()

login_label = tk.Label(window, text="Login :")
login_label.pack()

login_entry = tk.Entry(window)
login_entry.pack()

password_entry = tk.Label(window, text="Password :")
password_entry.pack()

password_entry = tk.Entry(window)
password_entry.pack()

save_button = tk.Button(window, text="Sauvegarder", command=save_password)
save_button.pack()

show_button = tk.Button(window, text="Afficher les mots de passe", command=show_passwords)
show_button.pack()

window.mainloop()
