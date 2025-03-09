from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import db.db_config as db
import db.Bike as Bike
import db.Order as Order
from PIL import Image, ImageTk
import db.Report as Report
import db.User as User

class NewReport(Tk):
    def __init__(self,user_id,order_id,bike_id):
        super().__init__()
        self.__win()
        self.user_id=user_id
        self.order_id = order_id
        self.bike_id =bike_id

        self.tk_frame_frame_left = self.__tk_frame_frame_left(self)
        self.tk_label_Tyoe = self.__tk_label_Tyoe(self.tk_frame_frame_left)
        self.tk_label_info = self.__tk_label_info(self.tk_frame_frame_left)
        self.tk_select_box_type = self.__tk_select_box_type(self.tk_frame_frame_left)
        self.tk_text_message = self.__tk_text_message(self.tk_frame_frame_left)
        self.tk_button_confirm = self.__tk_button_confirm(self.tk_frame_frame_left)

    def __win(self):
        self.title("NewReport")
        width = 298
        height = 308
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
        frame.place(x=10, y=10, width=273, height=279)
        return frame

    def __tk_label_Tyoe(self, parent):
        label = Label(parent, text="ChooseType: ", anchor="center", )
        label.place(x=10, y=10, width=113, height=30)
        return label

    def __tk_label_info(self, parent):
        label = Label(parent, text="Wrtten your words in there: ", anchor="center", )
        label.place(x=10, y=50, width=246, height=30)
        return label

    def __tk_select_box_type(self, parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("Broken", "Payment", "Other")
        cb.set("Broken")
        cb.place(x=140, y=10, width=122, height=30)
        return cb

    def __tk_text_message(self, parent):
        text = Text(parent)
        text.place(x=10, y=90, width=247, height=124)
        return text

    def __tk_button_confirm(self, parent):
        btn = Button(parent, text="confirm", takefocus=False, command=self.on_confirm_button_click)
        btn.place(x=80, y=230, width=109, height=30)
        return btn

    def on_confirm_button_click(self):
        info = db.query_data(User.getUserInfo(self.user_id))
        selected_type = self.tk_select_box_type.get()
        message = self.tk_text_message.get(1.0, END)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.insert_or_delete_data(Report.createReport(self.user_id,self.order_id,self.bike_id,message,selected_type,current_time,info[0]['city']))
        messagebox.showinfo("Info", "Your report is accepted")
        if(selected_type=="Broken"):
            db.insert_or_delete_data(Bike.broken(self.bike_id))
        self.destroy()



class Win(NewReport):
    def __init__(self):
        super().__init__(self.user_id,self.order_id,self.bike_id)
        self.__event_bind()

    def __event_bind(self):
        pass


if __name__ == "__main__":
    win = NewReport(1,1,1)
    win.mainloop()