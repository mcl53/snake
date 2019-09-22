import pygame
from random import randrange
import os
import pandas as pd
import fonts


def spawn_food(snake):
	x_spawn = randrange(0, 510 - snake.width, snake.velocity)
	y_spawn = randrange(0, 510 - snake.height, snake.velocity)
	while [x_spawn, y_spawn] in snake.rectangles:
		x_spawn = randrange(0, 510 - snake.width, snake.velocity)
		y_spawn = randrange(0, 510 - snake.height, snake.velocity)
	return x_spawn, y_spawn


def draw_food(x, y, window, snake_obj):
	pygame.draw.rect(window, (255, 0, 0), (x, y, snake_obj.width, snake_obj.height))


def end_game(window, score, game_over, new_game, quit_text):
	window.fill((0, 0, 0))
	score_text = fonts.font.render("Score: " + score, True, (0, 0, 255))
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


def evaluate_current_key(current_key, keys_in):
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
	
	return current_key


def read_scores_file(score, window):
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
	scores_data.to_csv(path_to_csv, columns=["Name", "Score"], index=False)
	return show_score_screen(window, scores_data, score)


def show_score_screen(window, scores_data, score):
	window.fill((0, 0, 0))
	score_text = fonts.font.render("Score: " + score, True, (0, 0, 255))
	window.blit(score_text, ((510 - score_text.get_width()) / 2, 60))
	for i in range(1, 9):
		string_to_display = str(i) + ".)   " + str(scores_data["Name"][i - 1]) + "   " + str(
			scores_data["Score"][i - 1])
		text = fonts.small_font.render(string_to_display, True, (255, 165, 0))
		window.blit(text, (
		(510 - text.get_width()) / 2, 60 + (score_text.get_height() + (text.get_height() * (i - 1))) + (i * 20)))
	
	# Set score_displayed variable
	return True

# events = pygame.event.get()
# for event in events:
# 	if event.type == pygame.QUIT:
# 		pygame.quit()
# text_input.update(events)
# window.blit(text_input.get_surface(), (0, 0))
