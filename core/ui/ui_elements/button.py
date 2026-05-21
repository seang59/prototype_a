import pygame


class Button:
    def __init__(self, x, y, width, height, text: str, on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.on_click = on_click

    def click(self):
        self.on_click()

    def update(self, mouse_pos, mouse_pressed):
        if self.is_hovered(mouse_pos) and mouse_pressed:  # Left mouse button
            self.click()

    def draw(self, surface, font):
        color = (200, 200, 200) if self.is_hovered(pygame.mouse.get_pos()) else (150, 150, 150)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height