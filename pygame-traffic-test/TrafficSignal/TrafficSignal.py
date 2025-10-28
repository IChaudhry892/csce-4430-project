from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig
from SimulationToolbox.SimulationConfig import SimulationConfig

class TrafficSignal(Animatable):
    def __init__(self, x, y, images, state, road_id):
        self.x = x
        self.y = y
        self.width = SimulationGraphicConfig.TRAFFIC_SIGNAL_WIDTH
        self.height = SimulationGraphicConfig.TRAFFIC_SIGNAL_HEIGHT
        self.images = images
        self.image = images[state]
        self.state = state
        self.road_id = road_id

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def getState(self):
        return self.state

    def getRoadID(self):
        return self.road_id
    
    def setState(self, state) -> None:
        """Set the traffic signal's state and update its image accordingly"""
        self.state = state
        self.image = self.images[state]

    def is_green(self) -> bool:
        return self.state == SimulationConfig.TRAFFIC_SIGNAL_STATES["Green"]
    
    def is_red(self) -> bool:
        return self.state == SimulationConfig.TRAFFIC_SIGNAL_STATES["Red"]