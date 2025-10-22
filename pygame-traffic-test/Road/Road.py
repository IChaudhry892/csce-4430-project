from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

class Road(Animatable):
    def __init__(self, x, y, length, image):
        self.x = x
        self.y = y
        self.width = SimulationGraphicConfig.ROAD_WIDTH
        self.length = length
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))