import turtle
import os

#Set up window
width = 1000
height = 700
window = turtle.Screen()
window.setup(width = width, height = height)
window.bgcolor("#C41E3A")
window.tracer(0)
window.title("Plong (Press x to close the game)")

####################
#On screen objects #
####################

#Scorekeeper
sk = turtle.Turtle()
sk.speed(0)
sk.shape("square")
sk.color("white")
sk.penup()
sk.hideturtle()
sk.setx(0)
sk.sety(300)
sk.write("Player A: 0              Player B: 0", align="center", font=("Coutier", 24, "normal"))


#End game greeting
g = turtle.Turtle()
g.speed(0)
g.shape("square")
g.color("white")
g.penup()
g.hideturtle()
g.setx(0)
g.sety(200)

#Default size of turtle is 20px high and 20px wide, 10 on each side of center.
#Player 1
p1 = turtle.Turtle()
p1.shape("square")
p1.speed(0)
p1.color("white")
p1.penup()
p1.setx(-450)
p1.sety(0)
p1.stretchwid = 3
p1.shapesize(stretch_wid = p1.stretchwid, stretch_len = 1)
p1.halfsize = 30
p1.points = 0

#Player 2
p2 = turtle.Turtle()
p2.color("white")
p2.shape("square")
p2.speed(0)
p2.penup()
p2.setx(450)
p2.sety(0)
p2.stretchwid = 3
p2.shapesize(stretch_wid = p2.stretchwid, stretch_len = 1)
p2.halfsize = 30
p2.points = 0

#Ball
#Don't stretch ball
ball = turtle.Turtle()
ball.shape("circle")
ball.speed(0)
ball.color("white")
ball.penup()
ball.setx(0)
ball.sety(0)
ball.x_speed = 3
ball.y_speed = 3

####################
#Movement Functions#
####################
def p1_up():
	y = p1.ycor()
	y += 25
	p1.sety(y)
	window.onkeypress(p1_down, "s")

def p1_down():
	y = p1.ycor()
	y -= 25
	p1.sety(y)
	window.onkeypress(p1_up, "e")

def p2_up():
    y = p2.ycor()
    y = y + 25
    p2.sety(y)

def p2_down():
    y = p2.ycor()
    y -= 25
    p2.sety(y)


###################
#Keyboard bindings#
###################
window.listen()
window.onkeypress(p1_up, "e")
window.onkeypress(p1_down, "s")
window.onkeypress(p2_up, "Up")
window.onkeypress(p2_down, "Down")

####################
#Gameplay functions#
####################

#Reset ball to original position
def resetball(speed):
	ball.setx(0)
	ball.sety(0)
	ball.x_speed = speed

#Give boost to player who scored
def goalboost(player):
	#Increase size of paddle for person who scored
	player.stretchwid *= 1.2
	player.shapesize(stretch_wid = p1.stretchwid, stretch_len = 1)
	player.halfsize *= 1.2
	#Update score
	player.points += 1

#Check if ball is going out of bounds vertically
def checkBallInbounds():
	ball_x = ball.xcor()
	ball_y = ball.ycor()
	if(ball_y >= height/2 - 20 or ball_y <= -(height/2 - 20)):
		ball.y_speed *= -1

#Check is ball is going to goal
def checkgoal():
	ball_x = ball.xcor()
	ball_y = ball.ycor()
	#Player 1 scored
	if(ball_x >= 470):
		#Reset ball
		resetball(-3)
		#boost for scoring point
		goalboost(p1)
		sk.clear()
		sk.write("Player 1: {}              Player 2: {}".format(p1.points, p2.points), align = "center", font = ("Coutier", 24, "normal"))
		os.system("afplay sounds/score.mp3&")


	#Player 2 scored
	if ball_x < -470:
		#Reset ball
		resetball(3)
		#Increase paddle size
		goalboost(p2)
		sk.clear()
		sk.write("Player 1: {}              Player 2: {}".format(p1.points, p2.points), align = "center", font = ("Coutier", 24, "normal"))
		os.system("afplay sounds/score.mp3&")

#Check if ball hit paddle
def hitpaddle():
	ball_x = ball.xcor()
	ball_y = ball.ycor()

	#Check if ball hit paddle 1
	if(ball_x < -440 and ball_x > -450 and (ball_y >= p1.ycor() - p1.halfsize and ball_y <= p1.ycor() + p1.halfsize)):
		#Speed up ball by 1.05 times
		ball.x_speed *= -1.1

	#Check if ball hit paddle2
	if(ball_x > 440 and ball_x < 450 and (ball_y >= p2.ycor() - p2.halfsize and ball_y <= p2.ycor() + p2.halfsize)):
		ball.x_speed *= -1.1

def paddle_isInbounds():
	#If paddle's upper or lower end is touching border, make stationary
	#Overrides onkeypress command
	if(p1.ycor() + p1.halfsize >= height/2):
		p1.sety(height/2 - p1.halfsize)

	if(p1.ycor() - p1.halfsize <= -height/2):
		p1.sety(-height/2 + p1.halfsize)

	if(p2.ycor() + p2.halfsize >= height/2):
		p2.sety(height/2 - p2.halfsize)

	if(p2.ycor() - p2.halfsize <= -height/2):
		p2.sety(-height/2 + p2.halfsize)

def endgame():
	if(p1.points == 5 or p2.points == 5):
		#Stop ball movement
		ball.x_speed = 0
		ball.y_speed = 0
		#Stop registering keys
		window.onkeypress(None, "e")
		window.onkeypress(None, "s")
		window.onkeypress(None, "Up")
		window.onkeypress(None, "Down")
		g.write("Victory! Good game folks. Quit the console to exit the game.", align = "center", font = ("Coutier", 24, "normal"))

#Main Game loop
while True:
	window.update()

	#Update ball position
	ball.setx(ball.x_speed + ball.xcor())
	ball.sety(ball.y_speed + ball.ycor())

	checkBallInbounds()
	checkgoal()
	hitpaddle()
	paddle_isInbounds()
	endgame()