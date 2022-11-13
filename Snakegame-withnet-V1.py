from tkinter import *
import random
from tkinter import simpledialog

# from turtle import width, window_height, window_width
import tkinter
import time

import tkinter as tk
import time
from tkinter.ttk import Label

from tk_sleep import tk_sleep
from style import set_style
from window_handler import create_window, start_window_loop

from network import connect, send

# window = Tk()


SPACE_SIZE = 50
BODY_PARTS = 3
GAME_WIDTH = 500
GAME_HEIGHT = 500
direction = "down"
SPEED = 400

# TKInter widgets
window = create_window(tk, "snake_game", GAME_HEIGHT + 100, GAME_WIDTH + 500)
set_style(window)

# game_area = Frame(
#   window, bg="black", bd=0, height=game_area_height, width=game_area_width
# )
game_area = Canvas(window, background="black", height=GAME_HEIGHT, width=GAME_WIDTH)
message = Label(game_area, style="Message.TLabel")

game_state = {
    "me": None,
    "opponent": None,
    "is_server": None,
}

# remember which keys are down
# keys_down_me = set()
# keys_down_opponent = set()

# locally
# keys_down = set()
# last_down = None


class Pl1food:
    # constructor of food class
    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        # window.title("Player-1")

        # setting coordinates of food object
        self.coordinates = [x, y]

        # starting corner is x,y and ending corner is space size
        player1.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="Green", tag="food"
        )


class Pl1snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.direction = "down"
        self.SNAKE_COLOR = "RED"
        canvas = player1.canvas
        canvas.pack()
        self.score_counter = 0

        # setting starting position of snake as top left corner
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # creating squares of the snake
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


def pl1_next_turn(pl1snake, pl1food):
    x, y = pl1snake.coordinates[0]
    direction = pl1snake.direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    pl1snake.coordinates.insert(0, (x, y))

    square = player1.canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red"
    )

    pl1snake.squares.insert(0, square)
    if x == pl1food.coordinates[0] and y == pl1food.coordinates[1]:

        # Score update in canvas
        pl1snake.score_counter += 1
        pl1_update_scores()
        player1.canvas.delete("food")
        pl1food = Pl1food()

    else:

        del pl1snake.coordinates[-1]

        player1.canvas.delete(pl1snake.squares[-1])

        del pl1snake.squares[-1]

    if pl1_check_collisions(pl1snake):
        pl1_game_over()
        return True

    else:
        window.after(SPEED, pl1_next_turn, pl1snake, pl1food)


def pl1_check_collisions(pl1snake):

    # starting coordinates of head of snake in x and y variables
    x, y = pl1snake.coordinates[0]

    # to check whether snake has  crossed left or right border

    if x < 0 or x >= GAME_WIDTH:
        return True

    # # to check whether snake has  crossed top or bottom border
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # to check if snake has collided with any of its bodypart

    for body_part in pl1snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def pl1_game_over():
    # to clear the canvas
    player1.canvas.create_text(
        player1.canvas.winfo_width() / 4,
        player1.canvas.winfo_height() / 4,
        font=("consolas", 20),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )
    if pl2_check_collisions(pl2snake) == True:
        handle1_game_over()
        player1.canvas.delete(ALL)
    else:
        print("Waiting for Oponent Pl2")


def handle1_game_over():
    # Method to print out the final message and declare the winner based on player scores
    print("Game Over of Player1!")
    # wait_until(pl2_next_turn == False, 5, period=0.25)
    if pl1snake.score_counter > pl2snake.score_counter:
        result_msg = pl1snake.SNAKE_COLOR + " Snake wins!"
    elif pl2snake.score_counter > pl1snake.score_counter:
        result_msg = pl2snake.SNAKE_COLOR + " Snake wins!"
    else:
        result_msg = "Its a tie!"
    widget = tkinter.Label(
        player1.canvas,
        text="Game Over!\n" + result_msg,
        fg="white",
        bg="black",
        font=("Times", 20, "bold"),
    )
    widget.pack()
    widget.place(relx=0.5, rely=0.5, anchor="center")
    return True


def pl1_update_scores():
    player1.canvas.itemconfig(
        player1.scoreboard, text="SCORE: " + str(pl1snake.score_counter)
    )


class Player1:
    def __init__(self):
        self.score = 0
        self.canvas = Canvas(window, bg="black", height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack(side=LEFT)
        self.scoreboard = self.canvas.create_text(
            self.canvas.winfo_screenwidth() * 0.05,
            self.canvas.winfo_screenheight() * 0.01,
            font=("consolas", 14, "bold"),
            text=("Player1 SCORE: " + str(0)),
            anchor=tkinter.NW,
            fill="red",
            tag="scoreboard",
        )

        controls = ["w", "s", "a", "d"]

        window.bind(controls[0], lambda event: pl1_change_direction("up"))
        window.bind(controls[1], lambda event: pl1_change_direction("down"))
        window.bind(controls[2], lambda event: pl1_change_direction("left"))
        window.bind(controls[3], lambda event: pl1_change_direction("right"))

    def wait1_until(gamestatus, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if gamestatus:
                return True
            time.sleep(period)
        return False


def pl1_change_direction(new_direction):
    # to avoid 180 degree turn of snak
    if new_direction == "left":
        if pl1snake.direction != "right":
            pl1snake.direction = new_direction
    elif new_direction == "right":
        if pl1snake.direction != "left":
            pl1snake.direction = new_direction
    elif new_direction == "up":
        if pl1snake.direction != "down":
            pl1snake.direction = new_direction
    elif new_direction == "down":
        if pl1snake.direction != "up":
            pl1snake.direction = new_direction
    send(pl1snake.direction)


class Pl2food:
    # constructor of food class
    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        # player2.label2.title("Player-2")

        # setting coordinates of food object
        self.coordinates = [x, y]

        # starting corner is x,y and ending corner is space size
        player2.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="Blue", tag="food2"
        )


class Pl2snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.direction = "down"
        self.SNAKE_COLOR = "Yellow"
        self.score_counter = 0

        canvas = player2.canvas

        # setting starting position of snake as top left corner
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # creating squares of the snake
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=self.SNAKE_COLOR,
                tag="snake2",
            )
            self.squares.append(square)


def pl2_next_turn(pl2snake, pl2food):
    x, y = pl2snake.coordinates[0]
    direction = pl2snake.direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    pl2snake.coordinates.insert(0, (x, y))

    square = player2.canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="Yellow"
    )

    pl2snake.squares.insert(0, square)

    if x == pl2food.coordinates[0] and y == pl2food.coordinates[1]:

        # Score update in canvas
        pl2snake.score_counter += 1
        pl2_update_scores()

        player2.canvas.delete("food2")
        pl2food = Pl2food()

    else:

        del pl2snake.coordinates[-1]

        player2.canvas.delete(pl2snake.squares[-1])

        del pl2snake.squares[-1]

    if pl2_check_collisions(pl2snake):
        pl2_game_over()
        return True

    else:
        window.after(SPEED, pl2_next_turn, pl2snake, pl2food)


def pl2_check_collisions(pl2snake):

    # starting coordinates of head of snake in x and y variables
    x, y = pl2snake.coordinates[0]

    # to check whether snake has  crossed left or right border

    if x < 0 or x >= GAME_WIDTH:
        return True

    # # to check whether snake has  crossed top or bottom border
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # to check if snake has collided with any of its bodypart

    for body_part in pl2snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def pl2_update_scores():
    player2.canvas.itemconfig(
        player2.scoreboard, text="SCORE: " + str(pl2snake.score_counter)
    )


def pl2_game_over():

    # to clear the canvas
    player2.canvas.create_text(
        player2.canvas.winfo_width() / 4,
        player2.canvas.winfo_height() / 4,
        font=("consolas", 20),
        text="GAME OVER",
        fill="red",
        tag="gameover2",
    )
    if pl1_check_collisions(pl1snake) == True:
        handle2_game_over()
        player2.canvas.delete(ALL)
    else:
        print("Waiting for Oponent Pl1")


class Player2:
    def __init__(self):

        self.canvas = Canvas(window, bg="black", height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack(side=RIGHT)

        window.bind("<Left>", lambda event: pl2_change_direction("left"))
        window.bind("<Right>", lambda event: pl2_change_direction("right"))
        window.bind("<Up>", lambda event: pl2_change_direction("up"))
        window.bind("<Down>", lambda event: pl2_change_direction("down"))

        self.scoreboard = self.canvas.create_text(
            self.canvas.winfo_screenwidth() * 0.05,
            self.canvas.winfo_screenheight() * 0.01,
            font=("consolas", 14, "bold"),
            text=("Player-2 SCORE: " + str(0)),
            anchor=tkinter.NW,
            fill="Yellow",
            tag="scoreboard",
        )

    def wait2_until(gamestatus, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if gamestatus:
                return True
            time.sleep(period)
        return False


def pl2_change_direction(new_direction):
    print(new_direction)
    # to avoid 180 degree turn of snak
    if new_direction == "left":
        if pl2snake.direction != "right":
            pl2snake.direction = new_direction
    elif new_direction == "right":
        if pl2snake.direction != "left":
            pl2snake.direction = new_direction
    elif new_direction == "up":
        if pl2snake.direction != "down":
            pl2snake.direction = new_direction
    elif new_direction == "down":
        if pl2snake.direction != "up":
            pl2snake.direction = new_direction


def handle2_game_over():
    # Method to print out the final message and declare the winner based on player scores
    print("Game Over of Player2!")
    # wait_until(pl1_next_turn == False, 5, period=0.25)
    if pl1snake.score_counter > pl2snake.score_counter:
        result_msg = pl1snake.SNAKE_COLOR + " Snake wins!"
    elif pl2snake.score_counter > pl1snake.score_counter:
        result_msg = pl2snake.SNAKE_COLOR + " Snake wins!"
    else:
        result_msg = "Its a tie!"
    widget = tkinter.Label(
        player2.canvas,
        text="Game Over!\n" + result_msg,
        fg="white",
        bg="black",
        font=("Times", 20, "bold"),
    )
    widget.pack()
    widget.place(relx=0.5, rely=0.5, anchor="center")
    return True


def get_opponent_and_decide_game_runner(user, message):
    # who is the server (= the creator of the channel)
    if "created the channel" in message:
        name = message.split("'")[1]
        game_state["is_server"] = name == game_state["local_user"]
        # who is the opponent (= the one that joined that is not me)
        print("channel created")
    if "joined channel" in message:
        name = message.split(" ")[1]
        if name != game_state["local_user"]:
            game_state["opponent"] = name
        print("channel joined")


def on_network_message(timestamp, user: str, message: str):
    if user == "system":
        get_opponent_and_decide_game_runner(user, message)
        Pl2snake.change_direction("end", message)
    global keys_down_me, keys_down_oppon
    if game_state["is_server"]:
        if user == game_state["me"] and type(message) is list:
            keys_down_me = set(message)
        if user == game_state["opponent"] and type(message) is list:
            keys_down_opponent = set(message)
            pl2_next_turn(pl2snake, pl2food)
    # shared state (only of interest to the none-server)
    if type(message) is dict and not game_state["is_server"]:
        game_state["shared"] = message
        # redraw_screen()
        pl1_next_turn(pl1snake, pl1food)
        pl2_next_turn(pl2snake, pl2food)


def main():

    global local_user

    game_state["me"] = simpledialog.askstring("Input", "Your username", parent=window)

    channel = "vssnakegame" + simpledialog.askstring(
        "Input", "channel to join", parent=window
    )

    print(channel)

    connect(channel, game_state["me"], on_network_message)

    message.config(text="Waiting for an opponent...")
    message.place(y=200, x=100, width=GAME_WIDTH - 200)
    # wait for an opponent
    while game_state["opponent"] == None:
        tk_sleep(window, 1 / 10)
    print("2")

    message.destroy()
    # start game loop if i am the server´

    if game_state["is_server"]:
        # game_loop()
        pl1_next_turn(pl1snake, pl1food)
        pl2_next_turn(pl2snake, pl2food)

    # Manuel Setting start ##
    # if user != local_user and user != "system":
    #    Pl2snake.change_direction("end", message)
    # else:
    #    # message.config(text="Waiting for an opponent...")
    #    # message.place(y=200, x=100, width=GAME_WIDTH - 200)
    #    # wait for an opponent
    #    while game_state["opponent"] == None:
    #        tk_sleep(window, 1 / 10)
    #        pl1_next_turn(pl1snake, pl1food)
    #        pl2_next_turn(pl2snake, pl2food)
    ###### Manuel Setting end #####


local_user: str = None

player1 = Player1()
pl1food = Pl1food()
pl1snake = Pl1snake()


player2 = Player2()
pl2food = Pl2food()
pl2snake = Pl2snake()


main()
# mainloop()
print("2")
start_window_loop(window)
