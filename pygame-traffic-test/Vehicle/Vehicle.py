from Animation.Animatable import Animatable
from SimulationToolbox.Simulatable import Simulatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

class Vehicle(Animatable, Simulatable):
    def __init__(self, width, height, velocity, image, road_id, lane_id):
        self.width = width
        self.height = height
        self.velocity = velocity
        self.image = image
        self.road_id = road_id
        self.lane_id = lane_id
        self.x, self.y = SimulationGraphicConfig.LANE_STARTING_POSITIONS[f"{road_id}_{lane_id}"]

    def move(self):
        if self.road_id == "vertical_road":
            self.y -= self.velocity
        elif self.road_id == "horizontal_road":
            self.x -= self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x < 0 - self.width or self.y < 0 - self.width
    
    def simulate(self):
        pass