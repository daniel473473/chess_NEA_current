import pygame
import Pac_man_colours
import Pac_man_side
import helper_functions
import sys
import actual_screen_objects
import threading


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

# loading screen control
loading = False


def run_loading_screen():
    global current_screen
    current_screen = loading_screen
    current_screen.reset()
    while loading:
        current_screen.play_step()



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


class End_Game_Button(Button): # button to exit the game
    def __init__(self, x, y, x_size, y_size, base_colour, selected_colour, text, text_size=None):
        super().__init__(x, y, x_size, y_size, base_colour, selected_colour, text, text_size)

    def click(self):
        sys.exit()


class High_Score_Button(Button):
    def __init__(self, x, y, x_size, y_size, base_colour, selected_colour, text, text_size=None):
        super().__init__(x, y, x_size, y_size, base_colour, selected_colour, text, text_size)

    def click(self):
        global current_screen
        current_screen = high_score_screen
        current_screen.reset()
        current_screen.get_scores()
        current_screen.scroll = 0


class Game_Button(Button):
    def __init__(self, x, y, x_size, y_size, base_colour, selected_colour, text, text_size=None):
        super().__init__(x, y, x_size, y_size, base_colour, selected_colour, text, text_size)

    def click(self):
        global current_screen
        global loading
        global game_screen
        loading_thread = threading.Thread(target=run_loading_screen)
        loading = True
        loading_thread.start()
        moves, boards, move_codes, taken_pieces, promotions = game_screen.prepare_game(main_menu.depth)
        loading = False
        current_screen = game_screen
        score, time = current_screen.play(moves=moves, boards=boards, move_codes=move_codes, taken_pieces=taken_pieces, promotions=promotions)
        data = helper_functions.load_data(helper_functions.user_data_path("high_scores.json"))
        data["scores"].append({"score": score, "time": time, "difficulty": main_menu.depth})
        # sort the scores from highest to lowest
        data["scores"].sort(key=lambda x: x["score"], reverse=True)
        helper_functions.store_data(helper_functions.user_data_path("high_scores.json"), data)
        current_screen = play_again_screen
        current_screen.reset()
        play_again_screen.update_score(score, time, main_menu.depth)


class Main_Menu_Button(Button):
    def __init__(self, x, y, x_size, y_size, base_colour, selected_colour, text, text_size=None):
        super().__init__(x, y, x_size, y_size, base_colour, selected_colour, text, text_size)

    def click(self):
        global current_screen
        current_screen = main_menu
        current_screen.reset()


class Slider(Button):
    def __init__(self, x, y, x_base, y_base, x_size, y_size, x_button_size, y_button_size, base_colour, selected_colour, options, text, text_size=None, ID = None):
        self.ID = ID
        
        # change the text before initialising the button
        self.base_text = text
        text = self.base_text + " : 1"
        
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
        if not self.selected:
            super().update()
        if self.selected:
            x = pygame.mouse.get_pos()[0] - self.x_size * 0.5
            if x > self.x_base and x < self.x_base + self.x_base_size:
                self.x_pos = x
                self.rect.x = x
                self.image.fill(self.base_colour)
                self.text = self.base_text + " : " + str(round((self.x_pos - self.x_base)/self.option_range) + 1)
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

            # update the text for where it snapped to
            self.image.fill(self.base_colour)
            self.text = self.base_text + " : " + str(round((self.x_pos - self.x_base)/self.option_range) + 1)
            self.text_sprite = self.font.render((self.text), True, (255, 255, 255))
            self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))

        return [round((self.x_pos - self.x_base)/self.option_range) + 1, self.ID]


class Scroll_Bar(Button):
    def __init__(self, x, y, x_base, y_base, x_size, y_size, x_button_size, y_button_size, base_colour, selected_colour, ID = None):
        self.ID = ID
        
        
        super().__init__(x, y, x_button_size, y_button_size, base_colour, selected_colour, "", 0)
        
        # add details for the actual scroll bar
        self.x_base = x_base
        self.y_base = y_base
        self.x_base_size = x_size
        self.y_base_size = y_size

        self.selected = False # whether the scroll bar has been selected
        self.scroll = 0 # ratio of how scrolled through bar is

    def update(self):
        if not self.selected:
            super().update()
        if self.selected:
            y = pygame.mouse.get_pos()[1] - self.y_size * 0.5
            if y > self.y_base and y < self.y_base + self.y_base_size:
                self.y_pos = y
                self.rect.y = y
                self.image.fill(self.base_colour)
                self.scroll = (y - self.y_base) / self.y_base_size
            else:
                if y < self.y_base:
                    self.y_pos = self.y_base
                    self.rect.y = self.y_pos
                    self.scroll = 0
                else:
                    self.y_pos = self.y_base + self.y_base_size
                    self.rect.y = self.y_pos
                    self.scroll = 1


    def click(self):
        # change whether the slider is selected or not
        self.selected = not(self.selected)

        # snap the slider to the nearest option
        if not self.selected:
            self.image.fill(self.base_colour)

        return [self.scroll, self.ID]


class Base_Screen:
    def __init__(self):
        self.SURFACE_COLOUR = (0, 0, 0)

        # group of all of the buttons on the screen
        self.buttons = pygame.sprite.Group()

        # group of all of the sliders on the screen
        self.sliders = pygame.sprite.Group()

        # group of all of the images on the screen including text
        self.images = pygame.sprite.Group()

        # any data that the screen needs to store
        self.data = []


    def check_data(self): # function to be replaced by inherited classes to work with any stored data
        pass


    def play_step(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                # get a list of all buttons that are under the mouse cursor
                pressed_buttons = [button for button in self.buttons if button.rect.collidepoint(pos)]
                
                for button in pressed_buttons:
                    button.click()

                # get a list of all sliders that are under the mouse cursor
                pressed_sliders = [slider for slider in self.sliders if slider.rect.collidepoint(pos)]
                
                # reset the data when more is added
                self.data = []

                for slider in pressed_sliders:
                    self.data.append(slider.click())

                self.check_data()



        # update the sprites
        self.buttons.update()
        self.sliders.update()

        # draw the background of the screen
        screen.fill(self.SURFACE_COLOUR)

        # draw all of the buttons
        self.buttons.draw(screen)

        # draw all of the sliders
        self.sliders.draw(screen)

        # draw all of the non button images
        self.images.draw(screen)

        # draw the screen
        pygame.display.flip()

        # keep the speed to 60 fps
        clock.tick(60)


    def reset(self):
        for slider in self.sliders:
            slider.selected = False


class High_Score_Screen(Base_Screen):
    def __init__(self):
        super().__init__()
        self.scroll = 0
        self.score_seperation = HEIGHT * 0.1
        self.buttons.add(Main_Menu_Button(WIDTH * 0.85, HEIGHT * 0.2, WIDTH * 0.15, HEIGHT * 0.1, (255, 0, 0), (255, 255, 0), "Main Menu"))
        self.sliders.add(Scroll_Bar(WIDTH * 0.81, HEIGHT * 0.15, WIDTH * 0.85, HEIGHT * 0.15, WIDTH * 0.05, HEIGHT * 0.6, WIDTH * 0.025, HEIGHT * 0.2, Pac_man_colours.GRAY, Pac_man_colours.WHITE, ID="scroll"))
        self.score_sprite = actual_screen_objects.Text_Box(WIDTH * 0.2, HEIGHT * 0.2, WIDTH * 0.6, HEIGHT * 0.7, Pac_man_colours.GRAY, "", text_size= int(HEIGHT * 0.075))
        self.images.add(self.score_sprite)
        self.get_scores()
        

    def check_data(self):
        for item in self.data:
            if item[-1] == "scroll":
                self.scroll = item[0]
                self.get_scores()


    def get_scores(self):# load all of the high score data
        file_data = helper_functions.load_data(helper_functions.user_data_path("high_scores.json"))
        if "scores" not in file_data:
            file_data["scores"] = []
            helper_functions.store_data(helper_functions.user_data_path("high_scores.json"), file_data)
        self.scores = helper_functions.load_data(helper_functions.user_data_path("high_scores.json"))["scores"]
        # first reset the score sprite
        self.score_sprite.image.fill(self.score_sprite.colour)
        for i, item in enumerate(self.scores):
            temp_text = self.score_sprite.font.render((f"{i + 1}. Score : {item['score']}, Time : {item['time']}, Difficulty : {item['difficulty']}"), True, (255, 255, 255))
            self.score_sprite.image.blit(temp_text, (WIDTH * 0.01, HEIGHT * 0.05 + self.score_seperation * i - self.scroll * max(len(self.scores) - 6,0) * (self.score_seperation)))


class Main_Menu_Screen(Base_Screen):
    def __init__(self):
        super().__init__()
        self.depth = 1

        # add a button to go to the high score screen
        self.buttons.add(High_Score_Button(WIDTH * 0.2, HEIGHT * 0.8, WIDTH * 0.15, HEIGHT * 0.1, (255, 0, 0), (255, 255, 0), "High Scores"))
        self.sliders.add(Slider(WIDTH * 0.1, HEIGHT * 0.5, WIDTH * 0.1, HEIGHT * 0.5, WIDTH * 0.5, HEIGHT * 0.1, WIDTH * 0.3, HEIGHT * 0.2, Pac_man_colours.BLUE, Pac_man_colours.LIGHT_GREEN, 3, "Skill", ID="Depth"))
        self.buttons.add(Game_Button(WIDTH * 0.5, HEIGHT * 0.8, WIDTH * 0.15, HEIGHT * 0.1, (255, 0, 0), (255, 255, 0), "Play"))
        self.images.add(actual_screen_objects.Text_Box(WIDTH * 0.25, HEIGHT * 0.2, WIDTH * 0.5, HEIGHT * 0.1, Pac_man_colours.BLUE, "Welcome to Chess-Man", int(HEIGHT * 0.1)))
        # add a button to exit the game
        self.buttons.add(End_Game_Button(WIDTH * 0.825, HEIGHT * 0.125, WIDTH * 0.1, HEIGHT * 0.1, Pac_man_colours.BLUE, Pac_man_colours.YELLOW, "Quit", text_size=int(HEIGHT * 0.05)))


    def check_data(self):
        for item in self.data:
            if item[-1] == "Depth":
                self.depth = item[0]


class Play_Again_Screen(Base_Screen):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.time = 0
        self.difficulty = 1
        self.buttons.add(Main_Menu_Button(WIDTH * 0.2, HEIGHT * 0.8, WIDTH * 0.15, HEIGHT * 0.1, (255, 0, 0), (255, 255, 0), "Main Menu"))
        self.buttons.add(Game_Button(WIDTH * 0.5, HEIGHT * 0.8, WIDTH * 0.3, HEIGHT * 0.1, (255, 0, 0), (255, 255, 0), "Play Again"))
        self.images.add(actual_screen_objects.Text_Box(WIDTH * 0.25, HEIGHT * 0.2, WIDTH * 0.5, HEIGHT * 0.1, Pac_man_colours.BLUE, f"Game Over", int(HEIGHT * 0.1)))
        self.score_box = actual_screen_objects.Text_Box(WIDTH * 0.1, HEIGHT * 0.5, WIDTH * 0.3, HEIGHT * 0.1, Pac_man_colours.BLUE, f"Score : {self.score}", int(HEIGHT * 0.1))
        self.images.add(self.score_box)
        self.time_box = actual_screen_objects.Text_Box(WIDTH * 0.6, HEIGHT * 0.5, WIDTH * 0.3, HEIGHT * 0.1, Pac_man_colours.BLUE, f"Time : {self.time}", int(HEIGHT * 0.1))
        self.images.add(self.time_box)
        self.depth_box = actual_screen_objects.Text_Box(WIDTH * 0.35, HEIGHT * 0.35, WIDTH * 0.3, HEIGHT * 0.1, Pac_man_colours.BLUE, f"Difficulty : {self.difficulty}", int(HEIGHT * 0.1))
        self.images.add(self.depth_box)




    def update_score(self, score, time, difficulty):
        self.score = score
        self.time = time
        self.difficulty = difficulty
        self.score_box.update_text(f"Score : {self.score}")
        self.time_box.update_text(f"Time : {self.time}")
        self.depth_box.update_text(f"Difficulty : {self.difficulty}")
        

class Loading_Screen(Base_Screen):
    def __init__(self):
        super().__init__()
        self.images.add(actual_screen_objects.Text_Box(WIDTH * 0.3, HEIGHT * 0.45, WIDTH * 0.4, HEIGHT * 0.1, Pac_man_colours.BLUE, "Loading Game!", int(HEIGHT * 0.1)))



if __name__ == "__main__":
    main_menu = Main_Menu_Screen()
    high_score_screen = High_Score_Screen()
    game_screen = Pac_man_side.Pacman_chess_game()
    play_again_screen = Play_Again_Screen()
    loading_screen = Loading_Screen()
    current_screen = main_menu
    while True:
        current_screen.play_step()
    #current_screen.buttons.sprites()[1].click()
