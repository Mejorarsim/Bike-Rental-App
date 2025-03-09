
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import db.db_config as db
import db.Bike as Bike
import db.Order as Order
import db.Report as Report
import db.User as User


class ReportPage(Tk):
    def __init__(self,order_id,report_id,user_id):
        super().__init__()
        self.__win()
        self.report_id = report_id
        self.order_id = order_id
        self.title("Order Detail - ID: {}".format(self.order_id))
        self.order_dict = db.query_data(Report.getReportByOrderId(order_id))
        self.bike_id = self.order_dict[0]['bike_id']
        self.user_id = user_id

        self.tk_frame_frame_left = self.__tk_frame_frame_left(self)
        self.tk_label_user = self.__tk_label_user(self.tk_frame_frame_left)
        self.tk_label_date = self.__tk_label_date(self.tk_frame_frame_left)
        self.tk_label_problem_type = self.__tk_label_problem_type(self.tk_frame_frame_left)
        self.tk_label_bike_id = self.__tk_label_bike_id(self.tk_frame_frame_left)
        self.tk_text_user_box = self.__tk_text_user_box(self.tk_frame_frame_left)
        self.tk_text_date_box = self.__tk_text_date_box(self.tk_frame_frame_left)
        self.tk_text_problem_type_box = self.__tk_text_problem_type_box(self.tk_frame_frame_left)
        self.tk_text_bike_box = self.__tk_text_bike_box(self.tk_frame_frame_left)
        self.tk_button_bike_button = self.__tk_button_bike_button(self.tk_frame_frame_left)
        self.tk_frame_frame_right = self.__tk_frame_frame_right(self)
        self.tk_text_message = self.__tk_text_message(self.tk_frame_frame_right)
        self.tk_button_done = self.__tk_button_done(self.tk_frame_frame_right)

    def __win(self):
        # 设置窗口大小、居中
        width = 490
        height = 230
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    # 自动隐藏滚动条
    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def vbar(self, ele, parent, y, h, ph):
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(relx=1, rely=y / ph, relheight=h / ph, anchor=NE)
        self.scrollbar_autohide(vbar, ele)

    def __tk_frame_frame_left(self, parent):
        frame = Frame(parent, )
        frame.place(x=10, y=10, width=220, height=205)
        return frame

    def __tk_label_user(self, parent):
        label = Label(parent, text="User:", anchor="center", )
        label.place(x=10, y=10, width=59, height=30)
        return label

    def __tk_label_date(self, parent):
        label = Label(parent, text="Date:", anchor="center", )
        label.place(x=10, y=60, width=59, height=30)
        return label

    def __tk_label_problem_type(self, parent):
        label = Label(parent, text="Problem:", anchor="center", )
        label.place(x=10, y=110, width=59, height=30)
        return label

    def __tk_label_bike_id(self, parent):
        label = Label(parent, text="BikeId:", anchor="center", )
        label.place(x=10, y=160, width=57, height=30)
        return label

    def __tk_text_user_box(self, parent):
        text = Text(parent)
        text.place(x=78, y=10, width=136, height=31)
        text.insert("1.0",self.get_username(self.user_id))
        text.config(state=DISABLED)  # 设置Text小部件为只读
        self.vbar(text, parent, 10, 31, 205)
        return text

    def __tk_text_date_box(self, parent):
        text = Text(parent)
        text.place(x=79, y=60, width=135, height=31)
        text.insert("1.0",self.order_dict[0]['date'])
        text.config(state=DISABLED)  # 设置Text小部件为只读
        self.vbar(text, parent, 60, 31, 205)
        return text

    def __tk_text_problem_type_box(self, parent):
        text = Text(parent)
        text.place(x=81, y=110, width=133, height=31)
        text.insert("1.0", self.order_dict[0]['problem_type'])
        text.config(state=DISABLED)  # 设置Text小部件为只读
        self.vbar(text, parent, 110, 31, 205)
        return text

    def __tk_text_bike_box(self, parent):
        text = Text(parent)
        text.place(x=80, y=160, width=40, height=31)
        text.insert("1.0", self.bike_id)
        text.config(state=DISABLED)  # 设置Text小部件为只读
        self.vbar(text, parent, 160, 31, 205)
        return text

    def __tk_button_bike_button(self, parent):
        def on_button_click():
            self.open_detail_page(self.user_id,self.bike_id)
        btn = Button(parent, text="BikeInfo", takefocus=False, command=on_button_click)
        btn.place(x=140, y=160, width=71, height=30)
        return btn

    def __tk_frame_frame_right(self, parent):
        frame = Frame(parent, )
        frame.place(x=250, y=10, width=220, height=206)
        return frame

    def __tk_text_message(self, parent):
        text = Text(parent)
        text.place(x=10, y=10, width=200, height=130)
        text.insert("1.0",self.order_dict[0]['message'])
        text.config(state=DISABLED)  # 设置Text小部件为只读
        self.vbar(text, parent, 10, 130, 206)
        return text

    def __tk_button_done(self, parent):
        btn = Button(parent, text="Marked as Done", takefocus=False,command=self.done )
        btn.place(x=10, y=160, width=197, height=30)
        return btn

    def done(self):
        db.insert_or_delete_data(Report.doneReport(self.report_id))
        messagebox.showinfo("Successful", "Now this problem is solved")
    def open_detail_page(self, user_id,bike_id):
        from bikeInfo import BikePage
        detail_page = BikePage(user_id,bike_id,self.update)
        detail_page.mainloop()
    def get_username(self,user_id):
        user = db.query_data(User.getUserInfo(user_id))
        return user[0]['user_name']
    def update(self):
        pass


class OpertorReport(ReportPage):
    def __init__(self):
        super().__init__(self.order_id,self.report_id,self.user_id)
        self.__event_bind()

    def __event_bind(self):
        pass


if __name__ == "__main__":
    win = ReportPage(1,1,3)
    win.mainloop()
