import pygame
from time import time
from snake import Snake
import methods


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

current_key = None
food_spawned = False
food_x = None
food_y = None
score_displayed = False


snake = Snake()

current_time = time()

while run:
	pygame.time.delay(snake.delay)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	if not snake.dead:
		keys = pygame.key.get_pressed()
		
		methods.evaluate_current_key(keys)
		
		if current_key is not None:
			snake.move(current_key)
			
		snake.draw(window)
		
		snake.check_dead()
		
		if snake.head_x == food_x and snake.head_y == food_y:
			food_spawned = False
			snake.extend()
		
		if not food_spawned:
			food_x, food_y = methods.spawn_food()
			food_spawned = True
		else:
			methods.draw_food(food_x, food_y, snake)
		
	if snake.dead and not score_displayed:
		# run = end_game(game_over_text, new_game_text, quit_text)
		score = str(len(snake.rectangles) + len(snake.new_rects))
		methods.read_scores_file(score)
		current_time = time()
		
	if snake.dead and score_displayed:
		new_time = time()
		if new_time > current_time + 15:
			run = methods.end_game(game_over_text, new_game_text, quit_text)
			
			if run:
				current_key = None
				snake.__init__()
		
	pygame.display.update()
		
pygame.quit()
