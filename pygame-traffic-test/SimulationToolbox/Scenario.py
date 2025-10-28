from Animation.Animatable import Animatable
from SimulationToolbox.Simulatable import Simulatable
from Intersection.Intersection import Intersection

from Graphics.SimulationGraphicConfig import SimulationGraphicConfig
from Road.Road import Road
from TrafficSignal.TrafficSignal import TrafficSignal
from SimulationToolbox.SimulationConfig import SimulationConfig

import random
from Vehicle.Vehicle import Vehicle

class Scenario:
    def __init__(self, images: dict):
        self.simulatables = []   # List of simulatable objects
        self.animatables = []    # List of animatable objects
        self.components = []     # List of objects
        self.intersection = None # Intersection object
        self.images = images    # Images dictionary for loading graphics

        # FOR TESTING: Track how many vehicles spawned per lane (keys: "vertical_road_left_lane", etc.)
        self.spawn_counts = {
            "vertical_road_left_lane": 0,
            "vertical_road_right_lane": 0,
            "horizontal_road_left_lane": 0,
            "horizontal_road_right_lane": 0
        }

    def register_vehicle_in_scenario(self, vehicle: Vehicle) -> None:
        """Add a vehicle to components list and the appropriate lane list"""
        self.addComponent(vehicle)
        vehicle.scenario = self
        lane_key = f"{vehicle.road_id}_{vehicle.lane_id}"

        # FOR TESTING: Update spawn counts
        self.spawn_counts[lane_key] += 1

    def buildScenario(self):
        """Abstract method to be implemented by subclass (probably Main)""" # nvm, using it in scenarioHandler right now
        ROAD_VERTICAL = Road(0, 0, SimulationGraphicConfig.ROAD_VERTICAL_LENGTH, SimulationConfig.TRAFFIC_INTENSITIES["high"], SimulationConfig.ROAD_IDS["Vertical Road"], self.images['road_vertical'])
        self.addComponent(ROAD_VERTICAL)
        ROAD_HORIZONTAL = Road(0, 0, SimulationGraphicConfig.ROAD_HORIZONTAL_LENGTH, SimulationConfig.TRAFFIC_INTENSITIES["low"], SimulationConfig.ROAD_IDS["Horizontal Road"], self.images['road_horizontal'])
        self.addComponent(ROAD_HORIZONTAL)
        INTERSECTION = Intersection(0, 0, self.images['intersection'])
        self.addComponent(INTERSECTION)
        SIGNAL_ROAD_VERTICAL = TrafficSignal(SimulationGraphicConfig.SIGNAL_ROAD_VERTICAL_X_POS, SimulationGraphicConfig.SIGNAL_ROAD_VERTICAL_Y_POS, self.images, SimulationConfig.TRAFFIC_SIGNAL_STATES["Red"], SimulationConfig.ROAD_IDS["Vertical Road"])
        self.addComponent(SIGNAL_ROAD_VERTICAL)
        SIGNAL_ROAD_HORIZONTAL = TrafficSignal(SimulationGraphicConfig.SIGNAL_ROAD_HORIZONTAL_X_POS, SimulationGraphicConfig.SIGNAL_ROAD_HORIZONTAL_Y_POS, self.images, SimulationConfig.TRAFFIC_SIGNAL_STATES["Green"], SimulationConfig.ROAD_IDS["Horizontal Road"])
        self.addComponent(SIGNAL_ROAD_HORIZONTAL)

    def addComponent(self, o: object) -> None:
        """Add a component to the scenario in the appropriate list"""
        if o is None:
            return
        self.components.append(o)
        if isinstance(o, Simulatable):
            self.simulatables.append(o)
        if isinstance(o, Animatable):
            self.animatables.append(o)
        if isinstance(o, Intersection):
            self.intersection = o
    
    def removeComponent(self, o: object) -> None:
        """Remove a component from the scenario in the appropriate list"""
        if o is None:
            return
        if o in self.components:
            self.components.remove(o)
        if o in self.simulatables:
            self.simulatables.remove(o)
        if o in self.animatables:
            self.animatables.remove(o)
        if isinstance(o, Intersection) and self.intersection is o:
            self.intersection = None
        if isinstance(o, Vehicle):
            self.remove_vehicle_from_scenario(o)

    def remove_vehicle_from_scenario(self, vehicle) -> None:
        """Remove a vehicle from its lane list"""
        # lane_key = f"{vehicle.road_id}_{vehicle.lane_id}"
        # if vehicle in self.vehicle_lanes[lane_key]:
        #     self.vehicle_lanes[lane_key].remove(vehicle)
        for component in self.components:
            if isinstance(component, Road):
                component.remove_vehicle_from_lane(vehicle)
    
    def getComponents(self) -> list:
        """Get all components in the scenario"""
        return self.components
    
    def getSimulatables(self) -> list:
        """Get all simulatable components in the scenario"""
        return self.simulatables
    
    def getAnimatables(self) -> list:
        """Get all animatable components in the scenario"""
        return self.animatables

    def getIntersection(self) -> Intersection:
        """Get the intersection component in the scenario"""
        return self.intersection

    def get_signal_for_road(self, road_id) -> TrafficSignal:
        """Get the traffic signal for the specified road ID"""
        for component in self.components:
            if isinstance(component, TrafficSignal) and component.getRoadID() == road_id:
                return component
        return None