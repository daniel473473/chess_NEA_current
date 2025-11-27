import pygame

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
    def __init__(self, x, y, x_size, y_size, colour, selected_colour, text, text_size):
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.x_size = x_size
        self.y_size = y_size
        self.colour = colour
        self.selected_colour = selected_colour
        self.text = text
        self.text_size = text_size

        self.image = pygame.Surface([x_size, y_size])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour,pygame.Rect(x, y, x_size, y_size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        
        # text
        self.font = pygame.font.Font(None, self.text_size)
        self.text_sprite = self.font.render((self.text), True, (255, 255, 255))
        image_center = self.image.get_rect().center
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = image_center))

class Slider:
    pass

class Base_Screen:
    def __init__(self):
        self.SURFACE_COLOUR = (0, 0, 0)

        # group of all of the buttons on the screen
        self.buttons = pygame.sprite.Group()

        # group of all of the images on the screen including text
        self.images = pygame.sprite.Group()


    def play_step(self):
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

if __name__ == "__main__":
    current_screen = Base_Screen()
    x = Button(1000, 1000, 400, 400, (255, 0, 0), (255, 255, 0), "hi", 50)
    current_screen.buttons.add(x)
    while True:
        current_screen.play_step()