__author__ = 'Sng'

import pygame

class EasyConfigSurface ():

    def rotate (self, *surface):
        rotated = []
        for count in range (1,len(surface),1):
            rotated.append(pygame.transform.rotate (surface[count],surface[0]))
        return rotated
    def resize (self,surface, x,y):
        return pygame.transform.scale (surface, (x,y))
class ImageLoad (object):
    def __init__(self,path):
        self.SubsurfaceList = []
        self.colorKey = '#000000'
        self.loadedSprite = pygame.image.load (path)

    def __autokey (self,key):
        if key == True:
            self.loadedSprite.set_colorkey(self.loadedSprite.get_at((0,0)))
        else:
            self.loadedSprite.set_colorkey (pygame.Color(self.colorKey))


    def autoSplit (self,offsetX,offsetY,border=0, autocolorkey = True):
        x,y = 0,0
        self.__autokey(autocolorkey)
        lstSprites = list()
        for x in range(0+border,self.loadedSprite.get_width (),offsetX):
            for y in range(0+border, self.loadedSprite.get_height(),offsetY):
                rect = pygame.Rect (x,y,offsetX,offsetY)
                self.SubsurfaceList.append(self.loadedSprite.subsurface(rect))
        return self.SubsurfaceList

    def manualSplit (self,strtX,strtY,offsetX,offsetY,autocolorkey = True):
        self.__autokey(autocolorkey)
        rect = pygame.Rect(strtX,strtY, offsetX,offsetY)
        self.SubsurfaceList = [self.loadedSprite.subsurface (rect)]
        return self.SubsurfaceList

    def resize (self,x,y):
        resize = []
        for k in self.SubsurfaceList: resize.append(pygame.transform.scale (k,(x,y)))
        return resize

# Sprite
class Sprt(pygame.sprite.Sprite):
    def __init__(self, **surface):
        super (Sprt, self).__init__()
        self.clips = surface
        self.direction = self.clips.keys()[0]
        self.image = self.clips[self.direction][0]
        self.rect = self.image.get_rect()
        self.clipCounter = 0


# Game object - to create game objects
class GameObject (Sprt):
    def __init__(self, **surface):
        super(GameObject, self).__init__(**surface)

    def warp (self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getcoords (self):
        return self.rect.x, self.rect.y

class Label (GameObject):

    def __init__(self, fname, heigth):
        self.text = ''
        self.color = '#000000'
        self.font = pygame.font.Font (fname,heigth)

    def render (self):
        return self.font.render (self.text, True, pygame.Color(self.color))

class GameElement (GameObject):
    def __init__(self, **surface):
        super (GameElement, self).__init__(**surface)
        self.MoveWhereX, self.MoveWhereY = 0,0

    def moveElement (self, x,y, direction=''):
        self.MoveWhereX, self.MoveWhereY = x,y

        self.rect.x, self.rect.y = self.rect.x+self.MoveWhereX*self.dx,\
                                   self.rect.y+self.MoveWhereY*self.dy
        if self.direction != '':
            self.direction = direction

    def changedirectionvector (self,x,y):
        self.MoveWhereX, self.MoveWhereY = x,y

class AnimateGameElements (GameElement):
    def __init__(self, **surface):
        super(AnimateGameElements, self).__init__(**surface)
        self.dx,self.dy = 3,3
    # Animation (im milisec)
    def animate (self):
        self.image = self.clips[self.direction][self.clipCounter]
        if len(self.clips[self.direction])-1>self.clipCounter:
            self.clipCounter +=1
        else: self.clipCounter = 0

    def collideSprite (self, group, is_live):
        pygame.sprite.spritecollide(self, group, is_live)

    def setSpeed (self, x,y):
        self.dx,self.dy, = x,y
    def getSpeed (self):
        return  self.dx, self.dy

    def update (self):
        self.animate()

class Player (AnimateGameElements):
    def __init__(self, **surface):
        super(AnimateGameElements, self).__init__(**surface)
        self.HP = 10
        self.damage = 1
        self.Lives = 3

class Bullets (AnimateGameElements):
    def __init__(self, **surface):
        super(Bullets, self).__init__(**surface)
        self.damage = 1

    def update (self):
        self.moveElement(self.MoveWhereX,self.MoveWhereY, 'left')

class Monster (Player): #asteroids
    def __init__(self, **surface):

        super(Monster, self).__init__(**surface)
        self.iterate = True

    def getBorderEvent (self,x,y):
        if (self.rect.x < 0):
                self.warp(x-self.rect.x, self.rect.y)
        elif (self.rect.y < 0):
                self.warp( self.rect.x, y-self.rect.y)
        elif (self.rect.x > x):
                self.warp(self.rect.x-x, self.rect.y)
        elif (self.rect.y > y):
                self.warp(self.rect.x, self.rect.y-y)
    def update (self,x,y):
        self.getBorderEvent(x,y)
        self.animate()
        self.moveElement(self.MoveWhereX, self.MoveWhereY, self.direction)


