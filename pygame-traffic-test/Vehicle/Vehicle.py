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
        self.state = SimulationConfig.VEHICLE_STATES["moving"]  # default is "moving", can change to "waiting"
        self.stop_line_position = SimulationGraphicConfig.STOP_LINE_POSITIONS[road_id]
        self.scenario = None  # to be set when added to scenario

    # ----------------------------------
    # === BASIC MOVEMENT AND DRAWING
    # ----------------------------------
    def move(self):
        distance_pixels = self.velocity * self.delta_time * SimulationConfig.PIXELS_PER_METER # 16.665 pixels per frame at 20 FPS
        if self.road_id == "vertical_road":
            self.y -= distance_pixels
        elif self.road_id == "horizontal_road":
            self.x -= distance_pixels

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x < 0 - self.width or self.y < 0 - self.height

    # ----------------------------------
    # === AHEAD VEHICLE LOGIC
    # ----------------------------------
    def get_nearest_ahead_vehicle(self):
        """Get the nearest vehicle ahead in the same lane, if any"""
        road = None
        for road_component in self.scenario.getRoads():
            if road_component.getRoadID() == self.road_id:
                road = road_component
        lane_list = road.vehicle_lanes[self.lane_id] # Current lane of the current road of the current vehicle
        
        vehicles = [v for v in lane_list if v is not self]
        
        ahead_vehicles = []
        if self.road_id == "horizontal_road":
            for vehicle in vehicles:
                if vehicle.x < self.x:
                    ahead_vehicles.append(vehicle)
                
            if not ahead_vehicles:
                return None   # No car ahead, safe to move
            
            nearest_vehicle = max(ahead_vehicles, key=lambda v: v.x)
            return nearest_vehicle
        
        elif self.road_id == "vertical_road":
            for vehicle in vehicles:
                if vehicle.y < self.y:
                    ahead_vehicles.append(vehicle)

            if not ahead_vehicles:
                return None   # No car ahead, safe to move
            
            nearest_vehicle = max(ahead_vehicles, key=lambda v: v.y)
            return nearest_vehicle
        return None

    def is_nearest_ahead_vehicle_waiting(self):
        """Check if the nearest ahead vehicle is in 'waiting' state"""
        vehicle = self.get_nearest_ahead_vehicle()
        if vehicle:
            return vehicle.state == SimulationConfig.VEHICLE_STATES["waiting"]
        return False
    
    def get_ahead_vehicle_gap(self):
        """Get the pixel gap to the nearest ahead vehicle, if any"""
        ahead_vehicle = self.get_nearest_ahead_vehicle()
        if ahead_vehicle is None:
            return None
        if self.road_id == "horizontal_road":
            return (self.x - ahead_vehicle.x) - ahead_vehicle.width
        elif self.road_id == "vertical_road":
            return (self.y - ahead_vehicle.y) - ahead_vehicle.height
        return None

    # ----------------------------------
    # === HELPER METHODS FOR SIGNALS
    # ----------------------------------

    def should_stop_at_signal(self, next_frame_position) -> bool:
        if self.road_id == "vertical_road":
            return self.y > self.stop_line_position and next_frame_position < self.stop_line_position
        elif self.road_id == "horizontal_road":
            return self.x > self.stop_line_position and next_frame_position < self.stop_line_position
        return False

    def within_stop_zone(self) -> bool:
        pass

    def check_ahead_vehicle_gap(self) -> None:
        pass

    def handle_red_signal(self, signal) -> None:
        pass

    def handle_signal_behavior(self, signal) -> None:
        pass

    def simulate(self, delta_time):
        self.delta_time = delta_time
        signal = self.scenario.get_signal_for_road(self.road_id)
        calculated_ahead_vehicle_gap = self.get_ahead_vehicle_gap()
        distance_pixels = self.velocity * delta_time * SimulationConfig.PIXELS_PER_METER
        
        # if calculated_ahead_gap != None:        # Uncomment this to print the pixel gaps. I recommend commenting out the vertical road if you do this.
        #     print(calculated_ahead_gap)

        # Update vehicle state based on traffic signal
        if signal.is_red():
            # Check if vehicle will cross the stop line in the next frame
            if self.road_id == "vertical_road":
                next_frame_y = self.y - distance_pixels
                # Currently behind the stop line and would cross it next frame
                if self.y > self.stop_line_position and next_frame_y < self.stop_line_position:
                    # Move only up to the stop line and wait
                    self.y = self.stop_line_position
                    self.state = SimulationConfig.VEHICLE_STATES["waiting"]
                    print(f"Vehicle at ({self.x}, {self.y}) and stop line rectangle at ({self.stop_line_position}, {self.stop_line_position + 10}).")
                # If at stop line (within 5 pixels ahead of it) -> keep waiting
                elif self.y <= self.stop_line_position and self.y >= self.stop_line_position - 5:
                    self.state = SimulationConfig.VEHICLE_STATES["waiting"]
                # If already well past the stop line -> keep moving
                elif self.y < self.stop_line_position - 5:
                    self.state = SimulationConfig.VEHICLE_STATES["moving"]
                else:
                    # Not yet at stop line, keep moving until reaching it or ahead vehicle
                    self.state = SimulationConfig.VEHICLE_STATES["moving"]
                    if calculated_ahead_vehicle_gap is not None and self.is_nearest_ahead_vehicle_waiting(): # There is an ahead vehicle and it is waiting
                        min_gap = SimulationGraphicConfig.VEHICLE_MIN_GAP_METERS * SimulationConfig.PIXELS_PER_METER
                        if calculated_ahead_vehicle_gap <= min_gap:
                            self.state = SimulationConfig.VEHICLE_STATES["waiting"]
            elif self.road_id == "horizontal_road":
                next_frame_x = self.x - distance_pixels
                # Currently behind the stop line and would cross it next frame
                if self.x > self.stop_line_position and next_frame_x < self.stop_line_position:
                    # Move only up to the stop line and wait
                    self.x = self.stop_line_position
                    self.state = SimulationConfig.VEHICLE_STATES["waiting"]
                    print(f"Vehicle at ({self.x}, {self.y}) and stop line rectangle at ({self.stop_line_position}, {self.stop_line_position + 10}).")
                # If at stop line (within 5 pixels ahead of it) -> keep waiting
                elif self.x <= self.stop_line_position and self.x >= self.stop_line_position - 5:
                    self.state = SimulationConfig.VEHICLE_STATES["waiting"]
                # If already well past the stop line -> keep moving
                elif self.x < self.stop_line_position - 5:
                    self.state = SimulationConfig.VEHICLE_STATES["moving"]
                else:
                    # Not yet at stop line, keep moving until reaching it or ahead vehicle
                    self.state = SimulationConfig.VEHICLE_STATES["moving"]
                    if calculated_ahead_vehicle_gap is not None and self.is_nearest_ahead_vehicle_waiting(): # There is an ahead vehicle and it is waiting
                        min_gap = SimulationGraphicConfig.VEHICLE_MIN_GAP_METERS * SimulationConfig.PIXELS_PER_METER
                        if calculated_ahead_vehicle_gap <= min_gap:
                            self.state = SimulationConfig.VEHICLE_STATES["waiting"]              
        elif signal.is_green():
            self.state = SimulationConfig.VEHICLE_STATES["moving"]

        # Move vehicle if in "moving" state
        if self.state == SimulationConfig.VEHICLE_STATES["moving"]:
            self.move()