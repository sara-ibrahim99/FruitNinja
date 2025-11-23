# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 16:48:56 2025

@author: user
"""


import turtle
import random
import numpy as np


GRID_SIZE = 7
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
q_table = np.load("q_table.npy")

def move(pos, action_idx):
    dx = ACTIONS[action_idx][0]
    dy = ACTIONS[action_idx][1]
    new_x = min(max(pos[0] + dx, 0), GRID_SIZE - 1)
    new_y = min(max(pos[1] + dy, 0), GRID_SIZE - 1)
    return new_x, new_y

def turtle_to_grid(x, y):
    grid_x = int((x + 280) / (560.0 / 7))
    grid_y = int((y + 280) / (560.0 / 7))
    grid_x = min(max(grid_x, 0), 6)
    grid_y = min(max(grid_y, 0), 6)
    return grid_x, grid_y

def grid_to_turtle(grid_x, grid_y):
    x = -280 + grid_x * (560.0 / 7)
    y = -280 + grid_y * (560.0 / 7)
    return x, y

# === Turtle Setup ===
screen = turtle.Screen()
screen.title("Fruit Ninja - AI Edition")
screen.setup(width=700, height=600)
screen.tracer(0)

score = 0
time_left = 120
player_name = "AI"
game_speed = 50
score_multiplier_active = False
score_multiplier_timer = 0

screen.register_shape("sword.gif")
cursor_turtle = turtle.Turtle()
cursor_turtle.shape("sword.gif")
cursor_turtle.penup()
cursor_turtle.speed(0)
cursor_turtle.hideturtle()

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(0, 260)

timer_display = turtle.Turtle()
timer_display.hideturtle()
timer_display.penup()
timer_display.goto(200, 260)

screen.bgpic("bgf.gif")
fruit_images = ["banana.gif", "orange.gif", "red apple.gif", "strawberries.gif", "pear.gif", "double_score_fruit.gif"]
fruit_left_images = ["banana_left.gif", "orange_left.gif", "red apple_left.gif", "strawberry_left.gif", "pear_left.gif", "sparkle.gif"]
fruit_right_images = ["banana_right.gif", "orange_right.gif", "red apple_right.gif", "strawberry_right.gif", "pear_right.gif", "sparkle.gif"]

for img in fruit_images:
    screen.register_shape(img)
for img in fruit_left_images:
    screen.register_shape(img)
for img in fruit_right_images:
    screen.register_shape(img)

fruit_pool = []

def spawn_fruit(f):
    index = random.randint(0, len(fruit_images)-1)
    f.shape(fruit_images[index])
    f.fruit_index = index
    f.goto(random.randint(-250, 250), -250)
    f.dx = random.uniform(-1.5, 1.5)
    f.dy = random.uniform(12, 18)
    f.gravity = 0.35
    f.showturtle()

for i in range(20):
    f = turtle.Turtle()
    f.hideturtle()
    f.penup()
    f.speed(0)
    fruit_pool.append(f)

screen.register_shape("bomb.gif")
bomb = turtle.Turtle()
bomb.shape("bomb.gif")
bomb.penup()

def spawn_bomb():
    bomb.goto(random.randint(-250, 250), -250)
    bomb.dx = random.uniform(-1.5, 1.5)
    bomb.dy = random.uniform(12, 18)
    bomb.gravity = 0.35

spawn_bomb()

def update_score_display():
    score_display.clear()
    score_display.write(player_name + "'s Score: " + str(score), align="center", font=("Arial", 18, "bold"))

def slice_fruit(fruit):
    indx = fruit_images.index(fruit.shape())
    left_half = turtle.Turtle()
    right_half = turtle.Turtle()
    left_half.shape(fruit_left_images[indx])
    right_half.shape(fruit_right_images[indx])
    left_half.penup()
    right_half.penup()
    x, y = fruit.position()
    left_half.goto(x - 20, y)
    right_half.goto(x + 20, y)
    left_half.dy = 0
    right_half.dy = 0
    gravity = 0.35
    fruit.hideturtle()

    def animate_halves():
        left_half.sety(left_half.ycor() + left_half.dy)
        right_half.sety(right_half.ycor() + right_half.dy)
        left_half.dy = left_half.dy - gravity
        right_half.dy = right_half.dy - gravity
        if left_half.ycor() < -300:
            left_half.hideturtle()
            right_half.hideturtle()
            return
        screen.ontimer(animate_halves, 20)

    animate_halves()

def countdown():
    global time_left
    time_left = time_left - 1
    timer_display.clear()
    timer_display.write("Time: " + str(time_left), font=("Arial", 16, "bold"))
    if time_left > 0:
        screen.ontimer(countdown, 1000)
    else:
        end_game()

def end_game():
    cursor_turtle.hideturtle()
    screen.clear()
    screen.bgpic("medal_bg.gif")
    screen.register_shape("gold_medal.gif")
    screen.register_shape("silver_medal.gif")
    screen.register_shape("bronze_medal.gif")
    medal = turtle.Turtle()
    medal.hideturtle()
    medal.penup()
    medal.goto(0, 20)
    pen.goto(0, 120)
    pen.color("white")
    pen.write("TIME'S UP!\nFinal Score: " + str(score), align="center", font=("Arial", 24, "bold"))
    if score >= 300:
        medal.shape("gold_medal.gif")
        message = "The AI earned a GOLD medal!"
        pen.color("gold")
    elif score >= 200:
        medal.shape("silver_medal.gif")
        message = "The AI earned a SILVER medal!"
        pen.color("silver")
    elif score >= 100:
        medal.shape("bronze_medal.gif")
        message = "The AI earned a BRONZE medal!"
        pen.color("brown")
    else:
        message = "Better luck next time!"
        pen.color("white")
        pen.goto(0, -100)
        pen.write(message, align="center", font=("Arial", 20, "normal"))
        medal.hideturtle()
        screen.update()
        return
    medal.showturtle()
    pen.goto(0, -150)
    pen.write(message, align="center", font=("Arial", 20, "bold"))
    screen.update()

def spawn_fruit_batch():
    count = random.randint(1, 4)
    launched = 0
    for f in fruit_pool:
        if not f.isvisible():
            spawn_fruit(f)
            launched = launched + 1
        if launched >= count:
            break
    if time_left > 0:
        screen.ontimer(spawn_fruit_batch, 2000)

def increase_difficulty():
    global game_speed
    if game_speed > 20:
        game_speed = game_speed - 5
    screen.ontimer(increase_difficulty, 15000)

def game_loop():
    global score, score_multiplier_active, score_multiplier_timer

    visible_fruits = []
    for f in fruit_pool:
        if f.isvisible():
            visible_fruits.append(f)

    if len(visible_fruits) >= 2:
        f1 = visible_fruits[0]
        f2 = visible_fruits[1]
    elif len(visible_fruits) == 1:
        f1 = visible_fruits[0]
        f2 = visible_fruits[0]
    else:
        f1 = turtle.Turtle()
        f2 = turtle.Turtle()
        f1.goto(0, 0)
        f2.goto(0, 0)

    fx1, fy1 = turtle_to_grid(f1.xcor(), f1.ycor())
    fx2, fy2 = turtle_to_grid(f2.xcor(), f2.ycor())
    bx, by = turtle_to_grid(bomb.xcor(), bomb.ycor())
    sx, sy = turtle_to_grid(cursor_turtle.xcor(), cursor_turtle.ycor())

    state = (sx, sy, fx1, fy1, fx2, fy2, bx, by)
    action = np.argmax(q_table[state])
    next_sx, next_sy = move((sx, sy), action)
    new_x, new_y = grid_to_turtle(next_sx, next_sy)
    cursor_turtle.goto(new_x, new_y)
    cursor_turtle.showturtle()

    for f in fruit_pool:
        if f.isvisible():
            f.setx(f.xcor() + f.dx)
            f.sety(f.ycor() + f.dy)
            f.dy = f.dy - f.gravity
            if f.xcor() > 280 or f.xcor() < -280:
                f.dx = f.dx * -1
            if f.ycor() < -300:
                f.hideturtle()
            if f.distance(cursor_turtle) < 40:
                if f.shape() == "double_score_fruit.gif":
                    score_multiplier_active = True
                    score_multiplier_timer = 60
                else:
                    if score_multiplier_active:
                        score = score + 30
                    else:
                        score = score + 15
                update_score_display()
                slice_fruit(f)
                f.hideturtle()

    bomb.setx(bomb.xcor() + bomb.dx)
    bomb.sety(bomb.ycor() + bomb.dy)
    bomb.dy = bomb.dy - bomb.gravity
    if bomb.xcor() > 280 or bomb.xcor() < -280:
        bomb.dx = bomb.dx * -1
    if bomb.ycor() < -300:
        spawn_bomb()
    if bomb.distance(cursor_turtle) < 40:
        score = score - 50
        update_score_display()
        spawn_bomb()

    if score_multiplier_active:
        score_multiplier_timer = score_multiplier_timer - 1
        if score_multiplier_timer <= 0:
            score_multiplier_active = False

    screen.update()
    if time_left > 0:
        screen.ontimer(game_loop, game_speed)

update_score_display()
countdown()
increase_difficulty()
spawn_fruit_batch()
game_loop()
screen.mainloop()
