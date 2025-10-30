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
        self.virtual_time_elapsed = virtual_time_elapsed
        self.toggle_interval = toggle_interval
        self.both_signals_red_duration = SimulationConfig.BOTH_SIGNALS_RED_DURATION * SimulationConfig.SPEED_FACTOR # 3 virtual seconds
        self.both_signals_red_remaining_time = 0.0
        self.post_toggle_vertical_state = ""
        self.post_toggle_horizontal_state = ""

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
        # delta_time /= SimulationConfig.SPEED_FACTOR  # Adjust for simulation speed

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
                self.both_signals_red_remaining_time = 0.0
            return  # Skip toggling while in both-red duration


        # Update elapsed time until next toggle
        self.virtual_time_elapsed += delta_time
        # Toggle whenever we cross a multiple of the period
        while self.virtual_time_elapsed >= self.toggle_interval:  # Check if 15 virtual seconds have passed
            self.toggle_signals()
            self.virtual_time_elapsed -= self.toggle_interval  # reset elapsed back to 0