import random
import pygame
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

        self.vehicle_lanes = {
            "left_lane": [],
            "right_lane": []
        }

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def getTrafficIntensity(self):
        return self.traffic_intensity
    
    def getRoadID(self):
        return self.road_id
    
    def get_lane_key(self, lane_id):
        return f"{self.road_id}_{lane_id}"

    def can_spawn_in_lane(self, lane_id, screen) -> bool:
        """Check if a vehicle can be spawned in the specified lane based on existing vehicles"""
        lane_vehicle_list = self.vehicle_lanes[lane_id]
        lane_key = self.get_lane_key(lane_id)
        min_gap = max(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT) + (SimulationGraphicConfig.VEHICLE_SPAWN_GAP_METERS * SimulationConfig.PIXELS_PER_METER)
        spawn_x = SimulationGraphicConfig.LANE_STARTING_POSITIONS[lane_key][0]
        spawn_y = SimulationGraphicConfig.LANE_STARTING_POSITIONS[lane_key][1]

        spawn_rectangle = pygame.Rect((spawn_x, spawn_y, SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT))
        pygame.draw.rect(screen, (255, 0, 0), spawn_rectangle, 2)  # For debugging: visualize spawn area
        for vehicle in lane_vehicle_list:
            vehicle_rectangle = pygame.Rect((vehicle.x, vehicle.y, vehicle.width, vehicle.height))
            pygame.draw.rect(screen, (0, 255, 0), vehicle_rectangle, 2)  # For debugging: visualize existing vehicle
            if spawn_rectangle.colliderect(vehicle_rectangle):
                print(f"Cannot spawn in {lane_key}: spawn area occupied by vehicle at ({vehicle.x}, {vehicle.y})")
                return False
        return True
    
    def register_vehicle_in_lane(self, vehicle: Vehicle) -> None:
        """Register a vehicle in the specified lane's vehicle list"""
        lane_id = vehicle.lane_id
        self.vehicle_lanes[lane_id].append(vehicle)

    def remove_vehicle_from_lane(self, vehicle: Vehicle) -> None:
        """Remove a vehicle from the specified lane's vehicle list"""
        lane_id = vehicle.lane_id
        if vehicle in self.vehicle_lanes[lane_id]:
            self.vehicle_lanes[lane_id].remove(vehicle)

    def choose_spawn_lane(self) -> str:
        """Choose a lane to spawn a vehicle, ensuring it's not occupied"""
        possible_lanes = list(self.vehicle_lanes.keys())
        return random.choice(possible_lanes)
    
    def try_spawn_vehicle_in_lane(self, scenario, screen) -> bool:
        """Attempt to spawn a vehicle in the specified lane if possible"""
        first_lane = self.choose_spawn_lane()
        second_lane = "left_lane" if first_lane == "right_lane" else "right_lane"
        lane_order = [first_lane, second_lane]
        for lane_id in lane_order:
            if self.can_spawn_in_lane(lane_id, screen):
                vehicle = self.create_vehicle(scenario.images, lane_id)
                scenario.register_vehicle_in_scenario(vehicle)
                self.register_vehicle_in_lane(vehicle)
                return True
        return False

    def create_vehicle(self, images: dict, lane_id: str) -> Vehicle:
        """
        Create (but do not register) a Vehicle for this road.
        Returns a Vehicle instance; caller should add it to the scenario.
        """
        # lane_id = random.choice(["left_lane", "right_lane"])

        if self.road_id == SimulationConfig.ROAD_IDS["Vertical Road"]:
            img = images['car_north']
            return Vehicle(SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationGraphicConfig.VEHICLE_WIDTH, SimulationConfig.VEHICLE_VELOCITY_MPS, img, self.road_id, lane_id)
        elif self.road_id == SimulationConfig.ROAD_IDS["Horizontal Road"]:
            img = images['car_west']
            return Vehicle(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationConfig.VEHICLE_VELOCITY_MPS, img, self.road_id, lane_id)
        
    # def is_vehicle_spawn_occupied(self, vehicle, min_distance):
    #     """Check if a vehicle is too close to the spawn point"""
    #     if self.road_id == SimulationConfig.ROAD_IDS["Vertical Road"]:
    #         return abs(vehicle.y - SimulationGraphicConfig.VERTICAL_ROAD_START_Y) < min_distance
    #     elif self.road_id == SimulationConfig.ROAD_IDS["Horizontal Road"]:
    #         return abs(vehicle.x - SimulationGraphicConfig.HORIZONTAL_ROAD_START_X) < min_distance
    #     return False
    
    # def can_spawn_vehicle(self, scenario) -> bool:
    #     """Check if a vehicle can be spawned on this road based on existing vehicles in each lane"""
    #     for lane_id in ["left_lane", "right_lane"]:
    #         lane_key = f"{self.road_id}_{lane_id}"
    #         vehicles_in_lane = scenario.vehicle_lanes[lane_key]

    #         # Check if any vehicle in the lane is too close to the spawn point
    #         for vehicle in vehicles_in_lane:
    #             min_spawn_distance = max(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT) + (SimulationGraphicConfig.VEHICLE_SPAWN_GAP_METERS * SimulationConfig.PIXELS_PER_METER)
    #             if self.is_vehicle_spawn_occupied(vehicle, min_spawn_distance):
    #                 print(f"Cannot spawn on {lane_key}: too close to existing vehicle at ({vehicle.x}, {vehicle.y})")
    #                 return False  # Cannot spawn if any vehicle is too close
    #     return True