import pygame
import random

pygame.init()
pygame.display.set_caption("Traffic Simulation Test")

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ROAD_WIDTH = 160
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the images
car_west_image = pygame.image.load("pygame-traffic-test/Graphics/VehicleGraphics/car-west.png")
car_north_image = pygame.image.load("pygame-traffic-test/Graphics/VehicleGraphics/car-north.png")
background_image = pygame.image.load("pygame-traffic-test/Graphics/BackgroundGraphic/background.png")

road_vertical_image = pygame.image.load("pygame-traffic-test/Graphics/RoadGraphics/road-vertical.png")
road_horizontal_image = pygame.image.load("pygame-traffic-test/Graphics/RoadGraphics/road-horizontal.png")
intersection_image = pygame.image.load("pygame-traffic-test/Graphics/IntersectionGraphic/intersection.png")

signal_green_image = pygame.image.load("pygame-traffic-test/Graphics/SignalGraphics/signal-green.png")
signal_yellow_image = pygame.image.load("pygame-traffic-test/Graphics/SignalGraphics/signal-yellow.png")
signal_red_image = pygame.image.load("pygame-traffic-test/Graphics/SignalGraphics/signal-red.png")

# Object properties
class Vehicle(object):
    def __init__(self, x, y, velocity, image):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 60
        self.velocity = velocity
        self.image = image

    def move(self):
        self.x += self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

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
        self.width = 80
        self.height = 106
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

    pygame.display.update()

# Main simulation loop
while running:
    # Create vehicle object
    if random.randint(1, 60) == 1: # Object has a 1/60 change of spawning every frame
        y_pos = SCREEN_HEIGHT // 2
        vehicleVelocity = 5
        vehicles.append(Vehicle(0, y_pos, vehicleVelocity, car_west_image))

    # Update the vehicles
    for vehicle in vehicles[:]:
        vehicle.move()
        # Remove object if it goes off screen
        if vehicle.x > SCREEN_WIDTH:
            vehicles.remove(vehicle)

    # Event handler, pygame.Quit means user closed the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.display.update()
    redrawGameWindow()
    clock.tick(60)

pygame.quit()