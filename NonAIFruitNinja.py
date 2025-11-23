# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:18:47 2025

@author: user
"""

import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.title("Fruit Ninja - Custom Version")
screen.setup(width=700, height=600)
screen.tracer(0)

# Global variables
score = 0
time_left = 120
player_name = ""
game_speed = 50
score_multiplier_active = False
score_multiplier_timer = 0


screen.register_shape("sword.gif")
cursor_turtle = turtle.Turtle()
cursor_turtle.shape("sword.gif")
cursor_turtle.penup()
cursor_turtle.speed(0)
cursor_turtle.hideturtle() 

message_turtle = turtle.Turtle()
message_turtle.hideturtle()
message_turtle.penup()
message_turtle.goto(0, 0) 

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(0, 260)

# Timer display
timer_display = turtle.Turtle()
timer_display.hideturtle()
timer_display.penup()
timer_display.goto(200, 260)

# Mouse trail
trail = turtle.Turtle()
trail.hideturtle()
trail.color("white")
trail.pensize(3)
trail.speed(0)
trail.penup()
positions = []


#setting up design
screen.bgpic("ogbg.gif")
theme_choice = screen.textinput("Hello Player!", 
    "Choose Your Theme:\n1 - Classic\n2 - Tropical\n3 - Vegetables")

if theme_choice in ["1", "classic", "Classic"]:
    screen.bgpic("bgf.gif") 
    fruit_images = [
        "banana.gif", "orange.gif", "red apple.gif",  "strawberries.gif", "pear.gif","double_score_fruit.gif","timer_down.gif"
    ]
    fruit_left_images = [
       "banana_left.gif", "orange_left.gif", "red apple_left.gif", "strawberry_left.gif", "pear_left.gif","sparkle.gif","-10.gif"
    ]
    
    fruit_right_images = [
      "banana_right.gif", "orange_right.gif", "red apple_right.gif", "strawberry_right.gif", "pear_right.gif","sparkle.gif","sad.gif"
    ]
elif theme_choice in ["2", "tropical", "Tropical"]:
    screen.bgpic("tropical.gif")
    fruit_images=[ "coconut.gif","grape.gif", "watermelon.gif","cherries.gif", "pineapple.gif","double_score_fruit.gif","timer_down.gif"
        ]
    fruit_left_images = [
       "coconut_left.gif", "grape_left.gif", "watermelon_left.gif", "cherries_left.gif", "pineapple_left.gif","sparkle.gif","-10.gif"
    ]
    
    fruit_right_images = [
       "coconut_right.gif", "grape_right.gif", "watermelon_right.gif", "cherries_right.gif", "pineapple_right.gif","sparkle.gif","sad.gif"
    ]
elif theme_choice in ["3", "vegetables", "Vegetables"]:
    screen.bgpic("kitchen.gif")
    fruit_images=["cucumber.gif","carrot.gif","corn.gif","tomato.gif","eggplant.gif","double_score_fruit.gif","timer_down.gif"]
    
    fruit_left_images=["cucumber_left.gif","carrot_left.gif","corn_left.gif","tomato_left.gif","eggplant_left.gif","sparkle.gif","-10.gif"]
    
    fruit_right_images=["cucumber_right.gif","carrot_right.gif","corn_right.gif","tomato_right.gif","eggplant_right.gif","sparkle.gif","sad.gif"]
else:
    screen.bgpic("bgf.gif")
    fruit_images = [
        "banana.gif", "orange.gif", "red apple.gif",  "strawberries.gif", "pear.gif","double_score_fruit.gif","timer_down.gif"
    ]
    fruit_left_images = [
       "banana_left.gif", "orange_left.gif", "red apple_left.gif", "strawberry_left.gif", "pear_left.gif","sparkle.gif","-10.gif"
    ]
    
    fruit_right_images = [
      "banana_right.gif", "orange_right.gif", "red apple_right.gif", "strawberry_right.gif", "pear_right.gif","sparkle.gif","sad.gif"
    ]



    
[screen.register_shape(img) for img in fruit_images + fruit_left_images + fruit_right_images] #list comprehension

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


for _ in range(20):
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



def slice_fruit(fruit):
    indx = fruit_images.index(fruit.shape())
   
    left_half = turtle.Turtle()
    right_half = turtle.Turtle()

    left_half.shape(fruit_left_images[indx])
    right_half.shape(fruit_right_images[indx])
  
    left_half.penup()
    right_half.penup()
    
   
    x, y = fruit.position()
    left_half.goto(x -20, y) #disposition them to appear sliced
    right_half.goto(x + 20, y)
    
    
    left_half.dx = 0
    right_half.dx = 0
    
   
    left_half.dy = 0
    right_half.dy = 0
    
    gravity = 0.35
    
    fruit.hideturtle()
    
    def animate_halves():
        left_half.sety(left_half.ycor() + left_half.dy) #These two lines move the two sliced halves (left and right) up or down on the screen based on their current speed (dy).
        right_half.sety(right_half.ycor() + right_half.dy) #At first, dy = 0, but gravity pulls it down, so dy becomes more negative over time (falling faster)
        
        left_half.dy -= gravity
        right_half.dy -= gravity
        
    
        if left_half.ycor() < -300:
            left_half.hideturtle()
            right_half.hideturtle()
            return
        
        # Keeps animating
        screen.ontimer(animate_halves, 20)
    
    animate_halves()


def get_player_name():
    global player_name
    player_name = turtle.textinput("Welcome!", "Enter your name:")
    if not player_name:
        player_name = "Player"
    pen.goto(0, 0)
    pen.write("Welcome, "+player_name+"!\nClick to start", align="center", font=("Arial", 20, "bold"))
    screen.onscreenclick(start_game)

def update_score_display():
    score_display.clear()
    score_display.write(player_name+"'s Score: "+str(score), align="center", font=("Arial", 18, "bold"))
#Turtle’s (0, 0) is at the center of the screen
def track_mouse_motion(x, y):
    turtle_x = x - 300 #x - 300 shifts the origin horizontally. 
    turtle_y = 300 - y  #300 - y flips the y-axis so up is positive 
    cursor_turtle.goto(turtle_x, turtle_y)
    cursor_turtle.showturtle()
    positions.append((turtle_x, turtle_y))
    if len(positions) > 10: #Keeps track of last 10 positions to draw a fading trail.
        positions.pop(0) #Removes old ones to prevent it from getting too long.
    trail.clear()
    trail.penup()
    if positions:
        trail.goto(positions[0])
        trail.pendown()
        for pos in positions[1:]:
            trail.goto(pos)

def handle_mouse_motion(event):
    track_mouse_motion(event.x, event.y) #This connects the real system-level mouse movement (event.x, event.y) to our custom function.
#Turtle by default doesn’t track free movement—so we use getcanvas().bind() from the Tkinter layer underneath.

def start_game(x, y):
    pen.clear()
    screen.getcanvas().bind("<Motion>", handle_mouse_motion)# Each movement passes a Tkinter event, which has .x and .y.
    screen.onscreenclick(None)
    countdown()
    increase_difficulty()
    spawn_fruit_batch()
    game_loop()
    

def countdown():
    global time_left
    time_left -= 1
    timer_display.clear()
    timer_display.write("Time: "+str(time_left), font=("Arial", 16, "bold"))
    if time_left > 0:
        screen.ontimer(countdown, 1000)
    else:
        end_game()
        



def end_game():
    screen.getcanvas().unbind("<Motion>")
    cursor_turtle.hideturtle()
    trail.clear()
    screen.clear()
    screen.bgpic("medal_bg.gif")
    screen.register_shape("gold_medal.gif")
    screen.register_shape("silver_medal.gif")
    screen.register_shape("bronze_medal.gif")
    
    medal = turtle.Turtle()
    medal.hideturtle()
    medal.penup()
    medal.goto(0, 20)
    pen.clear()
    pen.goto(0, 120)
    pen.color("white")  
    pen.write("TIME'S UP!\nFinal Score: "+str(score), align="center", font=("Arial", 24, "bold"))

    if score >= 1500:
        medal.shape("gold_medal.gif")
        message = "You earned a GOLD medal!"
        pen.color("gold")
    elif score >= 1000:
        medal.shape("silver_medal.gif")
        message = "You earned a SILVER medal!"
        pen.color("silver")
    elif score >= 800:
        medal.shape("bronze_medal.gif")
        message = "You earned a BRONZE medal!"
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
            launched += 1
        if launched >= count:
            break
    if time_left > 0:
        screen.ontimer(spawn_fruit_batch, 2000)

def increase_difficulty():
    global game_speed
    if game_speed > 20:
        game_speed -= 5
    screen.ontimer(increase_difficulty, 15000)  
    
def show_message(text, color,duration):
    message_turtle.clear()
    message_turtle.color(color)
    message_turtle.write(text, align="center", font=("Courier", 30, "bold"))
    screen.ontimer(message_turtle.clear, duration)

def game_loop():
    global score, time_left, score_multiplier_active, score_multiplier_timer
    for f in fruit_pool:
        if f.isvisible():
            f.setx(f.xcor() + f.dx) 
            f.sety(f.ycor() + f.dy)
            f.dy -= f.gravity #decreasing

            if f.xcor() > 280 or f.xcor() < -280:
                f.dx *= -1
            if f.ycor() < -300:
                f.hideturtle()

            for pos in positions:
                if f.distance(pos[0], pos[1]) < 40:
                    if f.shape() == "timer_down.gif":
                        time_left = max(0, time_left - 10)
                        show_message("-10 Seconds!","red",1000)

                    elif f.shape() == "double_score_fruit.gif":
                            score_multiplier_active = True
                            score_multiplier_timer = 60
                            show_message("Score x2 Activated!","gold",3000)
                            

                    else:
                        if score_multiplier_active:
                            score += 30
                        else:
                            score += 15

                    update_score_display()
                    slice_fruit(f)
                    f.hideturtle()
                    break  

    bomb.setx(bomb.xcor() + bomb.dx)
    bomb.sety(bomb.ycor() + bomb.dy)
    bomb.dy -= bomb.gravity
    if bomb.xcor() > 280 or bomb.xcor() < -280:
        bomb.dx *= -1
    if bomb.ycor() < -300:
        spawn_bomb()

    for pos in positions:
        if bomb.distance(pos[0], pos[1]) < 40:
            score -= 50
            update_score_display()
            message_turtle.clear()
            message_turtle.color("yellow")
            message_turtle.write("BOOM!", align="center", font=("Courier", 50, "bold"))
            screen.ontimer(message_turtle.clear, 1000)
          

            spawn_bomb()

   
    if score_multiplier_active:
        score_multiplier_timer -= 1
        if score_multiplier_timer <= 0:
            score_multiplier_active = False

    screen.update()
    if time_left > 0:
        screen.ontimer(game_loop, game_speed)


get_player_name()
screen.mainloop()
