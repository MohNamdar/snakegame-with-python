import time
import keyboard
import os
from termcolor import colored
from random import randint


# get keyboard input in certain time
def get_user_input(timeout):
    start_time = time.time()
    user_input = None

    def on_key_event(e):
        nonlocal user_input
        user_input = e.name

    keyboard.hook(on_key_event)

    while True:
        if user_input is not None or time.time() - start_time > timeout:
            break

    keyboard.unhook_all()

    return user_input


# print the field
def print_field():
    for cell in cells:
        if cell in snake_body:
            print(colored('X', 'green'), end='')
        elif cell[0] in (0, FIELD_WIDTH - 1) or cell[1] in (0, FIELD_HEIGHT - 1):
            print(colored('#', 'blue'), end='')
        elif cell == apple_pos:
            print(colored('a', 'red'), end='')

        else:
            print(' ', end='')

        if cell[0] == FIELD_WIDTH - 1:
            print()


# update the snake body position
def update_snake():
    global eaten
    new_head = snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]
    snake_body.insert(0, new_head)
    if not eaten:
        snake_body.pop(-1)
    eaten = False


# update the apple (eaten or not)
def apple_collision():
    global apple_pos, eaten, score
    if apple_pos == snake_body[0]:
        apple_pos = place_apple()
        score += 1
        eaten = True


# generate a new place for apples
def place_apple():
    row = randint(1, FIELD_HEIGHT - 2)
    col = randint(1, FIELD_WIDTH - 2)
    while (col, row) in snake_body:
        row = randint(1, FIELD_HEIGHT - 2)
        col = randint(1, FIELD_WIDTH - 2)

    return (col, row)


# settings
FIELD_WIDTH = 32
FIELD_HEIGHT = 16
cells = [(col, row) for row in range(FIELD_HEIGHT) for col in range(FIELD_WIDTH)]
eaten = False
score = 0

# snake
snake_body = [(5, FIELD_HEIGHT // 2), (4, FIELD_HEIGHT // 2), (3, FIELD_HEIGHT // 2)]
DIRECTION = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
direction = DIRECTION['right']

# apple
apple_pos = place_apple()

while True:

    # clear the page
    os.system('cls')

    # field printing
    print_field()
    print('\nyour score:', score)

    # get direction
    key_pressed = get_user_input(timeout=0.3)
    match (key_pressed):
        case 'w':
            direction = DIRECTION['up']
        case 's':
            direction = DIRECTION['down']
        case 'a':
            direction = DIRECTION['left']
        case 'd':
            direction = DIRECTION['right']
        case 'esc':
            os.system('cls')
            break

    # updating the game
    update_snake()

    # check apples are eaten or not
    apple_collision()

    # check death
    if (snake_body[0] in snake_body[1:] or snake_body[0][0] in (0, FIELD_WIDTH - 1) or \
            snake_body[0][1] in (0, FIELD_HEIGHT - 1)):
        os.system('cls')
        print('Game Over!!')
        print('your score:', score)
        break
