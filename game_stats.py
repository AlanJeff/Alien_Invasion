class GameStats():
	"""Track statistics for Alien Invasion"""
	
	def __init__(self, ai_settings):
		"""Initialize statistics"""
		self.ai_settings = ai_settings
		self.reset_stats()
		self.last_high_score = self.open_high_score()
		#Start Alien Invasion in an inactive state
		self.game_active = False
		#High score should never be reset
		self.high_score = self.last_high_score
		
		
	def reset_stats(self):
		"""Initialize statistics that can change during the game"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
		self.alien_kills = 1
		
		#Shield initial stats
		self.shield_hit = 0
		self.shield_active = False
		
		#Bullet initial state
		self.bullet_active = False
		
	def open_high_score(self):
		"""Retrieving the all time high score from file"""
		filename = 'high_score.txt'
		with open(filename) as file_object:
			self.last_high_score = file_object.read()
			self.last_high_score = int(self.last_high_score)
			return self.last_high_score
