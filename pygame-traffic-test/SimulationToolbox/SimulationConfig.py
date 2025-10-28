class SimulationConfig:
    VEHICLE_VELOCITY_MPS = 4    # 40 km/h = 11.11 m/s
    PIXELS_PER_METER = 10   # 10 pixels = 1 meter, 0.1 meter = 10 pixels

    FPS = 20                # Frames per second
    SPEED_FACTOR = 3.0      # Simulation runs 3x faster than real time
    REAL_TIME = 0.0         # Real-time elapsed in seconds
    TIMER = 0.0             # Virtual time elapsed in seconds
    FRAME_COUNT = 0         # Frame counter
    STOP_REAL_TIME = 30.0   # Stop simulation after 30 real-time seconds

    ROAD_IDS = {"Vertical Road": "vertical_road", "Horizontal Road": "horizontal_road"}
    TRAFFIC_INTENSITIES = {"high": .15, "medium": 0.10, "low": 0.05} # Chance of spawning a vehicle per virtual minute per road
    TRAFFIC_SIGNAL_STATES = {"Red": "signal_red", "Green": "signal_green"}
    VEHICLE_STATES = {"moving": "moving", "waiting": "waiting"}