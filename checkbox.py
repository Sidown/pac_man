import pygame
from pygame import Surface


class Checkbox:
    def __init__(self, surface: Surface, x: int, y: int, idnum: int,
                 color: tuple[int, int, int] = (230, 230, 230),
                 caption: str = "",
                 outline_color: tuple[int, int, int] = (0, 0, 0),
                 check_color: tuple[int, int, int] = (40, 91, 232),
                 font_size: int = 36,
                 font_color: tuple[int, int, int] = (230, 230, 230),
                 text_offset: tuple[int, int, int] = (42, 1),
                 font: str = "assets/fonts/Retro Gaming.ttf"
                 ) -> None:
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.outline_color = outline_color
        self.check_color = check_color
        self.font_size = font_size
        self.font_color = font_color
        self.text_offset = text_offset
        self.ft = font
        self.idnum = idnum
        self.checkbox_obj = pygame.Rect(self.x, self.y, 36, 36)
        self.checked_obj = pygame.Rect(self.x + 5, self.y + 5, 26, 26)
        self.checkbox_outline = self.checkbox_obj.copy()
        self.checked = False

    def _draw_button_text(self) -> None:
        self.font = pygame.font.SysFont(self.ft, self.font_size)
        self.font_surf = self.font.render(self.caption, True, self.font_color)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.text_offset[0],
                         self.y + self.text_offset[1])
        self.surfac.blit(self.font_surf, self.font_pos)

    def draw(self) -> None:
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.outline_color,
                             self.checkbox_outline, 1)
            pygame.draw.rect(self.surface, self.check_color,
                             self.checked_obj, 14)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.outline_color,
                             self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self) -> None:
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object: pygame.event.Event) -> bool:
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)
            return True
        return False
