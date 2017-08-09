class Settings():
	"""A class to store all settings for Alien Invasion."""
	
	def __init__(self):
		"""Initialize the game's settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		
		#Bullet settings
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 10
		
		#Long bullet settings
		self.long_bullet_speed_factor = 3
		self.long_bullet_width = 300
		self.long_bullet_height = 15
		self.long_bullet_color = (60, 60, 60)
		self.long_bullet_limit = 8
		self.long_bullet_reload_point = 33 
				
		#Alien bullet settings
		self.alien_bullet_speed_factor = 1
		self.alien_bullet_width = 10
		self.alien_bullet_height = 10
		self.alien_bullet_color = (60, 60, 60)
		self.alien_bullets_allowed = 3
		
		# Ship settings
		self.ship_speed_factor = 2
		self.ship_limit = 3
		
		# Alien settings
		self.alien_speed_factor = 1 
		self.fleet_drop_speed = 40
		#fleet_direction of 1 = right; -1 = left
		self.fleet_direction = 1

		# Health settings
		self.health_drop_speed = 1
		self.health_drop_point = 70 

		# Shield settings
		self.shield_drop_speed = 1
		self.shield_drop_point = 95
		self.shield_hit_limit = 10
		
		# Bullet bar settings
		self.bullet_bar_width = 10
		self.bullet_bar_height = 25
		self.bullet_bar_color = (60, 60, 60)
		
		# How quickly the game speeds up
		self.speedup_scale = 1.1
		# How quickly the alien point values increase
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_direction = 1
		
		#Scoring
		self.alien_points = 50
	
		#Initialize long bullet count
		self.long_bullet_count = 1
		
	def increase_speed(self):
		"""Increase speed settings and alien point values"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
