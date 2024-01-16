from random import randint
from time import sleep


class Snake:
    def __init__(self,display):
        self.display = display
        self.apple_x = 0
        self.apple_y = 0
        self.player_x = 0
        self.player_y = 0
        self.direction = "droite"
        self.last_direction = "droite"
        self.interdiction = "gauche"
        self.vivant = 1
        self.taille = [[None,None,"droite"],[None,None,"droite"],[0,0,"droite"]]
        self.score = 0
        
    def playerPosition(self):
        for i in range(len(self.taille)):
            try:
                self.display.pixel(self.taille[i][0],self.taille[i][1],1) 
            except:
                pass
        for coord in self.taille[0:-1]:
            if coord[0] == self.taille[-1][0] and coord[1] == self.taille[-1][1]:
                self.vivant = 0
                for i in range(3):
                    self.playerDeath()          
        if self.player_x == self.apple_x and self.player_y == self.apple_y:
            self.score += 1
            self.newApple()
            self.taille.insert(0,[None,None,"droite"])
            
    def playerMouvement(self):
        if self.direction == "haut" and self.player_y > 0 :
            self.player_y -= 1
            self.interdiction = "bas"
        elif self.direction == "bas" and self.player_y < 7 :
            self.player_y += 1
            self.interdiction = "haut"
        elif self.direction == "gauche" and self.player_x > 0:
            self.player_x -= 1
            self.interdiction = "droite"   
        elif self.direction == "droite" and self.player_x < 7:
            self.player_x += 1   
            self.interdiction = "gauche"
        elif self.direction == "haut" and self.player_y == 0:
            self.player_y = 7
        elif self.direction == "bas" and self.player_y == 7:
            self.player_y = 0
        elif self.direction == "gauche" and self.player_x == 0:
            self.player_x = 7
        elif self.direction == "droite" and self.player_x == 7:
            self.player_x = 0
        
        for i in range(0,len(self.taille)-1):
            self.taille[i][0] = self.taille[i+1][0]
            self.taille[i][1] = self.taille[i+1][1]
            self.taille[i][2] = self.taille[i+1][2]
        self.taille[-1] = [self.player_x,self.player_y,self.direction]

    def newApple(self):
        while True:
            x = randint(0,7)
            y = randint(0,7)
            for i in self.taille:
                if i[0] == x and i[1] == y:
                    break
            else:
                self.apple_x = x
                self.apple_y = y
                break
            
    def applePosition(self):
        self.display.pixel(self.apple_x,self.apple_y,1)

    def playerDeath(self):
        self.display.fill(0)
        self.display.show()
        sleep(0.5)
        for i in range(len(self.taille)):
            try:
                self.display.pixel(self.taille[i][0],self.taille[i][1],1) 
            except:
                pass
        self.display.show()
        sleep(0.5)
        
    def scoreNote(self):
        note = ["F","E","D","C",'B',"A","S"]
        point = [2,4,6,8,10,12,14]
        for i in range(7):
            if self.score <= point[i]:
                return note[i]
            elif self.score > max(point):
                return note[-1]
                
    def reset(self):
        self.apple_x = 1
        self.apple_y = 1
        self.player_x = 0
        self.player_y = 0
        self.direction = "droite"
        self.last_direction = "droite"
        self.interdiction = "gauche"
        self.vivant = 1
        self.taille = [[None,None,"droite"],[None,None,"droite"],[0,0,"droite"]]
        self.score = 0

    def DirectionInterdiction(self,data):
        self.direction = data
        if self.direction == self.interdiction or self.direction == None:
            self.direction = self.last_direction
        # elif self.direction == "restart" and self.vivant == 0:
        #     self.reset()
        else:
            self.last_direction = self.direction

    def StartGame(self):
        self.newApple()
        while self.vivant:
            self.display.fill(0)
            self.applePosition()
            self.playerMouvement()
            self.playerPosition()
            self.display.show()
            sleep(0.5)
        note = self.scoreNote()
        self.display.fill(0)
        self.display.text(note,0,0,1)
        self.display.show()
        
        
