from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

class Road(Animatable):
    def __init__(self, x, y, length, traffic_intensity, road_id, image):
        self.x = x
        self.y = y
        self.width = SimulationGraphicConfig.ROAD_WIDTH
        self.length = length
        self.image = image
        self.road_id = road_id
        self.traffic_intensity = traffic_intensity # Probability of spawning a vehicle per virtual minute

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def getTrafficIntensity(self):
        return self.traffic_intensity
    
    def getRoadID(self):
        return self.road_id