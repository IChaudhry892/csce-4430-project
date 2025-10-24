from SimulationToolbox.Scenario import Scenario
from Animation.Animatable import Animatable

from Intersection.Intersection import Intersection
from Road.Road import Road
from Vehicle.Vehicle import Vehicle
from SimulationToolbox.SimulationConfig import SimulationConfig

import pygame
import random

class ScenarioHandler:

    def __init__(self, scenario: Scenario, display):
        self.scenario = scenario
        self.display = display
        self.fps = SimulationConfig.FPS
        self.clock = pygame.time.Clock()
        self.running = True
        self.real_time = SimulationConfig.REAL_TIME
        self.timer = SimulationConfig.TIMER
        self.frame_count = SimulationConfig.FRAME_COUNT
        self.stop_real_time = SimulationConfig.STOP_REAL_TIME
        self.speed_factor = SimulationConfig.SPEED_FACTOR

    def proceedSimulation(self) -> None:
        pass

    def drawAnimatables(self, screen) -> None:
        """Draw all animatable components in the scenario""" # Called in Display.redrawSimulationWindow
        animatables = self.scenario.getAnimatables()
        for animatable in animatables:
            animatable.draw(screen)

    def drawSimulatables(self, screen) -> None:
        """Draw all simulatable components in the scenario""" # Called in Display.redrawSimulationWindow
        simulatables = self.scenario.getSimulatables()
        for simulatable in simulatables:
            simulatable.draw(screen)
    
    def isTerminated(self) -> bool:
        """Check if the simulation scenario is terminated"""
        if self.real_time >= self.stop_real_time:
            return True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def runSimulation(self) -> None:
        """Run the simulation scenario"""
        self.scenario.buildScenario()

        while self.running:
            # Check termination conditions
            if self.isTerminated():
                self.cleanup()
                self.running = False

            # Timing control
            self.frame_count += 1
            real_time_per_frame = self.clock.tick(self.fps) / 1000.0
            self.real_time += real_time_per_frame
            virtual_time_per_frame = real_time_per_frame * self.speed_factor
            self.timer += virtual_time_per_frame

            # Spawn vehicles based on traffic intensity for each road
            for road in self.scenario.getComponents():
                if isinstance(road, Road) and random.random() < road.getTrafficIntensity() and road.can_spawn_vehicle(self.scenario):
                        vehicle = road.create_vehicle(self.scenario.images)
                        self.scenario.register_vehicle(vehicle)

                        # FOR TESTING: Update and print spawn counts
                        lane_key = f"{vehicle.road_id}_{vehicle.lane_id}"
                        print(f"Spawned vehicle in {lane_key}: total={self.scenario.spawn_counts[lane_key]}")

            # Update simulatable components (just vehicles for now)
            for simulatable in self.scenario.getSimulatables()[:]:
                simulatable.simulate(virtual_time_per_frame)
                if simulatable.is_off_screen():
                    self.scenario.removeComponent(simulatable)

            # Redraw the simulation window
            self.display.redrawSimulationWindow(self, self.timer, self.real_time, self.frame_count)

    def cleanup(self) -> None:
        """Cleanup resources used by the scenario handler"""
        while self.scenario.getComponents():
            component = self.scenario.getComponents()[0]
            self.scenario.removeComponent(component)

    def calculateAverageTime(self) -> float:
        """Calculate the average waiting time of all vehicles in the scenario??"""
        pass