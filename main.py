from matplotlib import pyplot as plt
from time import time
import sys
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')
sys.setrecursionlimit(999999999)

#NUMBER_OF_ITERATIONS = 4    # если поставить больше 8, то превышение рекурсии
#RE = 0.5                 #   -0.14   0
#IM = 0                   #   0.74    0.2
PARTS = 2                   # ** 2
#DOTS_PER_POINT = 4          # ** 2


def main(NUMBER_OF_ITERATIONS, RE, IM, DOTS_PER_POINT):
    cells = [(-2, -2), ]
    size = 4
    sum = 0
    for num in range(NUMBER_OF_ITERATIONS):
        start_time = time()
        graph = {}
        new_cells = []
        size = size / PARTS
        for cell in cells:
            for x in [cell[0] + size * i for i in range(PARTS)]:
                for y in [cell[1] + size * i for i in range(PARTS)]:
                    new_cells.append((x, y))

        cells = new_cells

        for cell in cells:
            for dot in get_dots_from_cell(cell, size, DOTS_PER_POINT):
                linked_cell = check_dot(get_new_dot(dot, RE, IM), cells, size)
                if linked_cell:
                    append_to_graph(graph, cell, linked_cell)

        # граф есть надо сильные компоненты
        strong_components = get_strong_components(graph)
        cells.clear()

        for component in strong_components:
            cells += component

        #print(num + 1, len(cells), time() - start_time)
        sum += time() - start_time

    #draw_this(cells, size)
    return cells, size, sum


def draw_this(cells, size):
    f, s = [], []
    for cell in cells:
        dots = get_dots_from_cell(cell, size)
        for dot in dots:
            f.append(dot[0])
            s.append(dot[1])
        plt.plot(f, s, color="blue", linewidth=0.1)
        f.clear()
        s.clear()

    #plt.show()


def dfs_second(graph, visited, vertex, strong_components):
    visited.append(vertex)
    if vertex in graph:
        for i in graph[vertex]:
            if i not in visited:
                dfs_second(graph, visited, i, strong_components)
    strong_components.append(vertex)


def get_reversed_graph(graph):
    reversed_graph = {}
    for key, values in graph.items():
        for value in values:
            append_to_graph(reversed_graph, value, key)
    return reversed_graph


def dfs_first(graph, visited, stack, vertex):
    visited.append(vertex)
    if vertex in graph:
        for i in graph[vertex]:
            if i not in visited:
                dfs_first(graph, visited, stack, i)
    stack.append(vertex)


def get_strong_components(graph):
    visited = []
    stack = []
    for vertex in graph:
        if vertex not in visited:
            dfs_first(graph, visited, stack, vertex)

    visited.clear()
    reversed_graph = get_reversed_graph(graph)
    strong_components = []
    for vertex in stack[::-1]:
        if vertex not in visited:
            strong_components.append([])
            dfs_second(reversed_graph, visited, vertex, strong_components[-1])
            if len(strong_components[-1]) < 2:
                strong_components.pop()

    return strong_components


def append_to_graph(graph, cell, linked_cell):
    if cell in graph:
        if linked_cell not in graph[cell]:
            graph[cell].append(linked_cell)
    else:
        graph[cell] = [linked_cell]


def check_dot(dot, cells, size):
    for cell in cells:
        if cell[0] < dot[0] < cell[0] + size and cell[1] < dot[1] < cell[1] + size:
            return cell
        else:
            # тут типо если на границу точка попала, сложно кароче
            pass


def get_new_dot(dot, RE, IM):
    return dot[0] ** 2 - dot[1] ** 2 + RE, 2 * dot[0] * dot[1] + IM


def get_dots_from_cell(cell, size, DOTS_PER_POINT):
    return ((cell[0] + size / (DOTS_PER_POINT - 1) * i, cell[1] + size / (DOTS_PER_POINT - 1) * j)
            for i in range(DOTS_PER_POINT) for j in range(DOTS_PER_POINT))


class Application(tk.Frame):
    '''Sample tkinter application class'''

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        '''Create all the widgets'''

class App(Application):
    def create_widgets(self):
        super().create_widgets()

        #self.Q = tk.Button(self, text="Quit", command=self.master.quit)


        self.fig = plt.figure(1, [4, 4])
        canvas = FigureCanvasTkAgg(self.fig)
        plot_widget = canvas.get_tk_widget()

        self.draw_button = tk.Button(self, text="Draw", command=self.draw_pls)

        self.choice = tk.IntVar()
        self.options = [i for i in range(1, 10)]
        self.choice.set(self.options[8])

        self.menu = tk.OptionMenu(self, self.choice, *self.options)


        self.E1 = tk.Entry(self, width=6)
        self.E2 = tk.Entry(self,width=6)

        self.a_label = tk.Label(self, text="a: ")
        self.b_label = tk.Label(self, text="b: ")

        #self.inf0_label = tk.Label(self, text="Time: ")

        self.label_text = tk.StringVar()
        self.label_text.set(" ")
        #self.inf_label = tk.Label(self, textvariable=self.label_text)

        self.a_label.grid(row=0, column=0)
        self.E1.grid(row=0, column=1)
        self.b_label.grid(row=0, column=2)
        self.E2.grid(row=0, column=3)
        self.menu.grid(row=0, column=4)

        #self.Q.grid(row=1, column=4)
        self.draw_button.grid(row=1, column=3)
        #self.inf0_label.grid(row=1, columnspan=2)
        #self.inf_label.grid(row=1, column=1)

        self.E1.insert(0, "-0.2")
        self.E2.insert(0, "-0.2")

        self.master.protocol("WM_DELETE_WINDOW", self.pr_exit)


        #plot_widget.grid(row=3, column=0)

    def pr_exit(self):
        sys.exit()

    def draw_pls(self):
        if self.choice.get() == 1:
            DOTS_PER_POINT = 70
        elif self.choice.get() == 2:
            DOTS_PER_POINT = 35
        elif self.choice.get() == 3:
            DOTS_PER_POINT = 20
        elif self.choice.get() == 4:
            DOTS_PER_POINT = 10
        elif self.choice.get() == 5:
            DOTS_PER_POINT = 10
        elif self.choice.get() == 6:
            DOTS_PER_POINT = 5
        elif self.choice.get() == 7:
            DOTS_PER_POINT = 5
        elif self.choice.get() >= 8:
            DOTS_PER_POINT = 5



        self.label_text.set(" ")
        plt.clf()

        a = float(self.E1.get())
        b = float(self.E2.get())
        cells, size, time = main(self.choice.get(), a, b, DOTS_PER_POINT)
        self.label_text.set(str(time))

        plt.ylim((-2, 2))
        plt.xlim((-2, 2))

        f, s = [], []
        for cell in cells:
            dots = get_dots_from_cell(cell, size, DOTS_PER_POINT)
            for dot in dots:
                f.append(dot[0])
                s.append(dot[1])
            plt.plot(f, s, color="blue", linewidth=0.1)
            f.clear()
            s.clear()
        plt.show()
        #self.fig.canvas.draw()


if __name__ == '__main__':
    app = App(title="Kosaraju mayhem")
    app.mainloop()
    #main()
