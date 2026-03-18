import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ClassicalSearch:
    def __init__(self, n):
        self.n = n  # Total number of elements
        self.target = np.random.randint(0, n)  # Random target index
        self.found = False

    def search(self):
        for i in range(self.n):
            yield i
            if i == self.target:
                self.found = True
                break

class QuantumSearch:
    def __init__(self, n):
        self.n = n  # Total number of elements
        self.target = np.random.randint(0, n)  # Random target index
        self.found = False

    def search(self):
        # Placeholder for quantum search logic
        index = self.target  # Simulate quantum search by directly finding the target
        self.found = True
        return index

def visualize_search(searcher, title):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlim(-1, searcher.n)
    ax.set_ylim(-1, 1)
    ax.set_xticks(range(searcher.n))
    ax.set_yticks([])
    bars = ax.bar(range(searcher.n), np.zeros(searcher.n), color='gray')

    # Animation function
    def update(frame):
        if isinstance(searcher, ClassicalSearch):
            if frame < searcher.n:
                for j in range(frame + 1):
                    bars[j].set_height(1)
        elif isinstance(searcher, QuantumSearch):
            for j in range(searcher.n):
                if j == searcher.target:
                    bars[j].set_height(1)
                    break
        return bars

    ani = FuncAnimation(fig, update, frames=range(searcher.n), repeat=False)
    plt.show()

if __name__ == '__main__':
    n_elements = 10  # Number of elements to search

    classical_search = ClassicalSearch(n_elements)
    print("Classical Search: Target found at index", list(classical_search.search()))
    visualize_search(classical_search, 'Classical Search Visualization')

    quantum_search = QuantumSearch(n_elements)
    print("Quantum Search: Target found at index", quantum_search.search())
    visualize_search(quantum_search, 'Quantum Search Visualization')
