import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

def is_valid_move(x, y, board, N):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

def get_valid_moves(x, y, board, N, x_moves, y_moves):
    valid_moves = []
    for k in range(8):
        next_x = x + x_moves[k]
        next_y = y + y_moves[k]
        if is_valid_move(next_x, next_y, board, N):
            count = 0
            for i in range(8):
                check_x = next_x + x_moves[i]
                check_y = next_y + y_moves[i]
                if is_valid_move(check_x, check_y, board, N):
                    count += 1
            valid_moves.append((next_x, next_y, count))
    return sorted(valid_moves, key=lambda x: x[2])

def knight_tour(N, start_x, start_y, delay=0.5):
    board = [[-1 for _ in range(N)] for _ in range(N)]
    x_moves = [2, 1, -1, -2, -2, -1, 1, 2]
    y_moves = [1, 2, 2, 1, -1, -2, -2, -1]

    move_number = 0
    board[start_x][start_y] = move_number

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    cmap = plt.get_cmap("tab10")
    norm = plt.Normalize(0, N * N - 1)

    def plot_board():
        ax.clear()
        ax.set_xticks(np.arange(-0.5, N, 1))
        ax.set_yticks(np.arange(-0.5, N, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        for i in range(N):
            for j in range(N):
                rect = patches.Rectangle((j - 0.5, N - i - 1 - 0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=cmap(norm(board[i][j])))
                ax.add_patch(rect)
                if board[i][j] != -1:
                    ax.text(j, N - i - 1, str(board[i][j]), ha='center', va='center', fontsize=10, fontweight='bold', color='white')

        plt.grid(color='black', linestyle='-', linewidth=1)
        plt.draw()
        plt.pause(delay)

    while move_number < N * N - 1:
        next_moves = get_valid_moves(start_x, start_y, board, N, x_moves, y_moves)
        if not next_moves:
            print("No solution exists.")
            break

        next_x, next_y, _ = next_moves[0]
        move_number += 1
        board[next_x][next_y] = move_number
        start_x, start_y = next_x, next_y

        plot_board()

    plt.title("Finish", fontsize=16, fontweight='bold', color='green')
    plt.ioff()
    plt.show(block=True)

N = 8
start_x, start_y = 0, 0
knight_tour(N, start_x, start_y)
