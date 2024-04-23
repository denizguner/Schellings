import math
import random
import numpy as np
import matplotlib.pyplot as plt
from seaborn import heatmap
from matplotlib import animation
import sys

class Board(object):
    """
    A mutable size x size board for the Schellings Segregation Model.
    At any given time, e squares of the board are intentionally left empty.
    Of the remaining squares, q proportion are occupied by group 1 and 1-q by group 2.
    Simulates the Schellings Segregation Model with parameter p.
    """
    def __init__(self, e, p, q, size = 50):
        """
        size: dimension of the board
        e: number of empty squares
        p: proportion of group 1 squares
        q: proportion of group 1 squares in the neighborhood for a square to be satisfied
        """
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.p = p
        self.e = e
        self.group1Count = int((size**2 - e) * q)
        self.group2Count = int((size**2 - e) - self.group1Count)
        self.animationList = []
        
        #Fill in the board
        for x in range(size):
            for y in range(size):
                self.board[x][y] = self._sampleGroup()

        self.emptyCells = {(x, y) for x in range(size) for y in range(size) if self.board[x][y] == 0}
            

    def _sampleGroup(self):
        """Samples a random group to fill in the board. Returns 0 for empty, 1 for group 1, 2 for group 2."""
        group = random.sample([0, 1, 2], counts=[self.e, self.group1Count, self.group2Count], k=1)[0]
        if group == 0:
            self.e -= 1
        elif group == 1:
            self.group1Count -= 1
        elif group == 2:
            self.group2Count -= 1
        else:
            raise ValueError("Invalid group")
        return group
    
    
    def _getNeighbors(self, x, y):
        """Returns list of (i, j) coordinates corresponding to neighbors of the x,y cell."""
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0) and 0 <= x + i < self.size and 0 <= y + j < self.size]
    
    def _getGroup(self, x, y):
        """Returns group of cell at x,y"""
        return self.board[x][y]

    def _calculateSatisfaction(self, x, y, hypotheticalGroup = 1):
        """Calculates the satisfaction of the x,y cell. If the group of the x,y cell is 0, calculates the hypothetical satisfaction if the cell were to be filled with the hypotheticalGroup."""
        neighbors = self._getNeighbors(x, y)
        group = self._getGroup(x, y) if (x,y) not in self.emptyCells else hypotheticalGroup
        if group == 1:
            return sum([1 if self._getGroup(*neighbor) == 1 or self._getGroup(*neighbor) == 0 else 0 for neighbor in neighbors]) / len(neighbors)
        elif group == 2:
            return sum([1 if self._getGroup(*neighbor) == 2 or self._getGroup(*neighbor) == 0 else 0 for neighbor in neighbors]) / len(neighbors)
        else:
            raise ValueError("Invalid group")
        
    def _findClosestEmptySatisfying(self, x, y):
        """Finds the closest empty cell to the x,y cell that would satisfy the q parameter"""
        if (x,y) in self.emptyCells:
            raise ValueError("Empty cell")
        group = self._getGroup(x, y)
        minDistance = float("inf")
        closestCell = (x, y)
        for cell in self.emptyCells:
            if (self._calculateSatisfaction(*cell, group) >= self.p) and math.sqrt((cell[0] - x)**2 + (cell[1] - y)**2) < minDistance:
                minDistance = math.sqrt((cell[0] - x)**2 + (cell[1] - y)**2)
                closestCell = cell
        return closestCell
    
    def _findClosestEmpty(self, x, y):
        group = self._getGroup(x, y)
        if group == 0:
            raise ValueError("Empty cell")
        minDistance = float("inf")
        closestCell = (x, y)
        for cell in self.emptyCells:
            if math.sqrt((cell[0] - x)**2 + (cell[1] - y)**2) < minDistance:
                minDistance = math.sqrt((cell[0] - x)**2 + (cell[1] - y)**2)
                closestCell = cell
        return closestCell 
           
    def _moveCell(self, x, y):
        """Moves cell according to Schelling simulation model"""
        group = self._getGroup(x, y)
        if group == 0:
            raise ValueError("Empty cell")
        closestEmptyCell = self._findClosestEmptySatisfying(x, y)
        if closestEmptyCell == (x, y):
            closestEmptyCell = self._findClosestEmpty(x, y) #If no satisfying empty cell, move to closest empty cell
        if closestEmptyCell == (x, y):
            return -1

        self.board[closestEmptyCell[0]][closestEmptyCell[1]], self.board[x][y] = self.board[x][y], self.board[closestEmptyCell[0]][closestEmptyCell[1]]
        self.emptyCells.add((x, y))
        self.emptyCells.remove(closestEmptyCell)

    def _simulateSingleStep(self):
        """Simulates a single step of the Schelling simulation"""
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        if (x, y) in self.emptyCells:
            return
        frac = self._calculateSatisfaction(x, y)
        if frac < self.p:
            success = self._moveCell(x, y)
            self.animationList.append([row.copy() for row in self.board])
            return success
        else:
            return -1

    def _calculateMeanSatisfaction(self):
        """Calculates the mean satisfaction of the board"""
        ratioSum = 0
        for x in range(self.size):
            for y in range(self.size):
                if (x,y) in self.emptyCells:
                    continue
                ratioSum += self._calculateSatisfaction(x, y)
        return ratioSum / (self.size**2 - len(self.emptyCells))

    def runSimulation(self, steps = 20000):
        """Runs the Schelling simulation for steps number of steps, or no cell moves for 100 steps. Returns the mean satisfaction of the board."""
        noChangeCounter = 0
        for _ in range(steps):
            success = self._simulateSingleStep()
            if success == -1:
                noChangeCounter += 1
            else:
                noChangeCounter = 0

            if noChangeCounter == 1000:
                break
        return self._calculateMeanSatisfaction()
    
    def _animate(self, total_frames=350, frame_jump=None, interval=0.5):
            '''
            After board has been run, plays frames in animation list.
            Arguments:
                total_frames: integer, approximate number of frames to play.
                frame_jump: integer, alternative to total_frames, assign exact number of frames to jump by.
                interval: float, effectively frames per second, corresponds to interval argument of FuncAnimation.
            '''

            fig = plt.figure()
            if frame_jump == None:
                frame_jump = len(self.animationList)//total_frames+1

            heatmap(self.animationList[0], cmap=["white", "blue", "red"], xticklabels=False, yticklabels=False, cbar=False)

            animationList = self.animationList[::frame_jump]
            animationList.append(self.animationList[-1])
            time = len(animationList)

            def animate_step(i):
                fig.clear()
                heatmap(animationList[i], cmap=["white", "blue", "red"], xticklabels=False, yticklabels=False, cbar=False)

            anim = animation.FuncAnimation(fig, animate_step, frames=time, repeat = True, interval=interval)
            plt.show()

            return anim
    
    def animate(self):
        self._animate(total_frames=len(self.animationList))

if __name__ == "__main__":
    mode = sys.argv[1]
    e = int(sys.argv[2])
    q = float(sys.argv[3])
    p = float(sys.argv[4]) if mode == "animate" else None

    if mode == "animate":
        board = Board(e=e, p=p, q=q)
        board.runSimulation()
        board.animate()
    elif mode == "plot":
        pVals = np.arange(0.1, 1, 0.1)
        meanSatisfactions = [Board(e=e, p=pval, q=q).runSimulation() for pval in pVals]
        plt.plot(pVals, meanSatisfactions)
        plt.xlabel("p")
        plt.ylabel("Mean Satisfaction")
        plt.title("Mean Satisfaction vs. p")
        plt.show()
    else:
        print("Invalid mode. Please choose either 'animate' or 'plot'.")