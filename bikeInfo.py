from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog,messagebox
from PIL import Image, ImageTk
import math
import db.db_config as db
import db.Bike as Bike
import db.Order as Order
import db.Report as Report
import db.User as User

class BikePage(Tk):
    def __init__(self,open_user_id,bike_id,update_function):
        super().__init__()
        self.__win()
        self.update_function = update_function
        self.open_user_id = open_user_id
        self.bike_id = bike_id
        self.title("BikeId: "+str(bike_id))
        self.bike_dict = db.query_data(Bike.getBikeById(bike_id))
        self.user = db.query_data(User.getUserInfo(open_user_id))

        self.tk_frame_frame_left = self.__tk_frame_frame_left(self)
        self.tk_label_Vechine = self.__tk_label_Vechine(self.tk_frame_frame_left)
        self.tk_label_status = self.__tk_label_status(self.tk_frame_frame_left)
        self.tk_label_battery = self.__tk_label_battery(self.tk_frame_frame_left)
        self.tk_text_bike_box = self.__tk_text_bike_box(self.tk_frame_frame_left)
        self.tk_text_status_box = self.__tk_text_status_box(self.tk_frame_frame_left)
        self.tk_text_battery_box = self.__tk_text_battery_box(self.tk_frame_frame_left)
        self.tk_label_min = self.__tk_label_min(self.tk_frame_frame_left)
        self.tk_text_min = self.__tk_text_min(self.tk_frame_frame_left)
        self.tk_frame_frame_right = self.__tk_frame_frame_right(self)
        self.tk_frame_button_different = self.__tk_frame_button_different(self)

    def __win(self):
        # 设置窗口大小、居中
        width = 240
        height = 289
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_frame_frame_left(self, parent):
        frame = Frame(parent, )
        frame.place(x=10, y=10, width=220, height=198)
        return frame

    def __tk_label_Vechine(self, parent):
        label = Label(parent, text="Vehicles:", anchor="center", )
        label.place(x=10, y=10, width=59, height=30)
        return label

    def __tk_label_status(self, parent):
        label = Label(parent, text="Status:", anchor="center", )
        label.place(x=10, y=60, width=59, height=30)
        return label

    def __tk_label_battery(self, parent):
        label = Label(parent, text="Battery:", anchor="center", )
        label.place(x=10, y=110, width=59, height=30)
        return label

    def __tk_text_bike_box(self, parent):
        text = Text(parent)
        text.insert("1.0",self.bike_dict[0]['bike_type'])
        text.place(x=78, y=10, width=136, height=31)
        text.config(state=DISABLED)  # 设置Text小部件为只读
        return text

    def __tk_text_status_box(self, parent):
        text = Text(parent)
        status = self.show_status_of_bike(self.bike_dict[0]['is_use'],self.bike_dict[0]['is_broken'])
        text.insert("1.0", status)
        text.config(state=DISABLED)  # 设置Text小部件为只读
        text.place(x=79, y=60, width=135, height=31)
        return text

    def __tk_text_battery_box(self, parent):
        text = Text(parent)
        text.insert("1.0", str(self.bike_dict[0]['battery'])+"%")
        text.place(x=79, y=110, width=135, height=31)
        text.config(state=DISABLED)  # 设置Text小部件为只读
        return text

    def __tk_label_min(self, parent):
        label = Label(parent, text="Total(min):", anchor="center", )
        label.place(x=5, y=158, width=64, height=30)
        return label

    def __tk_text_min(self, parent):
        text = Text(parent)
        text.insert("1.0", self.bike_dict[0]['total_minutes'])
        text.place(x=77, y=158, width=135, height=31)
        text.config(state=DISABLED)  # 设置Text小部件为只读
        return text

    def __tk_frame_frame_right(self, parent):
        frame = Frame(parent, )
        frame.place(x=250, y=10, width=220, height=268)
        return frame

    def __tk_frame_button_different(self, parent):
        frame = Frame(parent, )
        if self.user[0]['user_type'] == 'User':
            if self.bike_dict[0]['is_use'] == self.open_user_id:
                return_button = Button(frame, text="Return", command=self.return_bike)
                return_button.grid(row=0, column=0, padx=10)
            else:
                rent_button = Button(frame, text="Rent", command=self.rent_bike)
                rent_button.grid(row=0, column=0, padx=10)
            cancel_button = Button(frame, text="Cancel", command=self.cancel_bike)
            cancel_button.grid(row=0, column=1, padx=10)

        elif self.user[0]['user_type'] == 'Operator':
            charge_button = Button(frame, text="Charge", command=self.charge_bike, width=7)
            fix_button = Button(frame, text="Fix", command=self.fix_bike, width=7)
            move_button = Button(frame, text="Move", command=self.move_bike, width=7)
            charge_button.grid(row=0, column=0, padx=5)
            fix_button.grid(row=0, column=1, padx=5)
            move_button.grid(row=0, column=2, padx=5)

        elif self.user[0]['user_type'] == 'Manager':
            add_same_button = Button(frame, text="Add Same", command=self.add_same_bike)
            delete_button = Button(frame, text="Delete", command=self.delete_bike)
            add_same_button.grid(row=0, column=0, padx=10)
            delete_button.grid(row=0, column=1, padx=10)

        frame.place(x=11, y=223, width=218, height=54)
        return frame

    def show_status_of_bike(self,is_use,is_broken):
        if is_broken==1:
            return "Broken"
        else:
            if is_use==-1:
                return "Unused"
            else:
                user = db.query_data(User.getUserInfo(is_use))
                return "Used By "+user[0]['user_name']

    def rent_bike(self):
        if(len(db.query_data(Bike.findIsUse(self.open_user_id)))!=0):
            messagebox.showerror("Error", "You can only rent one bike at the same time")
            self.destroy()
            return
        else:
            if(self.bike_dict[0]['is_broken']==1):
                messagebox.showerror("Error", "It is broken")
                self.destroy()
                return
            elif(self.bike_dict[0]['is_use']!=-1):
                messagebox.showerror("Error", "Someone has already used it")
                self.destroy()
                return
            elif (self.bike_dict[0]['battery'] <= 10):
                messagebox.showerror("Error", "Low Battery")
                self.destroy()
                return
            elif (self.user[0]['wallet'] <= 0):
                messagebox.showerror("Error", "Your account doesn't have enough money")
                self.destroy()
                return
            from_X = self.bike_dict[0]['X']
            from_Y = self.bike_dict[0]['Y']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.insert_or_delete_data(Order.startOrder(self.open_user_id,self.bike_id,current_time,from_X,from_Y,self.bike_dict[0]['city']))
            db.insert_or_delete_data(Bike.ownBike(self.open_user_id,self.bike_id))
            messagebox.showinfo("Info", "You have started your order at "+current_time)
            self.destroy()
            self.update_function()

    def return_bike(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        to_X = simpledialog.askinteger("Your final X:", "Enter the new X coordinate:")
        to_Y = simpledialog.askinteger("Your final Y:", "Enter the new Y coordinate:") # TODO
        order = db.query_data(Order.getUnfinishedOrder(self.open_user_id))
        start_time = order[0]['start_date']
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        time_difference = end_datetime - start_datetime
        total_minutes = time_difference.total_seconds() / 60
        cost = self.count_fee(total_minutes)
        x = self.count_battery(order[0]['from_X'],order[0]['from_Y'],to_X,to_Y)  ##TODO
        db.insert_or_delete_data(Order.endOrder(order[0]['id'],current_time,to_X,to_Y,cost))
        db.insert_or_delete_data(Bike.returnBike(self.bike_id))
        db.insert_or_delete_data(Bike.lowBattery(self.bike_id,x))
        db.insert_or_delete_data(User.subMoney(self.open_user_id,cost))
        db.insert_or_delete_data(Bike.changelocation(self.bike_id,to_X,to_Y))
        db.insert_or_delete_data(Bike.addMinutes(self.bike_id,total_minutes))
        messagebox.showinfo("Info", "You have end your order at "+current_time)
        self.destroy()
        self.update_function()

    def cancel_bike(self):
        self.destroy()

    def count_fee(self,total_minutes):
        type = self.bike_dict[0]['bike_type']
        rate = 1
        if(type=="Bike"):
            rate=1
        elif(type=="Car"):
            rate=5
        C = 0
        while total_minutes >= 30:
            C += rate
            total_minutes -= 30
        return C+rate
    def count_battery(self,from_X,from_Y,to_X,to_Y):
        type = self.bike_dict[0]['bike_type']
        rate = 1
        if (type == "Bike"):
            rate = 50
        elif (type == "Car"):
            rate = 200
        road = abs(from_X-to_X)+abs(from_Y-to_Y)
        now_battery = self.bike_dict[0]['battery']
        lose_battery = max(1,road / rate)
        if(lose_battery>=now_battery):
            return 0
        else:
            return now_battery-lose_battery

    def charge_bike(self):
        battery_text = self.tk_text_battery_box.get("1.0","end-1c")
        battery = float(battery_text[:-1])
        status = self.tk_text_status_box.get("1.0","end-1c")
        if status == "Using":
            messagebox.showinfo("Info", "Is been using now!")
        else:
            if battery == 100:
                messagebox.showinfo("Info", "Already full!")
            else:
                self.tk_text_battery_box.delete("1.0", "end")
                self.tk_text_battery_box.insert("1.0", "100%")
                db.insert_or_delete_data(Bike.changeBattery(self.bike_id))
                messagebox.showinfo("Info", "Completed")
                self.update_function()

    def fix_bike(self):
        status = self.tk_text_status_box.get("1.0","end-1c")
        if status == "Using":
            messagebox.showinfo("Info", "Is been using now!")
        elif status == "Broken":
            messagebox.showinfo("Info", "Complete!")
            db.insert_or_delete_data(Bike.fix(self.bike_id))
            self.tk_text_status_box.delete("1.0", "end")
            self.tk_text_status_box.insert("1.0", "Unused")
            self.update_function()
        elif status == "Unused":
            messagebox.showinfo("Info", "It's OK now")

    def move_bike(self):
        status = self.tk_label_status['text']
        if status == "Using":
            messagebox.showinfo("Info", "Is been using now!")
        else:
            new_x = simpledialog.askinteger("Enter New X", "Enter the new X coordinate:")
            new_y = simpledialog.askinteger("Enter New Y", "Enter the new Y coordinate:")
            db.insert_or_delete_data(Bike.changelocation(self.bike_id,new_x,new_y))
            messagebox.showinfo("Info", "Completely Moved!")
            self.update_function()

    def add_same_bike(self):
        new_x = simpledialog.askinteger("Enter New X", "Enter the new X coordinate:")
        new_y = simpledialog.askinteger("Enter New Y", "Enter the new Y coordinate:")
        db.insert_or_delete_data(Bike.createBike(new_x,new_y,self.bike_dict['bike_type'],self.bike_dict['city']))
        messagebox.showinfo("Info", "Completely Created A same one!")
        self.update_function()

    def delete_bike(self):
        db.insert_or_delete_data(Bike.deleteBikeById(self.bike_id))
        messagebox.showinfo("Info", "Completely Delete!")
        self.update_function()

class Win(BikePage):
    def __init__(self):
        super().__init__(self.open_user_id,self.bike_id,self.update_function)
        self.__event_bind()
    def __event_bind(self):
        pass


# if __name__ == "__main__":
#     win = BikePage(3,2)
#     win.mainloop()
    # print(win.count_fee('2021/03/12 12:00:00','2021/03/12 12:01:00'))