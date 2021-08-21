import  pygame
import time
from random import *
import sqlite3

#couleur fond
blue = (143, 133, 243)
white = (255, 255, 255)

#initialisation pygame
pygame.init()



#base de données //SQL3//
data = "Archives/Data.sq3"
linker = sqlite3.connect(data)
cur = linker.cursor()

#les éléments ci-dessous sont à reactiver en cas de perte du fichier Data.sq3...

##cur.execute("create table member (point integer)")

##cur.execute("insert into member (point) values (0)")
##linker.commit()

##cur.execute("insert into member (point) values (0)")
##linker.commit()



#dimension écran
surfaceW = 800
surfaceH = 500

#dimension joueur
playerW = 120
playerH = 120

#dimension asteroides
asteW = 300
asteH = 300

#surface écran
surface = pygame.display.set_mode((surfaceW, surfaceH))

#nom de fenêtre
pygame.display.set_caption("SpaceRun Alpha 0.1")

#définition de l'horloge
clock = pygame.time.Clock()

#chargement images
img = pygame.image.load('pictures/spaceship.png')
img_asteroide1 = pygame.image.load('pictures/element01.png')
img_asteroide2 = pygame.image.load('pictures/element02.png')

#fonction score
def point(value):

     police = pygame.font.Font('calibri.ttf', 16)
     text = police.render("score :" + str(value), True, white)
     surface.blit(text, [10, 0])

#fonction HightScore
def HPoint(value):

     police = pygame.font.Font('calibri.ttf', 16)
     text = police.render("HPoint :" + str(value), True, white)
     surface.blit(text, [700, 0])

#fonction astéroides
def asteroides(x_aste, y_aste, space) :

    surface.blit(img_asteroide1, (x_aste, y_aste))
    surface.blit(img_asteroide2, (x_aste, y_aste+asteW+space))


#fonction recommencer
def retry() :

    for event in pygame.event.get ([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP :
            continue

        return event.key

#création texte
def creaTextObj(text, police):
    textSurface = police.render(text, True, white)
    return textSurface, textSurface.get_rect()

#affichage des messages
def message (text):

    #paramétrage police
    GOtext = pygame.font.Font('calibri.ttf', 150)
    smalltext = pygame.font.Font('calibri.ttf', 20)

    #création surface Game Over
    GOtextSurf, GOtextRect = creaTextObj(text, GOtext)
    GOtextRect.center = surfaceW/2, ((surfaceH/2)-50)
    surface.blit(GOtextSurf, GOtextRect)

    #création surface Continuer
    smalltextSurf, smalltextRect = creaTextObj("appuyer sur une touche pour continuer", smalltext)
    smalltextRect.center = surfaceW/2, ((surfaceH/2)+50)
    surface.blit(smalltextSurf, smalltextRect)

    #actualisation messages
    pygame.display.update()
    time.sleep(2)

#fonction horloge
    while retry() == None :

        clock.tick()

    main()

#message d'échec
def gameOver(point_add):

   a = [str(point_add)]

   data = "Archives/Data.sq3"
   linker = sqlite3.connect(data)
   cur = linker.cursor()
   cur.execute("select * from member")
   listing = list(cur)

   hpoint = []
   for i in range(0, len(listing)):
    hpoint += listing[i]

    if (int(hpoint[-1]) < point_add):

        cur.execute("insert into member(point) values(?)", a)
        linker.commit()
        cur.close()
        linker.close()



   message("Game Over")


#fonction joueur
def player (x, y, image):
 surface.blit(image, (x, y))

#positionnement elements
def main():
   x = 150
   y = 200

   y_movement = 0

   x_aste = surfaceW
   y_aste = randint(-300, 20)
   space = asteH*0.68
   #vitesse de déplacement asteroides
   aste_speed = 6

   point_add = 0

   Out_game = False

  #fonction sortie
   while not Out_game :
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             Out_game = True

          #evenements touches mouvements
          if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP :
             y_movement = -2
          if event.type == pygame.KEYUP :
             y_movement = 2

       y+= y_movement

       #rafraichissement écran
       surface.fill(blue)

       #appel fonction joueur, asteroides, score
       player(x, y, img)

       asteroides(x_aste, y_aste, space)

       #créer liste hightscore //SQL3//
       cur.execute("select * from member")
       listing = list(cur)
       print(cur)
       print(listing)

       #afficher dernier hightscore //SQL3//
       hpoint = []
       for i in range (0, len(listing)):
           hpoint += listing[i]
       print(hpoint)

       HPoint(hpoint[-1])



       #accumuler les points
       point(point_add)


       #déplacement asteroides
       x_aste -= aste_speed


       #collision bord écran
       if y > surfaceH -40 or y < -10 :
           gameOver(point_add)

       #augmentation de la difficultée
       if 3 <= point_add < 5 :
        aste_speed = 7
        space = playerH*2.8

        if 5 <= point_add < 5 :
         aste_speed = 8
         space = playerH*2.7

       #collisions asteroides
       if x + playerW > x_aste +90 :
        if y < y_aste + asteH -100 :
            if x-playerW < x_aste + asteW -10 :
                gameOver(point_add)

        if x +playerH > x_aste +80:
         if y +playerH > y_aste + asteH + space +80 :
           if x-playerW < x_aste +asteW -10:
              gameOver(point_add)

       #randomiser place asteroides
       if x_aste < (-1*asteW) :
          x_aste = surfaceW
          y_aste = randint(-300, 20)

       #compter les points en fonction du passage
       if x_aste <  (x- asteW) < x_aste + aste_speed :
           point_add += 1

       #actualisation écran
       pygame.display.update()

main()
pygame.quit()
quit()

