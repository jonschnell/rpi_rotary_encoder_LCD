# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import RPi.GPIO as GPIO

maxPage = 32
minPage = 0

class Encoder:

    def __init__(self, leftPin, rightPin, centerPin, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.centerPin = centerPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.click = 0
        self.p3last = 1
        self.callback = callback
        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.centerPin, GPIO.IN)
        GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)
        GPIO.add_event_detect(self.centerPin, GPIO.BOTH, callback=self.transitionOccurred)

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        p3 = GPIO.input(self.centerPin)
        newState = "{}{}".format(p1, p2)

        if self.p3last == 1:
            if p3 == 1:
                self.click = 0
            elif p3 == 0:
                self.click = 1
                if self.callback is not None:
                    self.callback(self.value, self.direction, self.click)

        if self.p3last == 0:
            if p3 == 0:
                self.click = 1
            elif p3 == 1:
                self.click = 0
                if self.callback is not None:
                    self.callback(self.value, self.direction, self.click)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    if self.value > minPage:
                        self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction, self.click)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    if self.value < maxPage:
                        self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction, self.click)

        elif self.state == "11":
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    if self.value > minPage:
                        self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction, self.click)
                elif self.direction == "R":
                    if self.value < maxPage:
                        self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction, self.click)

        self.state = newState
        self.p3last = p3

    def getValue(self):
        return self.value
