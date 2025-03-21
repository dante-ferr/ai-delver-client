import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from game.game import Game


# game = Game()
# game.run()

from editor import app as editor_app

editor_app.mainloop()
