from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
chosen_card = {}
flash_card_list = {}

try:
    updated_data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    flash_card_list = original_data.to_dict(orient="records")
else:
    flash_card_list = updated_data.to_dict(orient="records")



def create_new_flash_card():
    global chosen_card, flip_timer
    window.after_cancel(flip_timer)
    chosen_card = choice(flash_card_list)
    canvas.itemconfig(canvas_text, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=chosen_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(canvas_text, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=chosen_card["English"], fill="white")


def check_progress():
    flash_card_list.remove(chosen_card)
    df_new = pd.DataFrame(flash_card_list)
    df_new.to_csv("data/words_to_learn.csv",index=False)
    print(len(flash_card_list))
    create_new_flash_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

create_new_flash_card()

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=check_progress)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=create_new_flash_card)
wrong_button.grid(row=1, column=0)

create_new_flash_card()

window.mainloop()
