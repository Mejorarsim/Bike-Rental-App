import tkinter as tk
from tkinter import VERTICAL, RIGHT, Y, LEFT, BOTH, DISABLED, messagebox,simpledialog
from tkinter.ttk import *
import db.db_config as db
import db.Bike as Bike
import db.Order as Order
from PIL import Image, ImageTk
import db.Report as Report
import db.User as User

class Manager(tk.Tk):
    def __init__(self,user_id):
        super().__init__()
        self.__win()

        self.user_id = user_id
        self.now_type = 1
        self.title(self.get_title_name())
        self.filter = "All"
        self.city = 'Glasgow'

        self.panning = False
        self.default_map_x = 0
        self.default_map_y = 0
        self.last_x = 0
        self.last_y = 0
        self.bike_count = 0

        self.tk_frame_left = self.__tk_frame_left(self)

        self.tk_button_MainButton = self.__tk_button_MainButton(self.tk_frame_left)
        self.tk_button_ReportButton = self.__tk_button_ReportButton(self.tk_frame_left)
        self.tk_button_DetailButton = self.__tk_button_DetailButton(self.tk_frame_left)
        self.tk_button_InfoButton = self.__tk_button_InfoButton(self.tk_frame_left)

        self.tk_frame_right = self.__tk_frame_right(self)
        self.tk_select_box_type = self.__tk_select_box_type(self.tk_frame_right)
        self.tk_select_map_type = self.__tk_select_map_type(self.tk_frame_right)
        self.tk_button_view = self.__tk_button_view(self.tk_frame_right)
        self.tk_button_add = self.__tk_button_add(self.tk_frame_right)


        self.tk_canvas_mapBox = self.__tk_canvas_mapBox(self.tk_frame_right)

        self.tk_canvas_reports_container = self.__tk_canvas_reports_container(self.tk_frame_right)
        self.tk_canvas_detailed = self.__tk_canvas_detailed(self.tk_frame_right)
        self.tk_frame_info = self.__tk_frame_info(self.tk_frame_right)
        self.show_map_page()  # default showing map pages

    def get_title_name(self):
        operator_info = db.query_data(User.getUserInfo(self.user_id))
        return "Operator: " + operator_info[0]['user_name']

    def __win(self):
        width = 783
        height = 322
        style = Style()
        style.configure("My.TFrame", borderwidth=2, relief="solid", foreground="black")
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def configure_frame_border(self, frame):
        frame.configure(style="My.TFrame")
    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)
    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)
    def scrollbar_autohide(self,bar,widget):
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
    def vbar(self,ele, x, y, w, h, parent):
        sw = 15 # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar,ele)
    def __tk_frame_left(self, parent):
        frame = Frame(parent)
        frame.place(x=10, y=10, width=106, height=295)
        self.configure_frame_border(frame)
        return frame
    def __tk_button_MainButton(self, parent):
        btn = Button(parent, text="Map", takefocus=False, command=self.show_map_page)
        btn.place(x=10, y=20, width=80, height=48)
        return btn
    def __tk_button_ReportButton(self, parent):
        btn = Button(parent, text="Users", takefocus=False, command=self.show_reports_page)
        btn.place(x=10, y=90, width=80, height=48)
        return btn
    def __tk_button_DetailButton(self, parent):
        btn = Button(parent, text="Bikes", takefocus=False, command=self.show_detail_page)
        btn.place(x=10, y=160, width=80, height=48)
        return btn
    def __tk_button_InfoButton(self, parent):
        btn = Button(parent, text="Info", takefocus=False, command=self.show_info_page)
        btn.place(x=10, y=230, width=80, height=48)
        return btn
    def __tk_frame_right(self, parent):
        frame = Frame(parent)
        frame.place(x=130, y=10, width=638, height=295)
        self.configure_frame_border(frame)
        return frame
    def __tk_select_box_type(self, parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("All", "Bike", "Car")
        cb.set("All")
        cb.place(x=476, y=10, width=154, height=32)
        cb.bind("<<ComboboxSelected>>", self.on_combobox_select)
        return cb
    def __tk_select_map_type(self, parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("Glasgow", "Edinburgh", "Aberdeen","Dundee")
        cb.set("Glasgow")
        cb.place(x=10, y=10, width=154, height=32)
        cb.bind("<<ComboboxSelected>>", self.on_map_select)
        return cb
    def __tk_button_view(self,parent):
        btn = Button(parent, text="Visualization", takefocus=False, command=self.view)
        btn.place(x=174, y=10, width=130, height=32)
        return btn

    def __tk_button_add(self,parent):
        btn = Button(parent, text="AddNew", takefocus=False, command=self.add)
        btn.place(x=315, y=10, width=80, height=32)
        return btn
    def __tk_canvas_mapBox(self, parent):
        canvas = tk.Canvas(parent)
        canvas.place(x=10, y=50, width=607, height=233)
        return canvas
    def __tk_canvas_detailed(self,parent):
        canvas = tk.Canvas(parent)
        canvas.place(x=10, y=50, width=607, height=233)  # this is the containor of reports, IMPORTANT!! IT IS CANVAS!!
        return canvas
    def __tk_frame_info(self,parent):
        frame = Frame(parent)
        frame.place(x=10, y=50, width=607, height=233)
        self.configure_frame_border(frame)
        return frame
    def __tk_canvas_reports_container(self, parent):
        canvas = tk.Canvas(parent)
        canvas.place(x=10, y=50, width=607, height=233) # this is the containor of reports, IMPORTANT!! IT IS CANVAS!!
        return canvas


    def user_lists(self, parent,frame_index,user_name,user_type,user_id,user_email,wallet):  # this method is to show lots of small frame in a canvas
        frame = Frame(parent)                                               # You can copy it to other place you want
        frame.place(x=5, y=10 + frame_index * 60, width=570, height=50)
        frame.configure(style="My.TFrame")

        label_user_id = Label(frame, text=user_id, anchor="center")
        label_user_id.place(x=5, y=10, width=50, height=30)

        label_user_type = Label(frame, text=user_type, anchor="center")
        label_user_type.place(x=60, y=10, width=90, height=30)

        label_user = Label(frame, text=user_name, anchor="center")
        label_user.place(x=135, y=10, width=100, height=30)

        label_user_email = Label(frame, text=user_email, anchor="center")
        label_user_email.place(x=240, y=10, width=150, height=30)

        if(user_type=='User'):
            label_user_email = Label(frame, text="wallet: {}".format(wallet), anchor="center")
            label_user_email.place(x=395, y=10, width=100, height=30)

        return frame

    def bike_lists(self, parent, frame_index,bike_id, bike_type, city, battery,status):
        frame = Frame(parent)
        frame.place(x=5, y=10 + frame_index * 60, width=570, height=50)
        frame.configure(style="My.TFrame")

        label_id = Label(frame, text=bike_id, anchor="center")
        label_id.place(x=5, y=10, width=20, height=30)

        label_type = Label(frame, text=bike_type, anchor="center")
        label_type.place(x=25, y=10, width=30, height=30)

        label_city = Label(frame, text=city, anchor="center")
        label_city.place(x=60, y=10, width=80, height=30)

        label_battery = Label(frame, text=str(battery)+'%', anchor="center")
        label_battery.place(x=150, y=10, width=67, height=30)

        label_date = Label(frame, text=status, anchor="center")
        label_date.place(x=210, y=10, width=100, height=30)

        button_charge = Button(frame, text="AddSame", takefocus=False,command=lambda type=bike_type,city_name=city:self.add_same(type,city_name))
        button_charge.place(x=400, y=10, width=70, height=30)

        button_check = Button(frame, text="Detail", takefocus=False,command=lambda user=self.user_id,bike=bike_id:self.open_bike_page(user,bike))
        button_check.place(x=495, y=10, width=60, height=30)

        return frame

# Map showing method is here!!!!!!!!
    def show_map(self):
        self.map_image = Image.open(self.city+".jpg")  # Replace with your map image path
        self.map_width, self.map_height = self.map_image.size
        new_width = int(self.map_width)
        new_height = int(self.map_height)
        resized_image = self.map_image.resize((new_width, new_height))
        self.photo = ImageTk.PhotoImage(resized_image)
        # Clear the canvas and display the resized map
        self.tk_canvas_mapBox.delete("all")
        self.map_item = self.tk_canvas_mapBox.create_image(self.default_map_x, self.default_map_y, image=self.photo, anchor="nw") #TODO I will do with pos

        ids=[]
        if(self.filter=="All"):
            data = db.query_data(Bike.getAllBike(self.city))
        else:
            data = db.query_data(Bike.getBikeByTypes(self.filter,self.city))
        for item in data:
            x = item['X']+self.default_map_x
            y = item['Y']+self.default_map_y
            id = item['id']
            ids.append(id)
            color = Bike.getColorForBike(item['bike_type'])
            self.add_marker(x, y, id,color)
        self.tk_canvas_mapBox.bind("<ButtonPress-1>", self.on_map_click)
        # id_list is used in the lambda function below,this red line may due to edit's error, does't matter
        self.tk_canvas_mapBox.bind("<B1-Motion>", lambda event, id_list=ids: self.on_map_drag(event, id_list))
        # Bind click events for markers
        self.bike_count= len(data)
        for i in ids:
            self.tk_canvas_mapBox.tag_bind('marker_%s' % i, '<ButtonPress-1>',
                                 lambda evt, id=i: self.open_bike_page(self.user_id,id))
    def on_map_click(self, event):
        self.panning = True
        self.last_x = event.x
        self.last_y = event.y

    def on_map_drag(self, event,id_list):
        if self.panning:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.last_x = event.x
            self.last_y = event.y

            # Calculate the current map position
            current_x, current_y = self.tk_canvas_mapBox.coords(self.map_item)
            new_x = current_x + dx
            new_y = current_y + dy
            self.default_map_x = new_x
            self.default_map_y = new_y

            # Calculate the boundaries
            min_x = 607 - self.map_width
            min_y = 233 - self.map_height

            # Ensure the new position is within bounds
            new_x = max(min_x, min(0, new_x))
            new_y = max(min_y, min(0, new_y))

            self.tk_canvas_mapBox.move(self.map_item, new_x - current_x, new_y - current_y)

            # Update marker positions
            for i in id_list:
                x1, y1, x2, y2 = self.tk_canvas_mapBox.coords('marker_%s' % i) ##TODO

                self.tk_canvas_mapBox.coords('marker_%s' % i, x1 + new_x - current_x, y1 + new_y - current_y,
                                   x2 + new_x - current_x, y2 + new_y - current_y)

    def add_marker(self, x, y, id, color):
        # red
        self.tk_canvas_mapBox.coords('marker_%s' % id, x - 5, y - 5, x + 5, y + 5)
        self.tk_canvas_mapBox.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, tag='marker_%s' % id)

## map method ends!!!!!!!!!!!!!!!1

    def show_reports_page(self):
        # disappear the map frame
        self.tk_canvas_mapBox.place_forget()
        self.tk_canvas_detailed.place_forget()
        self.tk_frame_info.place_forget()
        self.now_type = 2
        self.tk_select_box_type['values'] = ("All")

        user = db.query_data(User.getAllUser(self.city))
        operator = db.query_data(User.getAllOpertor(self.city))
        operator.extend(user)
        report_data = operator

        canvas_height = len(report_data) * 70
        for widget in self.tk_canvas_reports_container.winfo_children():
            widget.destroy() #before show the lists, destroy the remain one first

        self.tk_canvas_reports_container.configure(height=canvas_height,scrollregion=(0, 0, 607, canvas_height))
        self.tk_canvas_reports_container.place(x=10, y=50, width=607, height=233)
        vbar = Scrollbar(self.tk_canvas_reports_container, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)  #create a vbar for canvas first

        frame = Frame(self.tk_canvas_reports_container,width=580,height=canvas_height)
        self.configure_frame_border(frame)
        frame.pack()        # then create a frame inside this canvas
        frame.bind("<Configure>", lambda e: self.tk_canvas_reports_container.configure(
            scrollregion=self.tk_canvas_reports_container.bbox("all")))  # connect the vbar with this frame

        self.tk_canvas_reports_container.create_window((0, 0), window=frame, anchor="nw") # connect the frame with canvas
        self.tk_canvas_reports_container.configure(yscrollcommand=vbar.set)
        vbar.configure(command=self.tk_canvas_reports_container.yview) #apply the vbar

        for index, data in enumerate(report_data):
            self.user_lists(
                frame,
                index,
                data['user_name'],
                data['user_type'],
                data['id'],
                data['email'],
                data['wallet']
            )                   # put your list inside the frame, NOT THE CANVAS!

    def show_map_page(self):
        self.tk_canvas_reports_container.place_forget()
        self.tk_canvas_detailed.place_forget()
        self.tk_frame_info.place_forget()
        self.now_type = 1
        self.tk_select_box_type['values'] = ("All", "Bike", "Car")
        for widget in self.tk_canvas_detailed.winfo_children():
            widget.destroy()
        self.tk_canvas_mapBox.place(x=10, y=50, width=607, height=233)
        self.show_map()

    def show_detail_page(self):
        self.tk_canvas_reports_container.place_forget()
        self.tk_canvas_mapBox.place_forget()
        self.tk_frame_info.place_forget()
        self.now_type = 3
        self.tk_select_box_type['values'] = ("All", "Bike", "Car")

        if(self.filter=="All"):
            deal_report_data=db.query_data(Bike.getAllBike(self.city))
        else:
            deal_report_data = db.query_data(Bike.getBikeByTypes(self.filter,self.city))

        canvas_height = len(deal_report_data) * 70
        for widget in self.tk_canvas_detailed.winfo_children():
            widget.destroy()

        self.tk_canvas_detailed.configure(height=canvas_height, scrollregion=(0, 0, 607, canvas_height))
        self.tk_canvas_detailed.place(x=10, y=50, width=607, height=233)
        vbar = Scrollbar(self.tk_canvas_detailed, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)  # create a vbar for canvas first

        frame = Frame(self.tk_canvas_detailed, width=580, height=canvas_height)
        self.configure_frame_border(frame)
        frame.pack()  # then create a frame inside this canvas
        frame.bind("<Configure>", lambda e: self.tk_canvas_detailed.configure(
            scrollregion=self.tk_canvas_detailed.bbox("all")))  # connect the vbar with this frame

        self.tk_canvas_detailed.create_window((0, 0), window=frame,
                                                       anchor="nw")  # connect the frame with canvas
        self.tk_canvas_detailed.configure(yscrollcommand=vbar.set)
        vbar.configure(command=self.tk_canvas_detailed.yview)  # apply the vbar

        for index, data in enumerate(deal_report_data):
            self.bike_lists(
                frame,
                index,
                data["id"],
                data["bike_type"],
                data["city"],
                data["battery"],
                self.show_status_of_bike(data['is_use'],data['is_broken'])
            )  # put your list inside the frame, NOT THE CANVAS!

    def show_info_page(self):
        self.tk_canvas_reports_container.place_forget()
        self.tk_canvas_detailed.place_forget()
        self.tk_canvas_mapBox.place_forget()
        self.now_type = 4

        self.tk_frame_info.place(x=10, y=50, width=607, height=233)
        labels = ["UserName", "Email:", "Phone:", "City:", "Wallet:"]
        keys=["user_name","email","phone","city","wallet"]
        user_info = db.query_data(User.getUserInfo(self.user_id))

        for i, label_text in enumerate(labels):
            label = tk.Label(self.tk_frame_info, text=label_text)
            label.place(x=120, y=8 + i * 30, width=100, height=30)

            text = tk.Text(self.tk_frame_info)
            text.insert("1.0", user_info[0][keys[i]])
            text.config(state=DISABLED)
            text.place(x=240, y=10 + i * 30, width=200, height=30)
            self.vbar(text, 240, 8 + i * 30, 200, 30, self.tk_frame_info)

        button_deal = Button(self.tk_frame_info, text="Logout", takefocus=False,command=self.logout)
        button_deal.place(x=280, y=180, width=50, height=30)

    def open_bike_page(self, user_id,bike_id):
        from bikeInfo import BikePage
        detail_page = BikePage(user_id,bike_id,self.update_function)
        detail_page.mainloop()

    def view(self):
        from man3 import ViewManager
        view = ViewManager()
        view.run()

    def add(self):
        from bikeAdd import BikeAdd
        win = BikeAdd()
        win.run()

    def add_same(self,type,city_name):
        new_x = simpledialog.askinteger("Enter New X", "Enter the new X coordinate:")
        new_y = simpledialog.askinteger("Enter New Y", "Enter the new Y coordinate:")
        db.insert_or_delete_data(Bike.createBike(new_x, new_y, type, city_name))
        messagebox.showinfo("Info", "Completely Created A Same One!")

    def on_combobox_select(self, event):
        selected_value = self.tk_select_box_type.get()
        if(self.now_type==3 or self.now_type==1):
            if selected_value == "All":
                self.filter = "All"
            elif selected_value == "Bike":
                self.filter = "Bike"
            elif selected_value == "Car":
                self.filter = "Car"
            if(self.now_type==3):
                self.show_detail_page()
            elif(self.now_type==1):
                self.show_map_page()

    def on_map_select(self,event):
        self.city = self.tk_select_map_type.get()
        if(self.now_type==1):
            self.show_map_page()
        elif(self.now_type==2):
            self.show_reports_page()
        elif(self.now_type==3):
            self.show_detail_page()

    def show_status_of_bike(self,is_use,is_broken):
        if is_broken==1:
            return "Broken"
        else:
            if is_use==-1:
                return "Unused"
            else:
                return "Using"

    def get_username(self,user_id):
        user = db.query_data(User.getUserInfo(user_id))
        return user[0]['user_name']
    def logout(self):
        self.destroy()
        from log import Login
        x = Login()
        x.run()
    def update_function(self):
        self.show_map_page()

class Manager_view(Manager):
    def __init__(self):
        super().__init__(self.user_id)
        self.__event_bind()

    def __event_bind(self):
        pass

if __name__ == "__main__":
    win = Manager(5)  # you should transfer the user_id to me(with login)
    win.mainloop()