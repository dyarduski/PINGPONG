
import sys
sys.path.append(r"venv\Lib\site-packages")
from collide import *
import pyglet
from pyglet.window import key
import random
import time

WIDTH,HEIGHT = 1100,500
window = pyglet.window.Window(WIDTH,HEIGHT,resizable = False)
keys = key.KeyStateHandler()
window.push_handlers(keys)

class PingPongball:
    def __init__(self,Imagepath,x,y):
        self.image = pyglet.image.load(Imagepath)
        self.x = x
        self.y = y
        self.velocity_x = 5
        self.velocity_y = random.randint(-5,5)
        self.ball = pyglet.sprite.Sprite(img=self.image,x=self.x,y=self.y)
        self.ball.scale = 0.8
        self.collision = SpriteCollision(self.ball)
    def draw(self,x,y):
        self.ball.x = x
        self.ball.y = y
        self.ball.draw()
    def inverse(self):
        self.velocity_x *=-1
        self.velocity_y *=-1
    def check_bounds(self):
        if self.y >= HEIGHT-2-self.image.height:
            self.y -= 5
            self.velocity_y = -self.velocity_y
        if self.y < 5:
            self.y += 5
            self.velocity_y = abs(self.velocity_y)
        if self.x > WIDTH-2-self.image.width:
            player1.score += 1
            self.x = WIDTH//2
            self.y = HEIGHT//2
            self.velocity_x = 5
            self.velocity_y = random.randint(1,5)
        if self.x < 2:
            player2.score += 1
            self.x = WIDTH//2
            self.y = HEIGHT//2
            self.velocity_x = 5
            self.velocity_y = random.randint(-5,-1)
    def detect_collision(self,obj=None):
        l1x = obj.x
        l1y = obj.y
        r1x = obj.x + obj.image.width
        r1y = obj.y + obj.image.height
        l2x = self.x
        l2y = self.y
        r2x = self.x + self.image.width
        r2y = self.y + self.image.height
        if collide(self.collision,obj.collision):
            self.inverse()
        # if (l2x > l1x and l2x < r1x) and (l2y > l1y and l2y < r1y):
        #     self.inverse()
        # elif (l2x > l1x and l2x < r1x) and (l2y+self.image.height > l1y and l2y+self.image.height < r1y):
        #     self.inverse()
        # if (r2x > l1x and r2x < r1x) and (r2y > l1y and r2y < r1y):
        #     self.inverse()
        # elif (r2x > l1x and r2x < r1x) and (r2y+self.image.height > l1y and r2y+self.image.height < r1y):
        #     self.inverse()
        

class PlatForm:
    def __init__(self,Imagepath,x,y) -> None:
        self.image = pyglet.image.load(Imagepath)
        self.x = x
        self.y = y
        self.score = 0
        self.paddle = pyglet.sprite.Sprite(img=self.image,x=self.x,y=self.y)
        self.collision = SpriteCollision(self.paddle)
    def draw(self,x,y):
        self.paddle.x = x
        self.paddle.y = y
        self.paddle.draw()
    def check_bounds(self):
        if self.y > (HEIGHT-2) - self.paddle.height:
            return False,True
        if self.y <= 2:
            return True,False
        return True,True

score = pyglet.text.Label('Hello, world',
                          font_name='Arial black',
                          font_size=36,
                          x=WIDTH//2, y=10,
                         )


player2 = PlatForm(r"Paddle.png",1100-40,250)
player1 = PlatForm(r"Paddle.png",abs(40-player2.image.width),250)
ballsprite = PingPongball(r"Ball.png",WIDTH//2,HEIGHT//2)

vel = 3.5
timeforchange = time.time()
def is_clicking(_):
    global timeforchange
    ballsprite.check_bounds()
    ballsprite.detect_collision(player1)
    ballsprite.detect_collision(player2)
    if abs(timeforchange - time.time()) > 3:
        timeforchange = time.time()
        ballsprite.velocity_x *= 1.1
        ballsprite.velocity_y *= 1.1
    ballsprite.x += ballsprite.velocity_x
    ballsprite.y += ballsprite.velocity_y
    # print(ballsprite.velocity_y)
    if keys[key.A] and player1.check_bounds()[0] == True:
        player1.y += vel
    elif keys[key.D] and player1.check_bounds()[1] == True:
        player1.y -= vel
    if keys[key.LEFT] and player2.check_bounds()[0] == True:
        player2.y += vel
    elif keys[key.RIGHT] and player2.check_bounds()[1] == True:
        player2.y -= vel

    
    


# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

@window.event
def on_draw():
    window.clear()
    score.text = f"{player1.score} : {player2.score}"
    score.draw()
    player1.draw(player1.x,player1.y)
    player2.draw(player2.x,player2.y)
    ballsprite.draw(ballsprite.x,ballsprite.y)



pyglet.clock.schedule_interval(is_clicking, 1/120.0)
pyglet.app.run()
