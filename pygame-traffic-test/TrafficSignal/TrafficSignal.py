from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

class TrafficSignal(Animatable):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = SimulationGraphicConfig.TRAFFIC_SIGNAL_WIDTH
        self.height = SimulationGraphicConfig.TRAFFIC_SIGNAL_HEIGHT
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))