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

END = -2
QUIT = -1 

DEFAULT = 0
WRIT_TREE = 1
TECH_TREE = 2
HIST_TREE = 3
MENU = 4
EVENT = 5

INTRO = 50
TUTORIAL = 51

#Size of trees
writ_size = 13
tech_size = 13
hist_size = 6

scale = 0.75

pygame.init()
clock = pygame.time.Clock()
FPS = 30

# #create display window
# #Each image is originally 1000 by 1000

SCREEN_HEIGHT = 1000 * scale
SCREEN_WIDTH = 1000 * scale

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Disinfo Game')

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
        self.intro_init()

        #self.curr_screen = DEFAULT

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Disinfo Game')

    def reset_graphics(self):
        for btn in self.writ:
            btn.deactivate()
        for btn in self.tech:
            btn.deactivate()
        for btn in self.hist:
            btn.deactivate()
        self.tut_stage = 0

    def intro_init(self):
        intro_bg = pygame.image.load(path + 'images/intro_bg.png').convert()
        start_icon = pygame.image.load(path + 'images/start_icon.png').convert_alpha()
        tut_icon = pygame.image.load(path + 'images/tut_icon.png').convert_alpha()
        next_icon = pygame.image.load(path + 'images/next.png').convert_alpha()
        tut_bg_1 = pygame.image.load(path + 'images/tut_1.png').convert_alpha()
        tut_bg_2 = pygame.image.load(path + 'images/tut_2.png').convert_alpha()
        tut_bg_3 = pygame.image.load(path + 'images/tut_3.png').convert_alpha()


        self.intro_bg_screen = button.Button(0, 0, intro_bg, scale)
        self.start_button = button.Button(SCREEN_WIDTH * 0.31, SCREEN_HEIGHT * 0.15, start_icon, scale * 0.4)
        self.tut_button = button.Button(SCREEN_WIDTH * 0.315, SCREEN_HEIGHT * 0.5, tut_icon, scale * 0.4)
        self.next_button = button.Button(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.7, next_icon, scale * 0.3)

        tut_bg_screen_1 = button.Button(0, 0, tut_bg_1, scale)
        tut_bg_screen_2 = button.Button(0, 0, tut_bg_2, scale)
        tut_bg_screen_3 = button.Button(0, 0, tut_bg_3, scale)
        self.tut_bg = []
        self.tut_bg.append(tut_bg_screen_1)
        self.tut_bg.append(tut_bg_screen_2)
        self.tut_bg.append(tut_bg_screen_3)

        self.tut_stage = 0
        


    def bg_init(self):
        map_bg = pygame.image.load(path + 'images/map_bg.png').convert()
        writ_bg = pygame.image.load(path + 'images/writ_bg.png').convert()
        hist_bg = pygame.image.load(path + 'images/hist_bg.png').convert()
        tech_bg = pygame.image.load(path + 'images/tech_bg.png').convert()
        lose_bg = pygame.image.load(path + 'images/lose_bg.png').convert()
        win_bg = pygame.image.load(path + 'images/win_bg.png').convert()

        self.map_bg_screen = button.Button(0, 0, map_bg, scale)
        self.writ_bg_screen = button.Button(0, 0, writ_bg, scale)
        self.hist_bg_screen = button.Button(0, 0, hist_bg, scale)
        self.tech_bg_screen = button.Button(0, 0, tech_bg, scale)
        self.lose_bg_screen = button.Button(0, 0, lose_bg, scale)
        self.win_bg_screen = button.Button(0, 0, win_bg, scale)

    def icon_init(self):
        wom_icon = pygame.image.load(path + 'images/wom_icon.png').convert_alpha()
        writ_icon = pygame.image.load(path + 'images/writ_icon.png').convert_alpha()
        hist_icon = pygame.image.load(path + 'images/hist_icon.png').convert_alpha()
        tech_icon = pygame.image.load(path + 'images/tech_icon.png').convert_alpha()
        map_icon = pygame.image.load(path + 'images/map_icon.png').convert_alpha()
        play_again_icon = pygame.image.load(path + 'images/play_again_icon.png').convert_alpha()


        wom_button = button.Button(SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.8, wom_icon, scale * 0.09)
        self.wom_power = button.Power(wom_button, "WOM")
        
        self.writ_button = button.Button(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.85, writ_icon, scale * 0.09)
        self.hist_button = button.Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85, hist_icon, scale * 0.09)
        self.tech_button = button.Button(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.85, tech_icon, scale * 0.09)
        self.map_button = button.Button(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, map_icon, scale * 0.09)
        self.play_again_button = button.Button(SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.675, play_again_icon, scale * 0.35)

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
        end_text = ""
        if game.win:
            self.win_bg_screen.draw(self.screen)
            end_text = "YOU WIN!! Mr. Oppenent was no match for you, and your \"cadidate\" has been elected."
            pygame.draw.rect(self.screen, (193, 225, 193), (100, 20, 550, 100), border_radius = 10)
        else:
            self.lose_bg_screen.draw(self.screen)
            end_text = "YOU LOSE!!! Mr. Opponent won reelection. Prepare to relive highschool and get bullied all over again."
            pygame.draw.rect(self.screen, (250, 160, 160), (100, 20, 550, 100), border_radius = 10)

        if self.play_again_button.draw(self.screen):
            curr_screen = INTRO
            game.reset_game()
            self.reset_graphics()

        button.make_text(screen, 645, 120, end_text, (105, 25), self.count_font, (0, 0, 0))

        #return current image
        return curr_screen

    def draw_intro_screen(self):
        self.intro_bg_screen.draw(self.screen)
        curr_screen = INTRO
        if self.start_button.draw(self.screen):
            curr_screen = DEFAULT
        # ADD TO IMPLEMENT TUTORIAL
        if self.tut_button.draw(self.screen):
            curr_screen = TUTORIAL
        return curr_screen

    def believers_and_timer(self, game):
        believer_txt = ""
        non_believer_txt = ""
        believer_txt += str(game.believers) + " believers"
        non_believer_txt += str(game.population - game.believers) + " non-believers"
        timer_text = str(round((game.end_time - game.counter) / 30)) + " days remaining"
        pygame.draw.rect(screen, (137, 207, 240), (45, 20, 225, 55), border_radius = 10)
        pygame.draw.rect(screen, (200, 200, 200), (550, 20, 175, 55), border_radius = 10)


        #surface, max_width, max_height, text, pos, font, color):
        button.make_text(screen, 725, 100, timer_text, (560, 25), self.count_font, (0, 0, 0))
        draw_text(screen, believer_txt, self.count_font, (0, 0, 0), 50, 25)
        draw_text(screen, non_believer_txt, self.count_font, (0, 0, 0), 50, 50)
        #end of test code

    def draw_tutorial_screen(self, game):
        tut_text = ""
        if self.tut_stage < 3:
            self.tut_bg[self.tut_stage].draw(self.screen)
            pygame.draw.rect(screen, (0, 0, 0), (10, 10, 740, 150), border_radius = 5)
            if self.tut_stage == 0:
                tut_text = "You were born on dark evening day in the forest. Without parents, only darkness guided you and taught you the lessons you needed to survive. A dark figure approached you one day and showed you kindness. This figure cared for you in your time of need and encouraged you to go to school to further your education."
            elif self.tut_stage == 1:
                tut_text = "Unfortunately, school was as unforgiving as the forest. You still had no friends but now you lost the comfort of the brooding trees. The school taught you much about the world around you, but it taught you more about yourself..."
            elif self.tut_stage == 2:
                tut_text = "Despite trying to share your toys with the other children, bullies made fun of you. Your biggest bully, Chad, has become the president. Luckily, you dark parental figure taught you what you need to know to start a disinformation campaign against him. Now is the time for revenge. Gain over half the population as believers before election time to elect a fake president. That will show chad."
            
            button.make_text(screen, 730, 140, tut_text, (20, 20), self.count_font, (255, 255, 255))
        
        if self.tut_stage >= 3:
            self.default_screen(DEFAULT, game)
            self.believers_and_timer(game)
            game.believers = 0
            pygame.draw.rect(screen, (255, 255, 255), (250, 250, 250, 250), border_radius = 5)
            if self.tut_stage == 3:
                draw_arrow(self.screen, (255,255,255), (250, 250), (100, 100), 7)
                tut_text = "your current believer count is located in the top left of the screen."
            if self.tut_stage == 4:
                draw_arrow(self.screen, (255,255,255), (400, 250), (600, 75), 7)
                tut_text = "The days remaining til the election is displayed in the top left."
            if self.tut_stage == 5:
                draw_arrow(self.screen, (255,255,255), (250, 400), self.wom_power.button.rect.topleft, 5)
                tut_text = "Upgrades cost current believers. Their cost and description are shown on the left of the screen when you hover your mouse over them. Click their icons to upgrade that skill."
            if self.tut_stage == 6:
                draw_arrow(self.screen, (255,255,255), (325, 400), self.writ_button.rect.topleft, 7)
                draw_arrow(self.screen, (255,255,255), (325, 400), self.tech_button.rect.topleft, 7)
                draw_arrow(self.screen, (255,255,255), (325, 400), self.hist_button.rect.topleft, 7)

                tut_text = "Navigate to different skill trees to add upgrades in different paths. Below are Writing, History, and Technology."

            if self.tut_stage == 7:
                self.draw_event(1, self.screen, game)
                tut_text = "Finally, take advantage of current events to further your disinformation campaing. Disinformation most often spreads during times of turmoil, so basing your misinformation on current events takes advantage of rising emotions while adding validity to your claims. Click next to start the game."
                button.make_text(screen, 650, 700, tut_text, (125, 425), self.count_font, (0, 0, 0))


            if self.tut_stage == 8:
                game.reset_game()
                self.curr_screen = DEFAULT
                return DEFAULT
            
            if self.tut_stage != 7:
                button.make_text(screen, 495, 395, tut_text, (255, 255), self.count_font, (0, 0, 0))

        if self.next_button.draw(self.screen):
            self.tut_stage += 1
        return TUTORIAL

    def update_screen(self, curr_screen, game):

        if curr_screen != EVENT:
            self.clock.tick(self.FPS)

        # #TODO ADD TIME INTERVAL
        # if believers == 8:
        #     curr_screen = EVENT
        if curr_screen == INTRO:
            curr_screen = self.draw_intro_screen()
        elif curr_screen == TUTORIAL:
            curr_screen = self.draw_tutorial_screen(game)
        elif curr_screen == END:
            curr_screen = self.draw_end_screen(curr_screen, game)
        elif curr_screen == EVENT:
            curr_screen = self.event_tree_screen(curr_screen, game)
        else:
            curr_screen = self.default_screen(curr_screen, game)
        #display the number of people converted
        if curr_screen >= 0 and curr_screen <= 10:
            self.believers_and_timer(game)

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                curr_screen = QUIT

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


def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#This arrow drawing code was generated using ChatGPT
def draw_arrow(screen, color, start, end, arrowhead_size):
    # Calculate the direction of the arrow
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)

    # Draw the arrow shaft
    pygame.draw.line(screen, color, start, end, arrowhead_size)

    # Draw the left side of the arrowhead
    x = end[0] - arrowhead_size * math.cos(angle - math.pi / 6)
    y = end[1] - arrowhead_size * math.sin(angle - math.pi / 6)
    pygame.draw.line(screen, color, end, (x, y), arrowhead_size)

    # Draw the right side of the arrowhead
    x = end[0] - arrowhead_size * math.cos(angle + math.pi / 6)
    y = end[1] - arrowhead_size * math.sin(angle + math.pi / 6)
    pygame.draw.line(screen, color, end, (x, y), arrowhead_size)