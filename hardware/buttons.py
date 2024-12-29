import lgpio
import time

class Button:
    def __init__(self, pin, chip=0):
        self.pin = pin
        self.h = lgpio.gpiochip_open(chip)
        lgpio.gpio_claim_input(self.h, self.pin, lgpio.SET_PULL_UP)

    def is_pressed(self):
        return lgpio.gpio_read(self.h, self.pin) == 0

    def monitor(self):
        try:
            while True:
                if self.is_pressed():
                    #print(f"Pin {self.pin} is connected to ground")
                    yield True
                else:
                    #print(f"Pin {self.pin} is NOT connected to ground")
                    yield False
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Script terminated by user")
        finally:
            self.cleanup()

    def cleanup(self):
        lgpio.gpiochip_close(self.h)

# Example usage:
# if __name__ == "__main__":
#     button = Button(26)  # Create button instance with pin 26
#     for chunk in button.monitor():
#         print(chunk)
