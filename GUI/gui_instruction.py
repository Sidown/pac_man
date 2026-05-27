import pygame
from pygame import Surface
from pygame.event import Event

from .scene import Scene
from .ui_elements.button import Button
from .ui_elements.theme import Theme


class InstructionScene(Scene):
    """
    Scene to show the game rules and keyboard controls
    """

    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        """
        initialise the instruction scene
        arguments:
        screen -> pygame surface
        theme -> the visual theme
        width_height -> width and height of the window in pixels
        """
        self.current_scene = "instruction"
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height

        self.btn_back_to_menu = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "Back to Main Menu",
            self._back_to_menu_callback,
            (50, 50),
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

    def _back_to_menu_callback(self) -> None:
        """
        Return to the main menu
        """
        self.current_scene = "main_menu"

    def handle_events(self, events: list[Event]) -> str:
        """
        Process the envents list and return the next scene to display
        arguments:
        events -> list of events to process
        return value:
        the next scene to display
        """
        self.current_scene = "instruction"
        for event in events:
            self.btn_back_to_menu.handle_event(event)
        return self.current_scene

    def update(self) -> None:
        """
        frame per frame logic, not needed in this scene
        """
        pass

    def _print_rules(self) -> None:
        """
        Render the game rules
        """
        line_height = 0
        instruction = []
        instruction.append(
            pygame.font.Font(self.theme.font_path, 26).render(
                "INSTRUCTION:", False, self.theme.title_color
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "You are PacMan.", False, self.theme.text_color
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "Your Goal is to eat all the PacGum of the 10 levels",
                False,
                self.theme.text_color,
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "of the game without being eaten by any Ghost.",
                False,
                self.theme.text_color,
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "You have 3 lives, and there is 4 Ghost ",
                False,
                self.theme.text_color,
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "comming for you (Blinky, Inky, Pinky and Clyde).",
                False,
                self.theme.text_color,
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "Each PacGum you eat earn you some points.",
                False,
                self.theme.text_color,
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "If you eat a SuperPacGum,",
                False,
                self.theme.text_color,
            )
        )
        instruction.append(
            pygame.font.Font(self.theme.font_path, 18).render(
                "Ghosts became vulnarable for a short amount of time.",
                False,
                self.theme.text_color,
            )
        )
        for text in instruction:
            self.screen.blit(text, (200, 120 + line_height))
            line_height += 38

    def _print_cmd(self) -> None:
        """
        Draw the keyboard control
        """
        # UP
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2, 600 - 86, 80, 80),
        )
        up_text = pygame.font.SysFont("Arial", 42).render(
            "↑",
            False,
            self.theme.text_color,
        )
        self.screen.blit(up_text, (self.WIDTH // 2 + 30, 600 - 70))

        # LEFT
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2 - 86, 600, 80, 80),
        )
        left_text = pygame.font.SysFont("Arial", 42).render(
            "←",
            False,
            self.theme.text_color,
        )
        self.screen.blit(left_text, (self.WIDTH // 2 - 65, 600 + 15))
        # DOWN
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2, 600, 80, 80),
        )
        down_text = pygame.font.SysFont("Arial", 42).render(
            "↓",
            False,
            self.theme.text_color,
        )
        self.screen.blit(down_text, (self.WIDTH // 2 + 30, 600 + 15))
        # RIGHT
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2 + 86, 600, 80, 80),
        )
        right_text = pygame.font.SysFont("Arial", 42).render(
            "→",
            False,
            self.theme.text_color,
        )
        self.screen.blit(right_text, (self.WIDTH // 2 + 100, 600 + 15))

        # SPACE
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (25, 500, 400, 60),
        )
        space_text = pygame.font.Font(self.theme.font_path, 18).render(
            "Press SPACE to pause the game",
            False,
            self.theme.text_color,
        )
        self.screen.blit(space_text, (35, 520))

    def draw(self) -> None:
        """
        Render the instruction screen
        """
        self.screen.fill(self.theme.background_color)
        self.btn_back_to_menu.draw(self.screen)
        self._print_rules()
        self._print_cmd()
