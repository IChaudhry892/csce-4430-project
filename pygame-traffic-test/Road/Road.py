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

        # FOR DEBUGGING
        self.debug_spawn_rect = None
        self.debug_vehicle_rects = []

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def getTrafficIntensity(self):
        return self.traffic_intensity
    
    def getRoadID(self):
        return self.road_id
    
    def get_lane_key(self, lane_id):
        return f"{self.road_id}_{lane_id}"

    def can_spawn_in_lane(self, lane_id) -> bool:
        """Check if a vehicle can be spawned in the specified lane based on existing vehicles"""
        lane_vehicle_list = self.vehicle_lanes[lane_id]
        lane_key = self.get_lane_key(lane_id)
        min_gap = SimulationGraphicConfig.VEHICLE_SPAWN_GAP_METERS * SimulationConfig.PIXELS_PER_METER
        spawn_x = SimulationGraphicConfig.LANE_STARTING_POSITIONS[lane_key][0]
        spawn_y = SimulationGraphicConfig.LANE_STARTING_POSITIONS[lane_key][1]

        spawn_rectangle = pygame.Rect((spawn_x, spawn_y, SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT))
        for vehicle in lane_vehicle_list:
            vehicle_rectangle = pygame.Rect((vehicle.x + min_gap, vehicle.y + min_gap, vehicle.width, vehicle.height))
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
    
    def try_spawn_vehicle_in_lane(self, scenario, screen) -> Vehicle | None:
        """Attempt to spawn a vehicle in the specified lane if possible"""
        first_lane = self.choose_spawn_lane()
        second_lane = "left_lane" if first_lane == "right_lane" else "right_lane"
        lane_order = [first_lane, second_lane]
        for lane_id in lane_order:
            if self.can_spawn_in_lane(lane_id):
                vehicle = self.create_vehicle(scenario.images, lane_id)
                if vehicle is None:
                    return None
                # register the vehicle in the scenario and this road's lane
                scenario.register_vehicle_in_scenario(vehicle)
                self.register_vehicle_in_lane(vehicle)
                return vehicle
        return None

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
        
    def get_number_of_vehicles_behind_intersection(self) -> int:
        """Get the number of vehicles currently behind the intersection on this road"""
        count = 0
        stop_line_position = SimulationGraphicConfig.STOP_LINE_POSITIONS[self.road_id]
        for lane_id, vehicle_list in self.vehicle_lanes.items():
            for vehicle in vehicle_list:
                if self.road_id == SimulationConfig.ROAD_IDS["Vertical Road"]:
                    if vehicle.y + vehicle.height > stop_line_position:
                        count += 1
                elif self.road_id == SimulationConfig.ROAD_IDS["Horizontal Road"]:
                    if vehicle.x + vehicle.width > stop_line_position:
                        count += 1
        return count