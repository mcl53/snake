import pygame
from random import randrange
import pandas as pd
import os
from time import time
from pygame_textinput import TextInput


pygame.init()

run = True

window = pygame.display.set_mode((510, 510))
window.fill((0, 0, 0))
pygame.display.update()
pygame.display.set_caption("Snake")

default_font = pygame.font.get_default_font()
font = pygame.font.Font(default_font, 42)
small_font = pygame.font.Font(default_font, 26)

game_over_text = font.render("Game Over", True, (0, 0, 255))
new_game_text = small_font.render("New game", True, (0, 0, 255))
quit_text = small_font.render("Quit", True, (0, 0, 255))
high_score_text = font.render("New high score!", True, (255, 165, 0))
high_score_width = high_score_text.get_width()
high_score_height = high_score_text.get_height()
text_input = TextInput()

current_key = None
food_spawned = False
food_x = None
food_y = None
score_displayed = False


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
			
			
def spawn_food():
	x_spawn = randrange(0, 510 - snake.width, snake.velocity)
	y_spawn = randrange(0, 510 - snake.height, snake.velocity)
	while [x_spawn, y_spawn] in snake.rectangles:
		x_spawn = randrange(0, 510 - snake.width, snake.velocity)
		y_spawn = randrange(0, 510 - snake.height, snake.velocity)
	return x_spawn, y_spawn
	
	
def draw_food(x, y, snake_obj):
	pygame.draw.rect(window, (255, 0, 0), (x, y, snake_obj.width, snake_obj.height))

	
def end_game(game_over, new_game, quit_text):
	window.fill((0, 0, 0))
	score_text = font.render("Score: " + score, True, (0, 0, 255))
	g_o_height = game_over.get_height()
	n_g_height = new_game.get_height()
	q_height = quit_text.get_height()
	s_height = score_text.get_height()
	all_height = g_o_height + n_g_height + q_height
	window.blit(game_over, ((510 - game_over.get_width()) / 2, (510 - all_height) / 2))
	window.blit(new_game, ((510 - new_game.get_width()) / 2, ((510 - all_height) / 2) + g_o_height))
	window.blit(quit_text, ((510 - quit_text.get_width()) / 2, ((510 - all_height) / 2) + g_o_height + n_g_height))
	window.blit(score_text, ((510 - score_text.get_width()) / 2, 60))
	pygame.display.update()
	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				if ((510 - all_height) / 2) + g_o_height < pos[1] < 510 - ((510 - all_height) / 2) - q_height:
					ret_val = True
					loop = False
				elif 510 - ((510 - all_height) / 2) - q_height < pos[1] < 510 - ((510 - all_height) / 2):
					ret_val = False
					loop = False
	return ret_val
	

def evaluate_current_key(keys_in):
	global current_key
	if keys_in[pygame.K_LEFT]:
		if current_key != "right":
			current_key = "left"
	
	elif keys_in[pygame.K_RIGHT]:
		if current_key != "left":
			current_key = "right"
	
	elif keys_in[pygame.K_UP]:
		if current_key != "down":
			current_key = "up"
	
	elif keys_in[pygame.K_DOWN]:
		if current_key != "up":
			current_key = "down"


def read_scores_file(score):
	high_score = False
	path_to_csv = "." + os.path.sep + "scores.csv"
	scores_data = pd.read_csv(path_to_csv)
	scores_data = scores_data.sort_values(["Score"], ascending=False)
	print(scores_data)
	if len(scores_data) > 5:
		if int(score) > scores_data["Score"][4]:
			print("New high score")
			high_score = True
	else:
		print("New high score")
		high_score = True
	new_score = pd.DataFrame([["game", int(score)]], columns=["Name", "Score"])
	scores_data = scores_data.append(new_score, ignore_index=True)
	scores_data = scores_data.sort_values(["Score"], ascending=False)
	print(scores_data)
	show_score_screen(high_score, scores_data, score)
	scores_data.to_csv(path_to_csv, columns=["Name", "Score"], index=False)


def show_score_screen(high_score, scores_data, score):
	window.fill((0, 0, 0))
	score_text = font.render("Score: " + score, True, (0, 0, 255))
	window.blit(score_text, ((510 - score_text.get_width()) / 2, 60))
	for i in range(1, 9):
		string_to_display = str(i) + ".)   " + str(scores_data["Name"][i-1]) + "   " + str(scores_data["Score"][i-1])
		text = small_font.render(string_to_display, True, (255, 165, 0))
		window.blit(text, ((510 - text.get_width()) / 2, 60 + (score_text.get_height() + (text.get_height() * (i - 1))) + (i * 20)))
		
	global score_displayed
	score_displayed = True
	
	# events = pygame.event.get()
	# for event in events:
	# 	if event.type == pygame.QUIT:
	# 		pygame.quit()
	# text_input.update(events)
	# window.blit(text_input.get_surface(), (0, 0))
	


snake = Snake()

current_time = time()

while run:
	pygame.time.delay(snake.delay)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	if not snake.dead:
		keys = pygame.key.get_pressed()
		
		evaluate_current_key(keys)
		
		if current_key is not None:
			snake.move(current_key)
			
		snake.draw(window)
		
		snake.check_dead()
		
		if snake.head_x == food_x and snake.head_y == food_y:
			food_spawned = False
			snake.extend()
		
		if not food_spawned:
			food_x, food_y = spawn_food()
			food_spawned = True
		else:
			draw_food(food_x, food_y, snake)
		
	if snake.dead and not score_displayed:
		# run = end_game(game_over_text, new_game_text, quit_text)
		score = str(len(snake.rectangles) + len(snake.new_rects))
		read_scores_file(score)
		current_time = time()
		
	if snake.dead and score_displayed:
		new_time = time()
		if new_time > current_time + 15:
			run = end_game(game_over_text, new_game_text, quit_text)
			
			if run:
				current_key = None
				snake.__init__()
		
	pygame.display.update()
		
pygame.quit()
