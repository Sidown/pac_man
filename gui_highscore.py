from pygame import Surface

from theme import Button, Theme


class HighScoreScene:
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        self.current_scene = "high_score"
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
        self.current_scene = "high_score"
        for event in events:
            self.btn_back_to_menu.handle_event(event)
        return self.current_scene

    def update(self):
        pass

    def draw(self):
        print(self.current_scene)
        self.screen.fill(self.theme.background_color)
        self.btn_back_to_menu.draw(self.screen)
