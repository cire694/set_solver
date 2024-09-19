from enum import Enum, auto
from itertools import combinations 

#attributes: 
class color(Enum):
    RED = 1
    GREEN = 2
    PURPLE = 3

class num(Enum):
    ONE = 1
    TWO = 2
    THREE = 3

class shading(Enum):
    SOLID = 1
    STRIPE = 2
    EMPTY = 3

class shape(Enum):
    DIAMOND = 1
    SQUIGGLE = 2
    OVAL = 3

class card: 
    def __init__(self, number, color, shading, shape, contour):
        self.number = number
        self.color = color
        self.shading = shading
        self.shape = shape
        self.contour = contour
    
    def __str__(self):
        return f"({self.number}, {self.color}, {self.shading}, {self.shape})"
    
    def get_contour(self):
        return self.contour


class set_field: 
    def __init__(self, *cards):
        self.cards = cards
        # if len(cards) < 3:
        #     raise ValueError('Not enough cards')

        self.sets = []
        self.find_all_sets()
    
    def check_num(a, b, c):
        return len(set([a.number, b.number, c.number])) != 2
    
    def check_color( a, b, c):
        return len(set([a.color, b.color, c.color])) != 2
    
    def check_shading(a, b, c):
        return len(set([a.shading, b.shading, c.shading])) != 2
    
    def check_shape( a, b, c):
        return len(set([a.shape, b.shape, c.shape])) != 2
    
    def is_set(self, a, b, c):
        return all([
            set_field.check_num(a, b, c), 
            set_field.check_color(a, b, c), 
            set_field.check_shading(a, b, c), 
            set_field.check_shape(a, b, c)
        ])
    
    def find_all_sets(self):
        for i in range(len(self.cards) - 2):
            first_card = self.cards[i]
            for j in range(i + 1, len(self.cards) - 1):
                second_card = self.cards[j]
                for k in range(j + 1, len(self.cards)):
                    third_card = self.cards[k]

                    if self.is_set(first_card, second_card, third_card):
                        self.sets.append((first_card, second_card, third_card))
    
    def get_set_contours(self):
        sets_contours = []
        for set in self.sets:
            for card in set: 
                sets_contours.append(card.get_contour())
        return sets_contours


    def __str__(self):
        result = "Sets:\n"

        for s in self.sets:
            result += "[ "
            for card in s:
                result += str(card) + ", "
            result = result[:-2] + " ]\n"

        return result
