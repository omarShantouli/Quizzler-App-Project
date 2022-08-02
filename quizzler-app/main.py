from tkinter import *
import requests
from playsound import playsound
import html
# getting question bank
response = requests.get(url="https://opentdb.com/api.php?amount=10&type=boolean")
response.raise_for_status()
data = response.json()["results"]
question_bank = []
for d in data:
    question_bank.append((html.unescape(d['question']), d['correct_answer']))

#====================================
# playing sounds
import winsound
from threading import Thread

def play_sound():
    playsound("sounds/end.wav", winsound.SND_ALIAS)

def correct():
    playsound("sounds/Bing.mp3", winsound.SND_ALIAS)

def wrong():
    playsound("sounds/Game-show-buzzer-sound.mp3", winsound.SND_ALIAS)

#===================================
window = Tk()
window.minsize(width= 300, height= 500)
window.config(bg= "#94B49F")

page = 1
score = 0
q = 0

score_lab = Label(text= f"Score: {score}", bg= "#94B49F", fg= "white", font= ('Arial', 14, 'normal'))
score_lab.grid(column= 2, row= 1)
canvas = Canvas(width= 300, height= 250, highlightthickness= 0, bg= "#E2DCC8")
question = canvas.create_text(150, 100, text= question_bank[q][0], font= ('Arial', 14, 'normal'), width= 280)
page_no = canvas.create_text(150, 230, text= page, font= ('Arial', 14, 'normal'))
canvas.grid(column= 1, row= 2, padx= 50, pady= 50, columnspan= 2)


def fin():
    global score
    canvas.delete(question)
    canvas.config(bg= "#A5C9CA")
    canvas.create_text(150, 125, text= f"YOUR SCORE IS \n          {score} / 10", font= ('Arial', 18, 'bold'), fill= "#231955")
    Thread(target=play_sound).start()
    count = 5
    cnt = canvas.create_text(150, 220, text= count, font= ('Arial', 14, 'normal'))
    x = None
    def counting(count = 5):
        global x
        if count > 0 :
            canvas.itemconfig(cnt, text = count)
            x = window.after(1000, counting, count - 1)
        else:
            window.destroy()
    counting(5)



def next(q):
    global page
    right_but["state"] = ACTIVE
    wrong_but["state"] = ACTIVE
    page += 1
    canvas.itemconfig(page_no, text=page)
    if q == len(question_bank):
        canvas.delete(page_no)
        right_but["state"] = DISABLED
        wrong_but["state"] = DISABLED
        window.after(200, fin)
    else:
        canvas.config(bg= "#E2DCC8")
        canvas.itemconfig(question, text= question_bank[q][0])


def answ(answer):
    global score, q, page
    if answer == question_bank[q][1]:
        Thread(target=correct).start()
        score += 1
        score_lab.config(text=f"Score: {score}")
        canvas.config(bg="green")

    else:
        Thread(target=wrong).start()
        canvas.config(bg="red")
    q += 1


    # if q == len(question_bank):
    right_but["state"] = DISABLED
    wrong_but["state"] = DISABLED
    window.after(2500, next, q)


r_img = PhotoImage(file= "./images/true.png")
right_but = Button(image= r_img, highlightthickness= 0, command= lambda : answ('True'))
right_but.grid(column= 1, row= 3, padx= 10, pady= 10)

w_img = PhotoImage(file= "./images/false.png")
wrong_but = Button(image= w_img, highlightthickness= 0, command= lambda : answ('False'))
wrong_but.grid(column= 2, row= 3, padx= 10, pady= 10)

window.mainloop()

