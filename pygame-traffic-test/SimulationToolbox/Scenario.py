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
        
        # FOR TESTING PURPOSES
        self.images = images

    # FOR TESTING PURPOSES
    def spawn_vehicle(self):
        road_id = random.choice(["vertical_road", "horizontal_road"])
        lane_id = random.choice(["left_lane", "right_lane"])
        if road_id == "vertical_road":
            img = self.images['car_north']
            self.addComponent(Vehicle(SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationGraphicConfig.VEHICLE_WIDTH, SimulationConfig.VEHICLE_VELOCITY_MPS, img, road_id, lane_id))
        else:
            img = self.images['car_west']
            self.addComponent(Vehicle(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationConfig.VEHICLE_VELOCITY_MPS, img, road_id, lane_id))
    
    def buildScenario(self):
        """Abstract method to be implemented by subclass (probably Main)""" # nvm, using it in scnearioHandler right now
        # PLACEHOLDER CODE FOR TESTING
        ROAD_VERTICAL = Road(0, 0, SimulationGraphicConfig.ROAD_VERTICAL_LENGTH, self.images['road_vertical'])
        self.addComponent(ROAD_VERTICAL)
        ROAD_HORIZONAL = Road(0, 0, SimulationGraphicConfig.ROAD_HORIZONTAL_LENGTH, self.images['road_horizontal'])
        self.addComponent(ROAD_HORIZONAL)
        INTERSECTION = Intersection(0, 0, self.images['intersection'])
        self.addComponent(INTERSECTION)
        SIGNAL_ROAD_VERTICAL = TrafficSignal(SimulationGraphicConfig.SIGNAL_ROAD_VERTICAL_X_POS, SimulationGraphicConfig.SIGNAL_ROAD_VERTICAL_Y_POS, self.images['signal_red'])
        self.addComponent(SIGNAL_ROAD_VERTICAL)
        SIGNAL_ROAD_HORIZONTAL = TrafficSignal(SimulationGraphicConfig.SIGNAL_ROAD_HORIZONTAL_X_POS, SimulationGraphicConfig.SIGNAL_ROAD_HORIZONTAL_Y_POS, self.images['signal_green'])
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
        # ONLY USED FOR REMOVING VEHCILES CURRENTLY
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