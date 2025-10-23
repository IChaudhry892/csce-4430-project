import pygame
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig


class Display:
    def __init__(self, screen, images: dict):
        self.screen = screen
        self.images = images
        self.font = pygame.font.SysFont(None, 36)

    def redrawSimulationWindow(self, handler, timer: float, real_time: float) -> None:
        """Redraw the entire simulation window with the current state"""
        self.screen.blit(self.images["background"], (0, 0))

        # Draw all animatable components in the scenario
        handler.drawAnimatables(self.screen)

        # Draw all simulatable components in the scenario (just vehicles for now)
        handler.drawSimulatables(self.screen)

        # HUD: Display virtual timer and real-time elapsed
        timer_text = self.font.render(f'Timer: {timer}', True, (255, 255, 255))
        real_time_text = self.font.render(f'Real Time: {real_time}', True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))
        self.screen.blit(real_time_text, (10, 40))

        pygame.display.update()