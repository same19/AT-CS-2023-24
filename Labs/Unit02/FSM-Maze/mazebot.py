import pygame
from fsm import FSM
import time

class MazeBot(pygame.sprite.Sprite):

    def __init__(self, game, x=50, y=50):
        super().__init__()

        self.game = game

        # Load initial image
        self.image = pygame.image.load("assets/images/bot.png")
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # The map of the maze
        self.maze = self.game.txt_grid

        # The route the bot will take to get to the $
        self.path = []

        # TODO: Create the Bot's finite state machine (self.fsm) with initial state
        self.fsm = None
        self.init_fsm()
    
    def init_fsm(self):
        # TODO: Add the state transitions

        self.fsm = FSM("South")

        #regular turn
        self.fsm.add_transition("X", "South", None, "East")
        self.fsm.add_transition("X", "East", None, "North")
        self.fsm.add_transition("X", "North", None, "West")
        self.fsm.add_transition("X", "West", None, "South")
        self.fsm.add_transition("#", "South", None, "East")
        self.fsm.add_transition("#", "East", None, "North")
        self.fsm.add_transition("#", "North", None, "West")
        self.fsm.add_transition("#", "West", None, "South")

        #breaker turn
        self.fsm.add_transition("#", "BSouth", None, "BEast")
        self.fsm.add_transition("#", "BEast", None, "BNorth")
        self.fsm.add_transition("#", "BNorth", None, "BWest")
        self.fsm.add_transition("#", "BWest", None, "BSouth")

        #normal/breaker transition
        self.fsm.add_transition("B", "South", self.move_south, "BSouth")
        self.fsm.add_transition("B", "East", self.move_east, "BEast")
        self.fsm.add_transition("B", "North", self.move_north, "BNorth")
        self.fsm.add_transition("B", "West", self.move_west, "BWest")
        self.fsm.add_transition("B", "BSouth", self.move_south, "South")
        self.fsm.add_transition("B", "BEast", self.move_east, "East")
        self.fsm.add_transition("B", "BNorth", self.move_north, "North")
        self.fsm.add_transition("B", "BWest", self.move_west, "West")

        #move normal
        self.fsm.add_transition(" ", "South", self.move_south, "South")
        self.fsm.add_transition(" ", "East", self.move_east, "East")
        self.fsm.add_transition(" ", "North", self.move_north, "North")
        self.fsm.add_transition(" ", "West", self.move_west, "West")

        #move in breaker mode
        self.fsm.add_transition(" ", "BSouth", self.move_south, "BSouth")
        self.fsm.add_transition(" ", "BEast", self.move_east, "BEast")
        self.fsm.add_transition(" ", "BNorth", self.move_north, "BNorth")
        self.fsm.add_transition(" ", "BWest", self.move_west, "BWest")
        self.fsm.add_transition("X", "BSouth", self.move_south, "BSouth")
        self.fsm.add_transition("X", "BEast", self.move_east, "BEast")
        self.fsm.add_transition("X", "BNorth", self.move_north, "BNorth")
        self.fsm.add_transition("X", "BWest", self.move_west, "BWest")
        
        #end
        self.fsm.add_transition("$", "South", self.move_south, "End")
        self.fsm.add_transition("$", "East", self.move_east, "End")
        self.fsm.add_transition("$", "North", self.move_north, "End")
        self.fsm.add_transition("$", "West", self.move_west, "End")
        self.fsm.add_transition("$", "BSouth", self.move_south, "End")
        self.fsm.add_transition("$", "BEast", self.move_east, "End")
        self.fsm.add_transition("$", "BNorth", self.move_north, "End")
        self.fsm.add_transition("$", "BWest", self.move_west, "End")
    
    def get_state(self):
        # TODO: Return the maze bot's current state
        return self.fsm.current_state
    
    def move_south(self):
        """
        Changes the bot's location 1 spot South
        and records the movement in self.path
        """
        self.rect.centery += self.game.SPACING
        self.path.append("SOUTH")

    def move_east(self):
        """
        Changes the bot's location 1 spot East
        and records the movement in self.path
        """
        self.rect.centerx += self.game.SPACING
        self.path.append("EAST")

    def move_north(self):
        """
        Changes the bot's location 1 spot North
        and records the movement in self.path
        """
        self.rect.centery -= self.game.SPACING
        self.path.append("NORTH")

    def move_west(self):
        """
        Changes the bot's location 1 spot West
        and records the movement in self.path
        """
        self.rect.centerx -= self.game.SPACING
        self.path.append("WEST")
    
    def get_next_space(self):
        """
        Uses the bot's current state to determine the next 
        space in the maze the bot would go to. The next 
        space is returned as a String from self.maze.

        Ex. If the bot is facing South, you should get 
        the character one row down from you.

        Returns:
            String: The next character in the maze the bot could go to
        """

        # This is the current x and y indices of the bot in the maze
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING

        # TODO: Use the bot's current state to determine
        # what the next maze location value is
        
        state = self.get_state()
        if state == "South" or state == "BSouth":
            return self.maze[grid_y + 1][grid_x]
        if state == "East" or state == "BEast":
            return self.maze[grid_y][grid_x + 1]
        if state == "North" or state == "BNorth":
            return self.maze[grid_y - 1][grid_x]
        if state == "West" or state == "BWest":
            return self.maze[grid_y][grid_x - 1]
        print("ERROR")
    
    def update(self):
        time.sleep(1)
        # TODO: Use the finite state machine to process input
        print(self.get_next_space())
        self.fsm.process(self.get_next_space())
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))
