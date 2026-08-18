import pygame
import math

# --- 1. Game Setup ---
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Driving Simulator")

# Colors
GRAY = (50, 50, 50)   # Road color
RED = (200, 0, 0)     # Car color
WHITE = (255, 255, 255)

# --- 2. The Car Class ---
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 90       # Starting angle (pointing up)
        self.speed = 0
        self.max_speed = 7    # Top speed
        self.acceleration = 0.2
        self.friction = 0.05  # Slows the car down when you let off the gas
        self.turn_speed = 4   # How fast the car rotates
        self.width = 20
        self.length = 40

    def move(self):
        # Apply friction to slow down gradually
        if self.speed > 0:
            self.speed -= self.friction
        elif self.speed < 0:
            self.speed += self.friction

        # Stop completely if speed is close to 0
        if abs(self.speed) < self.friction:
            self.speed = 0

        # Speed limits (going in reverse is slower)
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < -self.max_speed / 2: 
            self.speed = -self.max_speed / 2

        # Math to move the car forward based on the direction it's pointing
        radians = math.radians(self.angle)
        self.x += math.cos(radians) * self.speed
        self.y -= math.sin(radians) * self.speed

        # Screen wrapping (if you drive off one side, you appear on the other)
        if self.x > WIDTH: self.x = 0
        if self.x < 0: self.x = WIDTH
        if self.y > HEIGHT: self.y = 0
        if self.y < 0: self.y = HEIGHT

    def draw(self, surface):
        # Create a blank, transparent rectangle for the car
        car_surf = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
        car_surf.fill(RED)

        # Rotate the car surface based on our current angle
        rotated_car = pygame.transform.rotate(car_surf, self.angle)
        
        # Get the new bounding box so it rotates around its center, not the corner
        rect = rotated_car.get_rect(center=(self.x, self.y))

        # Draw the car to the screen
        surface.blit(rotated_car, rect.topleft)

# --- 3. Main Game Loop ---
def main():
    clock = pygame.time.Clock()
    car = Car(WIDTH // 2, HEIGHT // 2)
    running = True

    while running:
        # 1. Handle quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Handle Key Presses
        keys = pygame.key.get_pressed()

        # Acceleration and Braking
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            car.speed += car.acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            car.speed -= car.acceleration

        # Steering
        # We only allow steering if the car is actually moving
        if car.speed != 0:
            # Reversing changes the steering direction for realism
            turn_dir = 1 if car.speed > 0 else -1
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                car.angle += car.turn_speed * turn_dir
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                car.angle -= car.turn_speed * turn_dir

        # 3. Update Physics
        car.move()

        # 4. Draw Graphics
        screen.fill(GRAY) # Clear the screen with road color
        car.draw(screen)  # Draw the car

        # 5. Update Screen & Tick Clock
        pygame.display.flip()
        clock.tick(60) # Run the game at 60 Frames Per Second

    pygame.quit()

if __name__ == "__main__":
    main()
