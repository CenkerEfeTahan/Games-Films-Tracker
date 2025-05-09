import tkinter as tk
from tkinter import *
import json
import os
from tkinter import messagebox
from tkinter import ttk
from Games.GamesUtil import sort_games
from Films.FilmsUtil import sort_films
from tkinter import filedialog
import shutil
import re
import sys
import os
from tkinter import PhotoImage


def save_game_list(tree):
    data = [tree.item(item)["values"] for item in tree.get_children()]
    with open("Data/games.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def show_game_window():
    game_window = Toplevel()
    game_window.title("🎮 Games")
    game_window.geometry("1095x720")
    game_window.configure(bg="#b1cdd1")

    Label(game_window, text="🎮 Games", font=("Segoe UI", 19, "bold"), bg="#b1cdd1").pack(pady=10)

    top_frame = Frame(game_window, bg="#b1cdd1")
    top_frame.pack()

    search_entry = Entry(top_frame, font=("Segoe UI", 12), width=50)
    search_entry.grid(row=0, column=0, padx=5, pady=10)

    columns = ("Name", "Genre", "Year", "Your Score", "Metacritic", "Image")
    tree_frame = Frame(game_window)
    tree_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_games(tree, c))
        tree.column(col, anchor="center", width=210)

    tree.pack(fill=BOTH, expand=True)

    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=("Segoe UI", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#4b798b", foreground="black")

    def show_game_details(event):
        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected[0])['values']
        if len(values) < 6:
            return

        name, genre, year, your_score, meta_score, image_file = values

        detail_popup = Toplevel(game_window)
        detail_popup.title(name)
        detail_popup.configure(bg="#f0f0f0")
        detail_popup.geometry("700x750")
        detail_popup.resizable(False, False)

        Label(detail_popup, text=name, font=("Segoe UI", 18, "bold"), bg="#f0f0f0").pack(pady=(15, 10))

        try:
            image_path = os.path.join("Images", "Games", image_file)
            if os.path.exists(image_path):
                img = PhotoImage(file=image_path)
                img = img.subsample(2, 2)
                image_label = Label(detail_popup, image=img, bg="#f0f0f0")
                image_label.image = img
                image_label.pack(pady=10)
            else:
                Label(detail_popup, text="Image not found.", fg="red", bg="#f0f0f0").pack(pady=10)
        except Exception as e:
            Label(detail_popup, text=f"Error loading image: {e}", fg="red", bg="#f0f0f0").pack(pady=10)

        info_text = f"""  
    🎮 Genre: {genre}
    📅 Year: {year}
    🎯 Your Score: {your_score}
    ⭐Metacritic: {meta_score}""".strip()

        Label(detail_popup, text=info_text, justify="left", font=("Times New Roman", 15, "italic"), bg="#f0f0f0").pack(pady=10)

    tree.bind("<Double-1>", show_game_details)
    def refresh_tags():
        for i, item in enumerate(tree.get_children()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))
        tree.tag_configure('evenrow', background="#f7f7f7")
        tree.tag_configure('oddrow', background="#e6e6e6")

    def search():
        query = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        if os.path.exists("Data/games.json"):
            with open("Data/games.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for row in data:
                    if any(query in str(cell).lower() for cell in row):
                        tree.insert("", "end", values=row)
        refresh_tags()

    def open_game_popup(mode, selected=None):
        popup = Toplevel(game_window)
        popup.title("Add Game" if mode == "add" else "Edit Game")
        popup.geometry("450x500")
        popup.configure(bg="#e0f0f5")
        popup.grab_set()

        fields = ["Name", "Genre", "Year", "Your Score", "Metacritic"]
        entries = []
        selected_image = [None]

        Label(
            popup,
            text="Please fill in the details:" if mode == "add" else "Edit game details:",
            bg="#e0f0f5",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        for i, field in enumerate(fields):
            Label(popup, text=field + ":", bg="#e0f0f5", font=("Arial", 11)).pack(pady=(5, 2))
            ent = Entry(popup, font=("Arial", 12), width=30)
            ent.pack()
            entries.append(ent)

        # image_label'ı ÖNCE tanımla
        image_label = Label(popup, text="No image selected", bg="#e0f0f5", fg="gray", font=("Arial", 10))
        image_label.pack()

        # Eğer edit modundaysak, alanları doldur ve görseli ata
        if mode == "edit" and selected:
            existing_values = tree.item(selected)["values"]
            for i in range(len(fields)):
                entries[i].insert(0, existing_values[i])

            if len(existing_values) > 5:
                selected_image[0] = os.path.join("Images", "Games", existing_values[5])
                image_label.config(text=existing_values[5], fg="green")
        def choose_image():
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            if file_path and file_path.lower().endswith(".png"):
                selected_image[0] = file_path
                image_label.config(text=os.path.basename(file_path), fg="green")
            else:
                messagebox.showwarning("Format Error", "Please select a .png file only.", parent=popup)



        Button(popup, text="Select Image", command=choose_image, bg="#b0c4de").pack(pady=10)

        def save():
            values = [e.get().strip() for e in entries]
            if not selected_image[0]:
                messagebox.showwarning("Image Missing", "Please select a PNG image before saving.", parent=popup)
                return
            if all(values):
                try:
                    year = int(values[2])
                    if not (1970 <= year <= 2025):
                        raise ValueError("Invalid Year")

                    score = float(values[3])
                    meta = float(values[4])
                    if not (0.0 <= score <= 10.0 and 0.0 <= meta <= 10.0):
                        raise ValueError("Invalid Score")
                except ValueError:
                    messagebox.showwarning("Invalid", "Year must be 1970–2025 and scores must be between 0.0 and 10.0.",
                                           parent=popup)
                    return

                image_name = os.path.basename(selected_image[0])
                image_dest = os.path.join("Images", "Games", image_name)

                # Edit modundaysa ve görsel zaten proje içindeyse tekrar kopyalama
                if mode == "add" or not os.path.exists(image_dest):
                    os.makedirs("Images/Games", exist_ok=True)
                    shutil.copy(selected_image[0], image_dest)
                values.append(image_name)  # Görsel adını values'a ekle


                if mode == "add":
                    tree.insert("", "end", values=values)
                elif mode == "edit":
                    tree.item(selected, values=values)

                refresh_tags()
                save_game_list(tree)
                popup.destroy()
            else:
                messagebox.showwarning("Missing", "Please fill in all fields.", parent=popup)

        Button(popup, text="Save", command=save, width=12, bg="#f7be20").pack(pady=15)

    def add_game():
        open_game_popup("add")

    def edit_game():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a game to edit.", parent=game_window)
            return
        open_game_popup("edit", selected[0])

    def delete_game():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a game to delete.", parent=game_window)
            return

        game = tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{game}'?",
                                      parent=game_window)
        if confirm:
            tree.delete(selected[0])
            refresh_tags()
            save_game_list(tree)


    Button(top_frame, text="Search", command=search, width=12, height=1).grid(row=0, column=1, padx=2)
    Button(top_frame, text="Add", command=add_game, width=12, height=1).grid(row=0, column=2, padx=2)
    Button(top_frame, text="Edit", command=edit_game, width=12, height=1).grid(row=0, column=3, padx=2)
    Button(top_frame, text="Delete", command=delete_game, width=12, height=1).grid(row=0, column=4, padx=2)


    if os.path.exists("Data/games.json"):
        with open("Data/games.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for i, row in enumerate(data):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row, tags=(tag,))
    refresh_tags()

def sort_column(tree, col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children()]
    try:
        data.sort(key=lambda t: float(t[0]), reverse=reverse)
    except:
        data.sort(key=lambda t: t[0], reverse=reverse)
    for i, (val, k) in enumerate(data):
        tree.move(k, '', i)
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))





def save_film_list(tree):
    data = [tree.item(item)["values"] for item in tree.get_children()]
    with open("Data/films.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def show_film_window():
    film_window = Toplevel()
    film_window.title("🎬 Films")
    film_window.geometry("1095x720")
    film_window.configure(bg="#d9d5c4")

    Label(film_window, text="🎬 Films", font=("Segoe UI", 19, "bold"), bg="#d9d5c4").pack(pady=10)

    top_frame = Frame(film_window, bg="#d9d5c4")
    top_frame.pack()

    search_entry = Entry(top_frame, font=("Segoe UI", 12), width=50)
    search_entry.grid(row=0, column=0, padx=5, pady=10)

    columns = ("Name", "Genre", "Year", "Your Score", "IMDB", "Image")

    tree_frame = Frame(film_window)
    tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

    tree_scroll = Scrollbar(tree_frame, orient="vertical")
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_films(tree, c))
        tree.column(col, anchor="center", width=210)

    tree.pack(fill="both", expand=True)

    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=("Segoe UI", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#a99e8e", foreground="black")

    vsb = ttk.Scrollbar(film_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)

    def show_film_details(event):
        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected[0])['values']
        if len(values) < 6:
            return

        name, genre, year, score, imdb, image_file = values

        detail_popup = Toplevel(film_window)
        detail_popup.title(name)
        detail_popup.configure(bg="#f0f0f0")
        detail_popup.geometry("650x750")
        detail_popup.resizable(False, False)

        Label(detail_popup, text=name, font=("Segoe UI", 20, "bold"), bg="#f0f0f0").pack(pady=(15, 10))

        if image_file and image_file.lower() != "n/a":
            image_path = os.path.join("Images", "Films", image_file)
            if os.path.exists(image_path):
                try:
                    img = PhotoImage(file=image_path)
                    img = img.subsample(2, 2)
                    image_label = Label(detail_popup, image=img, bg="#f0f0f0")
                    image_label.image = img
                    image_label.pack(pady=10)
                except:
                    Label(detail_popup, text="Image error", fg="red", bg="#f0f0f0").pack(pady=10)
            else:
                Label(detail_popup, text="Image not found.", fg="gray", bg="#f0f0f0").pack(pady=10)
        else:
            Label(detail_popup, text="No image for this film.", fg="gray", bg="#f0f0f0").pack(pady=10)

        info_text = f"""
    🎬 Genre: {genre}
    📅 Year: {year}
    ⭐ Your Score: {score}
    🎞 IMDB: {imdb}
            """.strip()

        Label(detail_popup, text=info_text, justify="left", font=("Segoe UI", 16, "italic"), bg="#f0f0f0").pack(pady=10)
    tree.bind("<Double-1>", show_film_details)

    def refresh_tags():
        for i, item in enumerate(tree.get_children()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))
        tree.tag_configure('evenrow', background="#f7f7f7")
        tree.tag_configure('oddrow', background="#e6e6e6")

    def search():
        query = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        if os.path.exists("Data/films.json"):
            with open("Data/films.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for row in data:
                    if any(query in str(cell).lower() for cell in row):
                        tree.insert("", "end", values=row)
        refresh_tags()

    def open_film_popup(mode, selected=None):
        popup = Toplevel(film_window)
        popup.title("Add Film" if mode == "add" else "Edit Film")
        popup.geometry("450x500")
        popup.configure(bg="#e8e4d9")
        popup.grab_set()

        fields = ["Name", "Genre", "Year", "Your Score", "IMDB"]
        entries = []
        selected_image = [None]

        Label(popup, text="Please fill in the details:" if mode == "add" else "Edit film details:",
              bg="#e8e4d9", font=("Arial", 12, "bold")).pack(pady=10)

        for i, field in enumerate(fields):
            Label(popup, text=field + ":", bg="#e8e4d9", font=("Arial", 11)).pack(pady=(5, 2))
            ent = Entry(popup, font=("Arial", 12), width=30)
            ent.pack()
            entries.append(ent)

        image_label = Label(popup, text="No image selected", bg="#e8e4d9", fg="gray", font=("Arial", 10))
        image_label.pack()

        def choose_image():
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            if file_path and file_path.lower().endswith(".png"):
                selected_image[0] = file_path
                image_label.config(text=os.path.basename(file_path), fg="green")
            else:
                messagebox.showwarning("Format Error", "Please select a .png file only.", parent=popup)

        Button(popup, text="Select Image", command=choose_image, bg="#cfc8b8").pack(pady=10)

        # Edit modundaysa mevcut değerleri doldur
        if mode == "edit" and selected:
            existing_values = tree.item(selected)["values"]
            for i in range(len(fields)):
                entries[i].insert(0, existing_values[i])
            if len(existing_values) > 5 and existing_values[5] != "N/A":
                selected_image[0] = os.path.join("Images", "Films", existing_values[5])
                image_label.config(text=existing_values[5], fg="green")

        def save():
            values = [e.get().strip() for e in entries]
            if all(values):
                try:
                    year = int(values[2])
                    if not (1900 <= year <= 2025):
                        raise ValueError("Invalid Year")
                    score = float(values[3])
                    imdb = float(values[4])
                    if not (0.0 <= score <= 10.0 and 0.0 <= imdb <= 10.0):
                        raise ValueError("Invalid Score")
                except ValueError:
                    messagebox.showwarning("Invalid", "Year must be 1900–2025 and scores between 0.0 and 10.0.",
                                           parent=popup)
                    return

                if selected_image[0]:
                    image_name = os.path.basename(selected_image[0])
                    dest_path = os.path.join("Images", "Films", image_name)
                    if mode == "add" or not os.path.exists(dest_path):
                        os.makedirs("Images/Films", exist_ok=True)
                        shutil.copy(selected_image[0], dest_path)
                else:
                    image_name = "N/A"

                values.append(image_name)

                if mode == "add":
                    tree.insert("", "end", values=values)
                elif mode == "edit":
                    tree.item(selected, values=values)

                refresh_tags()
                save_film_list(tree)
                popup.destroy()
            else:
                messagebox.showwarning("Missing", "Please fill in all fields.", parent=popup)

        Button(popup, text="Save", command=save, width=12, bg="#ffc94a").pack(pady=15)

    def add_film():
        open_film_popup("add")

    def edit_film():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a film to edit.", parent=film_window)
            return
        open_film_popup("edit", selected[0])

    def delete_film():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a film to delete.", parent=film_window)
            return
        film = tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{film}'?", parent=film_window)
        if confirm:
            tree.delete(selected[0])
            refresh_tags()
            save_film_list(tree)

    Button(top_frame, text="Search", command=search, width=12, height=1).grid(row=0, column=1, padx=2)
    Button(top_frame, text="Add", command=add_film, width=12, height=1).grid(row=0, column=2, padx=2)
    Button(top_frame, text="Edit", command=edit_film, width=12, height=1).grid(row=0, column=3, padx=2)
    Button(top_frame, text="Delete", command=delete_film, width=12, height=1).grid(row=0, column=4, padx=2)

    if os.path.exists("Data/films.json"):
        with open("Data/films.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for i, row in enumerate(data):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row, tags=(tag,))
    refresh_tags()






def save_to_play_list(tree):
    games = [tree.item(item)["values"][0] for item in tree.get_children()]
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    save_dir = os.path.join(base_dir, "Data")
    os.makedirs(save_dir, exist_ok=True)  # <-- EKLENDİ
    save_path = os.path.join(save_dir, "ToPlay.json")
    try:
        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(games, file, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save ToPlay.json:\n{e}")



def show_to_play_window():
    play_window = Toplevel()
    play_window.title("🎮 To-Play")
    play_window.geometry("520x480")
    play_window.configure(bg="#b1cdd1")

    title_label = Label(play_window, text="🎮 To-Play", font=("Segoe UI", 16, "bold"), bg="#b1cdd1")
    title_label.pack(pady=(10, 5))

    top_frame = Frame(play_window, bg="#b1cdd1")
    top_frame.pack(pady=(0, 10))

    entry = Entry(top_frame, font=("Segoe UI", 11), width=25)
    entry.grid(row=0, column=0, padx=(10, 10), pady=5)

    columns = ("#1",)
    tree_frame = Frame(play_window)
    tree_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    tree.heading("#1", text="Game Name")
    tree.column("#1", anchor="center", width=480)
    tree.pack(fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    rowheight=32,
                    font=("Segoe UI", 11),
                    background="#f0f8ff",
                    fieldbackground="#f0f8ff")

    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                    background="#4b798b",
                    foreground="black")

    tree.tag_configure('evenrow', background="#f7f7f7")
    tree.tag_configure('oddrow', background="#e6e6e6")

    def refresh_tags():
        for index, item in enumerate(tree.get_children()):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))

    def add_game():
        popup = Toplevel(play_window)
        popup.title("Add Game")
        popup.geometry("350x150")
        popup.configure(bg="#e0f0f5")
        popup.grab_set()

        Label(popup, text="Enter game name:", bg="#e0f0f5", font=("Arial", 11)).pack(pady=(15, 5))
        name_entry = Entry(popup, font=("Arial", 12), width=30)
        name_entry.pack(pady=5)

        def save_game():
            game = name_entry.get().strip()
            if game:
                index = len(tree.get_children())
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(game,), tags=(tag,))
                refresh_tags()
                save_to_play_list(tree)
                popup.destroy()
            else:
                messagebox.showwarning("Empty", "Name cannot be empty.", parent=popup)

        Button(popup, text="Save", command=save_game, width=10).pack(pady=(10, 5))


    def edit_game():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a game to edit.", parent=play_window)
            return

        old_value = tree.item(selected[0])['values'][0]

        edit_popup = Toplevel(play_window)
        edit_popup.title("Edit Game")
        edit_popup.geometry("350x150")
        edit_popup.configure(bg="#e0f0f5")
        edit_popup.grab_set()

        Label(edit_popup, text="Please edit the name:", bg="#e0f0f5", font=("Arial", 11)).pack(pady=(15, 5))
        edit_entry = Entry(edit_popup, font=("Arial", 12), width=30)
        edit_entry.insert(0, old_value)
        edit_entry.pack(pady=5)

        def save_edit():
            new_value = edit_entry.get().strip()
            if new_value:
                tree.item(selected[0], values=(new_value,))
                refresh_tags()
                save_to_play_list(tree)
                edit_popup.destroy()
            else:
                messagebox.showwarning("Empty", "Name cannot be empty.", parent=edit_popup)

        Button(edit_popup, text="Save", width=10, command=save_edit).pack(pady=(10, 5))
        Button(edit_popup, text="Cancel", width=10, command=edit_popup.destroy).pack()

    def delete_game():
        selected = tree.selection()
        if selected:
            game = tree.item(selected[0])['values'][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{game}'?", parent=play_window)
            if confirm:
                tree.delete(selected[0])
                refresh_tags()
                save_to_play_list(tree)

    Button(top_frame, text="Add", command=lambda: add_game(), width=8).grid(row=0, column=1, padx=2)

    Button(top_frame, text="Edit", command=edit_game, width=8).grid(row=0, column=2, padx=2)
    Button(top_frame, text="Delete", command=delete_game, width=8).grid(row=0, column=3, padx=2)

    # JSON'dan veri yüklemek
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    load_path = os.path.join(base_dir, "Data", "ToPlay.json")
    if os.path.exists(load_path):
        with open(load_path, "r", encoding="utf-8") as file:

            games = json.load(file)
            for i, game in enumerate(games):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(game,), tags=(tag,))

    return play_window



def save_to_watch_list(tree):
    films = [tree.item(item)["values"][0] for item in tree.get_children()]
    with open("Data/ToWatch.json", "w", encoding="utf-8") as file:
        json.dump(films, file, ensure_ascii=False, indent=4)

def show_to_watch_window():
    watch_window = Toplevel()
    watch_window.title("🎬 To-Watch")
    watch_window.geometry("520x480")
    watch_window.configure(bg="#b1cdd1")

    title_label = Label(watch_window, text="🎬 To-Watch", font=("Segoe UI", 16, "bold"), bg="#b1cdd1")
    title_label.pack(pady=(10, 5))

    top_frame = Frame(watch_window, bg="#b1cdd1")
    top_frame.pack(pady=(0, 10))

    entry = Entry(top_frame, font=("Segoe UI", 11), width=25)
    entry.grid(row=0, column=0, padx=(10, 10), pady=5)

    columns = ("#1",)
    tree_frame = Frame(watch_window)
    tree_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    tree.heading("#1", text="Film Name")
    tree.column("#1", anchor="center", width=480)
    tree.pack(fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#4b798b", foreground="black")

    tree.tag_configure('evenrow', background="#f7f7f7")
    tree.tag_configure('oddrow', background="#e6e6e6")

    def add_film():
        popup = Toplevel(watch_window)
        popup.title("Add Film")
        popup.geometry("350x150")
        popup.configure(bg="#e0f0f5")
        popup.grab_set()

        Label(popup, text="Enter film name:", bg="#e0f0f5", font=("Arial", 11)).pack(pady=(15, 5))
        name_entry = Entry(popup, font=("Arial", 12), width=30)
        name_entry.pack(pady=5)

        def save_film():
            film = name_entry.get().strip()
            if film:
                index = len(tree.get_children())
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(film,), tags=(tag,))
                save_to_watch_list(tree)
                popup.destroy()
            else:
                messagebox.showwarning("Empty", "Name cannot be empty.", parent=popup)

        Button(popup, text="Save", command=save_film, width=10).pack(pady=(10, 5))

    def edit_film():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a film to edit.", parent=watch_window)
            return

        old_value = tree.item(selected[0])['values'][0]

        edit_popup = Toplevel(watch_window)
        edit_popup.title("Edit Film")
        edit_popup.geometry("350x150")
        edit_popup.configure(bg="#e0f0f5")
        edit_popup.grab_set()

        Label(edit_popup, text="Please edit the name:", bg="#e0f0f5", font=("Arial", 11)).pack(pady=(15, 5))
        edit_entry = Entry(edit_popup, font=("Arial", 12), width=30)
        edit_entry.insert(0, old_value)
        edit_entry.pack(pady=5)

        def save_edit():
            new_value = edit_entry.get().strip()
            if new_value:
                tree.item(selected[0], values=(new_value,))
                save_to_watch_list(tree)
                edit_popup.destroy()
            else:
                messagebox.showwarning("Empty", "Name cannot be empty.", parent=edit_popup)

        Button(edit_popup, text="Save", width=10, command=save_edit).pack(pady=(10, 5))
        Button(edit_popup, text="Cancel", width=10, command=edit_popup.destroy).pack()

    def delete_film():
        selected = tree.selection()
        if selected:
            film = tree.item(selected[0])['values'][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{film}'?", parent=watch_window)
            if confirm:
                tree.delete(selected[0])
                save_to_watch_list(tree)






    Button(top_frame, text="Add", command=add_film, width=8).grid(row=0, column=1, padx=2)
    Button(top_frame, text="Edit", command=edit_film, width=8).grid(row=0, column=2, padx=2)
    Button(top_frame, text="Delete", command=delete_film, width=8).grid(row=0, column=3, padx=2)

    # JSON’dan yüklemek
    if os.path.exists("Data/ToWatch.json"):
        with open("Data/ToWatch.json", "r", encoding="utf-8") as file:
            films = json.load(file)
            for i, film in enumerate(films):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(film,), tags=(tag,))

    return watch_window








def show_help(lang):
    if lang == "eng":
        help_text = """
Welcome to the Games & Films Tracker!
Here’s what you can do in this app:

🎮 GAMES SECTION
Firstly click the "joystick" image.
You can add games with name, genre, release year, your score, Metacritic score and an image from there.
You can edit or delete them anytime.
Click the column titles (Year, Score, etc.) to sort: descending, ascending, or original order.
Use the search bar to find games by name, genre, or score.
Double click to see the game's photo and information.
If you have a plan to play a game later, add it to the "To-Play" section.


🎬 FILMS SECTION
This time please click the "Films" image.
Same as games, but with IMDb score instead of Metacritic.
If you plan to watch a movie later, add it to the "To-Watch" list so you don't forget.
        """
    else:
        help_text = """
Games & Films Tracker'a Hoş Geldiniz!
Uygulamada neler yapabileceğinizi kısaca anlatalım:

🎮 OYUNLAR BÖLÜMÜ
Öncelikle oyun kolu simgesine tıklayınız.
Buradan oyunun ismini, türünü, çıkış yılını, kendi puanınınızı, Metacritic puanını ile ekleyebilirsiniz.
Dilediğinizde düzenleyebilir veya silebilirsiniz.
Yıl, Puan vb. sütun başlıklarına tıklayarak sırayla azalan, artan ya da orijinal sıraya geçebilirsiniz.
Arama çubuğuyla oyunları isme, türe veya puana göre bulabilirsiniz.
Oyunun üstüne çift tıklayarak oyunun fotoğrafını ve bilgilerini görebilirsiniz.
Gelecekte oynamak istediğiniz oyunlar için ise "To-Play" kısmını kullanabilirsiniz.


🎬 FİLMLER BÖLÜMÜ
Film görseline tıklayınız.
Oyunlarla tamamen aynı şekilde çalışır, sadece farklı olarak IMDb puanı kullanılır.
Ayrıca gelecekte izlemeyi düşündüğünüz filmleri "To-Watch" listesine ekleyerek unutmamış olursunuz.
            """

    help_popup = Toplevel(window)
    help_popup.title("Help")
    help_popup.geometry("680x510")
    help_popup.configure(bg="#65a6c2")
    Label(help_popup, text=help_text, bg="#65a6c2", justify="left", font=("Times New Roman", 12), anchor="w").pack(padx=20, pady=20)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



window=Tk()
window.title("Games/Films Tracker")
window.geometry("1095x720")
image_path = resource_path("games-films.png")
icon = PhotoImage(file=image_path)
window.iconphoto(True, icon)
window.configure(background="#b5a9a8")
image_path = resource_path("games-films.png")
game_icon = PhotoImage(file=resource_path("ps4.png"))
game_icon = game_icon.subsample(6, 6)  # Oran arttırmak
image_path = resource_path("games-films.png")
film_icon = PhotoImage(file=resource_path("filmphoto.png"))
film_icon = film_icon.subsample(6, 6)

help_button = Button(window, text="Help", bg="#756f6e", fg="white", font=("Arial", 10, "bold"), width=7, height=2)
help_button.place(x=10, y=10)

#Help Dropdown
help_menu = Menu(window, tearoff=0, bg='gray', fg="white", font=("Arial", 10))
help_menu.add_command(label="English", command=lambda: show_help("eng"))
help_menu.add_command(label="Türkçe", command=lambda: show_help("tr"))

def open_help_menu(event):
    help_menu.post(event.x_root, event.y_root)

help_button.bind("<Button-1>", open_help_menu)


def show_about():
    about_window = Toplevel(window)
    about_window.title("About")
    about_window.configure(bg="#514da1")
    about_window.geometry("400x150")
    about_window.resizable(False, False)

    label = Label(
        about_window,
        text="This application is designed for your personal game and movie collection.\n\nBu uygulama kişisel oyun ve film koleksiyonunuz için tasarlanmıştır. \n"
             "\n"
             "CONTACT: cenkerefetahan@gmail.com",
        font=("Arial", 11),
        bg="#514da1",
        fg="white",
        justify="center",
        wraplength=360,
        padx=20,
        pady=20
    )
    label.pack()


about_button = Button(window, text="About", bg="#756f6e", fg="white", font=("Arial", 10, "bold"), width=7, height=2, command=show_about)
about_button.config(activebackground="#8B8000", activeforeground="black")
about_button.place(x=980, y=10)
about_button.place(relx=1.0, x=-10, y=10, anchor="ne")


label = tk.Label(window, text="Welcome to the Games/Films Tracker!",
                 font=("Arial", 25),
                 bg="#b5a9a8",
                 relief= RAISED,
                 bd=8,
                 padx=5,
                 pady=3)
label.pack(pady=15)

photo = PhotoImage(file=resource_path('games-films-tracker.png'))
photo = photo.subsample(2, 2)

image_label = tk.Label(window, image=photo, bg="#b5a9a8")
image_label.image = photo
image_label.pack(pady=(1, 0), padx=1)

button_frame = Frame(window, bg="#b5a9a8")
button_frame.pack()


#Games and Films
btn_games = Button(button_frame, image=game_icon,
                   width=250, height=150,
                   bg="white", bd=2, relief=RAISED)
btn_games.image = game_icon  # referans
btn_games.grid(row=0, column=0, padx=30, pady=10)
btn_games.config(command=show_game_window)


btn_films = Button(button_frame, image=film_icon,
                   width=250, height=150,
                   bg="white", bd=2, relief=RAISED)
btn_films.image = film_icon
btn_films.grid(row=0, column=1, padx=30, pady=10)
btn_films.config(command=show_film_window)


#To-Play and To-Watch
btn_to_play = Button(button_frame, text="To-Play", width=20, height=2, font=("Arial", 12), bg="#756f6e", fg="white")
btn_to_play.grid(row=1, column=0, padx=30, pady=10)
btn_to_play.config(activebackground="gray", activeforeground="white")
btn_to_play.config(command=show_to_play_window)

btn_to_watch = Button(button_frame, text="To-Watch", width=20, height=2, font=("Arial", 12), bg="#756f6e", fg="white")
btn_to_watch.grid(row=1, column=1, padx=30, pady=10)
btn_to_watch.config(activebackground="gray", activeforeground="white")
btn_to_watch.config(command=show_to_watch_window)





window.mainloop()