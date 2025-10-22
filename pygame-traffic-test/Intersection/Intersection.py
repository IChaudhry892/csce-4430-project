from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

class Intersection(Animatable):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = SimulationGraphicConfig.ROAD_WIDTH
        self.height = SimulationGraphicConfig.ROAD_WIDTH
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))