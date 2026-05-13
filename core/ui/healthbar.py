import pygame
from entities.player import Player
    

class HealthBar:
    def __init__(self, player: Player):
        self.max_health = player.max_hp
        self.current_health = player.hp

    def update(self, player: Player):
        if player.is_alive == True:
            self.current_health = player.hp
            self.max_health = player.max_hp
        else:
            self.current_health = 0
            self.max_health = player.max_hp

    def draw(self, surface, x, y, width, height, font):
        health_percentage = self.get_health_percentage()
        health_bar_width = int(width * (health_percentage / 100))

        # Draw background
        pygame.draw.rect(surface, "black", (x, y, width, height))
        # Draw current health
        pygame.draw.rect(surface, (0, 190, 30), (x, y, health_bar_width, height))
        # Draw border
        pygame.draw.rect(surface, "black", (x, y, width, height), 2)
        # Draw health text
        health_text_outline = font[1].render(f"{int(health_percentage)}", True, "black")
        health_text = font[0].render(f"{int(health_percentage)}", True, "white")
        text_rect = health_text.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(health_text_outline, text_rect)
        surface.blit(health_text, text_rect)

    def get_health_percentage(self):
        return (self.current_health / self.max_health) * 100