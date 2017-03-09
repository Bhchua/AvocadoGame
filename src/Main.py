try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import time

current_time = time.time()*1000
last_pressed = current_time+100

#CONSTANTS
WIDTH = 1280
HEIGHT = 720
REFRESH = 60
#SPRITE CONSTANTS
SP_SIZE = [64, 64]
SP_CENTER = [32, 32]


#IMAGES
test_player_image = simplegui._load_local_image("sprite.png")
test_wall_image = simplegui._load_local_image("block.png")
#VARIABLES


# ----------------------------------------------------------------------------------------------------------
# BUTTON INPUT
# ----------------------------------------------------------------------------------------------------------

class Key:
    def __init__(self, key_name, action):
        self.name = key_name
        self.pressed = False
        self.inp = action

    def check_down(self, key_code):
        if key_code == simplegui.KEY_MAP[self.name]:
            self.pressed = True

    def check_up(self, key_code):
        if key_code == simplegui.KEY_MAP[self.name]:
            self.pressed = False

keys = [Key('a', "1l"),
        Key('d', "1r"),
        Key('w', "1j"),
        Key('left', "2l"),
        Key('right', "2r"),
        Key('up', "2j")]

def key_down(key_code):
    for k in keys:
        k.check_down(key_code)

def key_up(key_code):
    for k in keys:
        k.check_up(key_code)

# ----------------------------------------------------------------------------------------------------------
# MOUSE INPUT
# ----------------------------------------------------------------------------------------------------------

mouse_click_pos = (0,0)
mouse_click = False
def mouse_handler(position):
    global mouse_click_pos, mouse_click
    mouse_click = True
    mouse_click_pos = position

# ----------------------------------------------------------------------------------------------------------
# PLAYER
# ----------------------------------------------------------------------------------------------------------

class Player:
    def __init__(self, player_num, x, y, width, height, acc, max_speed):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.width = width
        self.height =  height
        self.max_speed = max_speed
        self.acc = acc
        self.cur_speed = 0
        self.grav = 0.2
        self.in_col = False
        self.in_air = True
        self.on_ground = False

    def draw(self, canvas):
        global wall_array
        global test_player_image
        canvas.draw_image(test_player_image, SP_CENTER, SP_SIZE, (self.x, self.y), SP_SIZE)
        self.control()
        self.collision(wall_array)


    def detect_collision(self, x, y, w, h):
        if ((x + w/2 >= self.x + self.width >= x - w/2) and (y + h/2 >= self.y + self.height >= y - h/2)):
            self.in_col = True
        else:
            self.in_col = False

    def collision(self, wall_list):
        if(self.y_vel != 0):
            self.in_air = True

        wall_x = 0 
        wall_y = 0
        wall_w = 0
        wall_h = 0
        for wall in wall_list:
            self.detect_collision(wall.x, wall.y, wall.width, wall.height)
            if (self.in_col):
                wall_x = wall.x
                wall_y = wall.y
                wall_w = wall.width
                wall.h = wall.height
                break

        if (self.in_air):
            if (self.in_col):
                self.in_air = False
                self.on_ground = True
                self.y_vel = 0
                self.y = wall_y - 2*self.height

        if (wall_x - (0.5 * wall_w) < self.x < wall_x + (0.5 * wall_w)):
            pass
        else:
            self.on_ground = False

        if (not self.on_ground):
            self.y_vel += self.grav
            self.y += self.y_vel

    def control(self):
        last_pressed = 0
        for k in keys:
            if k.pressed:
                i=0
                if k.inp == "1l":
                    self.accelerate(-1)
                    last_pressed = time.time() * 1000
                elif k.inp == "1r":
                    self.accelerate(1)
                    last_pressed = time.time() * 1000
            else:
                if(last_pressed + 100 < time.time()*1000):
                    self.decelerate()

            self.x += self.x_vel

    def accelerate(self, move):
        self.x_vel += self.acc*move
        if self.x_vel > self.max_speed:
            self.x_vel = self.max_speed
        elif self.x_vel < -self.max_speed:
            self.x_vel = -self.max_speed


    def decelerate(self):
        if self.x_vel < 0:
            self.x_vel += self.acc / 2
        elif self.x_vel > 0:
            self.x_vel += -self.acc / 2
        if(-self.acc/3 < self.x_vel < self.acc/3):
            self.x_vel = 0

# ----------------------------------------------------------------------------------------------------------
# GENERIC WALLS
# ----------------------------------------------------------------------------------------------------------

class Wall():
    #This is a "wall" object that acts like a tile
    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite

    def draw(self, canvas):
        canvas.draw_image(self.sprite,
                          (self.width/2, self.height/2),
                          (self.width, self.height),
                          (self.x, self.y),
                          (self.width, self.height))




# ----------------------------------------------------------------------------------------------------------
# GAME AND GAME RULES
# ----------------------------------------------------------------------------------------------------------
player_one = Player(1, WIDTH/2, HEIGHT/2, 32, 32, 0.2, 1.5)

wall_array = []
for i in range(0, int(WIDTH/64)-7):
    wall_array.append(Wall(i*64, HEIGHT, 64, 64, test_wall_image))

for i in range(0, 6):
    wall_array.append(Wall(i*64, HEIGHT/2, 64, 64, test_wall_image))

for i in range(0, 6):
    wall_array.append(Wall(WIDTH-(i*64), HEIGHT/2, 64, 64, test_wall_image))


class Game:

    def __init__(self):
        self.game_speed = 1

    def draw(self, canvas):
        player_one.draw(canvas)
        for wall in wall_array:
            wall.draw(canvas)

# ----------------------------------------------------------------------------------------------------------
# MAIN DISPLAY
# ----------------------------------------------------------------------------------------------------------
new_game = Game()
def display(canvas):
    new_game.draw(canvas)

# ----------------------------------------------------------------------------------------------------------
# SIMPLE GUI FRAME
# ----------------------------------------------------------------------------------------------------------

frame = simplegui.create_frame('PyPong', WIDTH, HEIGHT)

frame.set_canvas_background('rgb(12,50,120)')
frame._display_fps_average = True
frame.set_draw_handler(display)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_handler)

frame.start()

