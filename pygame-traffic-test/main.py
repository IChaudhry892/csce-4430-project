from Graphics.SimulationGraphicConfig import SimulationGraphicConfig
from Vehicle.Vehicle import Vehicle
from Road.Road import Road
from Intersection.Intersection import Intersection
from TrafficSignal.TrafficSignal import TrafficSignal

import pygame
import random

pygame.init()
pygame.display.set_caption("Traffic Simulation Test")

screen = pygame.display.set_mode((SimulationGraphicConfig.SCREEN_WIDTH, SimulationGraphicConfig.SCREEN_HEIGHT))

SPEED_FACTOR = 3.0      # Simulation runs 3x faster than real time
REAL_TIME = 0.0         # Real-time elapsed in seconds
TIMER = 0.0             # Virtual time elapsed in seconds
STOP_REAL_TIME = 30.0   # Stop simulation after 30 real-time seconds

# Object properties -> MOVED TO SEPARATE CLASS FILES

# Simulation variables
vehicles = []
simulation_over = False
running = True
clock = pygame.time.Clock()
ROAD_VERTICAL = Road(0, 0, SimulationGraphicConfig.ROAD_VERTICAL_LENGTH, SimulationGraphicConfig.road_vertical_image)
ROAD_HORIZONAL = Road(0, 0, SimulationGraphicConfig.ROAD_HORIZONTAL_LENGTH, SimulationGraphicConfig.road_horizontal_image)
INTERSECTION = Intersection(0, 0, SimulationGraphicConfig.intersection_image)
SIGNAL_ROAD_VERTICAL = TrafficSignal(SimulationGraphicConfig.SIGNAL_ROAD_VERTICAL_X_POS, SimulationGraphicConfig.SIGNAL_ROAD_VERTICAL_Y_POS, SimulationGraphicConfig.signal_red_image)
SIGNAL_ROAD_HORIZONTAL = TrafficSignal(SimulationGraphicConfig.SIGNAL_ROAD_HORIZONTAL_X_POS, SimulationGraphicConfig.SIGNAL_ROAD_HORIZONTAL_Y_POS, SimulationGraphicConfig.signal_green_image)

# Reset the simulation to play again if simulation_over is true
def resetSimulation():
    global vehicles, simulation_over
    # Reset vehicles to initial state
    vehicles = []
    simulation_over = False

# Draw the background image and all the vehicles
def redrawGameWindow():
    screen.blit(SimulationGraphicConfig.background_image, (0,0))
    ROAD_VERTICAL.draw(screen)
    ROAD_HORIZONAL.draw(screen)
    INTERSECTION.draw(screen)
    SIGNAL_ROAD_VERTICAL.draw(screen)
    SIGNAL_ROAD_HORIZONTAL.draw(screen)
    for vehicle in vehicles:
        vehicle.draw(screen)

    # Display timer
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f'Timer: {TIMER}', True, (255, 255, 255))
    real_time_text = font.render(f'Real Time: {REAL_TIME}', True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    screen.blit(real_time_text, (10, 40))

    pygame.display.update()

# Helper function to spawn a vehicle
def spawnVehicle():
    road_id = random.choice(["vertical_road", "horizontal_road"])
    lane_id = random.choice(["left_lane", "right_lane"])

    if road_id == "vertical_road":
        return Vehicle(SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_VELOCITY, SimulationGraphicConfig.car_north_image, road_id, lane_id)
    elif road_id == "horizontal_road":
        return Vehicle(SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT, SimulationGraphicConfig.VEHICLE_VELOCITY, SimulationGraphicConfig.car_west_image, road_id, lane_id)

# Main simulation loop
while running:
    if REAL_TIME == STOP_REAL_TIME:
        break

    # Create vehicle object
    if random.randint(1, 20) == 1: # Object has a 1/60 change of spawning every frame
        vehicles.append(spawnVehicle())

    # Update the vehicles
    for vehicle in vehicles[:]:
        vehicle.move()
        # Remove object if it goes off screen
        if vehicle.is_off_screen():
            vehicles.remove(vehicle)

    # Event handler, pygame.Quit means user closed the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.display.update()
    redrawGameWindow()
    real_time_per_frame = clock.tick(20) / 1000 # 20 fps
    REAL_TIME += real_time_per_frame
    TIMER += real_time_per_frame * SPEED_FACTOR
    print(real_time_per_frame)

pygame.quit()
