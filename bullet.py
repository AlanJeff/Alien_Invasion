import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	def __init__ (self, ai_settings, screen, ship):
		"""Create a bullet object at the ship's current position"""
		super().__init__()
		self.screen = screen 
		
		#Create a bullet rect from scratch, initialized position at (0,0)
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		
		#Locate bullet to ship position
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top 
		
		#Store the bullet's position as a decimal value 
		#You need to store decimal value in a separate variable bcoz self.rect cannot store decimal
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
	
	def update(self):
		"""Move the bullet up the screen"""
		#Update the decimal position of the bullet
		self.y -= self.speed_factor
		#Update the rect position: for actual display of bullet position in integer form
		self.rect.y = self.y
	
	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		#fills the part of the screen defined by the bullet's rect with the color defined by self.color
		pygame.draw.rect(self.screen, self.color, self.rect)
