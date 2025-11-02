from TrafficSignal.TrafficSignal import TrafficSignal
from SimulationToolbox.Simulatable import Simulatable
from SimulationToolbox.SimulationConfig import SimulationConfig

class SignalController(Simulatable):
    """Simple signal controller that toggles signals every fixed interval.

    Guarantees the two signals are always opposite colors: one Green, one Red.
    Uses simulation virtual time (delta_time passed to simulate).
    """

    def __init__(self, vertical_signal: TrafficSignal, horizontal_signal: TrafficSignal, scenario, virtual_time_elapsed: float = 0.0, toggle_interval: float = 15.0):
        self.vertical_signal = vertical_signal
        self.horizontal_signal = horizontal_signal
        # Store scenario so controller can inspect roads/queues
        self.scenario = scenario
        self.virtual_time_elapsed = virtual_time_elapsed
        self.toggle_interval = toggle_interval
        self.both_signals_red_duration = SimulationConfig.BOTH_SIGNALS_RED_DURATION * SimulationConfig.SPEED_FACTOR # 3 virtual seconds
        self.both_signals_red_remaining_time = 0.0
        self.post_toggle_vertical_state = None
        self.post_toggle_horizontal_state = None

        # Ensure initial states are opposite.
        # If both are the same (e.g., both Red), set vertical Green and horizontal Red by default.
        self.ensure_opposite_initial_signals()

    def ensure_opposite_initial_signals(self) -> None:
        vertical_signal_green = self.vertical_signal.is_green()
        horizontal_signal_green = self.horizontal_signal.is_green()
        if vertical_signal_green == horizontal_signal_green:  # both same (both green or both red)
            # Default to vertical=Green, horizontal=Red
            self.vertical_signal.setState("signal_green")
            self.horizontal_signal.setState("signal_red")

    def toggle_both_signals_red(self) -> None:
        """Set both signals to red state"""
        self.vertical_signal.setState("signal_red")
        self.horizontal_signal.setState("signal_red")

    def toggle_signals(self) -> None:
        # Flip: if vertical is green, make it red and horizontal green; else the opposite.
        # Make both signals red for a brief moment before switching

        if self.vertical_signal.is_green():
            # After both red duration, vertical -> red, horizontal -> green
            self.post_toggle_vertical_state = "signal_red"
            self.post_toggle_horizontal_state = "signal_green"
        else:
            # After both red duration, vertical -> green, horizontal -> red
            self.post_toggle_vertical_state = "signal_green"
            self.post_toggle_horizontal_state = "signal_red"

        # Set both signals to red for the specified duration
        self.toggle_both_signals_red()
        self.both_signals_red_remaining_time = self.both_signals_red_duration

    def simulate(self, delta_time: float) -> None:
        # If currently in both-red duration, count down
        if self.both_signals_red_remaining_time > 0.0:
            self.both_signals_red_remaining_time -= delta_time
            if self.both_signals_red_remaining_time <= 0.0:
                # Time to switch to the post-red states
                self.vertical_signal.setState(self.post_toggle_vertical_state)
                self.horizontal_signal.setState(self.post_toggle_horizontal_state)
                # Clear post states
                self.post_toggle_vertical_state = ""
                self.post_toggle_horizontal_state = ""
            return  # Skip toggling while in both-red duration


        # Update elapsed time since the current green started
        self.virtual_time_elapsed += delta_time

        # Adaptive toggling: prefer using scenario vehicle counts when available.
        # If `scenario` is not set on this controller, fall back to the original fixed-period behavior.
        if self.scenario is not None:
            # Count only vehicles currently stuck at the RED light (i.e., in 'waiting' state)
            red_wait_count = 0
            red_thresh = 0.0
            # Find which road is currently red and count vehicles waiting on that road
            if self.vertical_signal.is_green():
                # horizontal road is red
                red_road_id = self.horizontal_signal.getRoadID()
                red_thresh = SimulationConfig.HORIZONTAL_ROAD_CAR_THRESHOLD
            else:
                # vertical road is red
                red_road_id = self.vertical_signal.getRoadID()
                red_thresh = SimulationConfig.VERTICAL_ROAD_CAR_THRESHOLD

            for road_component in self.scenario.getRoads():
                if road_component.getRoadID() != red_road_id:
                    continue
                # road_component.vehicle_lanes is a dict of lane lists
                for lane_list in road_component.vehicle_lanes.values():
                    for vehicle in lane_list:
                        try:
                            if vehicle.state == SimulationConfig.VEHICLE_STATES["waiting"]:
                                red_wait_count += 1
                        except Exception:
                            # If vehicle lacks expected attributes, skip it
                            continue

            # Convert real-time durations into virtual seconds used by the controller (respect SPEED_FACTOR)
            min_green = SimulationConfig.MIN_GREEN_DURATION * SimulationConfig.SPEED_FACTOR
            max_green = SimulationConfig.MAX_GREEN_DURATION * SimulationConfig.SPEED_FACTOR

            # Force toggle if we've reached the absolute maximum green duration
            if self.virtual_time_elapsed >= max_green:
                print(f"\nMAX GREEN REACHED, TOGGLING SIGNALS: red_wait_count={red_wait_count}, time_elapsed={self.virtual_time_elapsed}\n")
                self.toggle_signals()
                self.virtual_time_elapsed = 0.0
            # If we've reached the minimum green, decide based on red-queue length
            elif self.virtual_time_elapsed >= min_green:
                # Switch when the red side has more waiting vehicles than its threshold
                if red_wait_count > red_thresh:
                    print(f"\nTOGGLING SIGNALS DUE TO RED QUEUE: red_wait_count={red_wait_count}, time_elapsed={self.virtual_time_elapsed}\n")
                    self.toggle_signals()
                    self.virtual_time_elapsed = 0.0
            # else: still within mandatory minimum green, do nothing
        else:
            # Fallback: keep previous fixed-interval behavior when scenario isn't available
            if self.virtual_time_elapsed >= self.toggle_interval:
                self.toggle_signals()
                self.virtual_time_elapsed = 0.0