#whatever I need to include
#from numpy import random
#import pygame
import pygame
from tree import Tree
import csvReader as csv
import graphics.graphicsloop as graphics
import math
import random

EVENT_PROB = 0.1
BELIEVER_PERCENT = 0.05
POP = 300000

DEFAULT = 0
EVENT = 5

WIN = -2
END = -1            

#Start with creating a system
class Game:
    def __init__(self, event_database):
        self.stage = 0
        self.believers = 1
        self.population = POP
        self.tree = Tree()

        self.end_time = 30 * 150

        self.counter = 0

        #if I want to select different event_databases replace filename with events.csv with event_database
        filename = event_database
        self.events = csv.read_events(filename)
        #add all events to the game
        self.curr_screen = DEFAULT

    

    #upgrades is a list of the updates in the upgrade tree
    def update(self, world):

        self.curr_screen = world.update_screen(self.curr_screen, self.believers, self.population, game=self)
        
        if self.curr_screen == END:
            self.end = True

        #create a function to increase believers
        if self.curr_screen != EVENT:
            self.counter += 1

        if self.counter % 5 == 0:
            self.tree.update_believers(self)
            #6 counter = 1 second. TIME OF GAME SHOULD BE 
            #print(self.believers)

        if round((self.end_time - self.counter) / 30) % 30 == 0 and self.counter > 30:
            self.curr_screen = EVENT
            self.counter += 1

        if round((self.end_time - self.counter) / 30) <= 0:
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

    #This function is used for automatic game testing.
    def set_events(self, events):
        self.events = []
        for event in events:
            new_button = button.Button(event.x, event.y, None, 1, event=event, type=1, color=(0,0,0))
            self.events.append(new_button)

    def bot_update_believers(self):
        #the screen updates the believers by the rate determined by tree every 1/6 of a second
        #by that logic, I need to update the screen every 6 times a second. an event happens every 30 seconds
        #there are 10 events
        #update the screen 6 * 30 times before switching to an event. At the end, 
        for i in range(6 * 30):
            self.tree.update_believers(self)
        self.counter += 30 * 30

    #Get options returns the list of upgrades available with the current number of believers
    def get_options(self):
        option_list = []
        for key in self.tree.skills:
            if not self.tree.skills[key].present and self.tree.is_legal(key, self):
                #print(self.tree.skills[key].present, self.tree.skills[key].cost, self.believers)
                option_list.append(key)
        if self.tree.is_legal("WOM", self):
            option_list.append("WOM")

        return option_list

    def get_event(self):
        return random.choice(self.events)

    def get_event_options(self, event):
        options = []
        for option in event.options:
            legal = True
            for req in option.requirements:
                if req != "0" and req not in self.tree.skills:
                    legal = False
                    break
            if legal:
                options.append(option)
        return options

    def simulate(self, upgrade_algo, event_algo):
        num_reps = 0
        self.reset_game()
        while not self.end:
            num_reps += 1
            self.bot_update_believers()
            upgrade_algo(self)
            event = self.get_event()
            event_algo(self, event).change(self)

            if self.counter >= self.end_time:
                self.end = True
            if self.believers >= (self.population / 2):
                self.end = True
                self.win = True
        #print(self.believers)
        #print("num reps = " + str(num_reps))
        return self.win

    def reset_game(self):
        self.win = False
        self.end = False
        self.believers = 1
        self.counter = 0
        for skill in self.tree.skills:
            self.tree.skills[skill].present = False

        self.tree.wom_cost = 10
        self.tree.word_of_mouth = 1
        self.curr_screen = DEFAULT
        

    def test_algorithm(self, reps, upgrade_algo, event_algo):
        total_wins = 0
        for i in range(reps):
            self.reset_game()
            if self.simulate(upgrade_algo, event_algo):
                total_wins += 1
        return total_wins / reps
            

def random_upgrades(game):
    upgrade = None
    options = game.get_options()
    options.append(None)
    upgrade = random.choice(options)
    if upgrade == None:
        return
    else:
        game.tree.upgrade(upgrade, game)
        random_upgrades(game)

def greedy_upgrades(game):
    #TODO Make an agent that upgrades as long as it has believers left
    options = game.get_options()
    while options != []:
        upgrade = random.choice(options)
        game.tree.upgrade(upgrade, game)
        options = game.get_options()
        

def random_events(game, event):
    return random.choice(game.get_event_options(event))

def greedy_events(game, event):
    #TODO write an agent that uses the best event option
    best = None
    options = game.get_event_options(event)
    for option in options:
        if best == None:
            best = option
        if best.effect < option.effect:
            best = option
    return best


def print_stats(game, tests):
    print("Stats: ")
    print("end_time = " + str(game.end_time / 30))
    print("num_tests = " + str(tests))

def main():
    database = "database/events.csv"

    #print("it gets past database")
    tests = 1000

    new_game = Game(database)

    print_stats(new_game, tests)

    #print(new_game.simulate(random_upgrades, random_events))
    # print("Random upgrades, random events: win percentage == " + str(new_game.test_algorithm(tests, random_upgrades, random_events)))
    # print("Greedy upgrades, greedy events: win percentage == " + str(new_game.test_algorithm(tests, greedy_upgrades, greedy_events)))
    # print("Random upgrades, greedy events: win percentage == " + str(new_game.test_algorithm(tests, random_upgrades, greedy_events)))
    # print("Greedy upgrades, random events: win percentage == " + str(new_game.test_algorithm(tests, greedy_upgrades, random_events)))
    new_game.run()

    new_game.run()

main()
