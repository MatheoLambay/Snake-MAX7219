from machine import Pin, SPI, PWM
import max7219
from random import randint
from time import sleep
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8


spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(1)

pin_ir = Pin(15, Pin.IN)

buzzer = PWM(Pin(16))
buzzer.freq(500)

apple_x = 1
apple_y = 1
player_x = 0
player_y = 0
direction = "droite"
last_direction = "droite"
interdiction = "gauche"
vivant = 1
taille = [[None,None,"droite"],[None,None,"droite"],[0,0,"droite"]]
score = 0


def decodeKeyValue(data):
    tab_code = [0x18,0x08,0x1C,0x5A,64]
    if data in tab_code:
        tab_ar = ["haut","gauche","bas","droite","restart"]
        for i in range(len(tab_ar)):
            if data == tab_code[i]:
                return tab_ar[i]
        return "ERROR"


def callback(data, addr, ctrl):
    global direction,last_direction,interdiction
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        direction = decodeKeyValue(data)    
        if direction == interdiction or direction == None:
            direction = last_direction
        elif direction == "restart" and vivant == 0:
            reset()
        else:
            last_direction = direction
        
       
ir = NEC_8(pin_ir, callback)  # Instantiate receiver
# ir.error_function(print_error)  # Show debug information

def playerPosition():
    global player_x,player_y,apple_x,apple_y,taille,vivant,score
    for i in range(len(taille)):
        try:
            display.pixel(taille[i][0],taille[i][1],1) 
        except:
            pass
    for coord in taille[0:-1]:
        if coord[0] == taille[-1][0] and coord[1] == taille[-1 ][1]:
            vivant = 0
            for i in range(3):
                playerDeath()          
    if player_x == apple_x and player_y == apple_y:
        score += 1
        newApple()
        newPlayer()
        
def playerMouvement(direction):
    global player_x,player_y,taille,interdiction
    
    if direction == "haut" and player_y > 0 :
        player_y -= 1
        interdiction = "bas"
    elif direction == "bas" and player_y < 7 :
        player_y += 1
        interdiction = "haut"
    elif direction == "gauche" and player_x > 0:
        player_x -= 1
        interdiction = "droite"   
    elif direction == "droite" and player_x < 7:
        player_x += 1   
        interdiction = "gauche"
    elif direction == "haut" and player_y == 0:
        player_y = 7
    elif direction == "bas" and player_y == 7:
        player_y = 0
    elif direction == "gauche" and player_x == 0:
        player_x = 7
    elif direction == "droite" and player_x == 7:
        player_x = 0
    
    for i in range(0,len(taille)-1):
        taille[i][0] = taille[i+1][0]
        taille[i][1] = taille[i+1][1]
        taille[i][2] = taille[i+1][2]
    taille[-1] = [player_x,player_y,direction]

def newPlayer():
    global taille
    taille.insert(0,[None,None,"droite"])

def newApple():
    global apple_x,apple_y,taille
    while True:
        x = randint(0,7)
        y = randint(0,7)
        for i in taille:
            if i[0] == x and i[1] == y:
                break
        else:
            apple_x = x
            apple_y = y
            break
        
        
    
def applePosition():
    global apple_x,apple_y
    display.pixel(apple_x,apple_y,1)

def playerDeath():
    display.fill(0)
    display.show()
    sleep(0.5)
    for i in range(len(taille)):
        try:
            display.pixel(taille[i][0],taille[i][1],1) 
        except:
            pass
    display.show()
    sleep(0.5)
    
def scoreNote():
    global score
    note = ["F","E","D","C",'B',"A","S"]
    point = [2,4,6,8,10,12,14]
    for i in range(7):
        if score <= point[i]:
            return note[i]
        elif score > max(point):
            return note[-1]
            
def reset():
    global apple_x,apple_y,player_x,player_y,direction,last_direction,interdiction,vivant,taille,score
    apple_x = 1
    apple_y = 1
    player_x = 0
    player_y = 0
    direction = "droite"
    last_direction = "droite"
    interdiction = "gauche"
    vivant = 1
    taille = [[None,None,"droite"],[None,None,"droite"],[0,0,"droite"]]
    score = 0
    

newApple()
try:
    while True:
        while vivant:
            display.fill(0)
            applePosition()
            playerMouvement(direction)
            playerPosition()
            display.show()
            sleep(0.5)
        note = scoreNote()
        display.fill(0)
        display.text(note,0,0,1)
        display.show()                  
except KeyboardInterrupt:
    ir.close()