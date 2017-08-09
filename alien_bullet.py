import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
	def __init__ (self, ai_settings, screen):
		super().__init__()
		self.screen = screen 
			
		self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width, ai_settings.alien_bullet_height)
		self.y = float(self.rect.y)
		self.screen_rect = self.screen.get_rect()
		
		self.color = ai_settings.alien_bullet_color
		self.speed_factor = ai_settings.alien_bullet_speed_factor
		
	def update(self):
		"""Move the bullet down the screen"""
		#Update the decimal position of the bullet
		self.y += self.speed_factor
		#Update the rect position: for actual display of bullet position in integer form
		self.rect.y = self.y
	
	def draw_alien_bullet(self):
		"""Draw the bullet to the screen"""
		#fills the part of the screen defined by the bullet's rect with the color defined by self.color
		pygame.draw.rect(self.screen, self.color, self.rect)
