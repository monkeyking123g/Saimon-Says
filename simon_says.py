import random
from livewires import games, color 

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Colors(games.Sprite):
    """ Creazione di colori random """
  
    COLOR_LIST2 = []
    RED = 1
    BLACK = 2
    YELLOW = 3
    GREEN = 4
    images = {RED  : games.load_image("red.bmp"),
             BLACK : games.load_image("b.bmp"),
             YELLOW : games.load_image("yellow.bmp"),
             GREEN : games.load_image("green.bmp") }

    def __init__(self, x, y, size, game, lifetime):
        super(Colors, self).__init__(
              image = Colors.images[size],
              x = x, y = y)
       
        self.size = size
       
        self.game = game
        # tempo per sopravivenza di colori 50 fps == 1.sec 
        self.lifetime = lifetime

    def update(self):
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.destroy()
      
    def add(self, colors):
        Colors.COLOR_LIST2.append(colors)

    def clears(self,):
        Colors.COLOR_LIST2.clear()
    
    def die(self):
        self.destroy()


class Player(games.Sprite):
    """Creazione Player e keyboard """
    Color = []
    COLOR_LIST = []
    COLOR_DELLY = 20
    image = games.load_image("player.bmp")
    def __init__(self, x, y, game):
        super(Player, self).__init__(image = Player.image, x = x, y = y)
        self.distn = Player.Distanza
        self.collor_wait = 0
        self.color_list = Player.COLOR_LIST
        self.game = game

        
    def update(self):
        # tempo di crezione fra uno colore e l'altro 
        if self.collor_wait > 0:
            self.collor_wait -= 1

        # Creazione di colori con Keyboard 
        if games.keyboard.is_pressed(games.K_r) and self.collor_wait == 0:
            self.sound()
            self.add(Colors.RED)
            self.creazione(color = Colors.RED)
            self.collor_wait = Player.COLOR_DELLY
            
        if games.keyboard.is_pressed(games.K_b) and self.collor_wait == 0:
            self.sound()
            self.add(Colors.BLACK)
            self.creazione(color = Colors.BLACK)
            self.collor_wait = Player.COLOR_DELLY
            
        
        if games.keyboard.is_pressed(games.K_y) and self.collor_wait == 0:
            self.sound()
            self.add(Colors.YELLOW)
            self.creazione(color = Colors.YELLOW)
            self.collor_wait = Player.COLOR_DELLY
            
           
        if games.keyboard.is_pressed(games.K_g) and self.collor_wait == 0:
            self.sound()
            self.add(Colors.GREEN)
            self.creazione(color = Colors.GREEN)
            self.collor_wait = Player.COLOR_DELLY


    def creazione(self, color):
        # distanza fra Sprites 
        self.distn += 55
    
        lifetime = 150000
        
        x = self.x + self.distn 
        y = 400
        
        self.new_color = Colors(x = x, y = y,size = color, game = self, lifetime = lifetime)
        Player.Color.append(self.new_color)
        games.screen.add(self.new_color)
        
        # check list 
        if  self.color_list == Colors.COLOR_LIST2 and len(self.color_list) == len(Colors.COLOR_LIST2):
            self.game.score.value += 10
            self.distn = 0
            self.game.lin = 0
            self.game.level_up()

            # clear color player
            for color in Player.Color:
                color.die()

        # check list  game over
        if self.color_list != Colors.COLOR_LIST2 and len(self.color_list) == len(Colors.COLOR_LIST2):
            self.game.end()


    def add(self, colors):
        # Append color for verific 
        self.color_list.append(colors)
    
    def sound(self):
        # suono per keyboard 
        sound = games.load_sound("vyibor-nujnogo-deystviya.wav")
        sound.play()               
            
class Game(object):

    def __init__(self):
        # level per game
        self.level = 0

        # distanza far sprite
        self.lin = 0

        self.score = games.Text(value = 0,
                                size = 30,
                                color = color.black,
                                top = 5,
                                right = games.screen.width - 10,
                                is_collideable = False)
        games.screen.add(self.score)

    def play(self):
        # mettiamo backgraund 
        white = games.load_image("white1.jpg", transparent = False)
        games.screen.background = white

        # background music
        games.music.load("bk1.mp3")
        games.music.play(-1)
        
        self.player = Player(x = 5, y = 400, game = self)
        games.screen.add(self.player)
        
        self.level_up()

        games.screen.mainloop()
    
    # creazioni colori  e level up 
    def level_up(self):
        self.level += 1
        for i in range(self.level):
            self.lin += 55
            x = 10 + self.lin
            y = 200
            size = random.choice([Colors.RED, Colors.BLACK, Colors.YELLOW, Colors.GREEN])
            self.new_colors = Colors(game = self, x = x, y = y,size = size, lifetime = 300)
            self.new_colors.add(size)
            
            games.screen.add(self.new_colors)
            

            # messagio level up 
            level_message = games.Message(value = "Level " + str(self.level),
                                      size = 40,
                                      color = color.black,
                                      x = games.screen.width/2,
                                      y = games.screen.width/10,
                                      lifetime = 3 * games.screen.fps,
                                      is_collideable = False)
        games.screen.add(level_message)
        
       

    def end(self):
        # messagio di "Game over"
        level_message = games.Message(value = "Game Over",
                                      size = 80,
                                      color = color.red,
                                      x = games.screen.width/2,
                                      y = games.screen.height/2,
                                      lifetime = 5 * games.screen.fps,
                                      after_death = games.screen.quit,
                                      is_collideable = False)
        games.screen.add(level_message)

    
        
        


def main():
    saimon_says = Game()
    saimon_says.play()


# Go
main()