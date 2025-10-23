class SimulationConfig:
    # VEHICLE_VELOCITY = 40
    VEHICLE_VELOCITY_MPS = 11.11    # 40 km/h = 11.11 m/s
    PIXELS_PER_METER = 10   # 10 pixels = 1 meter, 0.1 meter = 10 pixels

    FPS = 20                # Frames per second
    SPEED_FACTOR = 3.0      # Simulation runs 3x faster than real time
    REAL_TIME = 0.0         # Real-time elapsed in seconds
    TIMER = 0.0             # Virtual time elapsed in seconds
    STOP_REAL_TIME = 30.0   # Stop simulation after 30 real-time seconds