from tkinter import *
from random import choice
import pandas as pd

# -------------------- CONSTANTS ------------------ #

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"

# ----------------------- DATA ------------------------#
try:
    words = pd.read_csv('data/words_to_learn.csv')
    words_to_learn = words.to_dict(orient="records")
except FileNotFoundError:
    words = pd.read_csv('data/french_english_words.csv')
    words_to_learn = words.to_dict(orient="records")
else:
    new_word = {}

# --------------- Pick a Random Word --------------- #

def delete_card():
    global words_to_learn, new_word
    print(len(words_to_learn))
    words_to_learn.remove(new_word)
    df = pd.DataFrame(words_to_learn)
    df.to_csv('data/words_to_learn.csv', index=False)
    next_card()


def flip_card():
    global new_word, timer_to_flip
    en_random_word = new_word['English']
    canvas_front.itemconfig(canvas_image, image=back)
    canvas_front.itemconfig(text_title, text='English', fill='white')
    canvas_front.itemconfig(text_word, text=f'{en_random_word}', fill='white')


def next_card():
    global text_title, text_word, new_word, timer_to_flip
    window.after_cancel(timer_to_flip)
    new_word = choice(words_to_learn)
    fr_random_word = new_word['French']
    canvas_front.itemconfig(canvas_image, image=front)
    canvas_front.itemconfig(text_title, text='French', fill='black')
    canvas_front.itemconfig(text_word, text=f'{fr_random_word}', fill='black')
    timer_to_flip = window.after(3000, func=flip_card)

# ----------------------- UI ----------------------- #


window = Tk()
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
window.title("Flash Card")
timer_to_flip = window.after(3000, func=flip_card)

# Images
front = PhotoImage(file="images/card_front.png")
back = PhotoImage(file="images/card_back.png")
known = PhotoImage(file="images/right.png")
unknown = PhotoImage(file="images/wrong.png")

# Canvas
canvas_front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas_front.create_image(400, 263, image=front)
text_title = canvas_front.create_text(400, 150, text="Title", font=(FONT, 40, 'italic'))
text_word = canvas_front.create_text(400, 263, text="Word", font=(FONT, 60, 'bold'))
canvas_front.grid(row=0, column=0, columnspan=2)

# Buttons
button_known = Button(image=known,
                      border=0,
                      borderwidth=0,
                      highlightthickness=0,
                      bg=BACKGROUND_COLOR,
                      command=delete_card)
button_known.config(activebackground=BACKGROUND_COLOR)
button_known.grid(column=1, row=1)
button_unknown = Button(image=unknown,
                        border=0,
                        borderwidth=0,
                        highlightthickness=0,
                        bg=BACKGROUND_COLOR,
                        command=next_card)
button_unknown.config(activebackground=BACKGROUND_COLOR)
button_unknown.grid(column=0, row=1)



next_card()


window.mainloop()
