from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib
import matplotlib.pyplot as plt
import MySQLdb
import pandas as pd
import tkinter as tk
import tkinter.filedialog


matplotlib.use("TkAgg")


def get_db_data():
    db = MySQLdb.connect("localhost", "root", "2ZombiesEatBrains?")
    cursor = db.cursor()

    cols = [
        "ID", "Name", "Category", "Stock Available", "Selling Price", "Description"
    ]

    cursor.execute("SELECT * FROM sprint_datavault.products")
    data = cursor.fetchall()
    db.close()
    return cols, data


def plt_show(f, root):
    canvas = FigureCanvasTkAgg(f, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=12)


def import_csv():
    filename = tkinter.filedialog.askopenfilename()
    df = pd.read_csv(filename)
    return df


# Get a data from DB and import into pandas.DataFrame
df_cols, db_data = get_db_data()
products_df = pd.DataFrame(db_data, columns=df_cols).set_index("ID")


# Plot different datapoints from the DataFrame on the same figure.
fig = Figure(figsize=(15, 5), dpi=100)
ax1 = fig.add_subplot(1, 3, 1)
ax2 = fig.add_subplot(1, 3, 2)
ax3 = fig.add_subplot(1, 3, 3)

products_df.groupby(["Category"]).size().plot(ax=ax1, y="Stock Available", kind="bar", grid=True,
                                              title="Number of Items per Category")
products_df.groupby(["Category"]).sum().plot(ax=ax2, y="Stock Available", kind="bar", grid=True,
                                             title="Total Number of Products per Category")
products_df.groupby(["Category"]).mean().plot(ax=ax3, y="Stock Available", kind="bar", grid=True,
                                              title="Average Price of Products in Category")


root = tk.Tk()

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, padx=12, pady=12)

for col in range(12):
    main_frame.columnconfigure(col, weight=1)

# File Location
tk.Button(main_frame, text="Import a CSV", command=import_csv())\
    .grid(row=0, column=8)

plt_show(fig, root)

root.mainloop()
