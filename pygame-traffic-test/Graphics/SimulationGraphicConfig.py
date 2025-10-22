import pygame

class SimulationGraphicConfig:
    # Screen Dimensions
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # Simulatable Object Images
    car_west_image = pygame.image.load("Graphics/VehicleGraphics/car-west.png")
    car_north_image = pygame.image.load("Graphics/VehicleGraphics/car-north.png")
    background_image = pygame.image.load("Graphics/BackgroundGraphic/background.png")

    road_vertical_image = pygame.image.load("Graphics/RoadGraphics/road-vertical.png")
    road_horizontal_image = pygame.image.load("Graphics/RoadGraphics/road-horizontal.png")
    intersection_image = pygame.image.load("Graphics/IntersectionGraphic/intersection.png")

    signal_green_image = pygame.image.load("Graphics/SignalGraphics/signal-green.png")
    signal_yellow_image = pygame.image.load("Graphics/SignalGraphics/signal-yellow.png")
    signal_red_image = pygame.image.load("Graphics/SignalGraphics/signal-red.png")

    # Road Constants
    ROAD_WIDTH = 160
    ROAD_VERTICAL_LENGTH = SCREEN_HEIGHT
    ROAD_HORIZONTAL_LENGTH = SCREEN_WIDTH

    # Vehicle Constants
    VEHICLE_WIDTH = 80
    VEHICLE_HEIGHT = 60
    VEHICLE_VELOCITY = 40 # THIS BELONGS IN ANOTHER FILE
    LANE_STARTING_POSITIONS = {
        "vertical_road_left_lane": [(SCREEN_WIDTH // 2) - (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2), SCREEN_HEIGHT],
        "vertical_road_right_lane": [SCREEN_WIDTH // 2 + (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2), SCREEN_HEIGHT],
        "horizontal_road_left_lane": [SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2)],
        "horizontal_road_right_lane": [SCREEN_WIDTH, (SCREEN_HEIGHT // 2) - (ROAD_WIDTH // 4) - (VEHICLE_HEIGHT // 2)]
    }

    # Traffic Signal Constants
    TRAFFIC_SIGNAL_WIDTH = 80
    TRAFFIC_SIGNAL_HEIGHT = 106
    SIGNAL_ROAD_VERTICAL_X_POS = 730
    SIGNAL_ROAD_VERTICAL_Y_POS = 168
    SIGNAL_ROAD_HORIZONTAL_X_POS = 472
    SIGNAL_ROAD_HORIZONTAL_Y_POS = 448