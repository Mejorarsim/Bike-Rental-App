import tkinter as tk
import db.db_config as db
import db.Bike as Bike
from tkinter import messagebox

class BikeAdd:
    def __init__(self):
        self.root =  tk.Tk()
        self.root.title("Bike Add")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 200
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label1 = tk.Label(self.root, text="NewX")
        label1.place(x=20, y=20)
        self.entry_x = tk.Entry(self.root)
        self.entry_x.place(x=100, y=20)

        label2 = tk.Label(self.root, text="NewY")
        label2.place(x=20, y=50)
        self.entry_y = tk.Entry(self.root)
        self.entry_y.place(x=100, y=50)

        label3 = tk.Label(self.root, text="Location")
        label3.place(x=20, y=80)
        self.location_var = tk.StringVar()
        locations = ["Glasgow", "Edinburgh", "Aberdeen", "Dundee"]
        x_location = 100
        for location in locations:
            tk.Radiobutton(self.root, text=location, variable=self.location_var, value=location).place(x=x_location, y=80)
            x_location += 100
        self.location_var.set(locations[0])

        label4 = tk.Label(self.root, text="Transport")
        label4.place(x=20, y=110)
        self.transport_var = tk.StringVar()
        transports = ["Bike", "Car"]
        x_transport = 100
        for transport in transports:
            tk.Radiobutton(self.root, text=transport, variable=self.transport_var, value=transport).place(x=x_transport,
                                                                                                     y=110)
            x_transport += 100
        self.transport_var.set(transports[0])

        submit_button = tk.Button(self.root, text="Submit", command=self.get_data)
        submit_button.place(x=150, y=140)

    def get_data(self):
        x = self.entry_x.get()
        y = self.entry_y.get()
        location = self.location_var.get()
        transport = self.transport_var.get()
        db.query_data(Bike.createBike(x,y,transport,location))
        messagebox.showinfo("Info", "Completely Created A New One!")


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BikeAdd()
    app.run()
