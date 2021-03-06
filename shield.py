import pygame
from pygame.sprite import Sprite
from random import uniform

class Shield(Sprite):
	def __init__ (self, ai_settings, screen, size=''):
		super().__init__()  
		"""Initialize the shield bubble and set its starting position"""
		self.screen = screen 
		self.ai_settings = ai_settings
		self.size = size 
		
		#Load the shield bubble image and get its rect
		self.image = pygame.image.load('images/shield.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect() 
		
		if self.size=='mini':
			# Creating a shield of smaller size for scoreboard purposes
			self.width = int(self.rect.width/1.5)
			self.height = int(self.rect.height/1.5)
			self.image = pygame.transform.scale(self.image, (self.width, self.height))
			
		#Set up the start position of the bubble
		self.half_width = self.rect.width / 2
		self.rect.top = self.screen_rect.top - self.rect.height
		x_position = uniform(self.half_width, (self.screen_rect.right -
								self.half_width))
		self.rect.centerx = x_position
		
		#Store the y value as a float
		self.y = float(self.rect.centery)
		
	def update(self):
		"""Move the bubble down the screen"""
		self.y += self.ai_settings.shield_drop_speed
		self.rect.centery = self.y
	
	def blitme(self):
		"""Draw the bubble to the screen"""
		#fills the part of the screen defined by the bullet's rect with the color defined by self.color
		self.screen.blit(self.image, self.rect)
