import pygame, sys, random
from pygame.locals import *
import time

WINDOWWIDTH = 400
WINDOWHEIGHT = 600
# Bird
BIRDWIDTH = 60
BIRDHEIGHT = 45
G = 0.5
SPEEDFLY = -8
BIRDIMG = pygame.image.load("img\Khoi.jpg")
BACKGROUND = pygame.image.load(r"img\background.png")
# Columns
COLUMNWIDTH = 60
COLUMNHEIGHT = 500
BLANK = 200
DISTANCE = 200
COLUMNSPEED = 2
COLUMNIMG = pygame.image.load('img\column.png')

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird')

class Bird():
    def __init__(self):
        self.width = BIRDWIDTH
        self.height = BIRDHEIGHT
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
        self.speed = 0
        self.suface = BIRDIMG
        self.suface1 = self.suface

    def draw(self, t):
        """if self.speed <= 0:
            self.suface1 = pygame.transform.rotate(self.suface, 15)
        elif self.speed >= 10:
            self.suface1 = pygame.transform.rotate(self.suface, -15) """
        self.suface1 = pygame.transform.rotate(self.suface, t)
        self.x, self.y = self.x , self.y
        DISPLAYSURF.blit(self.suface1, (int(self.x), int(self.y)))

    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G
        if mouseClick == True:
            self.speed = SPEEDFLY



class Columns():
    def __init__(self):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMNSPEED
        self.surface = COLUMNIMG
        self.ls = []
        for i in range(3):
            x = WINDOWWIDTH + i*self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 20)
            self.ls.append([x, y])

    def draw(self):
        for i in range(3):
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))

    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        if self.ls[0][0] < -self.width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 10)
            self.ls.append([x, y])

class Score():
    def __init__(self):
        self.score = 0
        self.addScore = True

    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        scoreSuface = font.render(str(self.score), True, (0, 0, 0))
        textSize = scoreSuface.get_size()
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))

    def update(self, bird, columns):
        collision = False
        for i in range(3):
            rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
            rectBird = [bird.x, bird.y, bird.width, bird.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
            self.addScore = False
        else:
            self.addScore = True

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(bird, columns):
    for i in range(3):
        rectBird = [bird.x, bird.y, bird.width, bird.height]
        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            return True
    if bird.y + bird.height < 0 or bird.y + bird.height > WINDOWHEIGHT:
        return True
    return False

def gamePlay(bird, columns, score):
    bird.__init__()
    bird.speed = SPEEDFLY
    columns.__init__()
    score.__init__()
    count = 0
    t = 0
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        columns.update()
        bird.draw(t)
        t = t - 10
        if t == -180:
            t = 0
        bird.update(mouseClick)
        score.draw()
        score.update(bird, columns)

        if isGameOver(bird, columns) == True:
            return

        pygame.display.update()
        fpsClock.tick(FPS)

def gameStart(bird):
    bird.__init__()

    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('FLAPPY BIRD', True, (255, 0, 0))
    headingSize = headingSuface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Click to start', True, (0, 0, 0))
    commentSize = commentSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                return

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        bird.draw(0)
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))

        pygame.display.update()
        fpsClock.tick(FPS)

def gameOver(bird, columns, score):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
    commentSize = commentSuface.get_size()

    font = pygame.font.SysFont('consolas', 30)
    scoreSuface = font.render('Score: ' + str(score.score), True, (0, 0, 0))
    scoreSize = scoreSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    return

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        bird.draw(0)
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))

        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    bird = Bird()
    columns = Columns()
    score = Score()
    while True:
        gameStart(bird)
        gamePlay(bird, columns, score)
        gameOver(bird, columns, score)

if __name__ == '__main__':
    main()
