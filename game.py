#whatever I need to include
#from numpy import random
#import pygame
import pygame
from tree import Tree
import csvReader as csv
import graphics.graphicsloop as graphics
import math

EVENT_PROB = 0.1
BELIEVER_PERCENT = 0.05
POP = 300000

DEFAULT = 0
EVENT = 5

WIN = -1

# class Believers:
#     def __init__(self):
#         self.true_believers = 1
#         self.on_the_edge = 0
#     def total(self):
#         return self.true_believers + self.on_the_edge

# class Map:

#     def __init__(self):
#         self.population = POP 
#         self.believers = believers()

#         #set up states and whatnot
#             #maybe just make a general election, though
#             #or make it when a district, then you have to win the country
#                 #this emphasizes how bigger influence operations use a variety of different tactics
#     def update(self, tree, stage):
#         if stage == 0:
#             #TODO finish regular default updates to believers
#             #MATH not sure if I like this
#             self.believers.true_believers += self.believers.on_the_edge * BELIEVER_PERCENT
#             self.believers.on_the_edge -= self.believers.on_the_edge * BELIEVER_PERCENT
#             self.believers.on_the_edge += self.believers.total() * ((tree.word_of_mouth + 1) * BELIEVER_PERCENT)
#         elif stage == 1:
#             #TODO Midgame setup
#             j = 0
#         elif stage == 2:
#             i = 1
#             #TODO Endgame setup


#         if random.rand() < EVENT_PROB:
#             i = 2
            


#Start with creating a system
class Game:
    def __init__(self, event_database):
        self.stage = 0
        self.believers = 1
        self.population = POP
        self.tree = Tree()

        self.end_time = 3600 * 3

        self.counter = 0

        #if I want to select different event_databases replace filename with events.csv with event_database
        filename = event_database
        self.events = csv.read_events(filename)
        #add all events to the game
        self.curr_screen = DEFAULT

    

    #upgrades is a list of the updates in the upgrade tree
    def update(self, world):

        self.curr_screen = world.update_screen(self.curr_screen, self.believers, self.population, game=self)
        
        #create a function to increase believers
        if self.curr_screen != EVENT:
            self.counter += 1

        if self.counter % 5 == 0:
            self.tree.update_believers(self)
            #6 counter = 1 second. TIME OF GAME SHOULD BE 
            #print(self.believers)



        if round((self.end_time - self.counter) / 60) % 25 == 0:
            self.curr_screen = EVENT
            self.counter += 3

        if round((self.end_time - self.counter) / 60) <= 0:
            #lose condition
            self.win = False
            self.curr_screen = WIN
            #self.end = True

        if self.curr_screen == -1 or self.believers > self.population / 2:
            self.win = True
            self.curr_screen = WIN
            #self.end = True

        
        # event = random.random()
        # if event < EVENT_PROB:
        #     #TODO change event function name
        #     self.event(map, self.tree)
        # else:
        #     #based on tree update position slightly
        #     #base upgrade that increases the amount that people convert
        #     map = map.believers()

    def run(self):
        self.end = False
        world = graphics.Graphics(self)

        world.set_events(self.events)

        while not self.end:
            pygame.event.pump()
            self.update(world)
        
            
        world.quit()


def main():
    database = "database/events.csv"

    #print("it gets past database")

    new_game = Game(database)

    new_game.run()

main()
