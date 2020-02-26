import pygame as p
import random as r
#Initializing
p.init()

playboy = input("Plz enter your name for record pupose ")

#Creating pygame window
win = p.display.set_mode((1280, 720))

font = p.font.SysFont('comicsans', 50)
font1 = p.font.SysFont('comicsans', 100)
clock = p.time.Clock()
run = True
shootloop = 0
enemyloop = 0
rungame = False
score = 0

hitsound = p.mixer.Sound('hit.wav')
music = p.mixer.music.load("stars.mp3")
p.mixer.music.play(-1)

file = open('Scores.txt', 'r')   #file reading fuction
f = file.readlines()

newlist = []

for line in f:
    newlist.append(line.strip())    #coberting file into required list
d = newlist[0].split()
h={}

for i in range(len(d)):
    if i%2==0:
        h[d[i]]=int(d[i+1])

if not(playboy in h):
    h[playboy] = score


#pregame window
prebg = p.image.load('Pregamewin.jpg')
#character image
char = p.image.load('space-invaders.png')
#list of enemy images
enem = p.image.load('M1.png')
#List of background Images
bg = [p.image.load('l1.jpg'), p.image.load('l2.jpg'), p.image.load('l3.jpg'), p.image.load('l4.jpg'), p.image.load('l5.jpg'), p.image.load('l6.jpg'), p.image.load('l7.jpg')]

#main player class
class player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.vel = 10
        self.hitbox = [self.x, self.y, 64, 64]

    def animate(self, win):                    #metod for animating the player
        self.hitbox = [self.x, self.y, 64, 64]
        win.blit(char,(self.x, self.y))


#class for gunshots
class gun():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vel = 8
        self.radius = radius

    def animate(self, win):                                         #method for animating the bullet
        p.draw.circle(win, (0,255,0), (self.x, self.y), self.radius)

#class for enemies
class enemies():
    def __init__(self):
        self.x = r.randint(0, 1216)
        self.y = r.randint(0, 250)
        self.vel = 5
        self.end = r.randint(self.x, 1216)
        self.path = [self.x, self.end]
        self.hitbox = [self.x, self.y, 64, 64]
        self.visible = True

    def animate(self, win):                    #method for animating the enemy
        self.move()
        self.hitbox = [self.x, self.y, 64, 64]
        win.blit(enem, (self.x, self.y))

    def move(self):                   #method for movement of enemy
        if self.vel > 0 :
            if self.x < self.path[1]:
                self.x += self.vel
            else :
                self.vel = self.vel * -1
        else:
            if self.x > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        if self.x == self.path[0] or self.x == self.path[1]:
            self.y += 10

#main display function
def showtime():
    win.blit(bg[x], (0, 0))
    man.animate(win)
    for monster in monsters:
         monster.animate(win)
    for bullet in bullets:
        bullet.animate(win)
    text = font1.render("Score: " + str(score), 1, (0, 155, 0))
    win.blit(text, (950, 10))
    text1 = font1.render('LEVEL: ' + str(level), 1, (0,0,155))
    win.blit(text1, (0, 10))
    text2 = font1.render('LIVES: ' + str(lives), 1, (155, 0, 0))
    win.blit(text2, (0, 80))
    p.display.update()

man = player(620, 650)
monster = enemies()

#list of bullets
bullets = []

#list of enemies
monsters=[]

#main loop
while run:

    if not(rungame):                                                  #starting game function
        s = ''
        for key in h:
            s += str(key) + ' ' + str(h[key]) + ' '

        file = open('Scores.txt', 'w')

        file.write(s)

        file.close()
        maxh = max(h, key=h.get)
        win.blit(prebg, (0, 0))
        text = font1.render('LOST IN SPACE', 1, (255, 5, 25))
        win.blit(text, (420, 0))
        text1 = font1.render('Press SPACE BAR to START',1, (0,0,155))
        win.blit(text1, (220, 65))
        text2 = font.render('Highest Score:-  '+ maxh +': '+ str(h[maxh]), 1, (0,255,0))
        win.blit(text2,(0,650))
        text3 = font.render('Produced by:- RJ ', 1, (0,0,0))
        win.blit(text3, (950, 650))
        p.display.update()
        score = 0
        level = 1
        x = 0
        q = 150
        lives = 3
        for event in p.event.get():  #closing fuction
            if event.type == p.QUIT:
                run = False
        keys = p.key.get_pressed()  # list of inputs
        if keys[p.K_SPACE]:
            rungame = True
            p.time.delay(100)


    if rungame:

        if enemyloop > 0:
            enemyloop +=1  #for interval of enemy
        if enemyloop > q:
            enemyloop = 0

        if shootloop > 0:
            shootloop +=1  #for shooting every bullet distinctly
        if shootloop > 5:
            shootloop = 0

        for event in p.event.get():  #closing fuction
            if event.type == p.QUIT:
                run = False

        if enemyloop == 0:            #multiple enemmies
            enemyloop +=1
            monsters.append(enemies())

        for monster in monsters:                                                                                                          #Elimination of enemies and bullets
            if monster.y > 650:
                lives -= 1
                monsters.pop(monsters.index(monster))
            for bullet in bullets:
                if bullet.y - bullet.radius < monster.hitbox[1] + monster.hitbox[3] and bullet.y + bullet.radius > monster.hitbox[1]:
                    if bullet.x - bullet.radius > monster.hitbox[0] and bullet.x - bullet.radius < monster.hitbox[0] + monster.hitbox[2]:
                        monsters.pop(monsters.index(monster))
                        bullets.pop(bullets.index(bullet))

                        hitsound.play()
                        score +=1

        for bullet in bullets:                  #movement of bullets
            if bullet.y < 720 and bullet.y > 0:
                bullet.y -= bullet.vel
            else :
                bullets.pop(bullets.index(bullet))

        keys = p.key.get_pressed() #list of inputs

        if keys[p.K_LEFT] and man.x - man.vel > 0:           #movemt of player left or right
            man.x -= man.vel
        elif keys[p.K_RIGHT] and man.x + 64 + man.vel < 1280:
            man.x += man.vel

        if keys[p.K_SPACE]:                               #shooting
            if len(bullets) < 5 and shootloop == 0:
                shootloop += 1
                bullets.append(gun(man.x + 32, man.y, 6))

        if score > 5:
            level = 2
        if score > 15:
            level = 3
            monster.vel = 5
        if score > 25:
            level = 4
            monster.vel = 6
        if score > 35:
            level = 5
            monster.vel = 8
        if score > 45:
            level = 6
            monster.vel = 10
        if score > 55:
            level = 7
            monster.vel = 10
        if level == 2:
            x = 1
            q = 125
        if level == 3:
            x = 2
            q = 105
        if level == 4:
            x = 3
            q = 95
        if level == 5:
            x = 4
            q = 75
        if level == 6:
            x = 5
            q = 55
        if level == 7:
            x = 6
            q = 35
        if score > h[playboy]:
            h[playboy] = score
        if lives == 0:
            monsters.clear()
            bullets.clear()
            text = font1.render('GAME OVER',1, (255, 0, 0))
            win.blit(text, (420, 340))
            p.display.update()
            p.time.delay(3000)
            rungame = False

        
        showtime()
        clock.tick(0)
p.quit()