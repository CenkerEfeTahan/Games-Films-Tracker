import tkinter as tk
from tkinter import *

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

btn_to_watch = Button(button_frame, text="To-Watch", width=20, height=2, font=("Arial", 12), bg="#756f6e", fg="white")
btn_to_watch.grid(row=1, column=1, padx=30, pady=10)
btn_to_watch.config(activebackground="gray", activeforeground="white")





window.mainloop()