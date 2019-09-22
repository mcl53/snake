import pygame


class Snake:
	def __init__(self):
		self.width = 15
		self.height = 15
		self.velocity = 15
		self.rectangles = [[45, 45]]
		self.new_rects = {}
		self.directions = []
		self.colour = (0, 255, 0)
		self.head_x = self.rectangles[0][0]
		self.head_y = self.rectangles[0][1]
		self.dead = False
		self.delay = 150
	
	def move(self, direction):
		# add the new direction and shift everything else along one
		self.directions.insert(0, direction)
		if len(self.directions) > len(self.rectangles):
			self.directions.pop(-1)
		if len(self.new_rects) > 0:
			if "replace" in self.new_rects.values():
				index = list(self.new_rects.values()).index("replace")
				key = list(self.new_rects.keys())[index]
				self.new_rects[key] = self.directions[0]
			new_rect = list(self.new_rects)[0]
			new_dir = self.new_rects[new_rect]
			new_rect_list = [new_rect[0], new_rect[1]]
			if new_rect_list not in self.rectangles:
				self.rectangles.append(new_rect_list)
				self.directions.append(new_dir)
				self.new_rects.pop(new_rect)
		
		# Speed up every 6 food eaten
		if len(self.rectangles) >= 6:
			self.delay = int(150 * (2 / ((len(self.rectangles) // 6) + 1)))
		
		# move rectangle based on direction and check if off screen -> wrap
		for i in range(len(self.rectangles)):
			
			if self.directions[i] == "left":
				self.rectangles[i][0] -= self.velocity
			
			elif self.directions[i] == "right":
				self.rectangles[i][0] += self.velocity
			
			elif self.directions[i] == "up":
				self.rectangles[i][1] -= self.velocity
			
			elif self.directions[i] == "down":
				self.rectangles[i][1] += self.velocity
			
			if self.rectangles[i][0] < 0:
				self.rectangles[i][0] = 510 - self.width
			
			if self.rectangles[i][0] > 510 - self.width:
				self.rectangles[i][0] = 0
			
			if self.rectangles[i][1] < 0:
				self.rectangles[i][1] = 510 - self.width
			
			if self.rectangles[i][1] > 510 - self.width:
				self.rectangles[i][1] = 0
		
		# set head coordinates
		self.head_x = self.rectangles[0][0]
		self.head_y = self.rectangles[0][1]
	
	def draw(self, win):
		win.fill((0, 0, 0))
		for rectangle in self.rectangles:
			pygame.draw.rect(win, self.colour, (rectangle[0], rectangle[1], self.width, self.height))
	
	def extend(self):
		self.new_rects[(self.head_x, self.head_y)] = "replace"
	
	def check_dead(self):
		if [self.head_x, self.head_y] in self.rectangles[1:len(self.rectangles)]:
			self.dead = True
		else:
			return
