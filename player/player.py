import pygame
import os
from pygame.math import Vector2


class Player:
    def __init__(self):
        self.animations = {}
        self.initialize_animation_frames("./assets/dwarf/")

        self.frame = 0
        self.direction = "right"
        self.animation = "wait" + "_" + self.direction
        # animations_forced are here to loop entirely through these ones before moving to a next one
        self.animations_forced = ["hattack"]
        self.can_change_next_animation = True
        self.sprite = self.animations[self.animation][self.frame]
        self.sprite_rect = self.sprite.get_rect()
        self.speed = 4

    def initialize_animation_frames(self, main_path):
        # this method initialize all animations from the main_path by itself
        # given that main_path only contains one folder per animation
        # MAIN PATH /
        #       FOLDER_1 /
        #           FRAME_1
        #           FRAME_2
        #           FRAME_3
        #       FOLDER_2 /
        #           FRAME_1
        #           FRAME_2
        animation_subdirectories = os.walk(main_path)
        for name, sub_directories, files in filter(
            lambda sub_dir: sub_dir[0] != main_path, animation_subdirectories
        ):
            # we have to take name of the directory, excluding all path from it
            # ./assets/dwarf/death, we only want death
            # split all the path
            path_names = name.split("/")
            # and get the last element
            animation_type = path_names[len(path_names) - 1]

            for index, animation_file in enumerate(sorted(files)):
                if index == 0:
                    self.animations.update(
                        {
                            animation_type: [
                                pygame.image.load("{}/{}".format(name, animation_file))
                            ]
                        }
                    )
                    continue
                self.animations[animation_type].append(
                    pygame.image.load("{}/{}".format(name, animation_file))
                )

    def animate(self, animation):
        if self.can_change_next_animation:
            # will animate player with given animation
            match_previous_animation = (
                self.animation == animation + "_" + self.direction
            )
            # if the animation changes from previous frame, we will reset frame
            self.frame = self.frame if match_previous_animation else 0

            self.animation = animation + "_" + self.direction

        if animation in self.animations_forced:
            self.can_change_next_animation = False

        animation_sprites = self.animations[self.animation]
        # modulo, to always have frame index of animation_sprites, even if self.frame is way higher than the len of animation_sprites
        self.sprite = animation_sprites[int(self.frame) % len(animation_sprites)]
        # animation is rendered in sprite, we will now update frame to next animation
        # by updating of 0.5, we will slow down animation
        # 0.5 means animation will need 2 frames rendered by pygame to pass to the next frame
        self.frame += 0.5
        # if we have finished the loop for the forced_animation, we can change the next animation
        if (
            int(self.frame) == len(self.animations[self.animation])
            and not self.can_change_next_animation
        ):
            self.frame = 0
            self.can_change_next_animation = True

    def move(self, direction, camera):
        self.direction = "left" if direction.x < 0 else "right"
        # camera follow player
        # so we move player as we moved the camera
        camera_movement = camera.update(direction)
        self.sprite_rect = self.sprite_rect.move(camera_movement)

    def input(self, camera=None):
        # get state of all keys (pressed or not)
        keys = pygame.key.get_pressed()

        vector_direction = Vector2(0, 0)

        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        space = keys[pygame.K_SPACE]

        if up:
            vector_direction.y -= self.speed
            self.move(vector_direction, camera)
        elif down:
            vector_direction.y += self.speed
            self.move(vector_direction, camera)
        elif left:
            vector_direction.x -= self.speed
            self.move(vector_direction, camera)
        elif right:
            vector_direction.x += self.speed
            self.move(vector_direction, camera)

        # can_change_next_animation is here to avoid register too many animation when spamming escape
        if space and self.can_change_next_animation:
            self.animate("hattack")
        elif up or down or left or right:
            self.animate("run")
        else:
            self.animate("wait")
