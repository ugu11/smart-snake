
from src.game import Game
from src.ui.ui import UIWindow

def main():
    game = Game(500, 500, 10)
    ui = UIWindow(500, 500, game, framerate=10)

    ui.run()

if __name__ == '__main__':
    main()