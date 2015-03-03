#Este es un codigo de prueba de
#interpreracion de mapas y tilesets.
import pygame, sys, os, shutil, time, random
from pygame.locals import *

TILESET = 'tileset.txt'
MAP = 'map.txt'

FPS = 32 # frames per second to update the screen
WINWIDTH = 800
WINHEIGHT = 530
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

pygame.init()
FPSCLOCK = pygame.time.Clock()

characterslist = ["misc","characters.txt"]

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (120, 127, 121)
HELL_GRAY = (180, 191, 181)
ORANGE = (230,110,0)
PINK = (255,55,240)

SFONT = pygame.font.Font('misc/bonzai.ttf', 30)
BFONT = pygame.font.Font('misc/bonzai.ttf', 50)

def doClick(title):
    if title == "play":
        select_plyr()
    elif title == "credits":
        creditos()
    elif title == "cancel":
        main()
    else:
        print("Button not defined")

class character():
    def __init__(self,name,image,mug):
        self.name = name
        self.image = image
        self.mug = mug

def get_characters():
    chars = open(os.path.join(*characterslist),"r")
    chars_joined = []
    for char in chars:
        data = char.split(",")[:-1]
        chara = character(data[0],data[1],data[2])
        chars_joined.append(chara)
    return chars_joined

class btn_selector():
    def __init__(self,mug,pos,name="null"):
        self.name = name
        self.mug = mug
        self.pos = pos
    def draw(self):
        b_size = self.mug.get_size()
        b_surface = pygame.Surface((b_size[0]+16, b_size[1]+6))

        m_pos = pygame.mouse.get_pos()
        if m_pos[0] >= self.pos[0] and m_pos[0] <= self.pos[0]+b_size[0]+16 and m_pos[1] >= self.pos[1] and m_pos[1] <= self.pos[1]+b_size[1]+6:
            pygame.draw.rect(b_surface,GRAY,(0,0,b_size[0]+16,b_size[1]+6))
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.pressed = True
                        return b_surface,self.name
        else:
            pygame.draw.rect(b_surface,HELL_GRAY,(0,0,b_size[0]+16,b_size[1]+6))
        b_surface.blit(self.mug,(8,8))
        return b_surface,""

class button():
    def __init__(self,title,pos,size,name="null"):
        self.name = name
        self.title = title
        self.pos = pos
        self.size = size
    def draw(self):
        b_font = pygame.font.Font('misc/bonzai.ttf', self.size)
        b_title = b_font.render(self.title, True, BLACK)
        b_size = b_title.get_size()
        b_surface = pygame.Surface((b_size[0]+16, b_size[1]+6))

        m_pos = pygame.mouse.get_pos()
        if m_pos[0] >= self.pos[0] and m_pos[0] <= self.pos[0]+b_size[0]+16 and m_pos[1] >= self.pos[1] and m_pos[1] <= self.pos[1]+b_size[1]+6:
            pygame.draw.rect(b_surface,GRAY,(0,0,b_size[0]+16,b_size[1]+6))
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.pressed = True
                        return b_surface,self.name
        else:
            pygame.draw.rect(b_surface,HELL_GRAY,(0,0,b_size[0]+16,b_size[1]+6))
        b_surface.blit(b_title,(8,3))
        return b_surface,""

def play(player1, player2):
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    ALPHASURF = DISPLAYSURF.convert_alpha()
    pygame.display.set_caption('Play Gambattle!')
    title = BFONT.render("Créditos", True, BLACK)
    bg = pygame.image.load(os.path.join("backgrounds","restaurant.png"))
    frame = 0
    while 96 > frame:
        frame += 1
        DISPLAYSURF.blit(bg, (0,0))
        if frame < 70:
            b_font = pygame.font.Font('misc/bonzai.ttf', 30)
            b_title = b_font.render("Let's battle!", True, BLACK)
            DISPLAYSURF.blit(b_title,(30,30))
        #Draw players
        DISPLAYSURF.blit(pygame.image.load(os.path.join("characters",player1.image)), (20,300))
        DISPLAYSURF.blit(pygame.transform.flip(pygame.image.load(os.path.join("characters",player2.image)), True, False), (600,300))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    frame = 0

    while True:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(bg, (0,0))
        #Draw players
        DISPLAYSURF.blit(pygame.image.load(os.path.join("characters",player1.image)), (20,300))
        DISPLAYSURF.blit(pygame.transform.flip(pygame.image.load(os.path.join("characters",player2.image)), True, False), (600,300))
        #Draw life bar
        pygame.draw.rect(DISPLAYSURF,BLACK,(100,10,WINWIDTH-200,30))
        pygame.draw.rect(DISPLAYSURF,GREEN,(100,10,(WINWIDTH-200)/2,30))
        pygame.draw.rect(DISPLAYSURF,ORANGE,(100+(WINWIDTH-200)/2,10,(WINWIDTH-200)/2,30))
        #Draw energy bar
        pygame.draw.rect(DISPLAYSURF,PINK,(40,WINHEIGHT-50,120,40))
        pygame.draw.rect(DISPLAYSURF,PINK,(WINWIDTH-160,WINHEIGHT-50,120,40))
        for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    terminate()
        frame += 1
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def select_plyr():
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    ALPHASURF = DISPLAYSURF.convert_alpha()
    pygame.display.set_caption('Play Gambattle!')
    title = BFONT.render("Seleccion de personajes", True, BLACK)
    t_pl1 = SFONT.render("PL1", True, BLUE)
    t_pl2 = SFONT.render("PL2", True, RED)
    characters = get_characters()
    sel_pl1 = True
    sel_pl2 = False
    player1 = characters[0]
    player2 = characters[1]
    buttons = []
    buttons.append(button("Comenzar",(100,460),35,"start"))
    buttons.append(button("Cancelar",(300,460),35,"cancel"))

    buttons.append(button("Jugador 1",(20,90),35,"pl1"))
    buttons.append(button("Jugador 2",(640,90),35,"pl2"))

    buttons_sel = []
    posX = 0
    posY = 0
    column = 0
    row = 1
    for char in characters:
        mug = pygame.image.load(os.path.join("characters",char.mug))
        buttons_sel.append(btn_selector(mug,(160+posX,110*row),char.name))
        posX += 120
        column += 1
        if column >= 4:
            column = 0
            row += 1
            posX = 0

    while True:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(title,(20,20))

        for j in buttons_sel:
            surf,name = j.draw()
            DISPLAYSURF.blit(surf,(j.pos[0],j.pos[1]))
            if name != "":
                if sel_pl1 == True:
                    for char in characters:
                        if name == char.name:
                            player1 = char
                else:
                    for char in characters:
                        if name == char.name:
                            player2 = char

        for i in buttons:
            surf,name = i.draw()
            DISPLAYSURF.blit(surf,(i.pos[0],i.pos[1]))
            if name == "start":
                play(player1,player2)
            elif name=="cancel":
                main()
            elif name=="pl1":
                sel_pl1 = True
                sel_pl2 = False
            elif name == "pl2":
                sel_pl2 = True
                sel_pl1 = False

        posX = 0
        column = 0
        row = 1
        for char in characters:
            if player1.name == char.name:
                DISPLAYSURF.blit(t_pl1,(160+posX,110*row))
            if player2.name == char.name:
                DISPLAYSURF.blit(t_pl2,(220+posX,110*row))
            posX += 120
            column += 1
            if column >= 4:
                column = 0
                row += 1
                posX = 0

        for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def creditos():
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    ALPHASURF = DISPLAYSURF.convert_alpha()
    pygame.display.set_caption('Play Gambattle!')
    title = BFONT.render("Créditos", True, BLACK)
    buttons = []
    buttons.append(button("Cancelar",(300,460),35,"cancel"))
    text1 = SFONT.render("Desarrollador: Polectron.",True,BLACK)
    text2 = SFONT.render("Idea original: Polectron y Ana.",True,BLACK)
    while True:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(title,(20,20))
        DISPLAYSURF.blit(text1,(20,80))
        DISPLAYSURF.blit(text2,(20,110))

        for i in buttons:
            surf,name = i.draw()
            DISPLAYSURF.blit(surf,(i.pos[0],i.pos[1]))
            if name == "cancel":
                main()

        for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main():
    #pygame.display.set_icon(pygame.image.load('gameicon.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    ALPHASURF = DISPLAYSURF.convert_alpha()
    pygame.display.set_caption('Gambattle!')
    title = BFONT.render("Gambattle!", True, BLACK)
    buttons = []
    buttons.append(button("Jugar",(100,460),35,"play"))
    buttons.append(button("Créditos",(300,460),35,"credits"))
    while True:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(title,(20,20))

        for i in buttons:
            surf, name = i.draw()
            DISPLAYSURF.blit(surf,(i.pos[0],i.pos[1]))
            if name == "play":
                select_plyr()
            elif name == "credits":
                creditos()

        for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


