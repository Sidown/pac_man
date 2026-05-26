import pygame
from pygame import Surface

from theme import Button, Theme
from checkbox import Checkbox


class CheatScene:
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int], cheat
    ) -> None:
        self.cheat = cheat
        self.current_scene = "cheat"
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.btn_back_to_menu = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "Back To Game",
            self._back_to_game_callback,
            (50, 50),
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )
        self.invincibility_checkbox = Checkbox(self.screen, self.WIDTH // 2.5,
                                               self.HEIGHT / 4, 1,
                                               caption="Invincibility")
        self.freeze_checkbox = Checkbox(self.screen, self.WIDTH // 2.5,
                                               self.HEIGHT / 2.5, 2,
                                               caption="Freeze Ghosts")
        self.pacgum_checkbox = Checkbox(self.screen, self.WIDTH // 2.5,
                                               self.HEIGHT / 1.8, 3,
                                               caption="Skip Levels")

    def _back_to_game_callback(self) -> None:
        self.current_scene = "game"

    def handle_events(self, events) -> str:
        self.current_scene = "cheat"
        for event in events:
            if self.invincibility_checkbox.update_checkbox(event):
                self._invincibility(self.cheat)
            if self.freeze_checkbox.update_checkbox(event):
                self._freeze_ghost(self.cheat)
            if self.pacgum_checkbox.update_checkbox(event):
                self._skip_level(self.cheat)
            self.btn_back_to_menu.handle_event(event)
        return self.current_scene

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.theme.background_color)
        self.btn_back_to_menu.draw(self.screen)
        self.invincibility_checkbox.draw()
        self.freeze_checkbox.draw()
        self.pacgum_checkbox.draw()

    def _invincibility(self, cheat):
        if self.invincibility_checkbox.checked:
            cheat.invincible = True
            print(f"invincibility checked, value: {cheat.invincible}")
        else:
            cheat.invincible = False
            print(f"invincibility unchecked, value: {cheat.invincible}")

    def _freeze_ghost(self, cheat):
        if self.freeze_checkbox.checked:
            cheat.freeze = True
            print(f"freeze checked, value: {cheat.freeze}")
        else:
            cheat.freeze = False
            print(f"freeze unchecked, value: {cheat.freeze}")

    def _skip_level(self, cheat):
        if self.pacgum_checkbox.checked:
            cheat.skip = True
            print(f"skip checked, value: {cheat.skip}")
        else:
            cheat.skip = False
            print(f"skip unchecked, value: {cheat.skip}")

