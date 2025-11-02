from SimulationToolbox.Scenario import Scenario
from Animation.Animatable import Animatable

from Intersection.Intersection import Intersection
from Road.Road import Road
from Vehicle.Vehicle import Vehicle
from SimulationToolbox.SimulationConfig import SimulationConfig

import pygame
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os
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
        self.stop_virtual_time = SimulationConfig.STOP_VIRTUAL_TIME
        self.speed_factor = SimulationConfig.SPEED_FACTOR

        # Metrics for vehicle waiting times
        self.metrics = {
            "times": [],                      # List[float] virtual seconds
            "waiting_counts": [],             # List[int] total waiting vehicles at each time sample
            "vertical_waiting_counts": [],    # List[int] waiting vehicles on vertical road
            "horizontal_waiting_counts": [],  # List[int] waiting vehicles on horizontal road
            "integral_waiting": 0.0,          # Cumulative waiting time integral -> sum(waiting_count * dt_virtual)
            "total_virtual_time": 0.0,        # Total virtual time elapsed -> sum(dt_virtual)

            "next_vehicle_spawn_index": 0,    # Next spawn index for vehicles
            "vehicle_wait_map": {},           # Map vehicle id to total waiting time (virtual seconds)
            "vehicle_spawn_index": {},        # Map vehicle id to spawn index
            "final_wait_times": []            # list[tuple[int spawn_index, float wait_time_virtual]]
        }

        self.fig1 = None
        self.fig2 = None

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
            if hasattr(simulatable, 'draw'):
                simulatable.draw(screen)
    
    def isTerminated(self) -> bool:
        """Check if the simulation scenario is terminated"""
        if self.timer >= self.stop_virtual_time:
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
                self.finalizeVehicleMetrics()
                # Draw final frame and save it
                self.display.redrawSimulationWindow(self, self.timer, self.real_time, self.frame_count)
                pygame.display.flip()
                pygame.image.save(self.display.screen, "final_simulation_frame.png")
                self.cleanup()
                self.running = False

            # Timing control
            self.frame_count += 1
            real_time_per_frame = self.clock.tick(self.fps) / 1000.0
            self.real_time += real_time_per_frame
            virtual_time_per_frame = real_time_per_frame * self.speed_factor
            self.timer += virtual_time_per_frame

            # Metrics update: count waiting vehicles
            waiting_vehicles_count = 0
            vertical_waiting_count = 0
            horizontal_waiting_count = 0
            for vehicle in self.scenario.getVehicles():
                if vehicle.state == SimulationConfig.VEHICLE_STATES["waiting"]:
                    waiting_vehicles_count += 1
                    # Count by road
                    if vehicle.road_id == SimulationConfig.ROAD_IDS["Vertical Road"]:
                        vertical_waiting_count += 1
                    elif vehicle.road_id == SimulationConfig.ROAD_IDS["Horizontal Road"]:
                        horizontal_waiting_count += 1
            self.metrics["times"].append(self.timer)
            self.metrics["waiting_counts"].append(waiting_vehicles_count)
            self.metrics["vertical_waiting_counts"].append(vertical_waiting_count)
            self.metrics["horizontal_waiting_counts"].append(horizontal_waiting_count)

            # Time-weighted integral for average waiting vehicles across entire run
            self.metrics["integral_waiting"] += waiting_vehicles_count * virtual_time_per_frame
            self.metrics["total_virtual_time"] += virtual_time_per_frame

            # Metrics update: update waiting times for all vehicles
            for vehicle in self.scenario.getVehicles():
                vehicle_id = id(vehicle)
                # Ensure mapping exists (in case vehicle pre-existed before toggle)
                if vehicle_id not in self.metrics["vehicle_wait_map"]:
                    self.metrics["vehicle_wait_map"][vehicle_id] = 0.0
                    self.metrics["vehicle_spawn_index"][vehicle_id] = self.metrics["next_vehicle_spawn_index"]
                    self.metrics["next_vehicle_spawn_index"] += 1
                # Update waiting time for vehicles in 'waiting' state
                if vehicle.state == SimulationConfig.VEHICLE_STATES["waiting"]:
                    self.metrics["vehicle_wait_map"][vehicle_id] += virtual_time_per_frame

            # Spawn vehicles based on traffic intensity for each road
            for road in self.scenario.getComponents():
                if isinstance(road, Road) and random.random() < road.getTrafficIntensity():
                        vehicle = road.try_spawn_vehicle_in_lane(self.scenario, self.display.screen)
                        if vehicle is not None:
                            # Metrics update: add metrics tracking for the spawned vehicle
                            vehicle_id = id(vehicle)
                            self.metrics["vehicle_wait_map"][vehicle_id] = 0.0 # Initialize waiting time
                            self.metrics["vehicle_spawn_index"][vehicle_id] = self.metrics["next_vehicle_spawn_index"]
                            self.metrics["next_vehicle_spawn_index"] += 1

                            # FOR DEBUGGING/TESTING: Update and print spawn counts
                            lane_key = f"{vehicle.road_id}_{vehicle.lane_id}"
                            print(f"Spawned vehicle in {lane_key}: total={self.scenario.spawn_counts[lane_key]}")

            # Update simulatable components (just vehicles for now)
            for simulatable in self.scenario.getSimulatables()[:]:
                simulatable.simulate(virtual_time_per_frame)
                if isinstance(simulatable, Vehicle) and simulatable.is_off_screen():
                    # Record final waiting time metric before removing vehicle
                    vehicle_id = id(simulatable)
                    # Finalize wait time entry
                    if vehicle_id in self.metrics["vehicle_wait_map"] and vehicle_id in self.metrics["vehicle_spawn_index"]:
                        self.metrics["final_wait_times"].append((
                            self.metrics["vehicle_spawn_index"][vehicle_id],
                            self.metrics["vehicle_wait_map"][vehicle_id]
                        ))
                        # Delete mappings to free memory
                        del self.metrics["vehicle_wait_map"][vehicle_id]
                        del self.metrics["vehicle_spawn_index"][vehicle_id]
                    self.scenario.removeComponent(simulatable)

            # Redraw the simulation window
            self.display.redrawSimulationWindow(self, self.timer, self.real_time, self.frame_count)

    def cleanup(self) -> None:
        """Cleanup resources used by the scenario handler"""
        while self.scenario.getComponents():
            component = self.scenario.getComponents()[0]
            self.scenario.removeComponent(component)

    def finalizeVehicleMetrics(self) -> None:
        """Finalize vehicle waiting time metrics for all remaining vehicles in the scenario"""
        for vehicle in self.scenario.getVehicles():
            vehicle_id = id(vehicle)
            # Finalize wait time entry
            if vehicle_id in self.metrics["vehicle_wait_map"] and vehicle_id in self.metrics["vehicle_spawn_index"]:
                self.metrics["final_wait_times"].append((
                    self.metrics["vehicle_spawn_index"][vehicle_id],
                    self.metrics["vehicle_wait_map"][vehicle_id]
                ))
                # Delete mappings to free memory
                del self.metrics["vehicle_wait_map"][vehicle_id]
                del self.metrics["vehicle_spawn_index"][vehicle_id]

    def calculateTotalAverageWaitingVehicles(self) -> float:
        """Calculate the average number of waiting vehicles over the entire simulation run"""
        if self.metrics["total_virtual_time"] == 0.0:
            return 0.0
        return self.metrics["integral_waiting"] / self.metrics["total_virtual_time"]
    
    def calculateVerticalAverageWaitingVehicles(self) -> float:
        if not self.metrics["vertical_waiting_counts"]:
            return 0.0
        return sum(self.metrics["vertical_waiting_counts"]) / len(self.metrics["vertical_waiting_counts"])

    def calculateHorizontalAverageWaitingVehicles(self) -> float:
        if not self.metrics["horizontal_waiting_counts"]:
            return 0.0
        return sum(self.metrics["horizontal_waiting_counts"]) / len(self.metrics["horizontal_waiting_counts"])

    def calculateAverageVehicleWaitingTime(self) -> float:
        """Calculate the average waiting time of all vehicles in the scenario"""
        if not self.metrics["final_wait_times"]:
            return 0.0
        total_wait_time = sum(wait_time for _, wait_time in self.metrics["final_wait_times"])
        return total_wait_time / len(self.metrics["final_wait_times"])
    
    def createSimulationResultPlots(self) -> None:
        """Create plots for simulation results using matplotlib"""
        average_waiting_vehicles = self.calculateTotalAverageWaitingVehicles()
        average_vehicle_wait_time = self.calculateAverageVehicleWaitingTime()

        vertical_average_waiting_vehicles = self.calculateVerticalAverageWaitingVehicles()
        horizontal_average_waiting_vehicles = self.calculateHorizontalAverageWaitingVehicles()

        # Plot 1: show number of waiting vehicles over time
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        ax1.plot(self.metrics["times"], self.metrics["vertical_waiting_counts"], label="Vertical Road", color='blue', linewidth=1.5)
        ax1.plot(self.metrics["times"], self.metrics["horizontal_waiting_counts"], label="Horizontal Road", color='red', linewidth=1.5)
        # Add horizontal mean lines
        ax1.axhline(y=vertical_average_waiting_vehicles, color='blue', linestyle='--', linewidth=1.2, alpha=0.7, label=f'Vertical Road Avg = {vertical_average_waiting_vehicles:.2f}')
        ax1.axhline(y=horizontal_average_waiting_vehicles, color='red', linestyle='--', linewidth=1.2, alpha=0.7, label=f'Horizontal Road Avg = {horizontal_average_waiting_vehicles:.2f}')
        ax1.set_xlabel("Time (virtual seconds)")
        ax1.set_ylabel("Number of Waiting Vehicles")
        ax1.set_title(f"Waiting Vehicles Over Time (Avg Total: {average_waiting_vehicles:.2f})")
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        fig1.tight_layout()

        # Plot 2: show waiting time per vehicle spawn index
        final_sorted_waits = sorted(self.metrics["final_wait_times"], key=lambda t: t[0]) # Sort by spawn index
        xs = [idx for idx, _ in final_sorted_waits]
        ys = [wt for _, wt in final_sorted_waits]

        fig2, ax2 = plt.subplots(figsize=(6, 5))
        ax2.scatter(xs, ys, s=10, color='blue', alpha=0.6)
        ax2.set_xlabel("Vehicle Spawn Index")
        ax2.set_ylabel("Vehicle Waiting Time (virtual seconds)")
        ax2.set_title(f"Vehicle Waiting Time by Spawn Index (Avg: {average_vehicle_wait_time:.2f} virtual seconds)")
        # Add horizontal mean line
        ax2.axhline(y=average_vehicle_wait_time, color='red', linestyle='--', label='Average Waiting Time')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        fig2.tight_layout()

        return fig1, fig2
    
    def displaySimulationResults(self) -> None:
        """Display the simulation results using matplotlib"""
        if self.fig1 is None or self.fig2 is None:
            self.fig1, self.fig2 = self.createSimulationResultPlots()

        # Load and display the final saved frame using matplotlib
        img = mpimg.imread("final_simulation_frame.png")

        # Delete final frame image file after loading
        os.remove("final_simulation_frame.png")

        fig3, ax3 = plt.subplots(figsize=(12, 6))
        ax3.imshow(img)
        ax3.axis('off')
        ax3.set_title("Final Simulation Frame")
        fig3.tight_layout()

        # Show all 3 figures - blocks until all windows are closed
        print("\n" + "="*50)
        print("Displaying simulation results.")
        print("Close all plot windows to exit the program.")
        print("="*50 + "\n")

        # FOR TESTING: Save 3 plots as png files
        self.fig1.savefig("waiting_vehicles_over_time.png")
        self.fig2.savefig("vehicle_waiting_time_by_spawn_index.png")
        fig3.savefig("final_simulation_frame_display.png")
        
        plt.show(block=True)
        input("Press Enter to continue...")
        
        # Clean up matplotlib to prevent crash on exit
        print("All plots closed. Cleaning up...")
        plt.close('all')