import pygame
import sys
import numpy as np
import pickle

# Load AI Agent đã train trước
class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.load_model()

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)
        return self.q_table[state]

    def choose_action(self, state):
        state_tuple = tuple(state.flatten())
        q_values = self.get_q_values(state_tuple)
        available_actions = [i for i, val in enumerate(state.flatten()) if val == 0]
        if not available_actions:
            return None
        best_action = max(available_actions, key=lambda x: q_values[x])
        return best_action

    def load_model(self, filename="q_table.pkl"):
        try:
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("Không tìm thấy model!")

# Khởi tạo agent
agent = QLearningAgent()
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 50

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

# Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                           int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return not (board == 0).any()

def check_winner(player):
    for row in range(BOARD_ROWS):
        if np.all(board[row] == player):
            return True
    for col in range(BOARD_COLS):
        if np.all(board[:, col] == player):
            return True
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    return False

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    global board, player, game_over
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    player = 2
    game_over = False

# Game setup
draw_lines()
player = 2  # Người chơi đi trước
game_over = False

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Người chơi đi
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 2:
            mouseX, mouseY = event.pos
            clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_winner(player):
                    print('Người chơi thắng!')
                    game_over = True
                elif is_board_full():
                    print("Hòa!")
                    game_over = True
                else:
                    player = 1  # Chuyển lượt cho AI

        # AI đi
        if player == 1 and not game_over:
            pygame.time.wait(500)
            action = agent.choose_action(board)
            if action is not None:
                row, col = action // 3, action % 3
                mark_square(row, col, player)
                if check_winner(player):
                    print('AI thắng!')
                    game_over = True
                elif is_board_full():
                    print("Hòa!")
                    game_over = True
                else:
                    player = 2  # Trả lượt về người chơi

        # Nhấn R để chơi lại
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

    draw_figures()
    pygame.display.update()
