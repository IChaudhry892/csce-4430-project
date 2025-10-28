from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

class TrafficSignal(Animatable):
    def __init__(self, x, y, image, state, road_id):
        self.x = x
        self.y = y
        self.width = SimulationGraphicConfig.TRAFFIC_SIGNAL_WIDTH
        self.height = SimulationGraphicConfig.TRAFFIC_SIGNAL_HEIGHT
        self.image = image
        self.state = state
        self.road_id = road_id

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def getState(self):
        return self.state

    def getRoadID(self):
        return self.road_id
    
    def setState(self, state, image) -> None:
        """Set the traffic signal's state and update its image accordingly"""
        self.state = state
        self.image = image

    def is_green(self) -> bool:
        return self.state == SimulationGraphicConfig.TRAFFIC_SIGNAL_STATES["green"]
    
    def is_red(self) -> bool:
        return self.state == SimulationGraphicConfig.TRAFFIC_SIGNAL_STATES["red"]