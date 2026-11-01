import arcade as aa
from pyglet.media import Player, load, StaticSource
import time

screen_width = 1280
screen_height = 720

class IO(aa.View):
    def __init__(self):
        super().__init__()
        self.mb = aa.Sprite()
        self.bg = aa.Sprite()
        self.start_mb = False
        self.over_mb = True
        
    def in_out(self, c_view, start1, start2, over1, over2):
        # start代表结束时启用，over代表开始时启用，下同；1代表蒙版效果，2代表放大-缩小效果
        if start1:
            if self.start_mb:
                self.mb.alpha += 3
                if self.mb.alpha >= 205:
                    self.window.show_view(c_view)
                    self.start_mb = False

        elif start2:
            if self.start_mb:
                self.bg.scale += 0.01
                if self.bg.scale == 3:
                    self.start_mb = False
                    self.window.show_view(c_view)
                    
        if over1:
            if self.over_mb:
                self.mb.alpha -= 3
                if self.mb.alpha == 0:
                    self.over_mb = False
    
        elif over2:
            if self.over_mb:
                self.bg.scale -= 0.01
                if self.bg.scale == 2:
                    self.over_mb = False

class Start(IO):
    def __init__(self):
        super().__init__()
        self.mb = aa.Sprite('images/mb.jpg', scale=3)
        self.mb.position = 640, 360
        self.bg = aa.Sprite('images/bg1.jpg', scale=1.5)
        self.bg.position = 640, 360
        self.sb = aa.Sprite('images/start.png')
        self.sb.position = 640, 200
        self.gc = aa.Sprite('images/正侧面.png')
        self.gc.position = 200, 200
        self.jz = aa.Sprite('images/卷轴1.png', scale=3)
        self.jz.position = 1770, 320
        self.start_mb = False
        self.over_mb = False
        self.left = False
        self.mb.alpha = 0
        
        self.bgm_player = Player()
        self.bgm_player.queue(load('files/古风bgm.mp3'))
        self.bgm_player.loop = True
        self.bgm_player.play()

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.sb.draw()
        self.gc.draw()
        aa.draw_text("Jili Guche", 640, 480, aa.color.BLACK, 90, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("Reading China", 640, 320, aa.color.BLACK, 40, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        self.jz.draw()
        aa.draw_text("The Jili Drum Car, an ingenious ancient Chinese odometer, ", self.jz.center_x, 450, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("originated from the Qin and Han dynasties. It arose to meet", self.jz.center_x, 410, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("It arose to meet governance needs like road mileage", self.jz.center_x, 370, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("measurement for network management and post ", self.jz.center_x, 330, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("efficiency, relying on mature gear technology. ", self.jz.center_x, 290, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("It beat a drum every li and a bell every ten li,", self.jz.center_x, 250, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("serving both practical use and imperial ceremonial display.", self.jz.center_x, 210, aa.color.BLACK, 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        self.mb.draw()
    
    def on_update(self, time):
        self.in_out(main, True, False, False, False)
        self.lefting()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.sb.collides_with_point((x, y)):
            self.left = True
            
        if self.jz.collides_with_point((x, y)):
            self.start_mb = True

    def lefting(self):
        if self.left:
            self.jz.center_x -= 5
            if self.jz.center_x <= 640:
                self.center_x = self.jz.center_x = 640
                self.left = False

class Main(IO):
    def __init__(self):
        super().__init__()
        self.mb = aa.Sprite('images/mb.jpg', scale=3)
        self.mb.position = 640, 360
        self.bg = aa.Sprite('images/bg2.jpg')
        self.bg.position = 1200, 360
        self.gc = aa.Sprite('images/侧面.png', scale=2)
        self.gc.position = 500, 500
        self.lz = aa.Sprite('images/轮子.png', scale=0.9)
        self.lz.position = 360, 120
        self.move = aa.Sprite('images/箭头.png', scale=2)
        self.move.position = 1100, 360
        self.jz = aa.Sprite('images/卷轴2.png', scale=1)
        self.jz.position = 300, 1100
        self.stt = aa.Sprite('images/stt.png', scale=1)
        self.stt.position = 300, 1100
        self.continue_button = aa.Sprite('images/返回.png', scale=2)
        self.continue_button.position = 1100, 100
        
        self.start_mb = False
        self.over_mb = True
        self.left = False
        self.right = False
        self.mb.alpha = 255
        self.moved = 0
        self.moving = False
        self.moved_time = 0

        self.drum_sound = aa.load_sound('files/鼓.mp3')
        self.bell_sound = aa.load_sound('files/锣.mp3')

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.gc.draw()
        self.lz.draw()
        self.move.draw()
        if self.moved < 1:
            aa.draw_text(f"Traveled : {round(self.moved, 1)} li", 1000, 600, aa.color.BLACK, 50, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        else:
            aa.draw_text(f"Traveled : {int(self.moved)} li", 1000, 600, aa.color.BLACK, 50, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        self.jz.draw()
        self.stt.draw()
        self.mb.draw()
        self.continue_button.draw()
            
    def on_update(self, time):
        self.in_out(cause, True, False, True, False)
        self.righting()
        self.lzz()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.continue_button.collides_with_point((x, y)):
            self.start_mb = True
            
        if self.jz.collides_with_point((x, y)) and self.jz.center_y > 1000:
            self.right = True
            
        if self.jz.collides_with_point((x, y)) and self.jz.center_y < 400:
            self.left = True

        if self.move.collides_with_point((x, y)) and self.moved < 1:
            self.moved += 0.1
            self.moved = round(self.moved, 1)
            self.moving = True
            if self.moved == 1:
                self.drum_sound.play()
        elif self.move.collides_with_point((x, y)):
            self.moved += 1
            self.moving = True
            self.drum_sound.play()
            if self.moved % 10 == 0:
                self.bell_sound.play()

    def lzz(self):
        if self.moving:
            self.move_time = time.time()
            self.lz.angle -= 5
            if self.lz.angle <= -360:
                self.lz.angle = 0
                self.moving = False

    def righting(self):
        if self.right:
            self.jz.center_y -= 5
            self.stt.center_y -= 5
            if self.jz.center_y <= 360:
                self.center_y = self.jz.center_y = 360
                self.stt.change_y = 0
                self.right = False

        elif self.left:
            self.jz.center_y += 5
            self.stt.center_y += 5
            if self.jz.center_y >= 1100:
                self.center_y = self.jz.center_y = 1100
                self.stt.change_y = 0
                self.left = False

class Cause(IO):
    def __init__(self):
        super().__init__()
        self.mb = aa.Sprite('images/mb.jpg', scale=3)
        self.mb.position = 640, 360
        self.bg = aa.Sprite('images/bg3.jpg', scale=1.5)
        self.bg.position = 640, 360
        self.jz = aa.Sprite('images/卷轴1.png', scale=3)
        self.jz.position = 640, 360
        self.continue_button = aa.Sprite('images/返回.png', scale=2)
        self.continue_button.position = 1100, 80
        self.move = aa.Sprite('images/箭头.png', scale=2)
        self.move.position = 900, 80
        
        self.start_mb = False
        self.over_mb = True
        self.left = False
        self.right = False
        self.mb.alpha = 255

        self.story = False
        self.cause = True
        self.alpha1 = 255
        self.alpha2 = 0
        self.djcs = False

    def on_draw(self):
        self.bg.draw()
        self.jz.draw()
        self.continue_button.draw()
        self.move.draw()
        
        aa.draw_text('Conclusion', 1000, 670, (0, 0, 0, self.alpha1), 50, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('The Jili Ancient Chariot is amazing! ', 660, 510, (0, 0, 0, self.alpha1), 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('It’s an old Chinese cart with wooden figures.  ', 660, 460, (0, 0, 0, self.alpha1), 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('When it goes one "li",', 660, 410, (0, 0, 0, self.alpha1), 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('a figure hits a drum. It uses simple gears,', 660, 360, (0, 0, 0, self.alpha1), 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('just like today’s car odometers. ', 660, 310, (0, 0, 0, self.alpha1), 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('It shows how clever ancient Chinese people were', 660, 260, (0, 0, 0, self.alpha1), 20, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')

        aa.draw_text('Story——The fire fold', 900, 670, (0, 0, 0, self.alpha2), 50, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('The fire fold, an ancient fire preservation tool,', 660, 510, (0, 0, 0, self.alpha2), 20, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('is created by soaking paper or mugwort', 660, 460, (0, 0, 0, self.alpha2), 20, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('in nitrate solution and sealing it in a container', 660, 410, (0, 0, 0, self.alpha2), 20, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('while smoldering. When needed, ', 660, 360, (0, 0, 0, self.alpha2), 20, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('blowing on it provides oxygen to produce', 660, 310, (0, 0, 0, self.alpha2), 20, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('nstant flame, enabling portable fire.', 660, 260, (0, 0, 0, self.alpha2), 20, 
                     font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
                
        self.mb.draw()        

    def on_update(self, time):
        self.in_out(result, True, False, True, False)
        self.control()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.continue_button.collides_with_point((x, y)):
            self.start_mb = True
      
        if self.move.collides_with_point((x, y)) and not self.djcs:
            self.cause = False
            self.djcs = True

    def control(self):
        if not self.cause:
            self.alpha1 -= 3
            if self.alpha1 == 0:
                self.alpha1 = 0
                self.cause = True
                self.story = True

        if self.story:
            self.alpha2 += 3
            if self.alpha2 == 255:
                self.alpha2 = 255
                self.story = False

class Result(IO):
    def __init__(self):
        super().__init__()
        self.y = 0
        
    def on_draw(self):
        self.clear()
        self.y += 1
        
        aa.draw_text('Thank You for Whatching', 640, self.y, color=aa.color.WHITE, font_size=50, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("That's All", 640, self.y - 200, color=aa.color.WHITE, font_size=40, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Development Team 开发团队', 640, self.y - 400, color=aa.color.WHITE, font_size=40, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Director 总监 : Demo', 640, self.y - 500, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Programmer 程序员 : Demo', 640, self.y - 580, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Artist 美术设计 : Doubao AI    Deepseek', 640, self.y - 660, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Music 音乐 : 酷我音乐', 640, self.y - 740, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Contents 内容与设计', 640, self.y - 820, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Participant_002    Participant_003    Participant_005', 640, self.y - 900, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Participant_006    Participant_007', 640, self.y - 980, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')

w = aa.Window(screen_width, screen_height, 'Jili Guche')
start = Start()
main = Main()
cause = Cause()
result = Result()
w.show_view(start)
w.run()
