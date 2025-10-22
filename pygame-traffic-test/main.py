from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

from Animation.Display import Display
from SimulationToolbox.Scenario import Scenario
from SimulationToolbox.ScenarioHandler import ScenarioHandler

import pygame

pygame.init()

# Create the window
screen = pygame.display.set_mode((SimulationGraphicConfig.SCREEN_WIDTH, SimulationGraphicConfig.SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Traffic Simulation Test")

# Load images
images = SimulationGraphicConfig.load_images()

# Create Display object for rendering the simulation
display = Display(screen, images)

# Create Scenario and ScenarioHandler objects and run the simulation
scenario = Scenario(images)
handler = ScenarioHandler(scenario, display)
handler.runSimulation()

pygame.quit()