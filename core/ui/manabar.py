import pygame
from entities.player import Player
    

class ManaBar:
    def __init__(self, player: Player):
        self.mana = player.mana
        self.max_mana = player.max_mana

    def update(self, player: Player):
        self.mana = player.mana
        self.max_mana = player.max_mana

    def draw(self, surface, x, y, width, height, font):
        mana_percentage = self.get_mana_percentage()
        mana_bar_width = int(width * (mana_percentage / 100))

        # Draw background
        pygame.draw.rect(surface, "black", (x, y, width, height))
        # Draw current mana
        pygame.draw.rect(surface, (17, 17, 150), (x, y, mana_bar_width, height))
        # Draw border
        pygame.draw.rect(surface, "black", (x, y, width, height), 2)
        # Draw mana text
        mana_text_outline = font[1].render(f"{int(mana_percentage)}", True, "black")
        mana_text = font[0].render(f"{int(mana_percentage)}", True, "white")
        text_rect = mana_text.get_rect(center=((x + width // 2), y + height // 2))
        surface.blit(mana_text_outline, text_rect)
        surface.blit(mana_text, text_rect)

    def get_mana_percentage(self):
        return (self.mana / self.max_mana) * 100