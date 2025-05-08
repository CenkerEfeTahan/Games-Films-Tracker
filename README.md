# 🎮 Games & Films Tracker

This is a personal desktop application to track the games you’ve played and the films you’ve watched — or plan to!

## ✨ Features

- 🎮 **Games Panel**  
  - Add games with name, genre, release year, your score, Metacritic score, and image.
  - Sort by year or score (descending, ascending, original order).
  - Search by name, genre, or score.
  - Double click to view game info and cover.

- 🎬 **Films Panel**  
  - Works like games, with IMDb instead of Metacritic.
  - Optional image upload.
  - View all info on double click.

- 📝 **To-Play & To-Watch Lists**  
  - Add names of games/films you plan to finish.
  - Edit/delete anytime.

- 🌍 **Language Support**  
  - Help menu in both English and Turkish.

- 💾 **Persistent Storage**  
  - Data saved in JSON files: `games.json`, `films.json`, `ToPlay.json`, `ToWatch.json`.
  - If any image doesn’t appear, check that it is .png and stored under Images/Games or Images/Films.

## 📁 Project Structure
Games-Films-Tracker/
│
├── main.py # Main GUI application
├── Data/ # Stores JSON data files
│ ├── games.json
│ ├── films.json
│ ├── ToPlay.json
│ └── ToWatch.json
├── Images/
│ ├── Games/ # Game cover images (.png)
│ └── Films/ # Film poster images (.png)
├── Games/GamesUtil.py # Sorting logic for games
├── Films/FilmsUtil.py # Sorting logic for films
├── README.md # You’re reading it


## 🖥 How to Run
Make sure Python is installed.

```bash
python main.py







