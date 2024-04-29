import pygame

pygame.init()

FPS = 60

all_fonts = pygame.font.get_fonts()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

def test_font(max_width, text, pos, fonts, color):
    #true_pos = [pos[0] + 10, pos[1] + 10]
    iter = 0
    words = text.split(' ')
    for font in fonts:
        x, y = pos#true_pos
        print(font)
        curr_font = pygame.font.SysFont(font, 20)
        space = curr_font.size(' ')[0]  # The width of a space.
        for word in words:
            word_render = curr_font.render(word, 0, color)
            word_width, word_height = word_render.get_size()
            y += iter * word_height
            if x + word_width > max_width:
                x = pos[0]
                y += word_height
            #elif y + word_height > max_height:
                #print("error, message too long")
                #break
            screen.blit(word_render, (x, y))
            x += word_width + space
        word_render = curr_font.render("spacing", 0, color)
        iter += 1
    return (pos[0], y + word_render.get_size()[1])


def graphics_test():
    pygame.init()

    run = True
    all_fonts = pygame.font.get_fonts()
    txt = "123456789"
    while run:
        clock.tick(FPS)

        test_font(900, txt, [50, 50], all_fonts, (0, 0, 0))
        #end of test code

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()



graphics_test()