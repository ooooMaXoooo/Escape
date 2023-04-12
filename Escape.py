import pygame
import math


############################## CLASS #####################################

class Vector2 :
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.norme = self.norme()

    def norme(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def scalaire(self, vec1, vec2):
        #on est dans un repère orthonormé
        x = vec1.X
        y = vec1.y
        x2 = vec2.x
        y2 = vec2.y

        return x*x2 + y*y2
    
    ## addition/souscraction/
    


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
        self.path = 'sprite/Augur_Ambros/'

    def move(self, direction):
        # regarder si on peut aller dans la direction voulu
        # si on peut on bouge
        # si on peut pas on fait rien ou recule

        autorized = self.isInside((self.posX + self.speed, self.posY), self.posLvl)

        if (autorized):
            if(direction == 1):
                self.posX += self.speed
            elif (direction == -1):
                self.posX -= self.speed
    

        """
        print(f"[Player::move()] INFO:\tposX : {self.posX}\n[Player::move()] INFO:\tposY : {self.posY}")

        if self.posX >= largeur * TILE_SIZE or self.posX < 1:
            print("[Player::move()] INFO:\t" + "Can't go there")

            if self.posX >= largeur * TILE_SIZE :
                self.posX -= 5
                print("[Player::move()] INFO:\t" + "player is at the right border")
                print("[player::move()] INFO:\t" + f"posX : {self.posX}\t\t\tposY : {self.posY}")


            elif self.posX < 1:
                self.posX += 5
                print("[Player::move()] INFO:\t" + "player is at the left border")
                

        autorized = not isInside((self.posX,self.posY), self.posLvl)

        if direction == 1 and autorized:
            self.posX += self.speed
        if direction == -1 and autorized:
            self.posX -= self.speed


        if self.posX < 1:
            self.posX = 1
        elif self.posX*TILE_SIZE > 8*TILE_SIZE:
            self.posX = 8 * TILE_SIZE

        """
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
    print("[TP()]INFO :\ttp player")


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
NB_TILES = 21   #nombre de tiles a charger (ici de 00.png à 19.png) 20 au total
TILE_SIZE=64   #definition du dessin (carré) taille de la taille en px

largeur=8       #hauteur du niveau
hauteur=6       #largeur du niveau
tiles=[]       #liste d'images tiles

#variables de gestion du joueur
player = Player((1,5),32,32,5, 5)

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
    x= player.posX
    y = player.posY
    window.blit(pygame.image.load(player.path + "droit1.png"),(x, y)) #  changer tt ça



############################## BOUCLE #####################################

chargetiles(tiles)
isDead = False

while not isDead:

    #si on veut détectée une touche est pressée un seule fois
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDead = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.isJumping == False:
                print("jump")
                player.jump()


    
    keys=pygame.key.get_pressed()

    move_ticker = 0
    if keys[pygame.K_d]:
        if move_ticker == 0:
            move_ticker = 10
            print("right")
            player.move(1)

    if keys[pygame.K_a]:
        if move_ticker == 0:
            move_ticker = 10
            print('left')
            player.move(-1)
            

    if move_ticker > 0:
        move_ticker -= 1
        print("test")


    window.fill((0,0,0))   #efface la window

    afficheNiveau(niveau)   #affiche le niveau
    afficheJoueur()          #affiche le joueur et le score

    pygame.display.flip() #mets à jour la fentre graphique


pygame.quit()