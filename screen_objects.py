import pygame
import Pac_man_colours

# things to set up for the whole game
pygame.init()
 
 
# GLOBAL VARIABLES
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
# set up the size of the screen to be size of device's screen
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
 
RED = (255, 0, 0)
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Chess-man")

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, x_size, y_size, base_colour, selected_colour, text, text_size = None):
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.x_size = x_size
        self.y_size = y_size
        self.colour = base_colour
        self.base_colour = base_colour
        self.selected_colour = selected_colour
        self.text = text

        self.text_size = int(text_size) if text_size else int(min(x_size, y_size)//2)

        self.image = pygame.Surface([x_size, y_size])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour,pygame.Rect(x, y, x_size, y_size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        
        # text
        self.font = pygame.font.Font(None, self.text_size)
        self.text_sprite = self.font.render((self.text), True, (255, 255, 255))
        self.image_center = self.image.get_rect().center
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.colour != self.selected_colour:
                self.image.fill(self.selected_colour)
                self.colour = self.selected_colour
                self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))
        elif self.colour != self.base_colour:
            self.image.fill(self.base_colour)
            self.colour = self.base_colour
            self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))
        

    def click(self):
        pass


class High_Score_Button(Button):
    def __init__(self, x, y, x_size, y_size, base_colour, selected_colour, text, text_size=None):
        super().__init__(x, y, x_size, y_size, base_colour, selected_colour, text, text_size)

    def click(self):
        global current_screen
        current_screen = screen2


class Slider(Button):
    def __init__(self, x, y, x_base, y_base, x_size, y_size, x_button_size, y_button_size, base_colour, selected_colour, options, text, text_size=None):
        # change the text before initialising the button
        self.base_text = text
        text = self.base_text + " : 0"
        
        super().__init__(x, y, x_button_size, y_button_size, base_colour, selected_colour, text, text_size)
        
        # add details for the actual slider
        self.x_base = x_base
        self.y_base = y_base
        self.x_base_size = x_size
        self.y_base_size = y_size

        self.selected = False # whether the slider has been selected
        self.options = options # the number of options for the slider to move two
        self.option_range = self.x_base_size / self.options # the distance between each allowed option




    def update(self):
        super().update()
        if self.selected:
            x = pygame.mouse.get_pos()[0] - self.x_size * 0.5
            if x > self.x_base and x < self.x_base + self.x_base_size:
                self.x_pos = x
                self.rect.x = x
                self.image.fill(self.base_colour)
                self.text = self.base_text + " : " + str(int((self.x_pos - self.x_base)//self.option_range))
                self.text_sprite = self.font.render((self.text), True, (255, 255, 255))
                self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))
            else:
                if x < self.x_base:
                    self.x_pos = self.x_base
                    self.rect.x = self.x_pos
                else:
                    self.x_pos = self.x_base + self.x_base_size
                    self.rect.x = self.x_pos
                
        '''else:
            if (self.x_pos - self.x_pos) % self.option_range != 0:
                self.x_pos = ((self.x_pos - self.x_pos) // self.option_range) * self.option_range + self.x_pos'''


    def click(self):
        # change whether the slider is selected or not
        self.selected = not(self.selected)

        # snap the slider to the nearest option
        if not self.selected:
            self.x_pos = round((self.x_pos - self.x_base)/self.option_range) * self.option_range + self.x_base
            self.rect.x = self.x_pos


class Text_Box((pygame.sprite.Sprite)):
    def __init__(self, x, y, x_size, y_size, colour, text, text_size = None):
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.x_size = x_size
        self.y_size = y_size
        self.colour = colour
        self.text = text

        self.text_size = int(text_size) if text_size else int(min(x_size, y_size)//2)

        self.image = pygame.Surface([x_size, y_size])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour,pygame.Rect(x, y, x_size, y_size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        
        # text
        self.font = pygame.font.Font(None, self.text_size)
        self.text_sprite = self.font.render((self.text), True, (255, 255, 255))
        self.image_center = self.image.get_rect().center
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))





class Base_Screen:
    def __init__(self):
        self.SURFACE_COLOUR = (0, 0, 0)

        # group of all of the buttons on the screen
        self.buttons = pygame.sprite.Group()

        # group of all of the images on the screen including text
        self.images = pygame.sprite.Group()


    def play_step(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                self.game_over = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # get a list of all sprites that are under the mouse cursor
                pressed_buttons = [button for button in self.buttons if button.rect.collidepoint(pos)]
                
                for button in pressed_buttons:
                    button.click()

        # update the sprites
        self.buttons.update()

        # draw the background of the screen
        screen.fill(self.SURFACE_COLOUR)

        # draw all of the buttons
        self.buttons.draw(screen)

        # draw all of the non button images
        self.images.draw(screen)

        # draw the screen
        pygame.display.flip()

        # keep the speed to 60 fps
        clock.tick(60)

class High_Score_Screen(Base_Screen):
    def __init__(self):
        super().__init__()
        self.SURFACE_COLOUR = Pac_man_colours.BLUE

class Main_Menu_Screen(Base_Screen):
    def __init__(self):
        super().__init__()

        # add a button to go to the high score screen
        self.buttons.add(High_Score_Button(WIDTH * 0.2, HEIGHT * 0.8, WIDTH * 0.15, HEIGHT * 0.1, (255, 0, 0), (255, 255, 0), "High Scores"))
        self.buttons.add(Slider(WIDTH * 0.1, HEIGHT * 0.5, WIDTH * 0.1, HEIGHT * 0.5, WIDTH * 0.5, HEIGHT * 0.1, WIDTH * 0.3, HEIGHT * 0.2, Pac_man_colours.BLUE, Pac_man_colours.LIGHT_GREEN, 4, "Difficulty"))
        self.images.add(Text_Box(WIDTH * 0.25, HEIGHT * 0.2, WIDTH * 0.5, HEIGHT * 0.1, Pac_man_colours.BLUE, "Welcome to Chess-Man", int(HEIGHT * 0.1)))

if __name__ == "__main__":
    screen1 = Main_Menu_Screen()
    screen2 = High_Score_Screen()
    current_screen = screen1
    while True:
        current_screen.play_step()