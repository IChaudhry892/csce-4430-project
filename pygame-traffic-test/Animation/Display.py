import pygame
from Graphics.SimulationGraphicConfig import SimulationGraphicConfig

from Road.Road import Road


class Display:
    def __init__(self, screen, images: dict):
        self.screen = screen
        self.images = images
        self.font = pygame.font.SysFont(None, 36)

    def redrawSimulationWindow(self, handler, timer: float, real_time: float, frame_count: int) -> None:
        """Redraw the entire simulation window with the current state"""
        self.screen.blit(self.images["background"], (0, 0))

        # Draw all animatable components in the scenario
        handler.drawAnimatables(self.screen)

        # Draw all simulatable components in the scenario (just vehicles for now)
        handler.drawSimulatables(self.screen)

        # HUD: Display virtual timer and real-time elapsed
        timer_text = self.font.render(f'Timer: {timer:.2f}', True, (255, 255, 255))
        real_time_text = self.font.render(f'Real Time: {real_time:.2f}', True, (255, 255, 255))
        frame_count_text = self.font.render(f'Frame: {frame_count}', True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))
        self.screen.blit(real_time_text, (10, 40))
        self.screen.blit(frame_count_text, (10, 70))

        # FOR DEBUGGING: draw per-road spawn rectangles and all vehicle rects (keeps visuals in sync)
        scenario = handler.scenario
        for comp in scenario.getComponents():
            if isinstance(comp, Road):
                # Draw vehicle rects for every lane (keeps them in-sync with current vehicle positions)
                for lane_id, lane_list in comp.vehicle_lanes.items():
                    for v in lane_list:
                        v_rect = pygame.Rect(int(v.x), int(v.y), int(v.width), int(v.height))
                        pygame.draw.rect(self.screen, (0, 255, 0), v_rect, 1)

                # Draw spawn rectangles for both lanes (these are off-screen since spawn point is outside)
                for lane_id in comp.vehicle_lanes.keys():
                    lane_key = comp.get_lane_key(lane_id)
                    sx, sy = SimulationGraphicConfig.LANE_STARTING_POSITIONS[lane_key]
                    spawn_rect = pygame.Rect(int(sx), int(sy), SimulationGraphicConfig.VEHICLE_WIDTH, SimulationGraphicConfig.VEHICLE_HEIGHT)
                    pygame.draw.rect(self.screen, (255, 0, 0), spawn_rect, 1)

        pygame.display.update()