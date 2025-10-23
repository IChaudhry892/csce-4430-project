from Animation.Animatable import Animatable
from SimulationToolbox.Simulatable import Simulatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig
from SimulationToolbox.SimulationConfig import SimulationConfig

class Vehicle(Animatable, Simulatable):
    def __init__(self, width, height, velocity, image, road_id, lane_id):
        self.width = width
        self.height = height
        self.velocity = velocity # 11.11 m/s
        self.image = image
        self.road_id = road_id
        self.lane_id = lane_id
        self.x, self.y = SimulationGraphicConfig.LANE_STARTING_POSITIONS[f"{road_id}_{lane_id}"]

    def move(self):
        distance_pixels = self.velocity * self.delta_time * SimulationConfig.PIXELS_PER_METER # 16.665 pixels per frame at 20 FPS
        if self.road_id == "vertical_road":
            self.y -= distance_pixels
        elif self.road_id == "horizontal_road":
            self.x -= distance_pixels

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x < 0 - self.width or self.y < 0 - self.width
    
    def simulate(self, delta_time):
        # All a vehicle does is move right now
        self.delta_time = delta_time
        self.move()