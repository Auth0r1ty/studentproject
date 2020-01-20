from enum import  Enum

class StaticEl(Enum):
    path = 1
    wall = 2
    enter = 3
    trap = 4
    pathPlayer1 = 5   #
    pathPlayer2 = 6
    none = 7
    exit = 8


class Orientation(Enum):
    left = 1
    right = 2
    up = 3
    down = 4
    none = 5


class MudState(Enum):
    not_show= 0
    show = 1
    active= 2