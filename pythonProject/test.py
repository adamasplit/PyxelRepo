import pyxel
import math
import random
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
        self.enemies=[]
        self.clipsizex=200
        self.clipsizey=200
        self.clippos=[MAXWIDTH/2,MAXHEIGHT/2]

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
        if pyxel.btn(pyxel.KEY_J):
            self.enemies.append(Enemy(self,random.randint(0,MAXWIDTH), random.randint(0,MAXHEIGHT)))

    def closeclip(self):
        pass
        '''if self.clipsizex>100:
            self.clipsizex-=(self.clipsizex-100)/100
        if self.clipsizey>100:
            self.clipsizey-=(self.clipsizey-100)/100'''
            
    def deplacementClip(self):
        self.directionclip = [self.position[0] - self.clippos[0], self.position[1] - self.clippos[1]]
        # Normalisation du vecteur direction
        length = math.sqrt(self.directionclip[0] ** 2 + self.directionclip[1] ** 2)
        speed=max(length/20,1)
        if length != 0:
            self.directionclip[0] /= length
            self.directionclip[1] /= length
        # Déplacement vars la cible
        if abs(self.clippos[0]-self.position[0])>5 :
            self.clippos[0] += self.directionclip[0] * speed
        if abs(self.clippos[1]-self.position[1])>5 :
            self.clippos[1] += self.directionclip[1] * speed
    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau

        self.closeclip()
        self.deplacementClip()
        self.vaisseau_deplacement()
        self.tir()
        self.recharge()
        if len(self.projectiles)!=0:
            updateEntities(self.projectiles)
        if len(self.enemies)!=0:
            updateEntities(self.enemies)

    def tir(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.cooldown<=1:
            self.projectiles.append(Projectile(self.position[0], self.position[1]))
            self.cooldown=10

    def get_position(self):
        return self.position


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(1)

        # vaisseau (carre 8x8)
        pyxel.clip(self.clippos[0]-self.clipsizex/2,self.clippos[1]-self.clipsizey/2,self.clipsizex,self.clipsizey)
        pyxel.rectb(self.clippos[0]-self.clipsizex/2-10, self.clippos[1]-self.clipsizey/2-10, self.clipsizex,self.clipsizey, 2)
        pyxel.rect(0, 0, MAXWIDTH, MAXHEIGHT, 13)
        drawEntities(self.projectiles)
        drawEntities(self.enemies)
        drawVaisseau(self.position[0], self.position[1], 40)

class Projectile:
    def __init__(self,x,y):
        self.position = [x,y]
        self.speed=10
        self.target_position=[pyxel.mouse_x,pyxel.mouse_y]
        self.direction = [self.target_position[0] - self.position[0], self.target_position[1] - self.position[1]]
        # Normalisation du vecteur direction
        length = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if length != 0:
            self.direction[0] /= length
            self.direction[1] /= length
        self.cooldown=50
    def projectileDeplacement(self):
        # Déplacement vars la cible
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
    def update(self):
        self.projectileDeplacement()
        self.cooldown-=1

    def draw(self):
        pyxel.circ(self.position[0]+4, self.position[1]+4, 10, 10)

class Enemy:
    def __init__(self,game,x,y):
        self.position = [x,y]
        self.speed=2
        self.game=game
    def EnemyDeplacement(self):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
    def update(self):
        game=self.game
        self.target_position = game.get_position()
        self.direction = [self.target_position[0] - self.position[0], self.target_position[1] - self.position[1]]
        # Normalisation du vecteur direction
        length = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if length != 0:
            self.direction[0] /= length
            self.direction[1] /= length
        self.EnemyDeplacement()
        self.draw()
    def draw(self):
        pyxel.circ(self.position[0], self.position[1], 13, 2)
        

Jeu()




