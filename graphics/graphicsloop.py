import pygame
import math
import os
import random

path = ""
#from . import button

if os.path.exists("./graphics"):
    import graphics.button as button
    path = "graphics/"
else:
    import button


#much of this code was learned by and takes a similar form to the code of this link
#https://github.com/russs123/pygame_tutorials/blob/main/Button/button_main.py

WIN = -2
END = -1

DEFAULT = 0
WRIT_TREE = 1
TECH_TREE = 2
HIST_TREE = 3
MENU = 4
EVENT = 5

#Size of trees
writ_size = 13
tech_size = 13
hist_size = 6

scale = 0.75

class Graphics:
    def __init__(self, game):
        pygame.init()
        self.count_font = pygame.font.SysFont(None, 30)

        self.clock = pygame.time.Clock()
        self.FPS = 30

        self.scale = scale

        self.SCREEN_HEIGHT = 1000 * scale
        self.SCREEN_WIDTH = 1000 * scale

        game.tree.seed_init(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.tree_init(game)

        self.event_in_progress = False
        self.bg_init()
        self.icon_init()

        #self.curr_screen = DEFAULT

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Disinfo Game')

    def bg_init(self):
        map_bg = pygame.image.load(path + 'images/map_bg.png').convert()
        writ_bg = pygame.image.load(path + 'images/writ_bg.png').convert()
        hist_bg = pygame.image.load(path + 'images/hist_bg.png').convert()
        tech_bg = pygame.image.load(path + 'images/tech_bg.png').convert()

        self.map_bg_screen = button.Button(0, 0, map_bg, scale)
        self.writ_bg_screen = button.Button(0, 0, writ_bg, scale)
        self.hist_bg_screen = button.Button(0, 0, hist_bg, scale)
        self.tech_bg_screen = button.Button(0, 0, tech_bg, scale)

    def icon_init(self):
        wom_icon = pygame.image.load(path + 'images/wom_icon.png').convert_alpha()
        writ_icon = pygame.image.load(path + 'images/writ_icon.png').convert_alpha()
        hist_icon = pygame.image.load(path + 'images/hist_icon.png').convert_alpha()
        tech_icon = pygame.image.load(path + 'images/tech_icon.png').convert_alpha()
        map_icon = pygame.image.load(path + 'images/map_icon.png').convert_alpha()


        wom_button = button.Button(SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.8, wom_icon, scale * 0.09)
        self.wom_power = button.Power(wom_button, "WOM")
        
        self.writ_button = button.Button(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.85, writ_icon, scale * 0.09)
        self.hist_button = button.Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85, hist_icon, scale * 0.09)
        self.tech_button = button.Button(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.85, tech_icon, scale * 0.09)
        self.map_button = button.Button(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, map_icon, scale * 0.09)

    def tree_init(self, game):
        tree_path = ""
        self.writ = []
        self.tech = []
        self.hist = []
        section_size = 0

        #TODO change the range after testing
        locations = []
        for section in range(0, 3):
            if section == 0:
                section_size = writ_size
                tree_path = "images/tree_icons/WRIT/"
                locations = game.tree.writ_loc
                
            elif section == 1:
                section_size = tech_size
                tree_path = "images/tree_icons/TECH/"
                locations = game.tree.tech_loc
            elif section == 2:
                section_size = hist_size
                tree_path = "images/tree_icons/HIST/"
                locations = game.tree.hist_loc
            for id in range(1, section_size):
                temp = pygame.image.load(path + tree_path + str(id) + ".png").convert_alpha()

                #This creates all the buttons overlapping, so find a way to fix this.
                temp_btn = button.Button(locations[id][0], locations[id][1], temp, scale * 0.09)

                if section == 0:
                    temp_power = button.Power(temp_btn, "WRIT" + str(id))
                    self.writ.append(temp_power)
                elif section == 1:
                    temp_power = button.Power(temp_btn, "TECH" + str(id))
                    self.tech.append(temp_power)
                elif section == 2:
                    temp_power = button.Power(temp_btn, "HIST" + str(id))
                    self.hist.append(temp_power)


    def default_screen(self, curr_screen, game):
        ret_val = curr_screen
        if curr_screen == DEFAULT:
            self.map_bg_screen.draw(self.screen)
        elif curr_screen == WRIT_TREE:
            self.writ_bg_screen.draw(self.screen)
        elif curr_screen == HIST_TREE:
            self.hist_bg_screen.draw(self.screen)
        elif curr_screen == TECH_TREE:
            self.tech_bg_screen.draw(self.screen)

        if self.writ_button.draw(self.screen):
            ret_val = WRIT_TREE
        if self.hist_button.draw(self.screen):
            ret_val = HIST_TREE
        if self.tech_button.draw(self.screen):
            ret_val = TECH_TREE

        if curr_screen != DEFAULT:
            if self.map_button.draw(self.screen):
                return DEFAULT

        if curr_screen == DEFAULT:
            if self.wom_power.draw(self.screen, game):
                game.tree.upgrade("WOM", game)

        elif curr_screen == WRIT_TREE:
            #writ tree            
            self.draw_writ_tree(game)
        elif curr_screen == TECH_TREE:
            self.draw_tech_tree(game)
            #tech_tree
        elif curr_screen == HIST_TREE:
            self.draw_hist_tree(game)
            #hist_tree

        
        #return current image
        return ret_val

    def draw_writ_tree(self, game):
        for line in game.tree.writ_lines:
            #draw lines
            width = 5 if game.tree.skills["WRIT" + str(line[1])] else 2
            pygame.draw.line(self.screen, (0,0,0), (game.tree.writ_loc[line[0]][0] + (1000 * self.scale * 0.09 / 2), game.tree.writ_loc[line[0]][1]), (game.tree.writ_loc[line[1]][0] + (1000 * self.scale * 0.09 / 2), game.tree.writ_loc[line[1]][1] + (1000 * self.scale * 0.09)), width)
        for item in self.writ:
            item.draw(self.screen, game)    

    def draw_hist_tree(self, game):
        for line in game.tree.hist_lines:
            #draw lines
            width = 5 if game.tree.skills["HIST" + str(line[1])] else 2
            pygame.draw.line(self.screen, (0,0,0), (game.tree.hist_loc[line[0]][0] + (1000 * self.scale * 0.09 / 2), game.tree.hist_loc[line[0]][1]), (game.tree.hist_loc[line[1]][0] + (1000 * self.scale * 0.09 / 2), game.tree.hist_loc[line[1]][1] + (1000 * self.scale * 0.09)), width)
        for item in self.hist:
            item.draw(self.screen, game)

    def draw_tech_tree(self, game):
        for line in game.tree.tech_lines:
            #draw lines
            width = 5 if game.tree.skills["TECH" + str(line[1])] else 2
            pygame.draw.line(self.screen, (255,255,255), (game.tree.tech_loc[line[0]][0] + (1000 * self.scale * 0.09 / 2), game.tree.tech_loc[line[0]][1]), (game.tree.tech_loc[line[1]][0] + (1000 * self.scale * 0.09 / 2), game.tree.tech_loc[line[1]][1] + (1000 * self.scale * 0.09)), width)
        for item in self.tech:
            item.draw(self.screen, game)

    def event_tree_screen(self, curr_screen, game):
        self.map_bg_screen.draw(self.screen)
        self.wom_power.draw(self.screen, game)
        self.writ_button.draw(self.screen)
        self.hist_button.draw(self.screen)
        self.tech_button.draw(self.screen)

        if not self.event_in_progress:
            self.event_index = random.randint(0, len(self.events) - 1)
            self.event_in_progress = True
        curr_screen = self.draw_event(self.event_index, self.screen, game)
        if curr_screen != EVENT:
            self.event_in_progress = False
            return curr_screen

        #return current image
        return EVENT

    def draw_end_screen(self, curr_screen, game):
        self.map_bg_screen.draw(self.screen)
        self.wom_power.draw(self.screen, game)
            
        end_text = ""
        if game.win:
            end_text = "YOU WIN!! YOU HAVE " + str(game.believers) + " tHe EnD iS NIgh"
            pygame.draw.rect(self.screen, (20, 180, 20), (250, 250, 250, 250), border_radius = 10)
        else:
            end_text = "YOU LOSE!!!"
            pygame.draw.rect(self.screen, (180, 20, 20), (250, 250, 250, 250), border_radius = 10)

        button.make_text(screen, 495, 495, end_text, (255, 255), self.count_font, (0, 0, 0))

        self.writ_button.draw(self.screen)
        self.hist_button.draw(self.screen)
        self.tech_button.draw(self.screen)

        
        #return current image
        return curr_screen

    def update_screen(self, curr_screen, believers, tot_people, game=None):
        if curr_screen != EVENT:
            self.clock.tick(self.FPS)

        # #TODO ADD TIME INTERVAL
        # if believers == 8:
        #     curr_screen = EVENT
        if curr_screen == WIN:
            curr_screen = self.draw_end_screen(curr_screen, game)
        elif curr_screen == EVENT:
            curr_screen = self.event_tree_screen(curr_screen, game)
        else:
            curr_screen = self.default_screen(curr_screen, game)
        #display the number of people converted
        believer_txt = ""
        non_believer_txt = ""
        believer_txt += str(believers) + " believers"
        non_believer_txt += str(tot_people - believers) + " non-believers"
        timer_text = str(round((game.end_time - game.counter) / 30)) + " seconds remaining"
        pygame.draw.rect(screen, (137, 207, 240), (45, 20, 225, 55), border_radius = 10)
        pygame.draw.rect(screen, (200, 200, 200), (550, 20, 175, 55), border_radius = 10)


        #surface, max_width, max_height, text, pos, font, color):
        button.make_text(screen, 750, 100, timer_text, (560, 25), self.count_font, (0, 0, 0))
        draw_text(screen, believer_txt, self.count_font, (0, 0, 0), 50, 25)
        draw_text(screen, non_believer_txt, self.count_font, (0, 0, 0), 50, 50)
        #end of test code

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                curr_screen = END

        pygame.display.update()

        return curr_screen

    def quit(self):
        pygame.quit()

    def set_events(self, events):
        self.events = []
        for event in events:
            #add event to list with event data
            #create a graphic button for the event
            #tie everything together and return screen setting of event and event index.
            #then create a function in update that displays the event prob with map background
            new_button = button.Button(event.x, event.y, None, 1, event=event, type=1, color=(0,0,0))
            self.events.append(new_button)

    def draw_event(self, index, surface, game):
        pygame.draw.rect(surface, (255,255,255), self.events[index].rect, width=0)
        pygame.draw.rect(surface, (255,0,0), self.events[index].rect, width=2)
        return self.events[index].draw_event(surface, game)


pygame.init()
clock = pygame.time.Clock()
FPS = 30

#create display window
#Each image is originally 1000 by 1000

SCREEN_HEIGHT = 1000 * scale
SCREEN_WIDTH = 1000 * scale

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Disinfo Game')

#Worlds:
map_bg = pygame.image.load(path + 'images/map_bg.png').convert()
writ_bg = pygame.image.load(path + 'images/writ_bg.png').convert()
hist_bg = pygame.image.load(path + 'images/hist_bg.png').convert()
tech_bg = pygame.image.load(path + 'images/tech_bg.png').convert()

###TODO CREATE BUTTON IMAGE PNG
wom_icon = pygame.image.load(path + 'images/wom_icon.png').convert_alpha()
writ_icon = pygame.image.load(path + 'images/writ_icon.png').convert_alpha()
hist_icon = pygame.image.load(path + 'images/hist_icon.png').convert_alpha()
tech_icon = pygame.image.load(path + 'images/tech_icon.png').convert_alpha()
map_icon = pygame.image.load(path + 'images/map_icon.png').convert_alpha()

#create button instances
wom_button = button.Button(SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.8, wom_icon, scale * 0.09)
writ_button = button.Button(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.85, writ_icon, scale * 0.09)
hist_button = button.Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85, hist_icon, scale * 0.09)
tech_button = button.Button(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.85, tech_icon, scale * 0.09)
map_button = button.Button(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, map_icon, scale * 0.09)

#World buttons
map_bg_screen = button.Button(0, 0, map_bg, scale)
writ_bg_screen = button.Button(0, 0, writ_bg, scale)
hist_bg_screen = button.Button(0, 0, hist_bg, scale)
tech_bg_screen = button.Button(0, 0, tech_bg, scale)


#game loop

def default_screen(screen):
    map_bg_screen.draw(screen)
    if wom_button.draw(screen):
        print('wom')
    if writ_button.draw(screen):
        return WRIT_TREE
    if hist_button.draw(screen):
        return HIST_TREE
    if tech_button.draw(screen):
        return TECH_TREE
    
    #return current image
    return DEFAULT

#TODO create the def for writ,hist,tech screens and make the map icon button present
def writ_tree_screen(screen, ):
    writ_bg_screen.draw(screen)
    ret_val = WRIT_TREE
    if writ_button.draw(screen):
        ret_val = WRIT_TREE
    elif hist_button.draw(screen):
        ret_val = HIST_TREE
    elif tech_button.draw(screen):
        ret_val = TECH_TREE
    elif map_button.draw(screen):
        ret_val = DEFAULT

    return ret_val

def tech_tree_screen(screen):
    tech_bg_screen.draw(screen)
    ret_val = TECH_TREE
    if writ_button.draw(screen):
        ret_val = WRIT_TREE
    elif hist_button.draw(screen):
        ret_val = HIST_TREE
    elif tech_button.draw(screen):
        ret_val = TECH_TREE
    elif map_button.draw(screen):
        ret_val = DEFAULT

    #return the current image
    return ret_val

def hist_tree_screen(screen):
    hist_bg_screen.draw(screen)
    ret_val = TECH_TREE
    if writ_button.draw(screen):
        ret_val = WRIT_TREE
    elif hist_button.draw(screen):
        ret_val = HIST_TREE
    elif tech_button.draw(screen):
        ret_val = TECH_TREE
    elif map_button.draw(screen):
        ret_val = DEFAULT

    return ret_val

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# map_icon = pygame.image.load(path + 'images/map_icon.png').convert_alpha()

# wom_button = button.Button(SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.8, wom_icon, scale * 0.09)

event_image = pygame.Rect(75, 75, 600, 600)
event_button = button.Button(75, 75, event_image, 1, 1, (255, 255, 255)) 
#event_button_txt = button.button_txt(event, event_button)
font = pygame.font.SysFont(None, 20)

text = "THIS IS A TEST TEXT TO SEE IF THIS TYPE OF THING WILL WORK!"

def event_handler(screen):
    map_bg_screen.draw(screen)
    wom_button.draw(screen)
    writ_button.draw(screen)
    hist_button.draw(screen)
    tech_button.draw(screen)

    event_button.draw(screen)
    button.make_text(screen, 580, 580, text, event_button.rect.topleft, font, (0,0,0))

    #return current image
    return DEFAULT

def graphics_test():
    pygame.init()
    #font
    count_font = pygame.font.SysFont(None, 30)

    ###TEST CODE ONLY
    people = 300000
    believers = 1

    ###TEST CODE ENDS
    num_reps = 0

    run = True
    curr_screen = DEFAULT
    while run:

        event_handler(screen)

        clock.tick(FPS)
        num_reps += 1
        # if num_reps % FPS == 0:
        #     believers = math.ceil(believers * 1.1)

        # if curr_screen == DEFAULT:
        #     curr_screen = default_screen(screen)
        # elif curr_screen == WRIT_TREE:
        #     curr_screen = writ_tree_screen(screen)
        # elif curr_screen == TECH_TREE:
        #     curr_screen = tech_tree_screen(screen)
        # elif curr_screen == HIST_TREE:
        #     curr_screen = hist_tree_screen(screen)

        #display the number of people converted
        all_fonts = pygame.font.get_fonts()

        print(all_fonts)
        believer_txt = ""
        non_believer_txt = ""
        believer_txt += str(believers) + " believers"
        non_believer_txt += str(people - believers) + " non-believers"
        draw_text(screen, believer_txt, count_font, (0, 0, 0), 50, 25)
        draw_text(screen, non_believer_txt, count_font, (0, 0, 0), 50, 50)
        #end of test code

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()



#graphics_test()