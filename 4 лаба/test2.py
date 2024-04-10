import matplotlib.pyplot as plt
import numpy as np

# Function to draw a line in matplotlib


def drawline(p0, p1, c='black'):
    plt.plot([p0[0], p1[0]], [p0[1], p1[1]], 'k-', color=c)

# Function to draw a polygon, given vertices


def drawPolygon(vertices):
    # repeat the first point to create a 'closed loop'
    vertices.append(vertices[0])
    xs, ys = zip(*vertices)  # create lists of x and y values
    plt.fill(xs, ys, edgecolor='r', fill=False)

# Function to take dot product


def dot(p0, p1):
    return p0[0] * p1[0] + p0[1] * p1[1]

# Function to calculate the max from a list of floats


def max(t):
    return np.max(t)

# Function to calculate the min from a list of floats


def min(t):
    return np.min(t)

# Cyrus Beck function, returns a pair of values
# that are then displayed as a line


def CyrusBeck(vertices, line):
    n = len(vertices)
    P1_P0 = (line[1][0] - line[0][0], line[1][1] - line[0][1])

    normal = [(vertices[i][1] - vertices[(i + 1) % n][1],
               vertices[(i + 1) % n][0] - vertices[i][0]) for i in range(n)]
    
    P0_PEi = [(vertices[i][0] - line[0][0], 
               vertices[i][1] - line[0][1]) for i in range(n)]
    
    numerator = [dot(normal[i], P0_PEi[i]) for i in range(n)]

    denominator = [dot(normal[i], P1_P0) for i in range(n)]

    t = [numerator[i] / denominator[i]
         if denominator[i] != 0 else 0 for i in range(n)]
    
    tE = [t[i] for i in range(n) if denominator[i] > 0]
    tL = [t[i] for i in range(n) if denominator[i] < 0]
    tE.append(0)
    tL.append(1)
    temp = [max(tE), min(tL)]
    if temp[0] > temp[1]:
        return None
    newPair = [(line[0][0] + P1_P0[0] * temp[0], line[0][1] + P1_P0[1] * temp[0]),
               (line[0][0] + P1_P0[0] * temp[1], line[0][1] + P1_P0[1] * temp[1])]
    return newPair


# Driver code
if __name__ == "__main__":
    vertices = [(200, 50), (250, 100), (200, 150),
                (100, 150), (50, 100), (100, 50)]
    line = [(0, 0), (500, 500)]  # New line coordinates

    # Before Clipping
    plt.figure(figsize=(6, 6))
    plt.title('Before Clipping')
    drawPolygon(vertices)
    drawline(line[0], line[1])  # Draw the original line
    plt.xlim(0, 500)
    plt.ylim(0, 500)
    plt.show()

    # After Clipping
    newPair = CyrusBeck(vertices, line)
    if newPair is not None:
        plt.figure(figsize=(6, 6))
        plt.title('After Clipping')
        drawPolygon(vertices)
        drawline(line[0], line[1])
        drawline(newPair[0], newPair[1], 'green')  # Draw the clipped line
        plt.xlim(0, 500)
        plt.ylim(0, 500)
        plt.show()
