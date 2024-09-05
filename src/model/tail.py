
class Tail:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y
    
    def update_pos(self, x, y):
        self.x = x
        self.y = y