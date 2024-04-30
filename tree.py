import math
from collections import defaultdict
from csvReader import read_upgrades

WOM = 0
HISTORY = 1
WRITING = 2
TECHNOLOGY = 3

#OG Icon locations
        # self.wom_button = button.Button(SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.8, wom_icon, scale * 0.09)
        # self.writ_button = button.Button(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.85, writ_icon, scale * 0.09)
        # self.hist_button = button.Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85, hist_icon, scale * 0.09)
        # self.tech_button = button.Button(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.85, tech_icon, scale * 0.09)
        # self.map_button = button.Button(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, map_icon, scale * 0.09)

#TODO fix this dependency to get prereqs from csv file
writ_prereqs = [0, 1, 2, 0, 0, 5, 5, 5, 8, 8, 5, 0]
tech_prereqs = [0, 1, 1, 0, 4, 4, 4, 4, 0, 9, 10, 11]
hist_prereqs = [0, 0, 0, 0, 0]

class Upgrade:
    def __init__(self, row):
        self.ID = row[0]
        self.name = row[1]
        self.prereqs = row[2]
        self.cost = row[3]
        self.option_type = row[4]
        self.effect_type = row[5]
        self.effect_size = row[6]
        self.hover_text = row[7]
        self.present = False

class Tree:
    def __init__(self):
        self.word_of_mouth = 1
        self.wom_cost = 10
        self.skills = dict()
        writ_file = "database/WRIT_SKILLS.csv"
        tech_file = "database/TECH_SKILLS.csv"
        hist_file = "database/HIST_SKILLS.csv"

        writ_list = read_upgrades(writ_file)
        tech_list = read_upgrades(tech_file)
        hist_list = read_upgrades(hist_file)

        for skill in writ_list:
            #print(skill.ID)
            self.skills[skill.ID] = skill
        for skill in tech_list:
            self.skills[skill.ID] = skill
        for skill in hist_list:
            self.skills[skill.ID] = skill


        #TODO add line dependencies based on csv
        self.writ_lines = [(writ_prereqs[x], x + 1) for x in range(len(writ_prereqs))]
        self.tech_lines = [(tech_prereqs[x], x + 1) for x in range(len(tech_prereqs))]
        self.hist_lines = [(hist_prereqs[x], x + 1) for x in range(len(hist_prereqs))]


    def seed_init(self, width, height):
        #print(width, height)
        row_heights = [height * (0.85 - (x * 0.2)) for x in range(5)]
        column_widths = [width * (0.15 + (x * 0.2)) for x in range(4)]

        self.writ_loc = writ_loc_init([], width, height, row_heights, column_widths)
        self.tech_loc = tech_loc_init([], width, height, row_heights, column_widths)
        self.hist_loc = hist_loc_init([], width, height, row_heights, column_widths)


    def is_legal(self, ID, game):
        if ID == "WOM":
            if game.believers < self.wom_cost:
                return False
            else:
                return True

        legal = False
        num = int(ID[4::]) - 1

        if ID[0:4:] == "WRIT":
            if writ_prereqs[num] == 0:
                legal = True
            else:
                if self.skills[ID[0:4:] + str(writ_prereqs[num])].present:
                    legal = True
        elif ID[0:4:] == "TECH":
            if tech_prereqs[num] == 0:
                legal = True
            else:
                if self.skills[ID[0:4:] + str(tech_prereqs[num])].present:
                    legal = True
        elif ID[0:4:] == "HIST":
            if hist_prereqs[num] == 0:
                legal = True
            else:
                if self.skills[ID[0:4:] + str(hist_prereqs[num])].present:
                    legal = True
        if int(self.skills[ID].cost) > game.believers:
            legal = False
        return legal

    def upgrade(self, ID, game):
        legal = self.is_legal(ID, game)
        if ID == "WOM":
            if legal:
                game.believers = game.believers - self.wom_cost
                self.word_of_mouth += 1
                self.wom_cost += 10
                return True
            else:
                return False

        if not self.skills[ID].present and legal:
            #TODO change this to something that is not truee if I need it
            if legal:
                if game.believers < int(self.skills[ID].cost):
                    return False
                else:
                    game.believers = game.believers - int(self.skills[ID].cost)
                    self.skills[ID].present = True 
                    return True

        return False

    def update_believers(self, game):
        upgrade_amount = self.word_of_mouth
        for item in self.skills:
            if self.skills[item].present == True and self.skills[item].effect_type == "PASSIVE":
                upgrade_amount += self.word_of_mouth * float(self.skills[item].effect_size)
        game.believers = math.ceil(game.believers + upgrade_amount)
        


def writ_loc_init(writ_loc, width, height,row_heights, column_widths):
    #first icon placement
    half = (column_widths[1] - column_widths[0]) / 2

    writ_loc.append((width * 0.3, height * 0.85))

    #add other icons
    #Emotional Language
    writ_loc.append((column_widths[0], row_heights[1]))
    writ_loc.append((column_widths[0], row_heights[2]))
    writ_loc.append((column_widths[0], row_heights[3]))

    #illusory truth effect
    #TODO maybe change icon
    writ_loc.append((column_widths[1], row_heights[1]))

    #conspiracy theories
    writ_loc.append((column_widths[2], row_heights[1]))
    writ_loc.append((column_widths[1], row_heights[3]))
    writ_loc.append((column_widths[1] + half, row_heights[2]))
    #logical fallacies
    writ_loc.append((column_widths[2], row_heights[3]))
    writ_loc.append((column_widths[1] + half, row_heights[4]))
    writ_loc.append((column_widths[2] + half, row_heights[4]))

    writ_loc.append((column_widths[2] + half, row_heights[2]))

    #sign theory
    writ_loc.append((column_widths[3], row_heights[1]))

    return writ_loc


def tech_loc_init(tech_loc, width, height,row_heights, column_widths):
    #first icon placement
    half_x = (column_widths[1] - column_widths[0]) / 2
    half_y = (row_heights[1] - row_heights[0]) / 2

    tech_loc.append((width * 0.7, height * 0.85))

    #add other icons
    #Website Spoofing
    tech_loc.append((column_widths[0] + half_x, row_heights[1]))
    tech_loc.append((column_widths[0], row_heights[2] + half_y))
    tech_loc.append((column_widths[1], row_heights[2]))

    #Bots
    tech_loc.append((column_widths[2], row_heights[1]))
    tech_loc.append((column_widths[1], row_heights[3]))
    tech_loc.append((column_widths[1] + half_x, row_heights[3] + half_y))
    tech_loc.append((column_widths[2], row_heights[2] + half_y))
    tech_loc.append((column_widths[2] + half_x, row_heights[2]))

    #AI
    tech_loc.append((column_widths[3] + half_x, row_heights[1]))
    tech_loc.append((column_widths[3] + half_x, row_heights[2]))
    tech_loc.append((column_widths[3] + half_x, row_heights[3]))
    tech_loc.append((column_widths[3] + half_x, row_heights[4]))

    return tech_loc

def hist_loc_init(hist_loc, width, height,row_heights, column_widths):
    #first icon placement
    x_inc = (column_widths[3] - column_widths[0]) / 4
    half_y = (row_heights[1] - row_heights[0]) / 2

    hist_loc.append((width * 0.5, height * 0.85))

    hist_loc.append((column_widths[0], row_heights[1] + half_y))
    hist_loc.append((column_widths[0] + x_inc, row_heights[2] + half_y))
    hist_loc.append((column_widths[0] + (x_inc * 2), row_heights[3] + half_y))
    hist_loc.append((column_widths[0] + (x_inc * 3), row_heights[2] + half_y))
    hist_loc.append((column_widths[0] + (x_inc * 4), row_heights[1] + half_y))

    return hist_loc

