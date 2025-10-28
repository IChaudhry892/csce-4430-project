from Animation.Animatable import Animatable
from SimulationToolbox.Simulatable import Simulatable
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig
from SimulationToolbox.SimulationConfig import SimulationConfig
from Road.Road import Road
class Vehicle(Animatable, Simulatable):
    def __init__(self, width, height, velocity, image, road_id, lane_id):
        self.width = width
        self.height = height
        self.velocity = velocity # 11.11 m/s
        self.image = image
        self.road_id = road_id
        self.lane_id = lane_id
        self.x, self.y = SimulationGraphicConfig.LANE_STARTING_POSITIONS[f"{road_id}_{lane_id}"]
        self.state = SimulationConfig.VEHICLE_STATES["moving"]  # default is "moving", can change to "waiting"
        self.stop_line_position = SimulationGraphicConfig.STOP_LINE_POSITIONS[road_id]
        self.scenario = None  # to be set when added to scenario

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
    
    # Finds the gap between a vehicle and the ahead vehicle
    def calculate_ahead_vehicle_gap(self):
        road = None 
        for component in self.scenario.getComponents(): # 
            if isinstance(component, Road) and component.road_id == self.road_id:
                road = component
        lanelist = road.vehicle_lanes[self.road_id] # Current lane of the current road of the current vehicle

        vehicles = []
        for vehicle in lanelist: # Find all vehicles that are not current vehicle
            if vehicle is not self:
                vehicles.append(vehicle)

        aheadvehicles = []
        if self.road_id == "horizontal_road":
            for vehicle in vehicles:
                if vehicle.x < self.x:
                    aheadvehicles.append(vehicle)
            nearestvehicle = max(aheadvehicles, key=lambda v: v.x)
            return (self.y - nearestvehicle.y) - nearestvehicle.height # returns the pixel gape between a vehicle and the nearest ahead vehicle
        elif self.road_id == "vertical_road":
            for vehicle in vehicles:
                if vehicle.y < self.y:
                    aheadvehicles.append(vehicle)
            nearestvehicle = max(aheadvehicles, key=lambda v: v.y)
            return (self.y - nearestvehicle.y) - nearestvehicle.height # returns the pixel gape between a vehicle and the nearest ahead vehicle






        return 

    def simulate(self, delta_time):
        self.delta_time = delta_time
        signal = self.scenario.get_signal_for_road(self.road_id)

        # Update vehicle state based on traffic signal
        if signal.is_red():
            # Check if approaching stop line
            if self.road_id == "vertical_road" and self.y <= self.stop_line_position:
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
            elif self.road_id == "horizontal_road" and self.x <= self.stop_line_position:
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
            else:
                self.state = SimulationConfig.VEHICLE_STATES["moving"]
        elif signal.is_green():
            self.state = SimulationConfig.VEHICLE_STATES["moving"]

        # Move vehicle if in "moving" state
        if self.state == SimulationConfig.VEHICLE_STATES["moving"]:
            self.move()