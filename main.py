import tkinter as tk
from tkinter import *
import json
import os
from tkinter import messagebox
from tkinter import ttk

def save_to_play_list(tree):
    games = [tree.item(item)["values"][0] for item in tree.get_children()]
    with open("Data/ToPlay.json", "w", encoding="utf-8") as file:
        json.dump(games, file, ensure_ascii=False, indent=4)

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
    tree = ttk.Treeview(play_window, columns=columns, show="headings", height=15)
    tree.heading("#1", text="Game Name")
    tree.column("#1", anchor="center", width=480)
    tree.pack(padx=10, pady=(0, 10))


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

    # Ek olarak satır düzenini koru
    tree.tag_configure('evenrow', background="#f7f7f7")
    tree.tag_configure('oddrow', background="#e6e6e6")

    def refresh_tags():
        for index, item in enumerate(tree.get_children()):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))

    def add_game():
        game = entry.get().strip()
        if game:
            index = len(tree.get_children())
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=(game,), tags=(tag,))

            entry.delete(0, END)
            refresh_tags()
            save_to_play_list(tree)


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

    Button(top_frame, text="Add", command=add_game, width=8).grid(row=0, column=1, padx=2)
    Button(top_frame, text="Edit", command=edit_game, width=8).grid(row=0, column=2, padx=2)
    Button(top_frame, text="Delete", command=delete_game, width=8).grid(row=0, column=3, padx=2)

    # JSON'dan veri yükle
    if os.path.exists("Data/ToPlay.json"):
        with open("Data/ToPlay.json", "r", encoding="utf-8") as file:
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
    tree = ttk.Treeview(watch_window, columns=columns, show="headings", height=15)
    tree.heading("#1", text="Film Name")
    tree.column("#1", anchor="center", width=480)
    tree.pack(padx=10, pady=(0, 10))

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#4b798b", foreground="black")

    tree.tag_configure('evenrow', background="#f7f7f7")
    tree.tag_configure('oddrow', background="#e6e6e6")

    def add_film():
        film = entry.get().strip()
        if film:
            index = len(tree.get_children())
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=(film,), tags=(tag,))
            entry.delete(0, END)
            save_to_watch_list(tree)

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

    # JSON’dan yükle
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
Welcome to the Games and Films Tracker!
This guide will help you use each section of the application effectively:

🎮 Games Section:
- Click the joystick image button to access your played games.
- In the games table, you can view:
  • Game name
  • Release year
  • Developer
  • Platforms
  • Your score
  • Metacritic score
- You can add, edit, or delete games.
- If you plan to play a game in the future, click the "To-Play" button and add it to your planned list.

🎬 Films Section:
- Click the Films button to manage your watched films.
- In the films table, you can view:
  • Film name
  • Genre
  • Release year
  • Lead actor
  • Your score
  • IMDb score
- You can add, edit, or delete films.
- If you plan to watch a movie later, add it to the "To-Watch" list so you don't forget.
        """
    else:
        help_text = """
    Games and Films Tracker'a Hoş Geldiniz!
    Bu rehber, uygulamanın bölümlerini nasıl kullanacağınızı açıklar:

    🎮 Oyunlar Bölümü:
    - Bitirmiş olduğunuz oyunlara ulaşmak için oyun kolu simgesine tıklayın.
    - Oyunlar tablosunda şunları görüntüleyebilirsiniz:
      • Oyun adı
      • Çıkış yılı
      • Geliştirici
      • Platformlar
      • Kendi puanınız
      • Metacritic puanı
    - Oyunları ekleyebilir, düzenleyebilir veya silebilirsiniz.
    - Gelecekte oynamayı düşündüğünüz oyunlar için "To-Play" butonuna tıklayarak liste oluşturabilirsiniz.

    🎬 Filmler Bölümü:
    - İzlediğiniz filmleri yönetmek için Films butonuna tıklayın.
    - Filmler tablosunda şunları görüntüleyebilirsiniz:
      • Film adı
      • Türü
      • Çıkış yılı
      • Başrol oyuncusu
      • Kendi puanınız
      • IMDb puanı
    - Filmleri ekleyebilir, düzenleyebilir veya silebilirsiniz.
    - Gelecekte izlemeyi düşündüğünüz filmleri "To-Watch" listesine ekleyerek unutmamış olursunuz.
            """

    help_popup = Toplevel(window)
    help_popup.title("Help")
    help_popup.geometry("675x610")
    help_popup.configure(bg="#65a6c2")
    Label(help_popup, text=help_text, bg="#65a6c2", justify="left", font=("Times New Roman", 12), anchor="w").pack(padx=20, pady=20)


window=Tk()
window.title("Games/Films Tracker")
window.geometry("1095x720")
icon= PhotoImage(file='games-films.png')
window.iconphoto(True, icon)
window.configure(background="#b5a9a8")
game_icon = PhotoImage(file="ps4.png")
game_icon = game_icon.subsample(6, 6)  # Gerekirse oranı artır, 8x8 gibi
film_icon = PhotoImage(file="filmphoto.png")
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
    about_window.configure(bg="#8B8680")
    about_window.geometry("400x150")
    about_window.resizable(False, False)

    label = Label(
        about_window,
        text="This application is designed for your personal game and movie collection.\n\nBu uygulama kişisel oyun ve film koleksiyonunuz için tasarlanmıştır.",
        font=("Arial", 11),
        bg="#8B8680",
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

photo = PhotoImage(file='games-films-tracker.png')
photo = photo.subsample(2, 2)  # Görseli 2 kat küçült

image_label = tk.Label(window, image=photo, bg="#b5a9a8")
image_label.image = photo
image_label.pack(pady=(1, 0), padx=1)

button_frame = Frame(window, bg="#b5a9a8")
button_frame.pack()


# Satır 1: Games ve Films
btn_games = Button(button_frame, image=game_icon,
                   width=250, height=150,
                   bg="white", bd=2, relief=RAISED)
btn_games.image = game_icon  # referansı tutmayı unutma!
btn_games.grid(row=0, column=0, padx=30, pady=10)

btn_films = Button(button_frame, image=film_icon,
                   width=250, height=150,
                   bg="white", bd=2, relief=RAISED)
btn_films.image = film_icon
btn_films.grid(row=0, column=1, padx=30, pady=10)


# Satır 2: To-Play ve To-Watch
btn_to_play = Button(button_frame, text="To-Play", width=20, height=2, font=("Arial", 12), bg="#756f6e", fg="white")
btn_to_play.grid(row=1, column=0, padx=30, pady=10)
btn_to_play.config(activebackground="gray", activeforeground="white")
btn_to_play.config(command=show_to_play_window)

btn_to_watch = Button(button_frame, text="To-Watch", width=20, height=2, font=("Arial", 12), bg="#756f6e", fg="white")
btn_to_watch.grid(row=1, column=1, padx=30, pady=10)
btn_to_watch.config(activebackground="gray", activeforeground="white")
btn_to_watch.config(command=show_to_watch_window)





window.mainloop()