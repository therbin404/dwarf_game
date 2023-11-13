import sys, time, pygame
import camera.camera as Camera
import player.player as Player

pygame.init()


class Game:
    ##############
    #### GAME ####
    ##############

    def __init__(self):
        self.current_map = "./assets/terrain/map.png"

        self.screen_width, self.screen_height = 1024, 768

        self.screen_size = self.screen_width, self.screen_height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.background = pygame.image.load(self.current_map).convert()
        # make a rect by bg size to avoid player and camera to be outside of it
        self.background_rect = self.background.get_rect()

    def play(self):
        self.screen.blit(self.background, (0, 0))
        player = Player.Player()
        camera = Camera.Camera(player, self)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # this blit is here to erase previous images of the player (we copy the bakground area corresponding to the third argument on the are of second argument)
            self.screen.blit(self.background, player.sprite_rect, player.sprite_rect)
            player.input(camera)
            # we take the source, here the background image to work
            # the second parameter is where do we want to put the background according to the screen ? here 0, 0 is the topleft of the screen
            # third element is what do we want to draw from background ? (top_left, top_right, width, height). here we want to take an area from the background image, and area corresponding to what we have to see on screen
            self.screen.blit(
                self.background,
                (0, 0),
                (
                    camera.pos.x,
                    camera.pos.y,
                    camera.size.x,
                    camera.size.y,
                ),
            )
            self.screen.blit(player.sprite, player.sprite_rect)
            time.sleep(0.05)
            pygame.display.update()


game = Game()
game.play()
