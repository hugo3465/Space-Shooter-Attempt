from abc import ABC, abstractmethod

class Enemy(ABC):
    def __init__(self, game, pos):
        self.game = game

        self.x, self.y = pos

        self.image = None
        self.rect = None

    @abstractmethod
    def update(self):
        pass