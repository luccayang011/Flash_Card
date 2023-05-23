from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT = 'Ariel'

try:
    french_english_words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    french_english_words = pd.read_csv("data/french_words.csv")
    to_learn = french_english_words.to_dict(orient="records")  # remove the index
else:
    to_learn = french_english_words.to_dict(orient="records")  # remove the index

current_card = {}

# -------------------------- FUNCTIONS -------------------------- #
def generate_word():
    global current_card, flip_timer  # so the other function could use this same variable also
    window.after_cancel(flip_timer) # to make sure while we are choosing the words, the timer will be invalid
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text='French', fill='black')
    canvas.itemconfig(word_text, text=current_card["French"], fill='black')
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title_text, text='English', fill='white')
    canvas.itemconfig(word_text, text=current_card["English"], fill='white')

def remove_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_word()

# -------------------------- UI SETUP -------------------------- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(
    file='images/card_back.png')  # has to be created outside the function, otherwise it would be gone
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title_text = canvas.create_text(400, 150, text='title', font=(FONT, 40, 'italic'))
word_text = canvas.create_text(400, 263, text='word', font=(FONT, 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, bg=BACKGROUND_COLOR, command=remove_known)
right_button.grid(column=1, row=1)

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, bg=BACKGROUND_COLOR, command=generate_word)
wrong_button.grid(column=0, row=1)

generate_word()

window.mainloop()
