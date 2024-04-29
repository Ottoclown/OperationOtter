import pygame

#this code is taken from https://github.com/russs123/pygame_tutorials/blob/main/Button/button.py 

END = -1
DEFAULT = 0
WRIT_TREE = 1
TECH_TREE = 2
HIST_TREE = 3
MENU = 4
EVENT = 5

class Power:
    def __init__(self, button, id):
        self.active = False
        self.id = id
        self.button = button

    def draw(self, surface, game):
        #pygame.draw.rect(surface, (137, 207, 240), (45, 20, 225, 55), border_radius = 10)
        if self.active:
            pygame.draw.rect(surface, (255, 255, 255), self.button.rect)
        else:
            pygame.draw.rect(surface, (50, 50, 50), self.button.rect)
        if self.button.draw(surface):
            if game.tree.upgrade(self.id, game):
                self.active = True

class Button:
    def __init__(self, x, y, image, scale, event=None, type=0, color=(0,0,0)):
        #if the image is a button
        self.clicked = False
        self.type = type
        if type == 0:
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        elif type == 1:
            self.rect = pygame.Rect(event.x, event.y, event.width, event.height)
            self.color = color
            self.event = event
            self.font = pygame.font.SysFont(None, 20)
        return
        
    def draw(self, surface):
        action = False
		#get mouse position
        pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on 
        if self.type == 0:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        elif self.type == 1:
            pygame.draw.rect(surface, self.color, self.rect, width=0)
            pygame.draw.rect(surface, (255,0,0), self.rect, width=2)
            

        return action

    def draw_txt(self, surface, max_width, max_height, prompt, print_loc, color=(0,0,0)):
        action = False
		#get mouse position
        pos = pygame.mouse.get_pos()

        pygame.draw.rect(surface, (200, 200, 200), (print_loc[0], print_loc[1], max_width, max_height), border_radius = 5)
        text_rect = pygame.Rect(print_loc[0], print_loc[1], max_width, max_height)

		#check mouseover and clicked conditions
        if text_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen

        end_pos = make_text(surface, max_width, max_height, prompt, print_loc, self.font, color)

        return (action, end_pos)

    def draw_event(self, surface, game):
        print_loc = [x + 25 for x in self.rect.topleft]
        opt_distance = 50
        opt_width = 600

        #draw the word EVENT at the top
        pygame.draw.rect(surface, (200, 200, 200), (print_loc[0], print_loc[1], self.event.width - 50, 50), border_radius = 5)
        curr_loc = self.draw_txt(surface, self.event.width - 50, 50, self.event.prompt, print_loc)
        
        curr_loc = [curr_loc[0], (curr_loc[1][0], curr_loc[1][1] + opt_distance)]
        #say option prompt 

        for option in self.event.options:
            #check if I that option is available,
            #then draw
            if option.requirements in game.tree.skills or option.requirements == "0":
                #draw an outline maybe
                
                curr_loc = self.draw_txt(surface, opt_width, opt_distance, option.text, curr_loc[1])
                if curr_loc[0]:
                    option.change(game)
                    return DEFAULT
                curr_loc = [curr_loc[0], (curr_loc[1][0], curr_loc[1][1] + opt_distance)]
                #edit population information
                #use type eventually
                
        return EVENT    

    #TODO make text setting.
    # def set_text(self, text, font, size, type):
    #     self.text = text
    #     self.font = font
    #     self.size = 

    #     if type == "EVENT":
    #         self.text = text
    #         self.font = font
    #         self.size = 

    #     elif type == "HOVER":
    #         self.text = text

#https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame

#TODO, create a draw text that is not completely copied and pasted
def make_text(surface, max_width, max_height, text, pos, font, color):
    words = text.split(' ')
    space = font.size(' ')[0]  # The width of a space.

    #true_pos = [pos[0] + 10, pos[1] + 10]

    x, y = pos#true_pos
    for word in words:
        word_render = font.render(word, 0, color)
        word_width, word_height = word_render.get_size()
        if x + word_width > max_width:
            x = pos[0]
            y += word_height
        #elif y + word_height > max_height:
            #print("error, message too long")
            #break
        surface.blit(word_render, (x, y))
        x += word_width + space
    word_render = font.render("spacing", 0, color)
    return (pos[0], y + word_render.get_size()[1])


class btn_text:
    def __init__(self, event, button):
        self.button = button
        self.txt = event.prompt

        self.font = font.render(None, True, (0,0,0))


    def draw_txt(self, surface, prompt):
        action = False
		#get mouse position
        pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        make_text(surface, 580, 580, prompt, self.button.rect.topleft, self.font, (0, 0, 0))

        return action

    # def draw_q(self):


    # def draw_p(self):
