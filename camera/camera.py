from pygame.math import Vector2


class Camera:
    def __init__(self, subject, screen):
        self.subject = subject
        # position of the camera (top left)
        self.pos = Vector2(subject.sprite_rect.x, subject.sprite_rect.y)
        # size of the game window
        self.size = Vector2(screen.screen_width, screen.screen_height)
        # size of the background image
        self.border = Vector2(
            screen.background.get_width(), screen.background.get_height()
        )
        # speed is a multiplicator coefficient to calculate the speed of a camera based on the screen size, image size, and player speed
        # to know when the player, starting from the left of the map and the screen, must end at the end of the screen and end of the map
        x_speed = 2 + (screen.screen_width - subject.sprite.get_width()) / (
            screen.screen_width - self.border.x
        )
        y_speed = 2 + (screen.screen_height - subject.sprite.get_height()) / (
            screen.screen_height - self.border.y
        )
        self.speed = Vector2(x_speed, y_speed)

    def update(self, movement):
        # we're going to determinate if the camera is out of the map
        # if it's the case, we determine what direction is involved
        # and allow camera to move only in the opposite direction and of course the other vector
        if self.is_outside_map("right"):
            # if we're at the right border of the map, and the movement tells us to move to the right, we nullify x movement
            if movement.x > 0:
                movement.x = 0
        if self.is_outside_map("left"):
            if movement.x < 0:
                movement.x = 0
        if self.is_outside_map("down"):
            if movement.y > 0:
                movement.y = 0
        if self.is_outside_map("up"):
            if movement.y < 0:
                movement.y = 0

        self.pos.x += movement.x * self.speed.x
        self.pos.y += movement.y * self.speed.y
        return movement

    def is_outside_map(self, direction):
        if direction == "right":
            return (
                self.pos.x + self.size.x
            ) + self.subject.sprite.get_width() >= self.border.x
        if direction == "left":
            return self.pos.x <= 0
        if direction == "down":
            return (
                self.pos.y + self.size.y
            ) + self.subject.sprite.get_height() >= self.border.y
        if direction == "up":
            return self.pos.y <= 0
