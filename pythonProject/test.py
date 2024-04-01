import pyxel
import math
MAXWIDTH=1080
MAXHEIGHT=720
def updateEntities(entities):
    for entity in entities:
        entity.update()


def drawEntities(entities):
    for entity in entities:
        entity.draw()

def drawVaisseau(x,y,taille):
    pyxel.tri(x-taille/2,y,x,y+taille,x+taille/2,y,9)

class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(MAXWIDTH, MAXHEIGHT, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.cooldown=0
        self.position=[MAXWIDTH/2,MAXHEIGHT/2]
        self.projectiles=[]

        pyxel.run(self.update, self.draw)

    def recharge(self):
        self.cooldown-=1
    def vaisseau_deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.position[0]<MAXWIDTH:
            self.position[0] += 3
        if pyxel.btn(pyxel.KEY_LEFT) and self.position[0]>0:
            self.position[0] += -3
        if pyxel.btn(pyxel.KEY_DOWN) and self.position[1]<MAXHEIGHT:
            self.position[1] += 3
        if pyxel.btn(pyxel.KEY_UP) and self.position[1]>0:
            self.position[1] += -3


    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        pyxel.clip(pyxel.mouse_x-200,pyxel.mouse_y-200,400,400)
        self.vaisseau_deplacement()
        self.tir()
        self.recharge()
        if len(self.projectiles)!=0:
            updateEntities(self.projectiles)

    def tir(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.cooldown<=1:
            self.projectiles.append(Projectile(self.position[0], self.position[1]))
            self.cooldown=5



    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(1)

        # vaisseau (carre 8x8)
        pyxel.rect(0, 0, MAXWIDTH, MAXHEIGHT, 13)
        drawEntities(self.projectiles)
        drawVaisseau(self.position[0], self.position[1], 20)

class Projectile:
    def __init__(self,x,y):
        self.position = [x,y]
        self.speed=10
        self.target_position=[pyxel.mouse_x,pyxel.mouse_y]
        self.direction = [self.target_position[0] - self.position[0], self.target_position[1] - self.position[1]]
        # Normalize direction vector
        length = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if length != 0:
            self.direction[0] /= length
            self.direction[1] /= length
        self.cooldown=50
    def projectileDeplacement(self):
        # Move towards target
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
    def update(self):
        self.projectileDeplacement()
        self.cooldown-=1

    def draw(self):
        pyxel.circ(self.position[0]+4, self.position[1]+4, 10, 10)


Jeu()




