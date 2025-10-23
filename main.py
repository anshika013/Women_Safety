import pygame
import geocoder
import smtplib
from email.message import EmailMessage
import sys
import os

def play_sound(sound_file):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        return pygame.mixer.music.get_busy
    except pygame.error as e:
        print(f"Error loading or playing sound file: {e}")
        return lambda: False  # Return a function that immediately returns False

def get_geolocation():
    try:
        g = geocoder.ip('me')
        return f"{g.city}, {g.state}, {g.country}"
    except Exception as e:
        return "Location unavailable"
        return "Unknown location"

def send_email(subject, message, from_addr, to_addr, password):
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_addr, password)
            server.send_message(msg)
        print("Emergency email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def fake_call(screen):
    ringing = play_sound('ringing.mp3')

    font = pygame.font.Font(None, 36)
    call_text = font.render("Mom is calling...", True, (255, 255, 255))
    attend_text = font.render("Press 'A' to Attend Call", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    draw_title(screen)
    screen.blit(call_text, (100, 100))
    screen.blit(attend_text, (100, 150))
    pygame.display.flip()

    while ringing():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.mixer.music.stop()
                    return

def draw_menu(screen, options, selected_index):
    font = pygame.font.Font(None, 36)
    base_y = 150
    for index, option in enumerate(options):
        color = (255, 255, 255) if index == selected_index else (200, 200, 200)
        text_surface = font.render(option, True, color)
        rect = text_surface.get_rect(center=(320, base_y + index * 50))
        pygame.draw.rect(screen, (0, 0, 0), rect.inflate(20, 10))
        screen.blit(text_surface, rect)
    pygame.display.flip()

def draw_title(screen):
    font = pygame.font.Font(None, 72)
    title_text = font.render("Women Safety", True, (255, 0, 0))
    rect = title_text.get_rect(center=(320, 50))
    screen.blit(title_text, rect)

def draw_welcome(screen):
    font = pygame.font.Font(None, 48)
    welcome_text = font.render("Welcome Back! My lady", True, (20, 255, 0))
    instructions_text = font.render("Press any key to continue...", True, (50, 50, 50))

    screen.fill((0, 0, 0))
    draw_title(screen)
    
    # Load and display the image
    try:
        woman_image = pygame.image.load('woman_image.jpg')
        woman_image = pygame.transform.scale(woman_image, (150, 150))  # Adjust size as needed
        
        # Get the dimensions of the image
        image_width = woman_image.get_width()
        image_height = woman_image.get_height()
        
        # Calculate the position to center the image
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        x = (screen_width - image_width) // 2
        y = (screen_height - image_height) // 2 - 30  # Adjust y position if needed

        screen.blit(woman_image, (x, y))  # Position the image
    except pygame.error as e:
        print(f"Error loading image: {e}")
    
    # Adjust the positions to ensure they fit within the screen
    welcome_text_x = (screen.get_width() - welcome_text.get_width()) // 2
    welcome_text_y = screen.get_height() - 100  # Ensure it's not too close to the bottom
    instructions_text_x = (screen.get_width() - instructions_text.get_width()) // 2
    instructions_text_y = screen.get_height() - 50  # Adjust as needed

    screen.blit(welcome_text, (welcome_text_x, welcome_text_y))
    screen.blit(instructions_text, (instructions_text_x, instructions_text_y))
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    waiting_for_key = False

def main():
    sound_file = 'alarm.wav'
    from_addr = os.getenv('EMAIL_USER', 'thingslittle253@gmail.com')
    to_addr = os.getenv('EMAIL_TO', 'anshikatripathi133@gmail.com')
    password = os.getenv('EMAIL_PASSWORD', 'vcyn aafh oapg zytu')

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Women Safety')

    draw_welcome(screen)  # Show the welcome screen

    menu_options = ["Start Alarm", "Fake Call", "Quit"]
    selected_index = 0
    in_menu = True

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_index] == "Start Alarm":
                        in_menu = False
                        play_sound(sound_file)
                        geolocation = get_geolocation()
                        print(f"Alarm triggered at {geolocation}!")
                        subject = "Alarm Triggered!"
                        message = f"Alarm triggered at {geolocation}!"
                        send_email(subject, message, from_addr, to_addr, password)
                        in_menu = True
                    elif menu_options[selected_index] == "Fake Call":
                        in_menu = False
                        fake_call(screen)
                        in_menu = True
                    elif menu_options[selected_index] == "Quit":
                        pygame.quit()
                        sys.exit()

        screen.fill((0, 0, 0))
        draw_title(screen)
        draw_menu(screen, menu_options, selected_index)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
