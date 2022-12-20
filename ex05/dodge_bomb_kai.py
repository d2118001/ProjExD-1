import pygame as pg
import sys, random
import tkinter as tk
import tkinter.messagebox as tkm


bombs = []
vxs = []
vys = []


class Screen:
    def __init__(self, title, screen, bg_img):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(screen)
        self.rct = self.sfc.get_rect()
        self.image = pg.image.load(bg_img)


class Bird(pg.sprite.Sprite):
    key_delta = {pg.K_w:[0, -5], pg.K_s:[0, +5], 
    pg.K_a:[-5, 0], pg.K_d:[+5, 0]}

    def __init__(self, imgname, scale, cord):
        super().__init__()
        self.image = pg.image.load(imgname)
        self.image = pg.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.center = cord
    
    def update(self, screen: Screen):
        key_state = pg.key.get_pressed()
        for key, delta in self.key_delta.items():
            if key_state[key] == 1:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
                if check_bound(self.rect, screen.rct) != (1, 1): # 練習7
                    self.rect.centerx -= delta[0]

    def attack(self):
        return Bullet(self)


class Bomb(pg.sprite.Sprite):
    def __init__(self, color, size, vxy, scr: Screen):
        super().__init__()
        self.image = pg.Surface((2*size, 2*size)) # Surface
        self.image.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.image, color, (size, size), size)
        self.rect = self.image.get_rect() # Rect
        self.rect.centerx = random.randint(0, scr.rct.width)
        self.rect.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6
    
    def update(self, scr: Screen):
        # 練習6
        self.rect.move_ip(self.vx, self.vy)
        # 練習7
        yoko, tate = check_bound(self.rect, scr.rct)
        self.vx *= yoko
        self.vy *= tate   
        # 練習5
        #self.blit(scr)

class Bullet:
    def __init__(self, tori: Bird):
        size = 15
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, "Blue", (size, size), size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = tori.rect.centerx
        self.rct.centery = tori.rect.centery
        self.vx, self.vy = (20,20) # 練習6

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, 0)
        self.blit(scr)
        if check_bound(self.rct, scr.rct) != (1, 1): # 練習7
            del self

def makebomb(sc_rect:pg.Rect):
    global bombs, vxs, vys
    colors = ["red", "green", "blue", "yellow", "magenta"]
    bomb = pg.Surface((20, 20))
    bomb.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb, colors[random.randint(0,len(colors)-1)],(10,10), 10)
    bomb_rect = bomb.get_rect()
    bomb_rect.centerx = random.randint(0, sc_rect.width)
    bomb_rect.centery = random.randint(0, sc_rect.height)
    bombs.append((bomb, bomb_rect))
    vxs.append(random.choice([-1, +1]))
    vys.append(random.choice([-1, +1]))


def main():
    clock = pg.time.Clock()

    screen = Screen("逃げろ！こうかとん", (1600, 900), "fig/pg_bg.jpg")
    screen.sfc.blit(screen.image,(0,0))

    tori = pg.sprite.Group()
    tori.add(Bird("fig/6.png", 2.0, (900, 400)))
    tori.draw(screen.sfc)

    bomb = pg.sprite.Group()
    colors = ["red", "green", "blue", "yellow", "magenta"]
    for _ in range(5):
        bomb.add(Bomb(colors[random.randint(0,len(colors)-1)], 10, (random.choice([-1, +1]),random.choice([-1, +1])), screen))
    bomb.draw(screen.sfc)
    font = pg.font.SysFont("メイリオUI", 80)
    print(font)
    beam = None
    while(True):
        screen.sfc.blit(screen.image,(0, 0))
        txt = font.render(f"{int(pg.time.get_ticks()/1000)}秒", True, "WHITE")
        screen.sfc.blit(txt, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beam = tori.attack()

        if isinstance(beam, Bullet):
            beam.update(screen)
        tori.update(screen)
        tori.draw(screen.sfc)
        bomb.update(screen)
        bomb.draw(screen.sfc)

        if len(pg.sprite.groupcollide(tori, bomb, False, False)) != 0:
            tkm.showinfo("ゲームオーバー", f"{int(pg.time.get_ticks()/1000)}秒")
            return

        pg.display.update()
        clock.tick(1000)


def check_bound(rect:pg.Rect, screen:pg.Rect): # 範囲内：+1／範囲外：-1
    x, y = +1, +1
    if rect.left < screen.left or screen.right  < rect.right :
        x = -1
    if rect.top  < screen.top  or screen.bottom < rect.bottom:
        y = -1
    return x, y


if __name__ =="__main__":
    pg.init()
    root = tk.Tk()
    root.withdraw()
    main()
    pg.quit()
    sys.exit()
