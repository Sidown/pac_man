import pygame


class Visualizer():
    """"""
    def __init__(self)-> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        WIDTH=1280
        HEIGHT=720
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.screen.fill("white")
        self.header_text = pygame.font.SysFont("Arial", 42)
        pygame.display.update()

    def run(self) -> None:
        """The full game visualisation"""
        background = pygame.Surface(self.screen.get_size())
        background.fill((255,255,255))
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            text = self.header_text.render("PAC-MAN", True, "blue")
            background.blit(text, (0, 0))
        pygame.quit()

    def _show_main_menu(self) -> None:
        pass


    def _show_game(self) -> None:
        pass

    def _show_game_over(self) -> None:
        pass
