from src.model.tail import Tail

class Player:
    def __init__(self, velocity=1, initial_speed=[1, 0]):
        self.x = 0
        self.y = 0
        self.speed = initial_speed
        self.velocity = velocity

        self.score = 0

        self.tails = []

    def is_eating_food(self, food):
        x, y = self.get_xy()

        if x == food.x and y == food.y:
            self.add_score()
            self.add_tail()

            return True
        
        return False
    
    def add_tail(self):
        self.tails.append(
            Tail(-1, -1)
        )

    def update_tail_positions(self):
        if len(self.tails) == 0: return

        if len(self.tails) > 1:
            for i in range(len(self.tails)-1, 0, -1):
                curr_tail = self.tails[i]
                next_x, next_y = self.tails[i-1].get_xy()
                curr_tail.update_pos(next_x, next_y)

        # Update first tail
        head_x, head_y = self.get_xy()

        self.tails[0].update_pos(head_x, head_y)

    def get_xy(self):
        return self.x, self.y

    def add_score(self, points=1):
        self.score += points

    def move_up(self):
        if self.speed[1] <= 0:
            self._move(0, -self.velocity)

    def move_down(self):
        if self.speed[1] >= 0:
            self._move(0, self.velocity)

    def move_right(self):
        if self.speed[0] >= 0:
            self._move(self.velocity, 0)

    def move_left(self):
        if self.speed[0] <= 0:
            self._move(-self.velocity, 0)

    def update_position(self, n_grid):
        x, y = self.get_xy()
        new_x, new_y = x + self.speed[0], y + self.speed[1]

        if new_x >= n_grid:
            new_x = 0
        if new_x < 0:
            new_x = n_grid - 1

        if new_y >= n_grid:
            new_y = 0
        if new_y < 0:
            new_y = n_grid - 1
            
        self.x = new_x
        self.y = new_y

    def stop(self, horizontal=False, vertical=False):
        if horizontal:
            self._move(0, self.speed[1])
        if vertical:
            self._move(self.speed[0], 0)

    def _move(self, horizontal_speed, vertical_speed):
        self.speed[0] = horizontal_speed
        self.speed[1] = vertical_speed

    def handle_screen_boundaries(self, max_width, max_height):
        if self.x <= 0 and self.speed[0] < 0:
            self.stop(horizontal=True)
        if self.x + self.width >= max_width and self.speed[0] > 0:
            self.stop(horizontal=True)

        if self.y <= 0 and self.speed[1] < 0:
            self.stop(vertical=True)
        if self.y + self.height >= max_height and self.speed[1] > 0:
            self.stop(vertical=True)

    def is_head_is_colliding_with_tail(self):
        head_x, head_y = self.get_xy()
        for tail in self.tails:
            tail_x, tail_y = tail.get_xy()
            if head_x == tail_x and head_y == tail_y:
                return True
            
        return False
    
    def get_tail(self, index):
        return self.tails[index]
    
    def get_total_tails(self):
        return len(self.tails)

    def update(self, n_grid):
        self.update_tail_positions()
        self.update_position(n_grid)

    