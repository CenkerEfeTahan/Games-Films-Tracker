import json

sort_states = {}

def sort_games(tree, col):
    global sort_states

    for other_col in tree["columns"]:
        if other_col != col:
            tree.heading(other_col, text=other_col)

    if col not in sort_states:
        sort_states[col] = 0

    current_state = sort_states[col]

    if current_state == 0:
        data = [(tree.set(k, col), k) for k in tree.get_children()]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=True)
        except:
            data.sort(key=lambda t: t[0], reverse=True)
        arrow = "▼"

    elif current_state == 1:
        data = [(tree.set(k, col), k) for k in tree.get_children()]
        try:
            data.sort(key=lambda t: float(t[0]))
        except:
            data.sort(key=lambda t: t[0])
        arrow = "▲"

    elif current_state == 2:
        tree.delete(*tree.get_children())
        with open("Data/games.json", "r", encoding="utf-8") as file:
            rows = json.load(file)
            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row, tags=(tag,))
        tree.heading(col, text=col)
        sort_states[col] = 0
        return


    if current_state in (0, 1):
        for i, (_, k) in enumerate(data):
            tree.move(k, '', i)
        tree.heading(col, text=f"{col} {arrow}")
        sort_states[col] = (current_state + 1) % 3  # Döngü: 0 → 1 → 2 → 0


