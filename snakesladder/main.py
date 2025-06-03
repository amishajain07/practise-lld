import random
from typing import Optional

class Player:
    def __init__(self, playername):
        self.playername = playername
        self.curr_position = 0

class Dice:
    def __init__(
            self,
            no_of_dice: int = 1,
            dice_min: Optional[int] = 1, 
            dice_max: Optional[int] = 6
        ):
        self.MIN = dice_min
        self.MAX = dice_max
        self.dice_count = no_of_dice

    def roll_dice(self):
        dicesum = dice_rolled = 0

        while dice_rolled < self.dice_count:
            dicesum += random.randint(self.MIN, self.MAX)
            dice_rolled += 1
        
        return dicesum

class Jump:
    def __init__(self):
        self.start: int = 0
        self.end: int = 0

class BoardCell:
    def __init__(self):
        self.jump: Jump = None

class Board:
    def __init__(
            self,
            no_of_snakes: int = 5,
            no_of_ladders: int = 6,
            board_size: int = 10 #(10X10)
        ):
        self.cells: list[list] = []
        self.boardsize = board_size
        self.snakes = no_of_snakes
        self.ladders = no_of_ladders
        self.totalcells = self.boardsize * self.boardsize - 1
        self.initialize_cells()

    def initialize_cells(self):
        self.cells = [
            [
                BoardCell() for _ in range(self.boardsize)
            ] for _ in range(self.boardsize)
        ]
    
    def add_snakes(self):
        while self.snakes > 0:
            snakehead = random.randint(1, self.totalcells)
            snaketail = random.randint(snakehead, self.totalcells)

            snake_obj = Jump()
            snake_obj.start = snakehead
            snake_obj.end = snaketail

            cell: BoardCell = self.get_cell(snakehead)
            cell.jump = snake_obj

            self.snakes -= 1

    def add_ladders(self):
        while self.ladders > 0:
            laddertail = random.randint(1, self.totalcells)
            ladderhead = random.randint(laddertail, self.totalcells)

            ladder_obj = Jump()
            ladder_obj.start = ladderhead
            ladder_obj.end = laddertail

            cell: BoardCell = self.get_cell(ladderhead)
            cell.jump = ladder_obj

            self.ladders -= 1

    def get_cell(self, position: int) -> BoardCell:
        boardrow = position // self.boardsize
        boardcol = position % self.boardsize
        return self.cells[boardrow][boardcol]

from collections import deque
class SNLGame:
    def __init__(self):
        self.players = deque([]) # maintain a queue for players

    def initialise_game(self):
        self.board = Board(5,4,10)
        self.dice = Dice(2)
        self.winner = None
        self.add_players(player_count= 3)

    def add_players(self, player_count):
        for i in range(player_count):
            self.players.append(Player(f'p{i+1}'))
    
    def start_game(self):
        while self.winner is None:
            playerTurn: Player = self.findplayerturn()
            print(f'player {playerTurn} is playing now... ')

            diceroll = self.dice.roll_dice()
            print("Dice: ", diceroll)

            playermovedto = playerTurn.curr_position + diceroll

            playermovedto = self.jump_check(playermovedto)

            playerTurn.curr_position = playermovedto

            if playermovedto == len(self.board.cells)*len(self.board.cells)-1: self.winner = playerTurn


        print(f"Winner is {playerTurn}")

    def findplayerturn(self):
        player = self.players.popleft()
        self.players.append(player)
        return player
    

    def jump_check(self, newposition):
        if newposition > len(self.board.cells) * len(self.board.cells) -1: return newposition

        cell = self.board.get_cell(newposition)

        if cell.jump and cell.jump.start == newposition:
            return cell.jump.end
        
        return newposition