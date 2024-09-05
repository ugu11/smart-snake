from src.game import DOWN, UP, LEFT, RIGHT
import pygame, sys

from src.ui.sprite_ui import SpriteUI

class UIWindow:
    def __init__(self, width, height, game, framerate=20):
        pygame.init()
        pygame.font.init() # you have to call this at the start, 
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = width, height
        self.black = 51, 51, 51
        self.framerate = framerate

        self.direction_map = {
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT,
        }

        self.game = game

        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont('Comic Sans MS', 18)
        self.score_text_surface = self.font.render("SCORE: 0", False, (255, 255, 255))

        player_xy = self.game.get_player_xy()
        self.player_ui = SpriteUI(
            x=player_xy[0], y=player_xy[1],
            width=self.game.grid_size, height=self.game.grid_size,
            icon="assets/ultron.png"
        )
        food_xy = self.game.get_food_xy()
        self.food_ui = SpriteUI(
            x=food_xy[0], y=food_xy[1],
            width=self.game.grid_size, height=self.game.grid_size,
            icon="assets/mind-stone.png"
        )

        self.tails_ui = []

    def display_data(self):
        player_score = self.game.get_player_score()
        print("SCORE:", player_score)
        self.score_text_surface = self.font.render("SCORE: " + str(player_score), False, (255, 255, 255))

    def append_tail_ui(self):
        self.tails_ui.append(
            SpriteUI(
                x=-1, y=-1,
                width=self.game.grid_size, height=self.game.grid_size,
                icon="assets/ultron-bot.jpg"
            )
        )

    def reset_ui(self):
        player_xy = self.game.get_player_xy()
        self.player_ui = SpriteUI(
            x=player_xy[0], y=player_xy[1],
            width=self.game.grid_size, height=self.game.grid_size,
            icon="assets/ultron.png"
        )
        food_xy = self.game.get_food_xy()
        self.food_ui = SpriteUI(
            x=food_xy[0], y=food_xy[1],
            width=self.game.grid_size, height=self.game.grid_size,
            icon="assets/mind-stone.png"
        )

        self.tails_ui = []

    def draw_sprites(self):
        player_xy = self.game.get_player_xy()
        food_xy = self.game.get_food_xy()
        self.player_ui.draw(player_xy[0], player_xy[1], self.screen)
        self.food_ui.draw(food_xy[0], food_xy[1], self.screen)

        if len(self.tails_ui) != self.game.get_total_tails():
            self.tails_ui = []

            for _ in range(self.game.get_total_tails()):
                self.append_tail_ui()

        for i in range(len(self.tails_ui)):
            tail_ui = self.tails_ui[i]
            tail_xy = self.game.get_tail_xy(i).get_xy()
            tail_ui.draw(tail_xy[0], tail_xy[1], self.screen)

        self.screen.blit(self.score_text_surface, (15,15))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in self.direction_map.keys():
                    self.game.move_player(self.direction_map[event.key])


    def run(self):
        while True:
            self.handle_events()

            game_has_ended = self.game.step_game()

            if game_has_ended:
                print("Final score:", self.game.get_player_score())
                self.game.reset()

            # Draw
            self.screen.fill(self.black)
            self.draw_sprites()
            self.display_data()
            pygame.display.flip()
            self.clock.tick(self.framerate)
