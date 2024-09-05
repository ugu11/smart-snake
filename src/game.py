from src.model.food import Food
from src.model.player import Player
import random
import torch

PLAYER_LABEL = 1
FOOD_LABEL = 3

UP = 1000
DOWN = 1001
LEFT = 1002
RIGHT = 1003

class Game:
    def __init__(self, width, height, n_grid):
        self.size = self.width, self.height = width, height
        self.n_grid = n_grid
        self.grid_size = self.width / self.n_grid

        self.reset()

    def update_board(self):
        self.board = torch.zeros(self.size)
        player_xy = self.player.get_xy()
        self.board[player_xy] = PLAYER_LABEL

        self.board[(self.food.x, self.food.y)] = FOOD_LABEL

        self.board = self.board.T

    def spawn_food(self):
        self.food = Food(
            x=random.randint(0, self.n_grid-1),
            y=random.randint(0, self.n_grid-1)
        )

        while self.is_food_hidden():
            self.food = Food(
                x=random.randint(0, self.n_grid-1),
                y=random.randint(0, self.n_grid-1)
            )

    def is_food_hidden(self):
        for tail in self.player.tails:
            tail_x, tail_y = tail.get_xy()

            if tail_x == self.food.x and tail_y == self.food.y:
                return True
            
        head_x, head_y = self.player.get_xy()
        
        return head_x == self.food.x and head_y == self.food.y

    def check_player_is_eating_food(self):
        if self.player.is_eating_food(self.food):
            self.spawn_food()

    def reset(self):
        self.board = torch.zeros(self.size)

        self.player = Player()

        self.spawn_food()

    def move_player(self, direction):
        if direction == DOWN:
            self.player.move_down()
        elif direction == UP:
            self.player.move_up()
        elif direction == RIGHT:
            self.player.move_right()
        elif direction == LEFT:
            self.player.move_left()

    def step_game(self):
        self.player.update(self.n_grid)
        self.check_player_is_eating_food()

        self.update_board()

        if self.player.is_head_is_colliding_with_tail():
            return True
        
        return False
    
    def get_player_score(self):
        return self.player.score
    
    def get_player_xy(self):
        return self.player.get_xy()
    
    def get_food_xy(self):
        return self.food.x, self.food.y
    
    def get_tail_xy(self, index):
        return self.player.get_tail(index)
    
    def get_total_tails(self):
        return self.player.get_total_tails()