import pygame

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

    def update_text(self, text):
        self.text = text
        self.image.fill(self.colour)
        self.text_sprite = self.font.render((self.text), True, (255, 255, 255))
        self.image_center = self.image.get_rect().center
        self.image.blit(self.text_sprite, self.text_sprite.get_rect(center = self.image_center))
