from collections import OrderedDict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandastable import Table

import matplotlib
import matplotlib.pyplot as plt
import math
import MySQLdb
import os.path
import pandas as pd
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog


class Application (tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(background="#fff")

        self.fonts = {
            "title": tkfont.Font(family="Lucida Grande", size=24)
        }

        self.tabs = [
            DataFrame,
            StatsFrame
        ]
        self.create_widgets()
        self.set_tab(0)

    def create_widgets(self):
        self.rowconfigure(index=2, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Create title Widget
        self.title_label = tk.Label(
            self, text="DataVault Inc.", font=self.fonts["title"], justify="left", bg="#f0f0f0")
        self.title_label.grid(row=0, column=0, ipady=8,
                              ipadx=12, sticky="NSEW")

        # Create view selection widgets, i.e. tab buttons
        if len(self.tabs) > 1:
            self.subheader_frame = tk.Frame(self, bg="#f0f0f0")
            self.subheader_frame.grid(
                row=1, column=0, ipady="8", sticky="NSEW")

            # Set subheader_frame to have 8 columns.
            for col in range(12):
                self.subheader_frame.columnconfigure(index=col, weight=1)

        # Create container for actual tabs.
        self.tab_container = tk.Frame(self, bg="#fff")
        self.tab_container.grid(row=2, column=0, sticky="NSEW")
        # Set tab_container 0 index row & column to weight of 1
        self.tab_container.rowconfigure(index=0, weight=1)
        self.tab_container.columnconfigure(index=0, weight=1)

        self.tab_buttons = []
        for idx, tab in enumerate(self.tabs):
            if len(self.tabs) > 1:
                # Create tab buttons
                t = tk.Button(self.subheader_frame, text=tab.label, relief="ridge",
                              command=lambda index=idx: self.set_tab(index))

                self.tab_buttons.append(t)
                self.tab_buttons[idx].grid(ipadx=10, ipady=5, sticky="NSEW",
                                           row=0, column=(6 - math.floor(len(self.tabs) / 2) + idx),
                                           columnspan=(len(self.tabs) % 2 + 1))

            # Create tab frames
            self.tabs[idx] = tab(master=self.tab_container, bg="#ff0")
            self.tabs[idx].grid(row=0, column=0, sticky="NSEW")

    def set_tab(self, frame_idx):
        for idx, _ in enumerate(self.tab_buttons):
            if idx == frame_idx:
                self.tab_buttons[idx]["state"] = "disabled"
                self.tabs[idx].tkraise()
            else:
                self.tab_buttons[idx]["state"] = "normal"


class DataFrame(tk.Frame):
    label = "View Data"

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        df_cols, db_data = get_db_data()
        data_df = pd.DataFrame(db_data, columns=df_cols).set_index("ID")

        self.data_table = Table(self, dataframe=data_df)
        self.data_table.autoResizeColumns()
        self.data_table.show()


class StatsFrame(tk.Frame):
    label = "View Stats"

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        f = self.get_plot_data()
        self.plt_show(f)

    def plt_show(self, f):
        """Method to add the matplotlib graph onto a tkinter window."""
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        for ax in f.get_axes():
            for tick in ax.get_xticklabels():
                tick.set_rotation(35)

        self.plot_widget = canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky="NSEW")

    def get_plot_data(self):
        # Get a data from DB and import into pandas.DataFrame
        df_cols, db_data = get_db_data()
        products_df = pd.DataFrame(db_data, columns=df_cols).set_index("ID")

        # Create the matplotlib figure and axes that will be used to display the graphs for the statistics.
        fig = Figure(figsize=(15, 5), dpi=100)

        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)

        fig.subplots_adjust(bottom=.25)

        # Create different statistics and plot them the figure previously defined.
        products_df.groupby(["Category"]).size().plot(ax=ax1, y="Stock Available", kind="bar", grid=True,
                                                      title="Number of Items per Category")
        products_df.groupby(["Category"]).sum().plot(ax=ax2, y="Stock Available", kind="bar", grid=True,
                                                     title="Total Number of Products per Category")
        products_df.groupby(["Category"]).mean().plot(ax=ax3, y="Stock Available", kind="bar", grid=True,
                                                      title="Average Price of Products in Category")

        return fig


def get_db_data():
    """ Method to get the data from the database and return it as a tuple consisting
    of a list of the names of the columns and a list of the actualy data in tuple format."""
    db = MySQLdb.connect("localhost", "root", "2ZombiesEatBrains?")
    cursor = db.cursor()

    cols = [
        "ID", "Name", "Category", "Stock Available", "Selling Price", "Description"
    ]

    cursor.execute("SELECT * FROM sprint_datavault.products")
    data = cursor.fetchall()
    db.close()
    return cols, data


app = Application()
app.mainloop()
