from AsteroidsCore import *
import random
def spriteGroup(*lst):
    return pygame.sprite.Group (*lst)


GameColors = ({
            'black':'#000000',
            'white':'#ffffff',
            'red'  :'#ff0000',
            'green':'#00ff00',
            'blue' :'#0000ff'
            })

gameover = ImageLoad ('Dead.png')
GameOverSprt = GameObject(end=[EasyConfigSurface().resize(gameover.loadedSprite,640,480)])
GGameOver = pygame.sprite.Group ()
GGameOver.add (GameOverSprt)

Planets = ImageLoad ('Planets.png')
PlanetList = []
PlanetList.append (Planets.manualSplit(0,0,160,166))
PlanetList.append(Planets.manualSplit(160,0,160,158))
PlanetList.append(Planets.manualSplit(160+160,0,170,166))
PlanetList.append(Planets.manualSplit(160+160+172,0,180,160))
PlanetList.append(Planets.manualSplit(160+160+170+180,0,166,164))
PlanetList.append(Planets.manualSplit(160+160+170+180+166,0,157,157))

Gplanet = pygame.sprite.Group ()
PlanetSprite = AnimateGameElements (Planet = random.choice(PlanetList))
PlanetSprite.warp(random.randint (100,640), random.randint (0,480))
Gplanet.add(PlanetSprite)

starz = ImageLoad ('stars.png')
manuallist = []
for index in range(0,48,16): #sprites
    manuallist.append(starz.manualSplit(index,0,16,14)[0])

Gstars = pygame.sprite.Group ()
for i in range(0,100,1):
    choiced = []
    for randomstars in range(0,len(manuallist),1):
        choiced.append(random.choice (manuallist))
    StarsSprite = AnimateGameElements (Glow = choiced)
    StarsSprite.warp(random.randint (0,640), random.randint (0,480))
    Gstars.add (StarsSprite)



dogyclip = ImageLoad ('Animal2.png')
dogyclip=dogyclip.autoSplit(40,40, autocolorkey=True)
playerone = Player \
                    (right= [dogyclip[2],dogyclip[6],dogyclip[10]],
                     up   = [dogyclip[3],dogyclip[7],dogyclip[11]],
                     down = [dogyclip[0],dogyclip[4],dogyclip[8]],
                     left = [dogyclip[1],dogyclip[5],dogyclip[9]])

playerone.setSpeed(2,2)
playerone.warp(150,150)
GPlayerone = spriteGroup(playerone)

AsteroidSprite= ImageLoad ('asteroid3.png') #Big Asteroid
Asteroidclip = AsteroidSprite.autoSplit(32,32)
rotatedanim  =  [Asteroidclip[0],Asteroidclip[4], Asteroidclip[8],Asteroidclip[12],Asteroidclip[16]]

blastSprite = ImageLoad ('Blast.png')
blastSprite = blastSprite.autoSplit(100,100)
blastlist = []
for count in range(32,45,1):
    resized = EasyConfigSurface().resize (blastSprite[count], 32,32)
    blastlist.append(resized)

GAsteroidz = pygame.sprite.Group()
for cout in range(0,20,1):
    Ast = Monster (rotate = rotatedanim,
                   zap = blastlist) #Sprite for rotation animation Asteroid
    Ast.direction = 'rotate'
    Ast.setSpeed(random.randint(0,5),random.randint(0,5)) #SpeedAsteriod If moved
    Ast.warp(random.randint(10,600),random.randint(10,400)) #StartPos Asteroid
    Ast.changedirectionvector(random.randint(-1,1),random.randint(-1,1)) #Move Asteroid
    GAsteroidz.add (Ast) #Get Group

GBullet = pygame.sprite.Group ()
BulletPic = ImageLoad('Bulletz.png').manualSplit(0,0,9,12)


pygame.init()
screen = pygame.display.set_mode ([640,480])
FPS = pygame.time

lives = Label ('Data 70 LET.ttf', 30)
lives.text = 'Lives: '+ str (playerone.Lives)
lives.color = GameColors['green']

playerScore = 0
score = Label ('Data 70 LET.ttf', 28)
score.text = 'Score: '+ str (playerScore)
score.color = GameColors['green']

WinText = Label ('Data 70 LET.ttf', 50)
WinText.text = 'You win! Game loose. ' \
               'End.'
WinText.color = GameColors['green']

playeroneanimationEvent = pygame.USEREVENT
FPS.set_timer (playeroneanimationEvent ,60)
FPS.set_timer (playeroneanimationEvent+1, 750)

ifmainwindowclose = False
counter = False

def keys ():
    keys =  pygame.key.get_pressed()
    if keys [pygame.K_RIGHT] and keys[pygame.K_UP]:
        playerone.moveElement(1,-1, 'right')
    elif keys [pygame.K_LEFT] and keys[pygame.K_UP]:
        playerone.moveElement(-1,-1, 'left')
    elif keys [pygame.K_LEFT] and keys[pygame.K_DOWN]:
        playerone.moveElement(-1,1, 'left')
    elif keys [pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        playerone.moveElement(1,1, 'right')

    elif keys[pygame.K_UP]:
        playerone.moveElement(0,-1,'up')

    elif keys[pygame.K_DOWN]:
        playerone.moveElement(0,1, 'down')

    elif keys [pygame.K_LEFT]:
        playerone.moveElement(-1,0,'left')

    elif keys [pygame.K_RIGHT]:
        playerone.moveElement(1,0, 'right')

    if not (keys [pygame.K_RIGHT])and  \
       not (keys[pygame.K_LEFT])  and  \
       not (keys[pygame.K_DOWN])  and  \
       not (keys[pygame.K_UP]):
           playerone.image = playerone.clips[playerone.direction][0]


while not ifmainwindowclose:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            ifmainwindowclose = True

        if event.type == playeroneanimationEvent:
            playerone.animate()
            GAsteroidz.update(640,480)

        if event.type == playeroneanimationEvent+1:
            Gstars.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if len(GBullet) < 3:
                    BulletSprt = Bullets (left=BulletPic)
                    BulletSprt.warp(playerone.rect.x, playerone.rect.y)
                    BulletSprt.setSpeed (5,5)
                    GBullet.add (BulletSprt)
                    BulletSprt.warp(playerone.rect.x+12, playerone.rect.y+12)
                    BulletSprt.MoveWhereX, BulletSprt.MoveWhereY = playerone.MoveWhereX, playerone.MoveWhereY
    keys()
    GBullet.update()

    screen.fill (pygame.Color(GameColors['black']))
    collide = pygame.sprite.spritecollide(playerone, GAsteroidz, False)
    if len(collide) !=0:
            if collide[0].direction != 'zap':
                playerone.Lives -=1
            scorePlayer = 0
            collide[0].moveElement (0,0, 'zap')
            lives.text = 'Lives: ' + str(playerone.Lives)

    for bullet in GBullet:
        bul = pygame.sprite.spritecollide(bullet, GAsteroidz, False)
        if len(bul) !=0: #hit# !
            GBullet.remove (bullet)
            bul[0].moveElement (0,0, 'zap')
            playerScore +=10
            score.text = 'Score: ' + str(playerScore)
            smalize = []
            for sprt in rotatedanim:
                    smalize.append(EasyConfigSurface().resize(sprt,10,10))
            if bul [0].iterate == True:
                for number in range (0,3,1):
                    SS = Monster (rotate = smalize, zap = blastlist)
                    SS.setSpeed(random.randint(0,5),random.randint(0,5)) #SpeedAsteriod If moved
                    SS.warp(bul[0].rect.x, bul[0].rect.y) #StartPos Asteroid
                    SS.changedirectionvector(random.randint(-1,1),random.randint(-1,1)) #Move Asteroid
                    SS.iterate =False
                    GAsteroidz.add (SS)

    if playerone.Lives <= 0:
        lives.text = 'GAME OVER!'
        GGameOver.draw (screen)
    elif len (GAsteroidz) == 0:
        screen.blit (WinText.render(), (75,220))
    else:
        for bullet in GBullet:
            if bullet.rect.x < -10 or bullet.rect.x > 650:
                GBullet.remove(bullet)
            elif bullet.rect.y < -10 or bullet.rect.y > 490:
                GBullet.remove (bullet)
        for asteroid in GAsteroidz:
            if asteroid.direction == 'zap':
                #There live
                if len (asteroid.clips[asteroid.direction])-1 == asteroid.clipCounter: GAsteroidz.remove (asteroid)
        Gstars.draw (screen)
        Gplanet.draw (screen)
        GAsteroidz.draw (screen)
        GBullet.draw (screen)
        GPlayerone.draw(screen)

    screen.blit (lives.render(), (10,10))
    screen.blit (score.render(), (10,35))

    FPS.Clock().tick (40)
    pygame.display.flip()
pygame.quit()