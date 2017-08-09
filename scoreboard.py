import pygame
import pygame.font
from pygame.sprite import Group 

from ship import Ship
from shield import Shield
from bullet_bar import BulletBar

class Scoreboard():
	"""A class to report scoring information"""
	def __init__(self, ai_settings, screen, stats, ship):
		"""Initialize scorekeeping attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats 
		self.ship = ship 
		
		#Font settings for scoring information
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		#Prepare the initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships() 
		self.prep_shield_count()
		self.prep_bullet_bar()
		
	def prep_score(self):
		"""Turn the score into a rendered image"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, 
			self.ai_settings.bg_color)

		#Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def prep_high_score(self):
		"""Turn the high score into a rendered image"""
		high_score = int(round(self.stats.high_score, -1)) 
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, self.ai_settings.bg_color)
		
		# Center the high score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top		

	def prep_level(self):
		"""Turn the level into a rendered image"""
		self.level_image = self.font.render(str(self.stats.level), True, 
				self.text_color, self.ai_settings.bg_color)
				
		# Position the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right 
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Show how many ships are left."""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			self.ship = Ship(self.ai_settings, self.screen, size='mini')
			self.ship.rect.x = 20 + ship_number * self.ship.width * 1.5
			self.ship.rect.y = 10
			self.ships.add(self.ship) 

	def prep_shield_count(self):
		"""Show how many shields are left"""
		# Position the shield_image below the ship_image
		self.shield_image = Group()	
		shield = Shield(self.ai_settings, self.screen, size='mini')
		shield.rect.x = 20
		shield.rect.y = 20 + self.ship.height
		self.shield_image.add(shield)
		
		# Display the shield count image
		self.display_shield_count()
		
		#Position the shield count image
		self.shield_count_rect = self.shield_count.get_rect()
		self.shield_count_rect.y = shield.rect.y + 10
		self.shield_count_rect.left = shield.rect.right + 10
	
	def display_shield_count(self):
		self.shield_left = self.ai_settings.shield_hit_limit - self.stats.shield_hit 
		self.shield_count = self.font.render(str(self.shield_left), True,
				self.text_color, self.ai_settings.bg_color)		
	
	def prep_bullet_bar(self):
		"""Show how many long bullets are left"""
		self.long_bullet_bar = Group()
		for bullet_number in range(self.ai_settings.long_bullet_count):
			bullet_bar = BulletBar(self.ai_settings, self.screen)
			
			#Ship count area span
			ship_count_area_span = 20 + (self.ai_settings.ship_limit + 2) * (self.ship.width * 1.5)
			
			#Bullet bar position
			bullet_bar.rect.x =  ship_count_area_span + 10 + (bullet_number * bullet_bar.rect.width * 1.5)
			bullet_bar.rect.y = self.ship.rect.y + 10
			self.long_bullet_bar.add(bullet_bar)
		
	def show_score(self):
		"""Draw score to the screen"""
		self.screen.blit(self.score_image, self.score_rect) 
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)
		# Update bullet bar
		self.prep_bullet_bar()
		for bullet_bar in self.long_bullet_bar.sprites():
			bullet_bar.draw_bullet()		
		
		if self.stats.shield_active:
			self.display_shield_count()
			self.shield_image.draw(self.screen)
			self.screen.blit(self.shield_count, self.shield_count_rect)
