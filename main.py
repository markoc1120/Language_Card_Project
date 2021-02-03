from tkinter import *
import pandas
import random
import json

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 32, "italic")
WORD_FONT = ("Ariel", 48, "bold")
LANGUAGE = ["Deutsch", "English"]
current_card = []
is_front = True

# -------------------READING------------------- #

try:
    try:
        data_csv = pandas.read_csv("data/to_learn.csv")
    except pandas.errors.EmptyDataError:
        pass

except FileNotFoundError:
    data_csv = pandas.read_csv("data/Data.csv")
    pandas.DataFrame(data_csv).to_json("data/data_json.json", orient="records")
    data_json = json.load(open("data/data_json.json"))
    to_learn = [item for item in data_json]
    is_over = False
else:
    try:
        pandas.DataFrame(data_csv).to_json("data/data_json.json", orient="records")
        data_json = json.load(open("data/data_json.json"))
        to_learn = [item for item in data_json]
        is_over = False
    except NameError:
        is_over = True
        to_learn = []

# -------------------LOGIC------------------- #


def right():
    if is_over:
        pass
    else:
        try:
            to_learn.remove(current_card)
        except ValueError:
            pass
        finally:
            pandas.DataFrame(to_learn).to_csv("data/to_learn.csv", index=False)
        new_card()


def changing():
    global is_front
    if is_front:
        canvas.itemconfig(card, image=image_front)
        canvas.itemconfig(word, text=current_card[LANGUAGE[0]])
        canvas.itemconfig(language, text=LANGUAGE[0])
        is_front = False
    else:
        canvas.itemconfig(card, image=image_back)
        canvas.itemconfig(language, text=LANGUAGE[1])
        canvas.itemconfig(word, text=current_card[LANGUAGE[1]])
        is_front = True


def new_card():
    global current_card, flip_timer, is_over

    if len(to_learn) == 0:
        is_over = True

    if is_over:
        window.after_cancel(flip_timer)
        canvas.itemconfig(card, image=image_finished)
        right.config(width=0, image="")
        wrong.config(width=0, image="")
        canvas.itemconfig(language, text="")
        canvas.itemconfig(word, text="")
    else:
        if is_front:
            window.after_cancel(flip_timer)
            current_card = random.choice(to_learn)
            changing()
            flip_timer = window.after(3000, changing)


# --------------------UI--------------------- #
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")
flip_timer = window.after(3000, changing)

image_back = PhotoImage(file="images/card_back.png")
image_front = PhotoImage(file="images/card_front.png")
image_finished = PhotoImage(file="images/finished.png")
canvas = Canvas(width=650, height=428, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(325, 214, image=image_front)
language = canvas.create_text(325, 122, font=LANGUAGE_FONT)
word = canvas.create_text(325, 214, font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

tick = PhotoImage(file="images/right.png")
right = Button(image=tick, highlightthickness=0, bd=0, bg=BACKGROUND_COLOR, borderwidth=0, command=right)
right.grid(column=0, row=1)

cross = PhotoImage(file="images/wrong.png")
wrong = Button(image=cross, highlightthickness=0, bd=0, bg=BACKGROUND_COLOR, borderwidth=0, command=new_card)
wrong.grid(column=1, row=1)

new_card()
window.mainloop()
