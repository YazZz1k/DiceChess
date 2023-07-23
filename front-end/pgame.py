import pygame
import random

from board import Board

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (500, 500)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board()


def draw(display):
    display.fill("white")
    board.draw(display)
    pygame.display.update()


if __name__ == "__main__":
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse is clicked
                if event.button == 1:
                    board.handleClick(mx, my)
        if board.isCheckmate():
            running = False
            print("GameOver")

            # Draw the board
        draw(screen)
