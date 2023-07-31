# Imports
import pygame, sys

# Setting up pygame
pygame.init()

WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()

# Initilizing the image for the pacground
background = pygame.image.load("Assets/Background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Initilizing the sound when placing
place_sound = pygame.mixer.Sound("Assets/Place_sound.mp3")

class button:
    def __init__(self, x, y):
        # Accepts x, y as aruments for where to put the button and image

        # Initlizing all possible images
        self.Ximg = pygame.image.load('Assets/Xmark.png')
        self.Ximg = pygame.transform.scale(self.Ximg, (240 , 300))

        self.Oimg = pygame.image.load('Assets/Omark.png')
        self.Oimg = pygame.transform.scale(self.Oimg, (240 , 300))

        self.cord = (x + 10, y-60)

        # Bliimage is for the image that will be blit that wont change
        # Fadeimage is when the square isnt occupied and the image is just for display
        self.blitimage = None
        self.fadeimage = self.Ximg.copy()

        # Checking is the square occupied or not
        self.imageisblank = True

        self.hitbox = pygame.Rect(x, y, self.Ximg.get_width() + 10, self.Ximg.get_height() - 100)

        self.mouse = False
        self.clicked = False

        self.turn = 1

    def image_fader(self, image):
        # This function takes an image and return a faded image of the original

        target_image = image.copy()

        target_image.fill((255, 255, 255, 155), special_flags=pygame.BLEND_RGBA_MULT)

        return target_image
    
    def image_determine(self, turn):
        # The fade image changes when the turn changes

        if turn == 1:
            self.fadeimage = self.Ximg
        
        else:
            self.fadeimage = self.Oimg


    def draw(self):
        # This function determines what shape should be on the button

        # When the mouse is hovering on a unoccupied square, it will display the shape that will be placed on it when clicked
        if self.mouse and self.imageisblank:
            screen.blit(self.image_fader(self.fadeimage), self.cord)

        #if the image is not blank, blit the bliimage
        elif self.imageisblank == False:
            screen.blit(self.blitimage, self.cord)

    def interaction_check(self):
        # This function captures the mouses activity and reacts to it

        pos = pygame.mouse.get_pos()

        # If the mouse collides with the button self.mouse would be true
        if self.hitbox.collidepoint(pos):
            self.mouse = True

            # If the button gets pressed and the square is unoccupied,
            # the square wukk be decleared occupied and initilize the blit image to fade image(self.blitimage variable isnt neccecary, but it's for readability)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.imageisblank = False
                self.blitimage = self.fadeimage

        else:
            self.mouse = False

        return self.clicked
    

class tictactoe:

    def __init__(self):

        # The status of the game
        self.game_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.button_list = []

        self.turn = 1

        self.initilize_button()

    def initilize_board(self):
        # Drawing the board

        board_size = min(WIDTH, HEIGHT) - 40
        line_width = 10
        cell_size = board_size // 3

        board_x = (WIDTH - board_size) // 2
        board_y = (HEIGHT - board_size) // 2

        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(screen, (0, 0, 0), (board_x + i * cell_size, board_y), (board_x + i * cell_size, board_y + board_size), line_width)
            # Horizontal lines
            pygame.draw.line(screen, (0, 0, 0), (board_x, board_y + i * cell_size), (board_x + board_size, board_y + i * cell_size), line_width)

    def initilize_button(self):
        # Setting up all the buttons

        for num in range(len(self.game_board)):
            self.button_list.append(button(100 + 250 * (num % 3), 50 + int(num/3) * 225))

    def change_turn(self):
        # When called the turn will switch

        if self.turn == 1:
            self.turn = 2

        else:
            self.turn = 1
    
    def determine_winner(self):
        # Listing all winning positions and check if they have been satisfyied

        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        # If a winning cobinition has all same number in them, the player will be decleared the winner
        for combination in winning_combinations:
            if self.game_board[combination[0]] == self.game_board[combination[1]] == self.game_board[combination[2]] != 0:
                return self.game_board[combination[0]]  # Return the player (1 or 2) who won
        
        # If theres no winner and all squares has been occupied, it will be a draw
        if 0 not in self.game_board:
            return 3
        
        # Return None if there is no winner
        return None 
    
def intro():
    # This function displays the texts in the intro screen

    # Displays "Tic Tac Toe"
    welcome_font = pygame.font.SysFont('times new roman', int(100))
    welcome_text = welcome_font.render("Tic Tac Toe", True, (0, 0, 0))
    screen.blit(welcome_text, (WIDTH//2 - welcome_text.get_width()//2 , 100))

    # Display "Press ENTER to continue..."
    enter_font = pygame.font.SysFont("times new roman", int(30))
    enter_text = enter_font.render("Press ENTER to continue...", True, (0, 0, 0))
    screen.blit(enter_text, (WIDTH//2 - enter_text.get_width()//2, HEIGHT - 300))

def outro(winner):
    # This function displays all texts in the ending screen 

    # Initlizing the fonts
    winner_font = pygame.font.SysFont('times new roman', int(100))
    continue_font = pygame.font.SysFont("times new roman", int(30))

    # Displaying who won based on the argument, or a draw
    if winner == 1:
        winner_text = winner_font.render("Winner is X!", True, (0, 0, 0))
    
    elif winner == 2:
        winner_text = winner_font.render("Winner is O!", True, (0, 0, 0))

    else:
        winner_text = winner_font.render("It's a tie!", True, (0, 0, 0))

    # Display "Press ENTER to play again..."
    continue_text = continue_font.render("Press ENTER to play again...", True, (0, 0, 0))
    
    # Blit them on screen
    screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, 100))
    screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT - 300))

# Game phase determination
pregame = True
playing = False
ending = False

# Main game loop
rungame = True
while rungame:

    for event in pygame.event.get():

        # Check if the user wants to quit
        if event.type == pygame.QUIT:
            rungame = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                # If the player press ENTER during intro, the game will start
                if pregame:
                    game = tictactoe()

                    pregame = False
                    playing = True
                    ending = False

                # If the player press ENTER during the ending, the game will restart
                elif ending:
                    game = tictactoe()

                    playing = True
                    ending = False
                

    # Displaying the background image
    screen.blit(background, (0, 0))

    # Call intro function when the player just started
    if pregame:
        intro()

    if playing:

        for index, presser in enumerate(game.button_list):

            clicked = presser.interaction_check()

            # If the player clicked on the button and the square is unoccupied
            if clicked and game.game_board[index] == 0:

                # Update the game board status, changes turn, play the "place_sound" sound
                game.game_board[index] = game.turn
                game.change_turn()
                place_sound.play()

            presser.image_determine(game.turn)
            presser.draw()

        # Draw the board
        game.initilize_board()
    
        winner = game.determine_winner()

        # When there is a winner or the gamed draws
        if winner != None:

            # The game ends and ending start
            playing = False
            ending = True
    
    # If the end starts
    if ending:
        
        # Display the outro
        outro(winner)

    pygame.display.update()
    clock.tick(32)