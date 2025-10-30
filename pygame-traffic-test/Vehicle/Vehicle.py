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
        """Check if the vehicle would cross the stop line in the next frame"""
        if self.road_id == "vertical_road":
            return self.y > self.stop_line_position and next_frame_position < self.stop_line_position
        elif self.road_id == "horizontal_road":
            return self.x > self.stop_line_position and next_frame_position < self.stop_line_position
        return False

    def within_stop_zone(self) -> bool:
        """Check if the vehicle is within 5 pixels ahead of the stop line"""
        if self.road_id == "vertical_road":
            return self.stop_line_position - 5 <= self.y <= self.stop_line_position
        elif self.road_id == "horizontal_road":
            return self.stop_line_position - 5 <= self.x <= self.stop_line_position
        return False

    def check_ahead_vehicle_gap(self, gap) -> None:
        """Check the gap to the nearest ahead vehicle and adjust state if needed"""
        if gap is not None and self.is_nearest_ahead_vehicle_waiting():
            min_gap = SimulationGraphicConfig.VEHICLE_MIN_GAP_METERS * SimulationConfig.PIXELS_PER_METER
            if gap <= min_gap:
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
            else:
                self.state = SimulationConfig.VEHICLE_STATES["moving"]

    def handle_red_signal(self, distance_pixels, gap) -> None:
        """Handle vehicle behavior when the traffic signal is red"""
        if self.road_id == "vertical_road":
            next_frame_y = self.y - distance_pixels
            if self.should_stop_at_signal(next_frame_y):
                self.y = self.stop_line_position
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
                print(f"Vehicle at ({self.x}, {self.y}) stopped at vertical line {self.stop_line_position}.")
            elif self.within_stop_zone():
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
            elif self.y < self.stop_line_position - 5: # Already 5 pixels past the stop line
                self.state = SimulationConfig.VEHICLE_STATES["moving"]
            else:
                self.check_ahead_vehicle_gap(gap)
        elif self.road_id == "horizontal_road":
            next_frame_x = self.x - distance_pixels
            if self.should_stop_at_signal(next_frame_x):
                self.x = self.stop_line_position
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
                print(f"Vehicle at ({self.x}, {self.y}) stopped at horizontal line {self.stop_line_position}.")
            elif self.within_stop_zone():
                self.state = SimulationConfig.VEHICLE_STATES["waiting"]
            elif self.x < self.stop_line_position - 5: # Already 5 pixels past the stop line
                self.state = SimulationConfig.VEHICLE_STATES["moving"]
            else:
                self.check_ahead_vehicle_gap(gap)

    def handle_signal_behavior(self, signal, distance_pixels, gap) -> None:
        """Handle vehicle behavior based on traffic signal state"""
        if signal.is_red():
            self.handle_red_signal(distance_pixels, gap)
        elif signal.is_green():
            self.state = SimulationConfig.VEHICLE_STATES["moving"]

    def simulate(self, delta_time):
        """Simulate vehicle behavior for the given delta time"""
        self.delta_time = delta_time
        signal = self.scenario.get_signal_for_road(self.road_id)
        ahead_vehicle_gap = self.get_ahead_vehicle_gap()
        distance_pixels = self.velocity * delta_time * SimulationConfig.PIXELS_PER_METER

        # Update vehicle state based on traffic signal
        self.handle_signal_behavior(signal, distance_pixels, ahead_vehicle_gap)

        # Move vehicle if in "moving" state
        if self.state == SimulationConfig.VEHICLE_STATES["moving"]:
            self.move()