import random
import numpy as np
import matplotlib.pyplot as plt

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

N = 8

# Move pattern on basis of the change of
# x coordinates and y coordinates respectively
cx = [1, 1, 2, 2, -1, -1, -2, -2]
cy = [2, -2, 1, -1, 2, -2, 1, -1]

# function restricts the knight to remain within
# the 8x8 chessboard
def limits(x, y):
    return ((x >= 0 and y >= 0) and (x < N and y < N))

# Checks whether a square is valid and empty or not
def isempty(a, x, y):
    return (limits(x, y)) and (a[y * N + x] < 0)

# Returns the number of empty squares adjacent to (x, y)
def getDegree(a, x, y):
    count = 0
    for i in range(N):
        if isempty(a, (x + cx[i]), (y + cy[i])):
            count += 1
    return count

# Picks next point using Warnsdorff's heuristic.
# Returns false if it is not possible to pick
# next point.
def nextMove(a, cell):
    min_deg_idx = -1
    c = 0
    min_deg = (N + 1)
    nx = 0
    ny = 0

    # Try all N adjacent of (*x, *y) starting
    # from a random adjacent. Find the adjacent
    # with minimum degree.
    start = random.randint(0, 1000) % N
    for count in range(0, N):
        i = (start + count) % N
        nx = cell.x + cx[i]
        ny = cell.y + cy[i]
        c = getDegree(a, nx, ny)
        if ((isempty(a, nx, ny)) and c < min_deg):
            min_deg_idx = i
            min_deg = c

    # If we could not find a next cell
    if (min_deg_idx == -1):
        return None

    # Store coordinates of next point
    nx = cell.x + cx[min_deg_idx]
    ny = cell.y + cy[min_deg_idx]

    # Mark next move
    a[ny * N + nx] = a[(cell.y) * N + (cell.x)] + 1

    # Update next point
    cell.x = nx
    cell.y = ny

    return cell

# displays the chessboard with all the legal knight's moves
def visualize_matrix(A):
    # Create a figure and axis
    plt.figure(figsize=(8, 8))
    
    # Set a uniform color for all iterations
    colors = np.ones_like(A, dtype='float') * 0.8  # You can adjust the color value as needed

    for i in range(A.size):
        # Find the minimum value's indices
        min_index = np.unravel_index(np.argmin(A), A.shape)

        # Update the colors matrix by marking the current minimum value
        colors[min_index] = 1.0  # Set color for current iteration

        # Visualize the current state
        plt.imshow(colors, cmap='Reds', alpha=0.7)
        plt.xticks([])
        plt.yticks([])
        plt.title(f"Iteration {i + 1}")

        # Update the matrix by setting the current minimum to a large value for the next iteration
        A[min_index] = np.max(A) + 1

        # Pause to show each iteration
        plt.pause(0.1)

    plt.show()

# checks its neighbouring squares
# If the knight ends on a square that is one knight's move from the beginning square, then the tour is closed
def neighbour(x, y, xx, yy):
    for i in range(N):
        if ((x + cx[i]) == xx) and ((y + cy[i]) == yy):
            return True
    return False

# Generates the legal moves using Warnsdorff's heuristics. Returns false if not possible
def findClosedTour():
    # Filling up the chessboard matrix with -1's
    a = [-1] * N * N

    # initial position
    sx = 3
    sy = 2

    # Current points are the same as initial points
    cell = Cell(sx, sy)

    a[cell.y * N + cell.x] = 1  # Mark first move.

    # List to store all moves for visualization
    move_list = []

    # Keep picking next points using Warnsdorff's heuristic
    ret = None
    for i in range(N * N - 1):
        move_list.append((cell.x, cell.y))  # Store current position for visualization
        ret = nextMove(a, cell)
        if ret is None:
            return False

    # Check if tour is closed (Can end at starting point)
    if not neighbour(ret.x, ret.y, sx, sy):
        return False

    # Don't visualize the tour inside the loop
    # Store the tour in 'a' and visualize it after finding a closed tour
    for move in move_list:
        a[move[1] * N + move[0]] = move_list.index(move) + 1

    return a

# Driver Code
if __name__ == '__main__':
    closed_tour = None
    closed_tour_found = False

    while not closed_tour_found:
        closed_tour = findClosedTour()
        if closed_tour:
            closed_tour_found = True

    # Visualize the tour after finding a closed tour
    visualize_matrix(np.array(closed_tour).reshape(N, N))
