import pygame
import random

pygame.init()
pygame.display.set_caption("Traffic Simulation Test")

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Simulation constants
ROAD_WIDTH = 160
VEHICLE_WIDTH = 80
VEHICLE_HEIGHT = 60
VEHICLE_VELOCITY = 40
TRAFFIC_SIGNAL_WIDTH = 80
TRAFFIC_SIGNAL_HEIGHT = 106
LANE_STARTING_POSITIONS = {
    "vertical_road_left_lane": [(SCREEN_WIDTH // 2) - (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2), SCREEN_HEIGHT],
    "vertical_road_right_lane": [SCREEN_WIDTH // 2 + (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2), SCREEN_HEIGHT],
    "horizontal_road_left_lane": [SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2)],
    "horizontal_road_right_lane": [SCREEN_WIDTH, (SCREEN_HEIGHT // 2) - (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2)]
}
SPEED_FACTOR = 3.0      # Simulation runs 3x faster than real time
REAL_TIME = 0.0         # Real-time elapsed in seconds
TIMER = 0.0             # Virtual time elapsed in seconds
STOP_REAL_TIME = 30.0   # Stop simulation after 30 real-time seconds

# Load the images
car_west_image = pygame.image.load("Graphics/VehicleGraphics/car-west.png")
car_north_image = pygame.image.load("Graphics/VehicleGraphics/car-north.png")
background_image = pygame.image.load("Graphics/BackgroundGraphic/background.png")

road_vertical_image = pygame.image.load("Graphics/RoadGraphics/road-vertical.png")
road_horizontal_image = pygame.image.load("Graphics/RoadGraphics/road-horizontal.png")
intersection_image = pygame.image.load("Graphics/IntersectionGraphic/intersection.png")

signal_green_image = pygame.image.load("Graphics/SignalGraphics/signal-green.png")
signal_yellow_image = pygame.image.load("Graphics/SignalGraphics/signal-yellow.png")
signal_red_image = pygame.image.load("Graphics/SignalGraphics/signal-red.png")

# Object properties
class Vehicle(object):
    def __init__(self, width, height, velocity, image, road_id, lane_id):
        self.width = width
        self.height = height
        self.velocity = velocity
        self.image = image
        self.road_id = road_id
        self.lane_id = lane_id
        self.x, self.y = LANE_STARTING_POSITIONS[f"{road_id}_{lane_id}"]

    def move(self):
        if self.road_id == "vertical_road":
            self.y -= self.velocity
        elif self.road_id == "horizontal_road":
            self.x -= self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x < 0 - self.width or self.y < 0 - self.width

class Road(object):
    def __init__(self, x, y, length, image):
        self.x = x
        self.y = y
        self.width = ROAD_WIDTH
        self.length = length
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Intersection(object):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = ROAD_WIDTH
        self.height = ROAD_WIDTH
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class TrafficSignal(object):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = TRAFFIC_SIGNAL_WIDTH
        self.height = TRAFFIC_SIGNAL_HEIGHT
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Simulation variables
vehicles = []
simulation_over = False
running = True
clock = pygame.time.Clock()
ROAD_VERTICAL = Road(0, 0, SCREEN_HEIGHT, road_vertical_image)
ROAD_HORIZONAL = Road(0, 0, SCREEN_WIDTH, road_horizontal_image)
INTERSECTION = Intersection(0, 0, intersection_image)
SIGNAL_ROAD_VERTICAL = TrafficSignal(730, 168, signal_red_image)
SIGNAL_ROAD_HORIZONTAL = TrafficSignal(472, 448, signal_green_image)

# Reset the simulation to play again if simulation_over is true
def resetSimulation():
    global vehicles, simulation_over
    # Reset vehicles to initial state
    vehicles = []
    simulation_over = False

# Draw the background image and all the vehicles
def redrawGameWindow():
    screen.blit(background_image, (0,0))
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
        return Vehicle(VEHICLE_HEIGHT, VEHICLE_WIDTH, VEHICLE_VELOCITY, car_north_image, road_id, lane_id)
    elif road_id == "horizontal_road":
        return Vehicle(VEHICLE_WIDTH, VEHICLE_HEIGHT, VEHICLE_VELOCITY, car_west_image, road_id, lane_id)

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
