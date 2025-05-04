import tkinter as tk
from tkinter import *

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
help_button.config(activebackground="#8B8000", activeforeground="black")
help_button.place(x=10, y=10)

about_button = Button(window, text="About", bg="#756f6e", fg="white", font=("Arial", 10, "bold"), width=7, height=2)
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