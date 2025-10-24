import random
from Animation.Animatable import Animatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig
from SimulationToolbox.SimulationConfig import SimulationConfig
from Vehicle.Vehicle import Vehicle

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
    
    def create_vehicle(self, images: dict) -> Vehicle:
        """
        Create (but do not register) a Vehicle for this road.
        Returns a Vehicle instance; caller should add it to the scenario.
        """
        lane_id = random.choice(["left_lane", "right_lane"])
        if self.road_id == SimulationConfig.ROAD_IDS["Vertical Road"]:
            img = images['car_north']
            return Vehicle(SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationGraphicConfig.VEHICLE_WIDTH, SimulationConfig.VEHICLE_VELOCITY_MPS, img, self.road_id, lane_id)
        elif self.road_id == SimulationConfig.ROAD_IDS["Horizontal Road"]:
            img = images['car_west']
            return Vehicle(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationConfig.VEHICLE_VELOCITY_MPS, img, self.road_id, lane_id)