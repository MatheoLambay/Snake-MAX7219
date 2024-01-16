from snake import Snake
from machine import Pin, SPI, PWM
from max7219 import Matrix8x8
from ir_rx.nec import NEC_8


spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = Matrix8x8(spi, cs, 1)
display.brightness(1)

pin_ir = Pin(15, Pin.IN)

game = ["snake","space_invader","nothings"]
current_game = None
game_started = 0

snake = Snake(display)

def decodeKeyValue(data):
    tab_code = [0x18,0x08,0x1C,0x5A,64]
    if data in tab_code:
        tab_ar = ["haut","gauche","bas","droite","restart"]
        for i in range(len(tab_ar)):
            if data == tab_code[i]:
                return tab_ar[i]
        return "ERROR"


def callback(data, addr, ctrl):
    global game_started
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        direction = decodeKeyValue(data)  
        if current_game == None:
            selectGame(direction)
        elif current_game == "snake" and game_started:    
            snake.DirectionInterdiction(direction)
            

            
def selectGame(data):
    global current_game, game_started
    if data == 'restart':
        current_game = game[0]
        game_started = 1
    elif data == "droite":
        game.append(game.pop(0))  
    elif data == "gauche":
        game.insert(0,game.pop())   
    display.fill(0)
    if game[0] == 'snake':
        display.text("1",0,0,1)
    elif game[0] == 'space_invader':
        display.text("2",0,0,1)
    elif game[0] == 'nothings':
        display.text("3",0,0,1)
    display.show()
       
ir = NEC_8(pin_ir, callback)  # Instantiate receiver


while True:
    
    if not(snake.vivant):
        current_game = None
        game_started = 0
        snake.reset()
    elif current_game == "snake" and game_started:
        snake.StartGame()   
