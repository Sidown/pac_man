import pygame
from pygame import Surface

from theme import Button, Theme


class InstructionScene:
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
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
        self.current_scene = "main_menu"

    def handle_events(self, events) -> str:
        self.current_scene = "instruction"
        for event in events:
            self.btn_back_to_menu.handle_event(event)
        return self.current_scene

    def update(self):
        pass

    def _print_rules(self) -> None:
        line_height = 0
        instruction = []
        instruction.append(
            pygame.font.Font(self.theme.font_path, 26).render(
                "INSTRUCTION:", False, self.theme.text_color
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
        # UP
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2, 600 - 86, 80, 80),
        )
        up_text = pygame.font.Font(self.theme.font_path, 18).render(
            "Upper arrow to go up",
            False,
            self.theme.text_color,
        )
        self.screen.blit(up_text, (self.WIDTH // 2, 600 - 86 + 40))

        # LEFT
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2 - 86, 600, 80, 80),
        )
        left_text = pygame.font.Font(self.theme.font_path, 18).render(
            "Left arrow to go left",
            False,
            self.theme.text_color,
        )
        self.screen.blit(left_text, (self.WIDTH // 2 - 86 - 170, 600 + 40))
        # DOWN
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2, 600, 80, 80),
        )
        down_text = pygame.font.Font(self.theme.font_path, 18).render(
            "Down arrow to go down",
            False,
            self.theme.text_color,
        )
        self.screen.blit(down_text, (self.WIDTH // 2, 600 + 80))
        # RIGHT
        pygame.draw.rect(
            self.screen,
            self.theme.game_background_color,
            (self.WIDTH // 2 + 86, 600, 80, 80),
        )
        right_text = pygame.font.Font(self.theme.font_path, 18).render(
            "Right arrow to go right",
            False,
            self.theme.text_color,
        )
        self.screen.blit(right_text, (self.WIDTH // 2 + 86, 600 + 40))

    def draw(self):
        self.screen.fill(self.theme.background_color)
        self.btn_back_to_menu.draw(self.screen)
        self._print_rules()
        self._print_cmd()
