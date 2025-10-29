class SimulationConfig:
    VEHICLE_VELOCITY_MPS = 11.11    # 40 km/h = 11.11 m/s
    PIXELS_PER_METER = 10   # 10 pixels = 1 meter, 0.1 meter = 10 pixels

    FPS = 20                # Frames per second
    SPEED_FACTOR = 3.0      # Simulation runs 3x faster than real time
    REAL_TIME = 0.0         # Real-time elapsed in seconds
    TIMER = 0.0             # Virtual time elapsed in seconds
    FRAME_COUNT = 0         # Frame counter
    STOP_REAL_TIME = 30.0   # Stop simulation after 30 real-time seconds

    MIN_GREEN_DURATION = 5.0   # Minimum green signal duration in real-time seconds
    MAX_GREEN_DURATION = 10.0  # Maximum green signal duration in real-time seconds
    VERTICAL_ROAD_CAR_THRESHOLD = 4.0 # Max number of cars behind vertical road intersection to not change signal
    HORIZONTAL_ROAD_CAR_THRESHOLD = 7.0 # Max number of cars behind horizontal road intersection to not change signal
    BOTH_SIGNALS_RED_DURATION = 1.0  # Duration when both signals are red in real-time seconds

    ROAD_IDS = {"Vertical Road": "vertical_road", "Horizontal Road": "horizontal_road"}
    TRAFFIC_INTENSITIES = {"high": 0.15, "medium": 0.10, "low": 0.05} # Chance of spawning a vehicle per virtual minute per road
    TRAFFIC_SIGNAL_STATES = {"Red": "signal_red", "Green": "signal_green"}
    VEHICLE_STATES = {"moving": "moving", "waiting": "waiting"}