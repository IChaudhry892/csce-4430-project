import pygame

class SimulationGraphicConfig:
    # Screen Dimensions
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # Asset paths (as strings)
    CAR_WEST_PATH = "Graphics/VehicleGraphics/car-west.png"
    CAR_NORTH_PATH = "Graphics/VehicleGraphics/car-north.png"
    BACKGROUND_PATH = "Graphics/BackgroundGraphic/background.png"

    ROAD_VERTICAL_PATH = "Graphics/RoadGraphics/road-vertical.png"
    ROAD_HORIZONTAL_PATH = "Graphics/RoadGraphics/road-horizontal.png"
    INTERSECTION_PATH = "Graphics/IntersectionGraphic/intersection.png"

    SIGNAL_GREEN_PATH = "Graphics/SignalGraphics/signal-green.png"
    SIGNAL_YELLOW_PATH = "Graphics/SignalGraphics/signal-yellow.png"
    SIGNAL_RED_PATH = "Graphics/SignalGraphics/signal-red.png"

    def load_images():
        """Load all images used in the simulation"""
        images = {}
        images["car_west"] = pygame.image.load(SimulationGraphicConfig.CAR_WEST_PATH)
        images["car_north"] = pygame.image.load(SimulationGraphicConfig.CAR_NORTH_PATH)
        images["background"] = pygame.image.load(SimulationGraphicConfig.BACKGROUND_PATH)
        images["road_vertical"] = pygame.image.load(SimulationGraphicConfig.ROAD_VERTICAL_PATH)
        images["road_horizontal"] = pygame.image.load(SimulationGraphicConfig.ROAD_HORIZONTAL_PATH)
        images["intersection"] = pygame.image.load(SimulationGraphicConfig.INTERSECTION_PATH)
        images["signal_green"] = pygame.image.load(SimulationGraphicConfig.SIGNAL_GREEN_PATH)
        images["signal_yellow"] = pygame.image.load(SimulationGraphicConfig.SIGNAL_YELLOW_PATH)
        images["signal_red"] = pygame.image.load(SimulationGraphicConfig.SIGNAL_RED_PATH)
        return images

    # Road Constants
    ROAD_WIDTH = 160
    ROAD_VERTICAL_LENGTH = SCREEN_HEIGHT
    ROAD_HORIZONTAL_LENGTH = SCREEN_WIDTH

    # Vehicle Constants
    VEHICLE_WIDTH = 80
    VEHICLE_HEIGHT = 60
    VERTICAL_ROAD_VEHICLE_START_Y = SCREEN_HEIGHT
    HORIZONTAL_ROAD_VEHICLE_START_X = SCREEN_WIDTH
    LANE_STARTING_POSITIONS = {
        "vertical_road_left_lane": [(SCREEN_WIDTH // 2) - (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2), VERTICAL_ROAD_VEHICLE_START_Y],
        "vertical_road_right_lane": [SCREEN_WIDTH // 2 + (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2), VERTICAL_ROAD_VEHICLE_START_Y],
        "horizontal_road_left_lane": [HORIZONTAL_ROAD_VEHICLE_START_X, (SCREEN_HEIGHT // 2) + (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2)],
        "horizontal_road_right_lane": [HORIZONTAL_ROAD_VEHICLE_START_X, (SCREEN_HEIGHT // 2) - (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2)]
    }
    VEHICLE_SPAWN_GAP_METERS = 0.5  # Minimum gap between spawned vehicles in meters

    # Traffic Signal Constants
    TRAFFIC_SIGNAL_WIDTH = 80
    TRAFFIC_SIGNAL_HEIGHT = 106
    SIGNAL_ROAD_VERTICAL_X_POS = 730
    SIGNAL_ROAD_VERTICAL_Y_POS = 168
    SIGNAL_ROAD_HORIZONTAL_X_POS = 472
    SIGNAL_ROAD_HORIZONTAL_Y_POS = 448