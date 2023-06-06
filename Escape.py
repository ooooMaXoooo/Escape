import pygame
import math


############################## CLASS #####################################

class Vector2 :
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norme(self):
        return math.sqrt(self.x**2 + self.y**2)

    def scalaire(self, vec2):
        #on est dans un repère orthonormé
        x = self.X
        y = self.y
        x2 = vec2.x
        y2 = vec2.y

        return x*x2 + y*y2

    def add(self, vec):
        self.x += vec.x
        self.y += vec.y

    def substract(self, vec):
        self.x -= vec.x
        self.y -= vec.y

    ## addition/souscraction/



class Player :     # sa position dans le monde s'affichera dans la loop
    def __init__(self, position, size, speed, mass):
        self.posX = position[1] * TILE_SIZE
        self.posY = position[0] * TILE_SIZE
        self.posLvl = [self.posY//TILE_SIZE, self.posX//TILE_SIZE]  #   [y, x]
        self.size = size
        self.direction = Vector2(0, 0)    # en 10px/s
        self.speed = speed
        self.mass = mass
        self.isJumping = False
        self.fluidité = 30   # en IPS
        self.onGround = True
        self.jumpHeight = 50
        self.jumpPower = 50
        self.path = 'sprite/Augur_Ambros/'
        self.falling = [False, False] # double boolean to detect if it's a real fall
        self.canMove = True
        self.acceleration = 0


    def move(self, direction):
        # regarder si on peut aller dans la direction voulu (et pas en l'air)
        # si on peut on bouge
        # si on peut pas on fait rien ou recule


        #inside = self.isInside()


        if(self.onGround and self.canMove):

            if(direction == 1):
                self.direction.x = self.speed

            elif (direction == -1):
                self.direction.x = -self.speed

            elif(direction == 0):
                self.direction.x = 0

    def jump(self):
        # on regarde si on est sur le sol
        if(self.onGround):
            # si on l'est, on applique une force
            self.direction.add(Vector2(0, -self.jumpPower)) # - jumpPower àcause du repere
            self.isJumping = True
            self.onGround = False
            print("jump")



    def actualizePos(self):

        if(not self.falling[0]):
            self.falling[0] = True
            self.falling[1] = False
            self.acceleration = 0
        else :
            if(not self.falling[1]):
                self.falling[1] = True

        #actualiser la pos
        self.posX += self.direction.x * self.speed

        if(self.falling[0] and self.falling[1]):
            self.acceleration += self.direction.y / self.mass
            self.posY += self.direction.y + self.acceleration
        else:
            self.posY += self.direction.y


        #gérer la gravité
        self.direction.y = GRAVITY


        # gérer les collisions
        collide = self.isInside()



        # actualiser la posLvl

        x = int(self.posX // TILE_SIZE)
        y = int(self.posY // TILE_SIZE)

        self.posLvl = [y,x]
        #print("[Player::actualizePos()] posLvl:\t " + str(self.posLvl))


    def isInside(self):  # on doit test avec tous les objets de la scène sans le sol --> pas optimal      --> soluc : créer un fichier avec les données de toute la map et le regarder intélligement
        inside = False
        
        up = False
        side = 1  ## 1, 0 or -1
        watch = []

        # the origin is at top left corner
        if(self.direction.y < 0):
            #print("regarder ceux du haut")
            up = True
        # else: # up is already at false


        if(self.direction.x > 0):
            #print("regarder ceux de la droite")
            side = 1
        elif self.direction.x == 0:
            #print("ne pas regarder sur les técos")
            side = 0
        else:
            #print("regarder ceux de la gauche")
            side = -1

        """

        1 2 3
        8 p 4
        7 6 5

        """

        if(up and side == 1):
            watch = [2, 3, 4]
        elif(up and side == 0):
            watch = [1, 2, 3]
        elif(up and side == -1):
            watch = [1, 2, 8]

        elif(not up and side == 1):
            watch = [4, 5, 6]
        elif(not up and side == 0):
            watch = [5, 6, 7]
        elif(not up and side == -1):
            watch = [6, 7, 8]

        for pos in watch:
            tempPos = pos
            if(pos < 4):
                if(pos == 2):
                    pos = 0
                elif(pos == 1):
                    pos = -1
                else :
                     pos = 1

                x2 = (self.posLvl[1] + pos) * TILE_SIZE
                y2 = (self.posLvl[0] - 1) * TILE_SIZE # error when posLvl == 0

                """
                print("***1***")
                print("x2 :", self.posLvl[1] + pos)
                print("y2 :", self.posLvl[0] - 1)
                print("pos :", pos)
                print()
                """

                if(self.posLvl[1] + pos > 7):
                    pos = 0
                elif(self.posLvl[1] + pos < 0):
                    pos = 0

                if(niveau[self.posLvl[0] - 1][self.posLvl[1] + pos] == 20):
                    continue


            elif pos == 4:
                x2 = (self.posLvl[1] + 1) * TILE_SIZE
                y2 = self.posLvl[0] * TILE_SIZE
                """
                print("***2***")
                print("x2 :", self.posLvl[1] + 1)
                print("y2 :", self.posLvl[0])
                print("pos :", pos)
                print()
                """

                if(self.posLvl[1] + 1 > 7):
                    self.posLvl[1] -= 1
                elif(self.posLvl[1] + 1 < 0):
                    self.posLvl[1] += 1

                if(niveau[self.posLvl[0]][self.posLvl[1] + 1] == 20):
                    continue


            elif pos < 8 :
                if(pos == 7):
                    pos = -1
                elif(pos == 6):
                    pos = 0
                else: #pos == 5
                    pos = 1

                x2 = (self.posLvl[1] + pos) * TILE_SIZE
                y2 = (self.posLvl[0] + 1) * TILE_SIZE # error when posLvl == max
                """
                print("***3***")
                print("x2 :", self.posLvl[1] + pos)
                print("y2 :", self.posLvl[0] + 1)
                print("pos :", pos)
                print()
                """

                if(self.posLvl[1] + pos > 7):
                    pos = 0
                elif(self.posLvl[1] + pos < 0):
                    pos = 0

                if(self.posLvl[0] == hauteur):
                    self.posLvl[0] = hauteur - 1

                if(niveau[self.posLvl[0] + 1][self.posLvl[1] + pos] == 20):
                    continue


            else:
                x2 = (self.posLvl[1] - 1) * TILE_SIZE
                y2 = self.posLvl[0] * TILE_SIZE
                """
                print("***4***")
                print("x2 :", self.posLvl[1] - 1)
                print("y2 :", self.posLvl[0])
                print("pos :", pos)
                print()
                """

                if(self.posLvl[1] - 1 > 7):
                    self.posLvl[1] += 1
                elif(self.posLvl[1] - 1 < 0):
                    self.posLvl[1] += 1

                if(niveau[self.posLvl[0]][self.posLvl[1] - 1] == 20):
                    continue




            horizontal = x2 + TILE_SIZE <= self.posX or x2 >= self.posX + self.size
            vertical = y2 + TILE_SIZE <= self.posY or y2 >= self.posY + self.size

            if(horizontal): # il est sur les técos
                continue

            if(vertical): #il est en haut ou en bas
                continue

            # uniquement si on touche une tile*
            touch = False



            if(4 < tempPos < 8): # on touche le sol
                ## ajout de isJumping ?
                self.onGround = True
                self.direction.substract(Vector2(0, GRAVITY))
                if(self.isJumping or (self.falling[0] and self.falling[1])):
                    self.isJumping = False
                    self.direction.x = 0
                self.falling = [False, False]

            elif 2 < tempPos < 6:
                self.direction.x = -self.speed
                print("touch right")
                self.canMove = False
                touch = True

            elif 1 == tempPos or tempPos > 6:
                self.direction.x = self.speed
                print("touch left")
                self.canMove = False
                touch = True
            
            if(not self.canMove and not touch):
                self.canMove = True


            inside = True

        if not inside:
            self.onGround = False
            return False
        return True




############################# PHYSIQUE ####################################


def tp(position, object):
    print("[TP()]INFO :\ttp player")

GRAVITY = 0.25  # m/s²


#########################################################################

pygame.init()
pygame.display.set_caption("Escape it !")
font = pygame.font.Font('freesansbold.ttf', 20)


#variables de la jungle
NB_TILES = 21   #nombre de tiles a charger (ici de 00.png à 19.png) 20 au total
TILE_SIZE=64   #definition du dessin (carré) taille de la taille en px

largeur=8       #hauteur du niveau
hauteur=6       #largeur du niveau
tiles=[]       #liste d'images tiles

#variables de gestion du joueur
player = Player((0,0),32,1, 10)
counterMovement = 1  # 1 --> 4
right = True

#definition du niveau les nb coressponde aux nb des tiles

niveau = [
     [20, 20, 20, 20, 20, 20, 20, 20],
     [8, 20, 20, 20, 20, 20, 20, 20],
     [8, 20, 20, 20, 20, 20, 20, 20],
     [8, 20, 20, 20, 20, 20, 20, 20],
     [8, 20, 20, 3, 4, 20, 20, 20],
     [13, 12, 12, 18, 19, 11, 12, 4]]


window = pygame.display.set_mode((largeur*TILE_SIZE, hauteur*TILE_SIZE), pygame.DOUBLEBUF, 32)

def chargetiles(tiles):
    """
    fonction permettant de charger les images tiles dans une liste tiles[]
    pour l'instant, que dans jungle
    """
    for n in range(NB_TILES):
        tiles.append(pygame.image.load(fr'Tilemaps/jungle/tile'+str(n)+'.png')) #attention au chemin
        #   U:/Documents/NSI/Mini-Projets/jeuNoel/image/map/Tilemaps/jungle/tile

def afficheNiveau(niveau):
    """
    affiche le niveau a partir de la liste a deux dimensions niveau[][]
    """
    bck = pygame.image.load("backgrounds/jungle.png")
    window.blit(bck, (0,0))
    for y in range(hauteur): # changer ça plus tard pour afficher une partie de la map
        for x in range(largeur):
            window.blit(tiles[niveau[y][x]],(x*TILE_SIZE,y*TILE_SIZE))


def afficheJoueur():
    """
    affiche le joueur en position x et y
    """
    x = player.posX
    y = player.posY

    global right

    if(player.direction.x > 0):
        window.blit(pygame.image.load(player.path + "droit" + str(counterMovement) + ".png"),(x, y)) #  changer tt ça
        right = True
    elif(player.direction.x < 0):
        window.blit(pygame.image.load(player.path + "gauche" + str(counterMovement) + ".png"),(x, y)) #  changer tt ça
        right = False
    else:
        if(right):
            window.blit(pygame.image.load(player.path + "droit" + str(counterMovement) + ".png"),(x, y))
        else:
            window.blit(pygame.image.load(player.path + "gauche" + str(counterMovement) + ".png"),(x, y)) 



############################## BOUCLE #####################################

moveBefore = False

chargetiles(tiles)
isDead = False

while not isDead:

    #si on veut détectée une touche est pressée un seule fois
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDead = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.isJumping == False:
                player.jump()
        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_d or event.key == pygame.K_q:
              player.move(0)
              

    if (player.direction.x == 0):
        counterMovement = 1


    keys = pygame.key.get_pressed()

    move_ticker = 0
    if keys[pygame.K_d]:
        if move_ticker == 0:
            move_ticker = 100
            counterMovement += 1

            if counterMovement > 4:
                counterMovement = 1
            player.move(1)

    if keys[pygame.K_q]:
        if move_ticker == 0:
            move_ticker = 100

            counterMovement += 1

            if counterMovement > 4:
                counterMovement = 1
            player.move(-1)


    if move_ticker > 0:
        move_ticker -= 1



    player.actualizePos()


    window.fill((0,0,0))   #efface la window

    afficheNiveau(niveau)   #affiche le niveau
    afficheJoueur()          #affiche le joueur et le score

    pygame.display.flip() #mets à jour la fentre graphique


pygame.quit()