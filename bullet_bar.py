import pygame
from pygame.sprite import Sprite

class BulletBar(Sprite):
	def __init__ (self, ai_settings, screen):
		"""Create a bullet bar"""
		super().__init__()
		self.screen = screen 
		
		#Create a bullet bar rect from scratch, initialized position at (0,0)
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_bar_width, ai_settings.bullet_bar_height)
		self.color = ai_settings.bullet_bar_color
	
	def draw_bullet(self):
		"""Draw the bullet bar to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)
