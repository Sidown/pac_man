import pygame


class Visualizer():
    """"""
    def __init__(self)-> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        WIDTH=1280
        HEIGHT=720
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill("purple")
        pygame.display.update()
        self.running = True


    def run(self) -> None:
        """The full game visualisation"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill("white")
        pygame.quit()

    def _show_main_menu(self) -> None:
        pass


    def _show_game(self) -> None:
        pass

    def _show_game_over(self) -> None:
        pass
