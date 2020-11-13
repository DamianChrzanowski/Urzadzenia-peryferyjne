from threading import Thread
from inputs import get_gamepad
import pygame


class PadSteering(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.input = [0, 0, 0, 0, 0]
        self.output = [0, 0, 0, 0, 0]
        self.prev_val = []
        self.left_vertical = self.left_horizontal = self.right_vertical = self.right_horizontal = 0
        self.left_trigger = self.right_trigger = self.trigger_value = self.trigger_steering = 0

    def run(self):
        while True:
            events = get_gamepad()
            for event in events:
                self.catch_input(event)
            self.convert_range()

    def catch_input(self, event):
        if event.code == "ABS_X":
            self.left_horizontal = event.state
        if event.code == "ABS_Y":
            self.left_vertical = event.state
        if event.code == "ABS_RX":
            self.right_horizontal = event.state
        if event.code == "ABS_RY":
            self.right_vertical = event.state
        if event.code == "ABS_Z":
            self.left_trigger = event.state
        if event.code == "ABS_RZ":
            self.right_trigger = event.state
        self.input = [self.left_horizontal, self.left_vertical, self.right_horizontal,
                      self.right_vertical, self.right_trigger - self.left_trigger]

    def get_input(self):
        return self.input

    def print_input(self):
        print(self.input)

    def convert_range(self):
        for i in range(0, 4):
            if self.input[i] > 0:
                self.input[i] /= 32767
            else:
                self.input[i] /= 32768
        self.input[4] /= 255

    def set_trigger(self, trigger_val):
        self.output[4] = trigger_val


class MainWindow(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.pad = PadSteering()
        self.pad.start()

    def run(self):
        width = 1080
        height = 720
        size = [width, height]
        window = pygame.display
        surface = window.set_mode(size)

        pygame.joystick.init()
        xbox_pad = pygame.joystick.Joystick(0)
        window.set_caption('Rysowanie z ' + xbox_pad.get_name())

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        color_num = 0
        circles = []
        x_pos = 500
        y_pos = 500
        speed = 1.5
        drawing = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.JOYBUTTONDOWN:
                    if xbox_pad.get_button(0):
                        drawing = True
                    if xbox_pad.get_button(1):
                        color_num += 1
                        color_num %= 3
                if event.type == pygame.JOYBUTTONUP:
                    drawing = False
                if drawing is True:
                    circles.append((x_pos, y_pos, colors[color_num]))

            surface.fill((255, 255, 255))

            for circle in circles:
                pygame.draw.circle(surface, circle[2], (circle[0], circle[1]), 20)

            move = self.pad.get_input()
            if move[4] != 0:
                x_pos += (move[0] * abs(move[4] * speed))
                y_pos -= (move[1] * abs(move[4] * speed))
            else:
                x_pos += move[0]
                y_pos -= move[1]

            pygame.draw.circle(surface, (0, 0, 0, 0), (x_pos, y_pos), 20)

            window.update()


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.start()
