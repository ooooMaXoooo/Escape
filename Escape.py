import pygame
import math


############################## CLASS #####################################

class Player :     # sa position dans le monde s'affichera dans la loop
    def __init__(self, position, height, width, speed, mass):
        self.posX, self.posY = position
        self.posLvl = [1,5]
        self.height = height
        self.width = width
        self.speed = speed    # en 10px/s
        self.mass = mass
        self.isJumping = False
        self.jumpPos = [] # sert à rien
        self.fluidité = 30   # en IPS
        self.onGround = True
        self.jumpHeight = 50
        self.jumpPower = 10
        self.path = './image/sprite/Augur_Ambros/'

    def move(self, direction):
        print(f"posX : {self.posX}\nposY : {self.posY}")
        if self.posX >= largeur * TILE_SIZE or self.posX < 1:
            print("[Player::actualizePos()] INFO:\t " + str("Can't go there"))
            if self.posX >= largeur * TILE_SIZE :
                self.posX -= 5
            elif self.posX < 1:
                self.posX += 5

        autorized = not isInside((self.posX,self.posY), self.posLvl)

        if direction == 1 and autorized:
            self.posX += self.speed
        if direction == -1 and autorized:
            self.posX -= self.speed

        if self.posX < 1:
            self.posX = 1
        elif self.posX*TILE_SIZE > 8*TILE_SIZE:
            self.posX = 8 * TILE_SIZE

        self.actualizePos()
        print()
        print()

    def jump(self):
        self.isJumping = True
        lenght = 2*math.degrees(math.tan(45*self.speed / self.jumpPower)) * self.jumpHeight
        autorized = True

        while autorized:    # remplir so tableau de pos avec la fonction à sa vitesse
            x = x*lenght / 60
            y = (-4*self.jumpHeight/lenght**2)*(x**2) + (4*self.jumpHeight/lenght)*x

            autorized = not isInside((x,y), self.posLvl) ### détecter si ça touche l'obj de la tile n° ...
            if autorized:
                self.jumpPos.append((self.posX + x, self.posY + y))
                self.posX += x
                self.posY += y
                self.actualizePos()
            else :
                break
        # regarder les colisions
        # arrêter le saut si on rencontre un obstacle


    def actualizePos(self):
        x = self.posX // TILE_SIZE
        y = self.posY // TILE_SIZE

        self.posLvl = [x,y]
        print("[Player::actualizePos()] posLvl:\t " + str(self.posLvl))




class Object:
    def __init__(self, name, position, height, width, imagePath):
        self.name = name
        self.position = position
        self.height = height
        self.width = width
        self.image = imagePath


############################# PHYSIQUE ####################################

def isInside(pos1, worldPos):  # on doit test avec tous les objets de la scène sans le sol --> pas optimal      --> soluc : créer un fichier avec les données de toute la map et le regarder intélligement

    x1, y1 = pos1 # les coordonnées du joueur
    x2 = worldPos[0] * TILE_SIZE
    y2 = worldPos[1] * TILE_SIZE

    sizeX, sizeY = findTileSize(niveau[y2//TILE_SIZE][(x2//TILE_SIZE) - 1])

    if x2 + sizeX <= x1 or x1 <= x2 - player.width: # si il est sur les côtés
        return False
    elif y2 + sizeY <= y1 or y1 <= y2 - player.height: # si il est en haut ou en bas
        return False
    else:  # il est dedans
        return True


def tp(position, object):
    print("tp player")


#########################################################################

def findTileSize(id):
    if 0 <= id >= 20:
        return (64,64)
    return (0,0)


#########################################################################

pygame.init()
pygame.display.set_caption("Escape it !")
font = pygame.font.Font('freesansbold.ttf', 20)


#variables de la jungle
NB_TILES = 20   #nombre de tiles a charger (ici de 00.png à 19.png) 20 au total
TILE_SIZE=64   #definition du dessin (carré) taille de la taille en px

largeur=8       #hauteur du niveau
hauteur=6       #largeur du niveau
tiles=[]       #liste d'images tiles

#variables de gestion du joueur
player = Player((1,5),32,32,5, 5)
compteurBilles=0

#variables de gestion du fantome
FRAMERATE_FANTOME= 120      #vitesse du fantome chiffre elevé = vitesse lente
NB_DEPLACEMENT_FANTOME = 4   #le fantome se deplace sur 9 cases  --> sol à sol+4
positionFantome=1
frameRateCounterFantome=0
posfX=4     #position initiale du fantome
posfY=1
directionF = 1

#definition du niveau les nb coressponde aux nb des tiles

niveau = [
     [-1, -1, -1, -1, -1, -1, -1, -1],
     [8, -1, -1, -1, -1, -1, -1, -1],
     [8, -1, -1, -1, -1, -1, -1, -1],
     [8, -1, -1, -1, -1, -1, -1, -1],
     [8, -1, -1, 3, 4, -1, -1, -1],
     [13, 12, 12, 18, 19, 11, 12, 4]]

fantome=[
     [0,0,0,0,0,0,0,0],
     [0,0,0,4,0,0,0,0],
     [0,0,0,3,0,0,0,0],
     [0,0,0,2,0,0,0,0],
     [0,0,0,1,0,0,0,0],
     [0,0,0,0,0,0,0,0]]


fenetre = pygame.display.set_mode((largeur*TILE_SIZE, (hauteur+1)*TILE_SIZE))

def chargetiles(tiles):
    """
    fonction permettant de charger les images tiles dans une liste tiles[]
    pour l'instant, que dans jungle
    """
    for n in range(NB_TILES):
        tiles.append(pygame.image.load(fr'image/map/Tilemaps/jungle/tile'+str(n)+'.png')) #attention au chemin
        #   U:/Documents/NSI/Mini-Projets/jeuNoel/image/map/Tilemaps/jungle/tile

def afficheNiveau(niveau):
    """
    affiche le niveau a partir de la liste a deux dimensions niveau[][]
    """
    for y in range(hauteur): # changer ça plus tard pour afficher une partie de la map
        for x in range(largeur):
            fenetre.blit(tiles[niveau[y][x]],(x*TILE_SIZE,y*TILE_SIZE))


def afficheJoueur(numero):
    """
    affiche le joueur en position x et y
    """
    x= player.posX
    y = player.posY
    fenetre.blit(pygame.image.load(player.path + "droit1.png"),(x, y)) #  changer tt ça


def afficheScore(score):
    """
    affiche le score
    changer le système de score
    """
    scoreAafficher = font.render(str(score), True, (0, 255, 0))
    fenetre.blit(scoreAafficher,(120,250))

def rechercheFantome(fantome,position): #recherche les coord du fantome dans la liste fantome
    """
    recherche les coordonnées du fantome en fonction du numéro de sa postion dans le parcours
    """
    print(position)                     #la position doit etre dans la liste fantome sinon plantage
    for y in range(hauteur):
        for x in range(largeur):
            if fantome[y][x]==position:
                coodFantome=x,y
    return coodFantome          #les coord du fantome x et y sont dans un tuple coodFantome

def deplaceFantome(fantome):
    """
    Incrémente automatiquement le déplacement du fantome, gère sa vitesse et son affichage
    """
    global frameRateCounterFantome
    global positionFantome
    global posfX,posfY
    global directionF
    if frameRateCounterFantome==FRAMERATE_FANTOME:      #ralenti la viteese du fantome
        posfX,posfY=rechercheFantome(fantome,positionFantome)   #deballage du tuple coordonnées du fantome
        if positionFantome==NB_DEPLACEMENT_FANTOME:     #un tour est fait donc on passe à la 1ere position
            directionF = -1
        if positionFantome == 1:
            directionF = 1

        positionFantome += 1*directionF

        frameRateCounterFantome=0                       #compteur de vitesse à zero
    fenetre.blit(tiles[15],(posfX * TILE_SIZE,posfY * TILE_SIZE)) #affichage du fantome
    frameRateCounterFantome+=1                          #incrémentation du compteur de vitesse






############################## BOUCLE #####################################

chargetiles(tiles)
isDead = False

while not isDead:

    #si on veut détectée une touche est pressée
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDead = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.isJumping == False:
                print("jump")
                player.jump()

    # si on veut détecter quand une touche reste enfoncée
    if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()

        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            print("right")
            player.move(1)

        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            print('left')
            player.move(-1)


    fenetre.fill((0,0,0))   #efface la fenetre
    pygame.display.update() #mets à jour la fentre graphique

    afficheNiveau(niveau)   #affiche le niveau
    afficheJoueur(14)          #affiche le joueur et le score
    deplaceFantome(fantome) #mettre un commentaire pour desactiver le déplacement du fantome
    afficheScore(compteurBilles)

pygame.quit()