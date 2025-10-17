import tkinter as tk
from tkinter import Tk, Button

import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler, MouseEvent, Event
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class GraphFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.parent = parent
        self.shift = 0

        # Draw buttons
        clear_button = Button(self, text="Clear points", command=self.plot_clear)
        quit_button = Button(self, text="Quit", command=self.parent.destroy)

        # Figure and tk_canvas
        self.fig = Figure(figsize=(7, 7), dpi=100)
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.points = np.empty((0, 2))
        self.line = None

        # Use grid to place elements
        clear_button.grid(row=0, column=0, padx=(10, 5))
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=(5, 15) , pady=5)
        quit_button.grid(row=2, column=1, padx=(5, 25), pady=(5, 15), sticky='e')

        # Draw the plot
        self.draw_plot()

    def draw_plot(self):
        self.ax.clear()
        # Plot the line and unpack it so that the points go into self.line (not a list)
        self.line, = self.ax.plot(self.points[:, 0], self.points[:, 1],
                     marker='o',
                     markersize=8,
                     linestyle='-',
                     color='darkblue')
        self.ax.set_title(f'Click to add Points')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        # update tk_canvas
        self.canvas.draw()

        # Add an on_button_click event
        self.canvas.mpl_connect('button_press_event', self.on_button_click)

    def on_button_click(self, event: Event) -> None:
        assert isinstance(event, MouseEvent)
        if event.inaxes is not None:
            new_point = np.array([event.xdata, event.ydata])
            self.points = np.vstack([self.points, new_point])
            self.line.set_data(self.points[:, 0], self.points[:, 1])
            self.canvas.draw()


    def plot_clear(self):
        self.points = np.empty((0, 2))
        self.draw_plot()


plt.style.use('ggplot')
# GUI
# matplotlib.use('TkAgg')
root = Tk()
root.title("Sample Sine Wave Graph in Tkinter")
graph_page = GraphFrame(root)
graph_page.pack()
root.mainloop()