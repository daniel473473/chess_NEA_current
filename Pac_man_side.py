import pygame
from pygame.locals import *
import random
import Pac_man_colours
import chess_main
import time
from CHESS import chess
import helper_functions
import sys
import actual_screen_objects


# things to set up for the whole game
pygame.init()
# GLOBAL VARIABLES
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
# set up the size of the screen to be size of device's screen
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Chess-man")


# pacman class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, height, width, min_height, min_width, board_size, speed = 0.008):
        # set the players x and y
        self.x = x
        self.y = y
        
        # set the limits of where the player can move to
        self.MAXHEIGHT = min_height + board_size
        self.MAXWIDTH = min_width + board_size
        self.MINHEIGHT = min_height
        self.MINWIDTH = min_width
        # inital points of the game
        self.points = 0
        # start with no movement
        self.stop()
        # speed varibles
        self.speed = speed * board_size
        self.width = width
        self.height = height
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
        picture = pygame.image.load(helper_functions.resource_path("pngs/Chess_Gray_King.png")).convert_alpha()
        picture = pygame.transform.scale(picture, (width, height))
        self.image.blit(picture, self.image.get_rect())
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def stop(self):
        self.down = False
        self.up = False
        self.left = False
        self.right = False
    def update(self):
      # update position of the player
      if self.down:
        self.y+=self.speed
        self.rect.y = self.y

      elif self.up:
        self.y-=self.speed
        self.rect.y = self.y

      elif self.left:
        self.x-=self.speed
        self.rect.x = self.x

      elif self.right:
        self.x+=self.speed
        self.rect.x = self.x

      # limiting the movement of the player
      if self.y < self.MINHEIGHT:# upper limit
        self.y = self.MINHEIGHT
        self.rect.y = self.MINHEIGHT
        self.up = False
        self.down = True
      if self.x < self.MINWIDTH:# left most limit
        self.x = self.MINWIDTH
        self.rect.x = self.MINWIDTH
        self.left = False
        self.right = True
      if self.y > self.MAXHEIGHT:# down most limit
        self.y = self.MAXHEIGHT
        self.rect.y = self.MAXHEIGHT
        self.down = False
        self.up = True
      if self.x > self.MAXWIDTH:# right most limit
        self.x = self.MAXWIDTH
        self.rect.x = self.MAXWIDTH
        self.right = False
        self.left = True

# fruit class
class Fruit(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size, points):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

# energizer class
class Energizer(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size, points):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

# Chess piece class
class Chess_Piece(pygame.sprite.Sprite):
  pieces_moving = []

  def __init__(self, x, y, board_x, board_y, size, colour, moving_colour, flashing_colour, time_to_move = 60, flash_time = 150, name = "", sprite_path = None):
        # what is the current movement
        self.x_speed = 0
        self.y_speed = 0
        self.time_to_move = time_to_move
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.name = name

        # set up the data about the piece
        self.size = size
        self.colour = colour
        self.moving_colour = moving_colour
        self.flashing_colour = flashing_colour
        self.image_state = "stopped"
        self.flashing = False
        self.flash_time = flash_time
        self.start_flash_time = 0
        self.flashed = False
        self.actual_x = x
        self.actual_y = y
        self.board_x = board_x
        self.board_y = board_y
        self.sprite_path = sprite_path
        # set up the sprite
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, size, size))
        self.draw_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


  def draw_image(self):
    if not self.sprite_path is None:
          self.picture = pygame.image.load(helper_functions.resource_path(self.sprite_path)).convert_alpha()
          self.picture = pygame.transform.scale(self.picture, (self.size, self.size))
          self.image.blit(self.picture, self.image.get_rect())
    else:
          # temporary draw text of the name of the piece
          self.font = pygame.font.Font(None, int(self.size/2))
          self.text_sprite = self.font.render((self.name), True, Pac_man_colours.WHITE)
          self.image_center = self.image.get_rect().center
          self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))
  
  
  def move_to(self, x, y):
        self.x_speed = (x - self.rect.x)/self.time_to_move
        self.y_speed = (y - self.rect.y)/self.time_to_move
        self.target_x = x
        self.target_y = y
        self.moving = True
        self.flashing = False
        self.set_image_moving()
        Chess_Piece.pieces_moving.append(True)
  

  def set_image_moving(self):
    self.image_state = "moving"
    self.image.fill(self.moving_colour)
    if not self.sprite_path is None:
        self.image.blit(self.picture, self.image.get_rect())
    else:
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))


  def set_image_stopped(self):
    self.image_state = "stopped"
    self.image.fill(self.colour)
    if not self.sprite_path is None:
        self.image.blit(self.picture, self.image.get_rect())
    else:
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))


  def set_image_flashing(self, flash_time = None):
    self.flashing = True
    self.flashed = False
    if not flash_time is None: self.flash_time = flash_time
    self.start_flash_time = pygame.time.get_ticks()


  def flash_off(self):
    self.flashed = False
    if self.image_state == "moving":
        self.set_image_moving()
    elif self.image_state == "stopped":
        self.set_image_stopped()
  

  def flash_on(self):
    self.flashed = True
    self.image.fill(self.flashing_colour)
    if not self.sprite_path is None:
        self.image.blit(self.picture, self.image.get_rect())
    else:
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))


  def update(self):
    if self.moving:
        if (self.target_x - self.rect.x) * self.x_speed <= 0 and (self.target_y - self.rect.y) * self.y_speed <= 0:
            self.rect.x = self.target_x
            self.rect.y = self.target_y
            self.actual_x = self.target_x
            self.actual_y = self.target_y
            self.x_speed = 0
            self.y_speed = 0
            self.moving = False
            self.set_image_stopped()
            Chess_Piece.pieces_moving.pop()
            #self.move_to(random.random() * (WIDTH - self.size), random.random() * (HEIGHT - self.size))
        else:
            self.actual_x += self.x_speed
            self.actual_y += self.y_speed
            self.rect.x = self.actual_x
            self.rect.y = self.actual_y
    elif self.flashing:
        if ((pygame.time.get_ticks() - self.start_flash_time) // self.flash_time) % 2 == 0 and self.flashed == False:
            self.flash_on()
        elif ((pygame.time.get_ticks() - self.start_flash_time) // self.flash_time) % 2 == 1 and self.flashed == True:
            self.flash_off()


  def __str__(self):
     return self.name

# ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self,x, y, color, height, width, min_height, min_width, board_size, normal_sprite_path = None, scared_sprite_path = None, dead_sprite_path = None, time_to_move = 60, speed = 0.005):
        # set up the inital position of the ghost
        self.x = x
        self.y = y
        self.home_x = x
        self.home_y = y
        self.active = False
        
        # set the limits of where the ghost can move to
        self.MAXHEIGHT = min_height + board_size
        self.MAXWIDTH = min_width + board_size
        self.MINHEIGHT = min_height
        self.MINWIDTH = min_width
        # start with no movement
        self.moving = False
        self.fleeing = False
        # speed varibles
        self.speed = speed * board_size
        self.time_to_move = time_to_move
        self.width = width
        self.height = height
        super().__init__()
        # set appearence
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
        if not normal_sprite_path is None:
          self.normal_picture = pygame.image.load(helper_functions.resource_path(normal_sprite_path)).convert_alpha()
          self.normal_picture = pygame.transform.scale(self.normal_picture, (width, height))
          self.image.blit(self.normal_picture, self.image.get_rect())
        if not scared_sprite_path is None:
          self.scared_picture = pygame.image.load(helper_functions.resource_path(scared_sprite_path)).convert_alpha()
          self.scared_picture = pygame.transform.scale(self.scared_picture, (width, height))
          #self.image.blit(self.scared_picture, self.image.get_rect())
        if not dead_sprite_path is None:
          self.dead_picture = pygame.image.load(helper_functions.resource_path(dead_sprite_path)).convert_alpha()
          self.dead_picture = pygame.transform.scale(self.dead_picture, (width, height))
          #self.image.blit(self.dead_picture, self.image.get_rect())
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
          
    def change_direction(self, player_x, player_y, energized):
      if self.active == True:
        if energized:
          if not self.fleeing:
            self.move_to(self.MAXWIDTH if self.x - player_x > 0 else self.MINWIDTH, self.MAXHEIGHT if self.y - player_y < 0 else self.MINHEIGHT, time = 120)
            self.fleeing = True
        elif self.moving == False:
          self.move_to(player_x, player_y)
          self.fleeing = False


    def move_to(self, x, y, time = None):
          self.x_speed = (x - self.rect.x)/(self.time_to_move if time is None else time)
          self.y_speed = (y - self.rect.y)/(self.time_to_move if time is None else time)
          self.target_x = x
          self.target_y = y
          self.moving = True
    
    
    def update(self):
      if self.moving:
          if (self.target_x - self.x) * self.x_speed <= 0 and (self.target_y - self.y) * self.y_speed <= 0:
              self.rect.x = self.target_x
              self.rect.y = self.target_y
              self.x = self.target_x
              self.y = self.target_y
              self.x_speed = 0
              self.y_speed = 0
              self.moving = False
          else:
              self.x += self.x_speed
              self.y += self.y_speed
              self.rect.x = self.x
              self.rect.y = self.y


    def go_home(self):
          self.move_to(self.home_x, self.home_y)

# game board class
class Board:
    def __init__(self, x, y, cell_count, cell_size):
        self.cell_count = cell_count
        self.board = [["  "] * cell_count for _ in range(cell_count)]
        self.x = x
        self.y = y
        self.cell_size = cell_size


    def set_view(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size


    def render(self, screen):
        for y in range(self.cell_count):
            for x in range(self.cell_count):
                pygame.draw.rect(screen, Pac_man_colours.BLACK if (y + x) % 2 == 1 else Pac_man_colours.WHITE, (
                    x * self.cell_size + self.x,
                    y * self.cell_size + self.y,
                    self.cell_size,
                    self.cell_size))

# the class of the actual game
class Pacman_chess_game():
  def __init__(self):
    # set up the font
    self.font = pygame.font.Font(None, 36)
    # setup for everything that will be reset later
    #self.reset()


  def reset(self):
    # reset pygame events
    pygame.event.clear()

    # reset background colour
    self.SURFACE_COLOR = Pac_man_colours.HAPPY_GREEN

    # reset the lists of sprites
    self.all_sprites_list = pygame.sprite.Group()
    self.fruits = pygame.sprite.Group()
    self.energizers = pygame.sprite.Group()
    self.pieces = pygame.sprite.Group()
    self.players = pygame.sprite.Group()
    self.ghosts = pygame.sprite.Group()
    self.images = pygame.sprite.Group()

    # reset the move warning
    self.move_warning = actual_screen_objects.Text_Box(WIDTH * 0.3, HEIGHT * 0.01, WIDTH * 0.4, HEIGHT * 0.08, Pac_man_colours.BLACK, f"Next Move : {self.move_codes.peek()}", HEIGHT * 0.07)
    self.images.add(self.move_warning)
    self.all_sprites_list.add(self.move_warning)

    # reset the points
    self.points = 0

    # reset the turn
    self.turn = 1

    # reset the time of the game
    self.time = 0
    self.game_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(self.game_timer, 1000)

    # reset last blitz timer
    self.blitz = False
    self.blitz_timer = pygame.USEREVENT + 4
    pygame.time.set_timer(self.blitz_timer, 0)

    # reset energized
    self.energized = False
    self.energized_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(self.energized_timer, 0) 
    

    # reset the board
    self.cell_size = HEIGHT // 10
    board_x = WIDTH // 2 - (self.cell_size * 4)
    board_y = HEIGHT // 2 - (self.cell_size * 4)
    self.board = Board(board_x, board_y, 8, self.cell_size) # temp board in synced with actual board
    self.start_delay = 50

    # reset dead ghosts
    self.dead_ghosts = 0
    self.dead_ghosts_this_round = 0
    self.dead_ghost_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(self.dead_ghost_timer, 0) 
    # set up the ghosts 
    # top left ghost
    ghost = Ghost(self.board.x - (self.cell_size * 3) // 4, self.board.y - (self.cell_size * 3) // 4, Pac_man_colours.GRAY, self.cell_size // 2, self.cell_size // 2, self.board.y, self.board.x, self.cell_size * 8 - self.cell_size // 2, normal_sprite_path="pngs/Chess_Gray_Pawn.png", time_to_move=60)
    self.all_sprites_list.add(ghost)
    self.ghosts.add(ghost)
    # top right ghost
    ghost = Ghost(self.board.x + self.cell_size * 8 + (self.cell_size) // 4, self.board.y - (self.cell_size * 3) // 4, Pac_man_colours.GRAY, self.cell_size // 2, self.cell_size // 2, self.board.y, self.board.x, self.cell_size * 8 - self.cell_size // 2, normal_sprite_path="pngs/Chess_Gray_Pawn.png", time_to_move=55)
    self.all_sprites_list.add(ghost)
    self.ghosts.add(ghost)
    # bottom left ghost
    ghost = Ghost(self.board.x - (self.cell_size * 3) // 4, self.board.y + self.cell_size * 8 + (self.cell_size * 1) // 4, Pac_man_colours.GRAY, self.cell_size // 2, self.cell_size // 2, self.board.y, self.board.x, self.cell_size * 8 - self.cell_size // 2, normal_sprite_path="pngs/Chess_Gray_Pawn.png", time_to_move=50)
    self.all_sprites_list.add(ghost)
    self.ghosts.add(ghost)
    # bottom right ghost
    ghost = Ghost(self.board.x + self.cell_size * 8 + (self.cell_size) // 4, self.board.y + self.cell_size * 8 + (self.cell_size * 1) // 4, Pac_man_colours.GRAY, self.cell_size // 2, self.cell_size // 2, self.board.y, self.board.x, self.cell_size * 8 - self.cell_size // 2, normal_sprite_path="pngs/Chess_Gray_Pawn.png", time_to_move=45)
    self.all_sprites_list.add(ghost)
    self.ghosts.add(ghost)
    
    
    # reset game over
    self.game_over = False
    
    # add the starting sprites back into the list
    self.player = Player(WIDTH // 2 - self.cell_size // 4, HEIGHT // 2 - self.cell_size // 4, Pac_man_colours.GRAY, self.cell_size // 2, self.cell_size // 2, board_y, board_x, self.cell_size * 8 - self.cell_size // 2)
    self.all_sprites_list.add(self.player)
    self.players.add(self.player)



    # create a set number of fruits
    for i in range(32):
      f1 = Fruit(Pac_man_colours.RED, *self.convert_board_coors(i % 8, i // 8 + 2, offset = self.board.cell_size // 2 - self.board.cell_size // 16), self.cell_size // 8, 1)
      self.all_sprites_list.add(f1)
      self.fruits.add(f1)
    
    # create the chess pieces
    self.chess_piece_size = self.cell_size * 0.9
    self.last_piece_moved = None
    self.piece_to_remove = False
    self.promotion_data = False
    Chess_Piece.pieces_moving = [] # reset the moving pieces so new pieces can move

    # black pieces
    self.blacknames = ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR", "BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"]
    self.black_file_paths = ["pngs/Chess_Black_Rook.png", "pngs/Chess_Black_Knight.png", "pngs/Chess_Black_Bishop.png", "pngs/Chess_Black_Queen.png", "pngs/Chess_Black_King.png", "pngs/Chess_Black_Bishop.png", "pngs/Chess_Black_Knight.png", "pngs/Chess_Black_Rook.png",
                         "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png", "pngs/Chess_Black_Pawn.png"]
    self.whitenames = ["WR", "WN", "WB", "WK", "WQ", "WB", "WN", "WR", "WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"]
    self.white_file_paths = ["pngs/Chess_White_Rook.png", "pngs/Chess_White_Knight.png", "pngs/Chess_White_Bishop.png", "pngs/Chess_White_King.png", "pngs/Chess_White_Queen.png", "pngs/Chess_White_Bishop.png", "pngs/Chess_White_Knight.png", "pngs/Chess_White_Rook.png",
                        "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png", "pngs/Chess_White_Pawn.png"]
    # black pieces
    for i in range(16):
        piece = Chess_Piece(*self.convert_board_coors(i % 8, i // 8, offset = self.cell_size * 0.05), i % 8, i // 8, self.chess_piece_size, Pac_man_colours.RED, Pac_man_colours.RED,  Pac_man_colours.DARK_RED, name = self.blacknames[i], sprite_path= self.black_file_paths[i])
        self.all_sprites_list.add(piece)
        self.pieces.add(piece)
        self.board.board[i//8][i%8] = piece

    # white pieces
    for i in range(16):
        piece = Chess_Piece(*self.convert_board_coors(7 - (i % 8), 7 - (i // 8), offset = self.cell_size * 0.05), 7 - (i % 8), 7 - (i // 8), self.chess_piece_size, Pac_man_colours.GREEN, Pac_man_colours.GREEN, Pac_man_colours.DARK_GREEN, name = self.whitenames[i], sprite_path= self.white_file_paths[i])
        self.all_sprites_list.add(piece)
        self.pieces.add(piece)
        self.board.board[7 - (i//8)][7 - (i%8)] = piece

    # reset the info box
    self.info_box = actual_screen_objects.Text_Box(WIDTH * 0.05, HEIGHT * 0.05, WIDTH * 0.1, HEIGHT * 0.15, Pac_man_colours.BLACK, "", 0)
    self.images.add(self.info_box)
    self.all_sprites_list.add(self.info_box)
    # reset the text for points
    self.text = self.font.render(f"Score : {str(self.points)}", True, (255, 255, 255))
    # reset the rect of the text
    self.text_rect = self.text.get_rect(center=(WIDTH * 0.1, HEIGHT * 0.1))  # Centered in the window
    # reset the text for time
    self.time_text = self.font.render(f"Time : {str(self.time)}", True, (255, 255, 255))
    # reset the rect of the text
    self.time_text_rect = self.time_text.get_rect(center=(WIDTH * 0.1, HEIGHT * 0.15))  # Centered in the window


  def convert_board_coors(self, board_x, board_y, offset = 0):
    return self.board.x + (board_x * self.board.cell_size) + offset, self.board.y + (board_y * self.board.cell_size) + offset


  def move_piece(self, start_coor, end_coor):
    # find what piece is moving
    piece = self.board.board[start_coor[0]][start_coor[1]]

    # last moved piece
    self.last_piece_moved = piece

    # set the piece moving
    x, y = end_coor[1], end_coor[0]

    # add a fruit where the piece was
    f1 = Fruit(Pac_man_colours.RED, *self.convert_board_coors(piece.board_x, piece.board_y, offset = self.cell_size // 2 - self.board.cell_size // 16 - 1), self.cell_size // 8, 1)
    self.all_sprites_list.add(f1)
    self.fruits.add(f1)

    
    # set the new location to be the location of the piece
    self.board.board[y][x] = self.board.board[piece.board_y][piece.board_x]
    piece.board_y, piece.board_x = y, x
    piece.move_to(*self.convert_board_coors(x, y, offset = self.board.cell_size * 0.05))
    
    # set the old location to be empty
    self.board.board[start_coor[0]][start_coor[1]] = "  "


  def check_collisions(self):
    # check for collisions with fruit and delete any fruit collided with
    eaten_fruits = pygame.sprite.spritecollide(self.player, self.fruits, True)
    if eaten_fruits:
      for fruit in eaten_fruits:
        self.points += fruit.points
      self.text = self.font.render(f"Score : {str(self.points)}", True, (255, 255, 255))

    # check for collisions with energizers and delete any collided with
    collected_energizers = pygame.sprite.spritecollide(self.player, self.energizers, True)
    if collected_energizers:
        for energizer in collected_energizers:
            self.points += energizer.points
        # create a timer for the energizer to last for
        self.energized = True
        pygame.time.set_timer(self.energized_timer, 3000)

        self.text = self.font.render(f"Score : {str(self.points)}", True, (255, 255, 255))
    
    # check for collisions with chess pieces and player to kill player if the piece is moving else act as a wall
    collided_pieces = pygame.sprite.spritecollide(self.player, self.pieces, False)
    if collided_pieces:
        for piece in collided_pieces:
            
            # if the piece is not moving so functions as a wall
            if piece.x_speed == piece.y_speed and piece.x_speed == 0:
                # move the player out of range of the piece
                if self.player.up:
                   self.player.y += (piece.rect.y + piece.size) - self.player.y
                   self.player.rect.y = self.player.y
                elif self.player.down:
                   self.player.y -= (self.player.y + self.player.height) - piece.rect.y
                   self.player.rect.y = self.player.y
                elif self.player.left:
                   self.player.x += (piece.rect.x + piece.size) - self.player.rect.x
                   self.player.rect.x = self.player.x
                elif self.player.right:
                   self.player.x -= (self.player.x + self.player.width) - piece.rect.x
                   self.player.rect.x = self.player.x
            else:
              self.game_over = True
        if self.player.up:
          self.player.up = False
          self.player.down = True
        elif self.player.down:
          self.player.down = False
          self.player.up = True
        elif self.player.left:
          self.player.left = False
          self.player.right = True
        elif self.player.right:
          self.player.right = False
          self.player.left = True
        
    # check for collisions with ghosts to when there is no energizer
    collided_pieces = pygame.sprite.spritecollide(self.player, self.ghosts, False)
    if collided_pieces:
        for piece in collided_pieces:
          if piece.active == True:
            if self.energized:# code for eating the ghosts
              self.dead_ghosts += 1 
              self.dead_ghosts_this_round += 1
              pygame.time.set_timer(self.dead_ghost_timer, 4000)
              # remove the eaten ghost
              piece.active = False
              piece.go_home()
              self.points += 2 ** (self.dead_ghosts_this_round - 1) * 50
              self.text = self.font.render(f"Score : {str(self.points)}", True, (255, 255, 255))
            else:
              self.game_over = True


  def run_next_move(self, move):
     if type(move[0][0]) == list:
        for sub_move in move:
          self.run_next_move(sub_move)
     else:
        self.move_piece(move[1], move[0])


  def check_next_move(self, move):
     if type(move[0][0]) == list:
        for sub_move in move:
          self.check_next_move(sub_move)
     else:
        self.check_move(move[1], move[0])


  def check_move(self, start_coor, end_coor):
      piece = self.board.board[start_coor[0]][start_coor[1]]
      piece.set_image_flashing()


  def play_step(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          sys.exit()
          self.game_over = True
      elif event.type == pygame.KEYDOWN:
        if event.key == K_DOWN:
          self.player.down = True
          self.player.up = False
          self.player.left = False
          self.player.right = False
        elif event.key == K_UP:
          self.player.down = False
          self.player.up = True
          self.player.left = False
          self.player.right = False
        elif event.key == K_LEFT:
          self.player.down = False
          self.player.up = False
          self.player.left = True
          self.player.right = False
        elif event.key == K_RIGHT:
          self.player.down = False
          self.player.up = False
          self.player.left = False
          self.player.right = True
      elif event.type == self.energized_timer:# if energizer time is up
          self.energized = False
          self.dead_ghosts_this_round = 0
          pygame.time.set_timer(self.energized_timer, 0)
      elif event.type == self.dead_ghost_timer:# if a ghost should respawn
          for i in self.ghosts:
            if not i.active:
                i.active = True
                i.waiting = False
                break
          self.dead_ghosts -= 1
          if self.dead_ghosts <= 0:
            pygame.time.set_timer(self.dead_ghost_timer, 0)
      elif event.type == self.game_timer:# increase the time of the game
          self.time += 1
          self.time_text = self.font.render(f"Time : {str(self.time)}", True, (255, 255, 255))
      elif event.type == self.blitz_timer:# end the game after blitz time
        self.points *= 2 # double the score for finishing the game
        print("Final Score : ", self.points)
        self.game_over = True
        self.blitz = False
        pygame.time.set_timer(self.blitz_timer, 0)
    
    # check if another piece should move
    if not Chess_Piece.pieces_moving and self.start_delay < 0:
       if self.piece_to_remove:
           print(f"piece there? {self.piece_to_remove in self.pieces}")
           # add a energizer where the piece was
           e1 = Energizer(Pac_man_colours.YELLOW, *self.convert_board_coors(self.piece_to_remove.board_x, self.piece_to_remove.board_y, offset = self.cell_size // 2 - self.board.cell_size // 12 - 1), self.cell_size // 6, 10)
           self.all_sprites_list.add(e1)
           self.energizers.add(e1)
           self.pieces.remove(self.piece_to_remove)
           self.all_sprites_list.remove(self.piece_to_remove)

           # spawn a new ghost if there are too few for the number of pieces
           if len(self.pieces) % 7 == 0:# spawn a ghost for every 7 pieces that are taken for a total of 4 ghosts at once
              for i in self.ghosts:
                  if not i.active:
                     i.active = True
                     break 
       if not self.moves.isEmpty():
          # update the data for the last moved piece
          if self.promotion_data:
            self.last_piece_moved.sprite_path = self.promotion_data[1]
            self.last_piece_moved.name = self.promotion_data[0]
            self.last_piece_moved.draw_image()
            self.promotion_data = False


          # change the piece for promotion
          
          promotion = self.promotions.dequeue()
          if promotion is not None:
            if self.turn % 2 == 1:
              match promotion:
                  case "Q":
                    self.promotion_data = ("WQ", "pngs/Chess_White_Queen.png")
                  case "K":
                    self.promotion_data = ("WK", "pngs/Chess_White_King.png")
                  case "B":
                    self.promotion_data = ("WB", "pngs/Chess_White_Bishop.png")
                  case "N":
                    self.promotion_data = ("WN", "pngs/Chess_White_Knight.png")
                  case "R":
                    self.promotion_data = ("WR", "pngs/Chess_White_Rook.png")
            else:
              match promotion:
                case "Q":
                  self.promotion_data = ("BQ", "pngs/Chess_Black_Queen.png")
                case "K":
                  self.promotion_data = ("BK", "pngs/Chess_Black_King.png")
                case "B":
                  self.promotion_data = ("BB", "pngs/Chess_Black_Bishop.png")
                case "N":
                  self.promotion_data = ("BN", "pngs/Chess_Black_Knight.png")
                case "R":
                  self.promotion_data = ("BR", "pngs/Chess_Black_Rook.png")

          
          # add the taken piece
          self.piece_to_remove = False if self.taken_pieces.peek() is None else self.board.board[self.taken_pieces[0][0]][self.taken_pieces[0][1]]
          self.taken_pieces.dequeue()
          # show the player the next move
          self.move_warning.update_text(f"Next Move : {self.move_codes.dequeue()}")
          self.run_next_move(self.moves.dequeue())
          self.boards.dequeue()
          
          #print(self.moves)
          if not self.moves.isEmpty():
            self.check_next_move(self.moves.peek())

          # increase the turn
          self.turn += 1
       else:
          if not self.blitz:
             # change background colour
             self.SURFACE_COLOR = Pac_man_colours.DARK_RED
             pygame.time.set_timer(self.blitz_timer, 10000)
             self.blitz = True
             for i in self.ghosts:
                i.active = True
                i.time_to_move /= 2
             for piece in self.pieces:
                 piece.flashing = False
          if self.energized: # turn off energized for end of game
             self.energized = False
             pygame.time.set_timer(self.energized_timer, 0)
    else:
       self.start_delay -= 1
    
    for ghost in self.ghosts:
        ghost.change_direction(self.player.x, self.player.y, self.energized)

    self.all_sprites_list.update()
    self.check_collisions()
    screen.fill(self.SURFACE_COLOR)
    self.board.render(screen)
    #self.all_sprites_list.draw(screen)
    self.images.draw(screen)
    self.fruits.draw(screen)
    self.energizers.draw(screen)
    self.pieces.draw(screen)
    self.ghosts.draw(screen)
    self.players.draw(screen)
    screen.blit(self.text, self.text_rect)
    screen.blit(self.time_text, self.time_text_rect)
    pygame.display.flip()
    clock.tick(60)
    #if clock.get_fps() < 60:
    #  print(clock.get_fps())


  def prepare_game(self, depth):
     return chess_main.play_game(depth)


  def play(self, moves = helper_functions.Queue([]), boards = helper_functions.Queue([]), move_codes = helper_functions.Queue([]), taken_pieces = helper_functions.Queue([]), promotions = helper_functions.Queue([])):
    self.moves, self.boards, self.move_codes, self.taken_pieces, self.promotions = moves, boards, move_codes, taken_pieces, promotions
    print(self.move_codes)

    self.reset()

    while not self.game_over:
          self.play_step()
    return self.points, self.time


if __name__ == "__main__":
    while True:
      game = Pacman_chess_game()
      start_time = time.time()
      moves, boards, move_codes, taken_pieces, promotions = chess_main.play_game(1)
      #moves = [[[4, 4], [6, 4]], [[3, 4], [1, 4]], [[5, 5], [7, 6]], [[2, 5], [0, 3]], [[3, 1], [7, 5]], [[3, 2], [0, 5]], [[[7, 6], [7, 4]], [[7, 5], [7, 7]]], [[2, 2], [1, 2]], [[5, 3], [3, 1]], [[3, 3], [1, 3]], [[3, 3], [4, 4]], [[4, 6], [0, 2]], [[2, 2], [3, 3]], [[2, 2], [1, 1]], [[5, 2], [7, 1]], [[2, 7], [1, 7]], [[4, 4], [5, 2]], [[6, 5], [3, 2]], [[6, 5], [7, 5]], [[2, 6], [2, 5]], [[3, 4], [5, 5]], [[7, 3], [4, 6]], [[2, 6], [3, 4]], [[2, 6], [1, 5]], [[4, 2], [5, 3]], [[6, 2], [7, 3]], [[5, 3], [6, 3]], [[2, 5], [0, 6]], [[6, 2], [6, 5]], [[1, 3], [0, 1]], [[4, 5], [7, 2]], [[2, 1], [1, 3]], [[2, 4], [4, 2]], [[0, 5], [0, 7]], [[2, 3], [4, 5]], [[0, 7], [0, 5]], [[3, 2], [4, 4]], [[1, 3], [0, 1]], [[1, 3], [2, 4]], [[1, 3], [0, 1]], [[7, 4], [7, 0]], [[0, 3], [0, 4]], [[1, 3], [3, 2]], [[1, 3], [0, 3]], [[4, 5], [2, 3]], [[0, 4], [0, 7]], [[5, 4], [4, 5]], [[0, 3], [0, 0]], [[4, 3], [5, 3]], [[0, 4], [0, 3]], [[5, 2], [6, 2]], [[0, 3], [0, 0]], [[5, 7], [6, 7]], [[0, 4], [0, 3]], [[7, 2], [5, 2]], [[4, 4], [0, 4]], [[7, 5], [7, 2]], [[0, 4], [0, 0]], [[7, 7], [7, 6]], [[3, 2], [2, 2]], [[3, 2], [4, 3]], [[2, 2], [1, 3]], [[7, 3], [7, 5]], [[3, 7], [2, 7]], [[4, 3], [7, 3]], [[0, 2], [0, 0]], [[4, 6], [6, 6]], [[0, 4], [0, 2]], [[3, 7], [4, 6]], [[3, 7], [2, 6]], [[7, 3], [4, 3]], [[0, 2], [0, 0]], [[5, 0], [6, 0]], [[0, 4], [0, 2]], [[7, 6], [7, 7]], [[0, 2], [0, 0]], [[4, 0], [5, 0]], [[0, 4], [0, 2]], [[3, 0], [4, 0]], [[0, 2], [0, 0]], [[2, 0], [3, 0]], [[0, 4], [0, 2]], [[7, 7], [7, 6]], [[0, 2], [0, 0]], [[5, 1], [6, 1]], [[0, 4], [0, 2]], [[4, 1], [5, 1]], [[4, 7], [3, 7]], [[5, 3], [7, 3]], [[2, 6], [1, 6]], [[4, 3], [5, 3]], [[0, 2], [0, 0]], [[3, 1], [4, 1]], [[3, 1], [2, 2]], [[4, 7], [4, 3]], [[2, 0], [3, 1]], [[4, 1], [4, 7]], [[3, 0], [2, 0]], [[7, 1], [4, 1]], [[4, 0], [3, 0]], [[7, 2], [5, 4]], [[3, 2], [0, 2]], [[5, 0], [5, 2]]]
      print(time.time() - start_time)
      #print(moves)
      game.play(moves, boards, move_codes, taken_pieces, promotions)
      print(game.points)
