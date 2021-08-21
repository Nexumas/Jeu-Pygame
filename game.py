import pygame

#couleur fond
blue = (143, 133, 243)
white = (255, 255, 255)

#initialisation pygame
pygame.init()

#taille fenêtre
surfaceW = 800
surfaceH = 500

#taille joueur
playerH = 120
playerW = 120

#surface de la fenêtre
surface = pygame.display.set_mode((surfaceW, surfaceH))

#nom fenêtre
pygame.display.set_caption("Game")

#chargement images
img = pygame.image.load('images/spaceship.png')

#fonction du joueur
def player (x, y, image):
 surface.blit(image, (x, y))

#positionnement elements
def main():

        x = 150
        y = 200

        y_movement = 0





    #fonction de sortie
Out_game = False

while not Out_game :

         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    Out_game = True

            if event.type == pygame.KEYDOWN :
                   if event.key == pygame.K_UP :
                      y_movement = -5


            if event.type == pygame.K_UP :
                        y_movement = 5

                        y+= y_movement


main()
pygame.quit()
quit()