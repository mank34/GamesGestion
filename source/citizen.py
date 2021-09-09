from envVar import *


# Class for the tile entity
class citizen(pygame.sprite.Sprite):

    def __init__(self, num, img, w, h, parent=0, name="null"):
        super().__init__()
        
        # Human need
        self.hungry = 0
        self.tired  = 0
        
        self.happy = 100 - self.hungry - self.tired
