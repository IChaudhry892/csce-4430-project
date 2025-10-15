import pygame
import random

pygame.init()
pygame.display.set_caption("Traffic Simulation Test")

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the images
left_facing_car_image = pygame.image.load("left-facing-car.png")
background_image = pygame.image.load("background-image.png")

# Object properties
class Vehicle(object):
    def __init__(self, x, y, velocity, image):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.velocity = velocity
        self.image = image

    def move(self):
        self.x += self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Simulation variables
vehicles = []
simulation_over = False
running = True
clock = pygame.time.Clock()

# Reset the simulation to play again if simulation_over is true
def resetSimulation():
    global vehicles, simulation_over
    # Reset vehicles to initial state
    vehicles = []
    simulation_over = False

# Draw the background image and all the vehicles
def redrawGameWindow():
    screen.blit(background_image, (0,0))
    for vehicle in vehicles:
        vehicle.draw(screen)

    pygame.display.update()

# Main simulation loop
while running:
    # Create vehicle object
    if random.randint(1, 60) == 1: # Object has a 1/60 change of spawning every frame
        y_pos = SCREEN_HEIGHT // 2
        vehicleVelocity = 5
        vehicles.append(Vehicle(0, y_pos, vehicleVelocity, left_facing_car_image))

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