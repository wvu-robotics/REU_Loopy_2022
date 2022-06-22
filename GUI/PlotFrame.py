from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk


class PlotFrame(tk.Frame):
    def __init__(self, container, ListX, ListY):
        super().__init__(container)

        self.configure(background='light blue', height=1, width=1)
#Plot labels
        self.label1 = ttk.Label(self, text='Current Position                                                                                                                                                                                      '
                                           'Goal Position', background='light blue', foreground="navy blue")
        self.label1.pack(side=tk.TOP, anchor=tk.NW, pady=5)

##Current Pose Plot
        f1 = Figure(figsize=(6, 2.7), dpi=100)
        a = f1.add_subplot(111)
        ###edit to get pose data from ROS
        a.plot(ListX,ListY)
        canvas = FigureCanvasTkAgg(f1, self)
        canvas.get_tk_widget().pack(side=tk.LEFT )

###Goal Pose Plot
        f2 = Figure(figsize=(2.7, 2.7), dpi=100)
        b = f2.add_subplot(111)
        b.plot([1, 1, 1.5, 1.5, 3, 3, 2, 1], [1, 5, 5, 2, 2, 1, 1, 1])
        self.canvasG = FigureCanvasTkAgg(f2, self)
        self.canvasG.get_tk_widget().pack(side=tk.LEFT, padx=30)
##Add to window
        self.grid(row=0, columnspan=60, padx=2, pady=0)

# does not work rn 6/22/22
    def UpdateGoalPlot(self, Goal):
        self.canvasG.get_tk_widget().delete()
        ##how to delete previous plot
        ##this section needs help
        f = Figure(figsize=(6, 2.7), dpi=100)
        c = f.add_subplot(111)
        if Goal == 'L':
            c.plot([1, 1, 1.5, 1.5, 3, 3, 2, 1], [1, 5, 5, 2, 2, 1, 1, 1])
        elif Goal == 'O':
            c.plot([1, 2, 3, 4, 5, 4, 3, 2, 1], [2, 3, 4, 5, 6, 5, 4, 3, 2])
        else:
            c.plot([1, 2, 3, 4, 5, 4, 3, 2, 1], [2, 3, 4, 5, 6, 5, 4, 3, 2])
        canvasG = FigureCanvasTkAgg(f, self)
        canvasG.get_tk_widget().pack
        #self.grid(row=0, columnspan=60, padx=2, pady=0)



