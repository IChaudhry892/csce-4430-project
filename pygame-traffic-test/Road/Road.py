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
        
    def is_vehicle_spawn_occupied(self, vehicle, min_distance):
        """Check if a vehicle is too close to the spawn point"""
        if self.road_id == SimulationConfig.ROAD_IDS["Vertical Road"]:
            return abs(vehicle.y - SimulationGraphicConfig.VERTICAL_ROAD_VEHICLE_START_Y) < min_distance
        elif self.road_id == SimulationConfig.ROAD_IDS["Horizontal Road"]:
            return abs(vehicle.x - SimulationGraphicConfig.HORIZONTAL_ROAD_VEHICLE_START_X) < min_distance
        return False
    
    def can_spawn_vehicle(self, scenario) -> bool:
        """Check if a vehicle can be spawned on this road based on existing vehicles in each lane"""
        for lane_id in ["left_lane", "right_lane"]:
            lane_key = f"{self.road_id}_{lane_id}"
            vehicles_in_lane = scenario.vehicle_lanes[lane_key]

            # Check if any vehicle in the lane is too close to the spawn point
            for vehicle in vehicles_in_lane:
                min_spawn_distance = max(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT) + (SimulationGraphicConfig.VEHICLE_SPAWN_GAP_METERS * SimulationConfig.PIXELS_PER_METER)
                if self.is_vehicle_spawn_occupied(vehicle, min_spawn_distance):
                    print(f"Cannot spawn on {lane_key}: too close to existing vehicle at ({vehicle.x}, {vehicle.y})")
                    return False  # Cannot spawn if any vehicle is too close
        return True