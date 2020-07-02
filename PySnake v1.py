
"""A simple program that utilizes Turtle to create a snake game."""


import turtle
import time
import random

paused = False
running = True

body_parts = []
colors = ["red", "orange", "blue", "pink"]

"""Initialize game screen"""
window = turtle.Screen()
window.title("PySnake")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)  # turns off the screen updates

"""Initialize snake head"""
head = turtle.Turtle()
head.shapesize(0.5,0.5)
head.speed(0)
head.shape("square")
head.color("green")
head.penup()  # turns off tracing animation when the object moves
head.goto(0, 0)
head.direction = "stop"

"""Initialize snake food"""
color = random.choice(colors)
food = turtle.Turtle()
food.shapesize(0.5, 0.5)
food.speed(0)
food.shape("circle")
food.color(color)
food.penup()  # turns off tracing animation when the object moves
food.goto(random.randint(-290, 290), random.randint(-290, 290))


"""Initialize score board"""
score_board = turtle.Turtle()
score_board.speed(0)
score_board.shape("square")
score_board.color("white")
score_board.penup()
score_board.hideturtle()
score_board.goto(0, 260)
score_board.write("Score: 0      High Score: 0", align="center", font=("Consolas", 24, "normal"))


"""Initialize game rules"""
rules = turtle.Turtle()
rules.speed(0)
rules.shape("square")
rules.color("white")
rules.penup()
rules.hideturtle()
rules.goto(0, -240)
rules.write("Use Arrow keys to move\nP to pause and Q to quit\nHit SPACE when you are ready!", align="center", font=("Consolas", 18, "normal"))


"""Movement logic"""
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+10)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y-10)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x-10)

    if head.direction == "right":
        head.setx(head.xcor()+10)  # shorthand


def handle_food():
    if head.distance(food) < 10:
        x = random.randrange(-280, 280, 10)
        y = random.randrange(-280, 280, 10)
        food.goto(x, y)
        return True


def grow_snake():
    if head.distance(food) < 10:
        body = turtle.Turtle()
        body.shapesize(0.5, 0.5)
        body.speed(0)
        body.shape("square")
        body.color("grey")
        body.penup()
        body_parts.append(body)



    for i in range(len(body_parts)-1, -1, -1):

        x = body_parts[i-1].xcor()
        y = body_parts[i-1].ycor()
        body_parts[i].goto(x, y)

    if len(body_parts) > 0:
        x = head.xcor()
        y = head.ycor()
        body_parts[0].goto(x, y)


def body_collision():
    for i in body_parts:
        if i.distance(head) < 10:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            return True


def collision_check():
    if (head.xcor() > 290 or head.xcor() < -290 or
            head.ycor() > 290 or head.ycor() < -290) or body_collision():
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for i in body_parts:
            i.hideturtle()
        body_parts.clear()
        return True


def update_score(score, high_score):
    score += 10

    if score > high_score:
        high_score = score

    score_board.clear()
    score_board.write("Score: {}      High Score: {}".format(score, high_score), align="center",
                      font=("Consolas", 24, "normal"))

    return score, high_score



"""Handle movement direction"""
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def pause():
    global paused
    paused = not paused

def quit_game():
    global running
    running = False

def clear_rules():
    rules.clear()


"""Keyboard bindings"""
window.listen()
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")
window.onkeypress(pause, "p")
window.onkeypress(quit_game, "q")
window.onkeypress(clear_rules, "space")


"""Main game loop"""
def main():
    global paused
    global running
    delay = 0.1
    score = 0
    high_score = 0



    while running:
        if not paused:
            window.update()
            if collision_check():
                delay = 0.1
                score = 0
                score_board.clear()
                score_board.write("Score: {}      High Score: {}".format(score, high_score), align="center",
                                  font=("Consolas", 24, "normal"))
            grow_snake()
            if handle_food():
                #update_score(score, high_score)
                score, high_score = update_score(score, high_score)[0],\
                                    update_score(score, high_score)[1] # for some reason this syntax doesnt make 2 functioncalls unlike the 2-line method
                delay -= 0.001

            move()
            time.sleep(delay)

        else:
            window.update()

main()

