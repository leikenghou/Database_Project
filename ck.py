import tkinter as tk
from tkinter import messagebox

import method
z1="w"
z2="w"
z3="w"
z4="w"
z5="w"
z6="w"
z7="w"
z8="w"
def open_search_window1():
    search_window = tk.Toplevel()
    search_window.title("搜索窗口")
    search_window.geometry("500x500")

    search_label = tk.Label(search_window, text="请输入要搜索的数据：")
    search_label.pack()

    search_entry = tk.Entry(search_window)
    search_entry.pack()

    search_button = tk.Button(search_window, text="搜索", command=lambda: perform_search(search_entry.get()))
    search_button.place(relx=0.67, rely=0.03)

    data_frame = tk.Frame(search_window, width=300, height=500, bg="white")
    data_frame.pack()

    data_scrollbar = tk.Scrollbar(data_frame)
    data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    data_listbox = tk.Listbox(data_frame, yscrollcommand=data_scrollbar.set)
    data_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    sql = "SELECT COUNT(gid) FROM finance.games;"
    data1 = method.execute_fetchone_query(sql)
    data1=data1[0]

    sql = "SELECT gname FROM finance.games"
    data2 = method.execute_fetchall_query(sql)


    for i in range(0, data1):
        x=data2[i][0]
        data_listbox.insert(tk.END, x)



    def perform_search(query):
        sql = "SELECT * FROM finance.games WHERE gname='" + str(query) + "';"
        date3 = method.execute_fetchone_query(sql)
        if date3==None:
            messagebox.showinfo("搜索结果", "搜索到不到相关的数据！")
        else:
            print(date3)
            window = tk.Tk()
            window.title("游戏信息窗口")
            window.geometry("500x500")

            labels = ["游戏编号", "游戏名称", "游戏价格", "发行时间", "发行商", "厂商编号", "折扣", "游戏简介"]

            for i, label_text in enumerate(labels):
               label = tk.Label(window, text=label_text, anchor="w", width=15)
               label.grid(row=i, column=0, padx=10, pady=5)

               text = tk.Text(window, height=1, width=30, bg="white")
               text.grid(row=i, column=1, padx=10, pady=5)

            # 设置右边的文本框内容为"test"
               text.insert("1.0", date3[i])

            window.mainloop()

    def delete_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT gid FROM finance.games LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z2 = date3[0]

        sql = "DELETE FROM games WHERE gid='" + z2 + "';"
        print(sql)
        date0 = method.execute_insert_query(sql)
        messagebox.showinfo("删除成功", "数据删除成功！")
        data_listbox.update()


    def modify_data():
        index = data_listbox.curselection()
        index=index[0]
        print(index)

        sql="SELECT gid FROM finance.games LIMIT "+str(index)+",1;"
        date3 = method.execute_fetchone_query(sql)
        z1=date3[0]


        modify_window = tk.Toplevel(search_window)
        modify_window.title("修改数据")
        modify_window.geometry("300x300")


        # Create five entry fields for modification

        entry_label = tk.Label(modify_window, text="游戏名称" )
        entry_label.place(relx=0.2, rely=0.2+(0.1*1), anchor=tk.CENTER)

        entry_field1 = tk.Entry(modify_window)
        entry_field1.place(relx=0.3, rely=0.2+(0.1*1))

        entry_label = tk.Label(modify_window, text="游戏价格" )
        entry_label.place(relx=0.2, rely=0.2+(0.1*2), anchor=tk.CENTER)

        entry_field2 = tk.Entry(modify_window)
        entry_field2.place(relx=0.3, rely=0.2+(0.1*2))

        entry_label = tk.Label(modify_window, text="发行日期" )
        entry_label.place(relx=0.2, rely=0.2+(0.1*3), anchor=tk.CENTER)

        entry_field3 = tk.Entry(modify_window)
        entry_field3.place(relx=0.3, rely=0.2+(0.1*3))

        def confirm_modification():
            x1=entry_field1.get()
            x2=entry_field2.get()
            x3=entry_field3.get()
            sql = "UPDATE finance.games SET gname='" + x1 + "',price="+ x2 +",release_date='" +x3+"' WHERE gid='"+z1+"';"
            print(sql)
            date0 = method.execute_insert_query(sql)

            messagebox.showinfo("修改成功", "数据修改成功！")
            modify_window.destroy()



        confirm_button = tk.Button(modify_window, text="确认", command=confirm_modification)
        confirm_button.place(relx=0.4, rely=0.7)

        cancel_button = tk.Button(modify_window, text="取消", command=modify_window.destroy)
        cancel_button.place(relx=0.6, rely=0.7)

    modify_button = tk.Button(search_window, text="修改", command=modify_data)
    modify_button.pack()

    delete_button = tk.Button(search_window, text="删除",command=delete_data)
    delete_button.pack()

def open_search_window2():
    search_window = tk.Toplevel()
    search_window.title("搜索窗口")
    search_window.geometry("500x500")

    search_label = tk.Label(search_window, text="请输入要搜索的数据：")
    search_label.pack()

    search_entry = tk.Entry(search_window)
    search_entry.pack()

    search_button = tk.Button(search_window, text="搜索", command=lambda: perform_search(search_entry.get()))
    search_button.place(relx=0.67, rely=0.03)

    data_frame = tk.Frame(search_window, width=300, height=500, bg="white")
    data_frame.pack()

    data_scrollbar = tk.Scrollbar(data_frame)
    data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    data_listbox = tk.Listbox(data_frame, yscrollcommand=data_scrollbar.set)
    data_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    sql = "SELECT COUNT(pid) FROM finance.players;"
    data1 = method.execute_fetchone_query(sql)
    data1 = data1[0]

    sql = "SELECT pname FROM finance.players"
    data2 = method.execute_fetchall_query(sql)



    for i in range(0, data1):
        x=data2[i][0]
        data_listbox.insert(tk.END, x)

    def perform_search(query):
        sql = "SELECT * FROM finance.players_view WHERE pname='" + str(query) + "';"
        date3 = method.execute_fetchone_query(sql)
        print(date3)
        if date3==None:
            messagebox.showinfo("搜索结果", "搜索到不到相关的数据！")
        else:
            window = tk.Tk()
            window.title("游戏信息窗口")
            window.geometry("500x500")

            labels = ["玩家编号","玩家名称", "玩家账户", "玩家密码", "玩家email", "玩家余额", "玩家简介"]

            for i, label_text in enumerate(labels):
                label = tk.Label(window, text=label_text, anchor="w", width=15)
                label.grid(row=i, column=0, padx=10, pady=5)

                text = tk.Text(window, height=1, width=30, bg="white")
                text.grid(row=i, column=1, padx=10, pady=5)

            # 设置右边的文本框内容为"test"
                text.insert("1.0", date3[i])

            window.mainloop()

    def delete_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT pid FROM finance.players LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z2 = date3[0]

        sql = "DELETE FROM finance.players WHERE pid='" + z2 + "';"
        print(sql)
        date0 = method.execute_insert_query(sql)
        messagebox.showinfo("删除成功", "数据删除成功！")
        data_listbox.update()

    def modify_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT pid FROM finance.players LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z1 = date3[0]

        modify_window = tk.Toplevel(search_window)
        modify_window.title("修改数据")
        modify_window.geometry("300x300")

        # Create five entry fields for modification

        entry_label = tk.Label(modify_window, text="玩家名称")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 1), anchor=tk.CENTER)

        entry_field1 = tk.Entry(modify_window)
        entry_field1.place(relx=0.3, rely=0.2 + (0.1 * 1))

        entry_label = tk.Label(modify_window, text="玩家email")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 2), anchor=tk.CENTER)

        entry_field2 = tk.Entry(modify_window)
        entry_field2.place(relx=0.3, rely=0.2 + (0.1 * 2))

        entry_label = tk.Label(modify_window, text="玩家余额")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 3), anchor=tk.CENTER)

        entry_field3 = tk.Entry(modify_window)
        entry_field3.place(relx=0.3, rely=0.2 + (0.1 * 3))

        def confirm_modification():
            x1 = entry_field1.get()
            x2 = entry_field2.get()
            x3 = entry_field3.get()
            sql = "UPDATE finance.players SET pname='" + x1 + "',email='" + x2 + "',account_balance=" + x3 + " WHERE pid='" + z1 + "';"
            print(sql)
            date0 = method.execute_insert_query(sql)

            messagebox.showinfo("修改成功", "数据修改成功！")
            modify_window.destroy()

        confirm_button = tk.Button(modify_window, text="确认", command=confirm_modification)
        confirm_button.place(relx=0.4, rely=0.7)

        cancel_button = tk.Button(modify_window, text="取消", command=modify_window.destroy)
        cancel_button.place(relx=0.6, rely=0.7)

    modify_button = tk.Button(search_window, text="修改", command=modify_data)
    modify_button.pack()

    delete_button = tk.Button(search_window, text="删除", command=delete_data)
    delete_button.pack()

def open_search_window3():
    search_window = tk.Toplevel()
    search_window.title("搜索窗口")
    search_window.geometry("500x500")

    search_label = tk.Label(search_window, text="请输入要搜索的数据：")
    search_label.pack()

    search_entry = tk.Entry(search_window)
    search_entry.pack()

    search_button = tk.Button(search_window, text="搜索", command=lambda: perform_search(search_entry.get()))
    search_button.place(relx=0.67, rely=0.03)

    data_frame = tk.Frame(search_window, width=300, height=500, bg="white")
    data_frame.pack()

    data_scrollbar = tk.Scrollbar(data_frame)
    data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    data_listbox = tk.Listbox(data_frame, yscrollcommand=data_scrollbar.set)
    data_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    sql = "SELECT COUNT(mid) FROM finance.manufacturers;"
    data1 = method.execute_fetchone_query(sql)
    data1 = data1[0]

    sql = "SELECT mname FROM finance.manufacturers"
    data2 = method.execute_fetchall_query(sql)



    for i in range(0, data1):
        x=data2[i][0]
        data_listbox.insert(tk.END, x)

    def perform_search(query):
        sql = "SELECT * FROM finance.manufacturers_view WHERE mname='" + str(query) + "';"
        date3 = method.execute_fetchone_query(sql)
        print(date3)
        if date3 == None:
            messagebox.showinfo("搜索结果", "搜索到不到相关的数据！")
        else:
            window = tk.Tk()
            window.title("游戏信息窗口")
            window.geometry("500x500")

            labels = ["厂商编号", "厂商名称","厂商账户", "厂商账户密码", "厂商官网", "收入", "厂商简介"]

            for i, label_text in enumerate(labels):
                label = tk.Label(window, text=label_text, anchor="w", width=15)
                label.grid(row=i, column=0, padx=10, pady=5)

                text = tk.Text(window, height=1, width=30, bg="white")
                text.grid(row=i, column=1, padx=10, pady=5)

                # 设置右边的文本框内容为"test"
                text.insert("1.0", date3[i])

            window.mainloop()

    def delete_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT mid FROM finance.manufacturers LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z2 = date3[0]

        sql = "DELETE FROM finance.manufacturers WHERE mid='" + z2 + "';"
        print(sql)
        date0 = method.execute_insert_query(sql)
        messagebox.showinfo("删除成功", "数据删除成功！")
        data_listbox.update()

    def modify_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT mid FROM finance.manufacturers LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z1 = date3[0]

        modify_window = tk.Toplevel(search_window)
        modify_window.title("修改数据")
        modify_window.geometry("300x300")

        # Create five entry fields for modification

        entry_label = tk.Label(modify_window, text="厂商名称")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 1), anchor=tk.CENTER)

        entry_field1 = tk.Entry(modify_window)
        entry_field1.place(relx=0.3, rely=0.2 + (0.1 * 1))

        entry_label = tk.Label(modify_window, text="厂商官网")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 2), anchor=tk.CENTER)

        entry_field2 = tk.Entry(modify_window)
        entry_field2.place(relx=0.3, rely=0.2 + (0.1 * 2))

        entry_label = tk.Label(modify_window, text="厂商收入")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 3), anchor=tk.CENTER)

        entry_field3 = tk.Entry(modify_window)
        entry_field3.place(relx=0.3, rely=0.2 + (0.1 * 3))

        def confirm_modification():
            x1 = entry_field1.get()
            x2 = entry_field2.get()
            x3 = entry_field3.get()
            sql = "UPDATE finance.manufacturers SET mname='" + x1 + "',official_web='" + x2 + "',income=" + x3 + " WHERE mid='" + z1 + "';"
            print(sql)
            date0 = method.execute_insert_query(sql)

            messagebox.showinfo("修改成功", "数据修改成功！")
            modify_window.destroy()

        confirm_button = tk.Button(modify_window, text="确认", command=confirm_modification)
        confirm_button.place(relx=0.4, rely=0.7)

        cancel_button = tk.Button(modify_window, text="取消", command=modify_window.destroy)
        cancel_button.place(relx=0.6, rely=0.7)

    modify_button = tk.Button(search_window, text="修改", command=modify_data)
    modify_button.pack()

    delete_button = tk.Button(search_window, text="删除", command=delete_data)
    delete_button.pack()


def open_search_window4():
    search_window = tk.Toplevel()
    search_window.title("搜索窗口")
    search_window.geometry("500x500")

    search_label = tk.Label(search_window, text="请输入要搜索的数据：")
    search_label.pack()

    search_entry = tk.Entry(search_window)
    search_entry.pack()

    search_button = tk.Button(search_window, text="搜索", command=lambda: perform_search(search_entry.get()))
    search_button.place(relx=0.67, rely=0.03)

    data_frame = tk.Frame(search_window, width=300, height=500, bg="white")
    data_frame.pack()

    data_scrollbar = tk.Scrollbar(data_frame)
    data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    data_listbox = tk.Listbox(data_frame, yscrollcommand=data_scrollbar.set)
    data_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    sql = "SELECT COUNT(goid) FROM finance.game_orders;"
    data1 = method.execute_fetchone_query(sql)
    data1 = data1[0]

    sql = "SELECT goid FROM finance.game_orders;"
    data2 = method.execute_fetchall_query(sql)


    for i in range(0, data1):
        x=data2[i][0]
        data_listbox.insert(tk.END, x)

    def perform_search(query):
        sql = "SELECT * FROM finance.order_view WHERE goid='" + str(query) + "';"
        date3 = method.execute_fetchone_query(sql)
        print(date3)
        if date3 == None:
            messagebox.showinfo("搜索结果", "搜索到不到相关的数据！")
        else:
            window = tk.Tk()
            window.title("订单信息窗口")
            window.geometry("500x500")

            labels = ["订单编号", "购买玩家名称", "游戏名称", "订单价格", "创建时间"]

            for i, label_text in enumerate(labels):
                label = tk.Label(window, text=label_text, anchor="w", width=15)
                label.grid(row=i, column=0, padx=10, pady=5)

                text = tk.Text(window, height=1, width=30, bg="white")
                text.grid(row=i, column=1, padx=10, pady=5)

                # 设置右边的文本框内容为"test"
                text.insert("1.0", date3[i])

            window.mainloop()

    def delete_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT goid FROM finance.game_orders LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z2 = date3[0]

        sql = "DELETE FROM finance.game_orders WHERE goid='" + z2 + "';"
        print(sql)
        date0 = method.execute_insert_query(sql)
        messagebox.showinfo("删除成功", "数据删除成功！")
        data_listbox.update()


    def modify_data():
        index = data_listbox.curselection()
        index = index[0]
        print(index)

        sql = "SELECT goid FROM finance.game_orders LIMIT " + str(index) + ",1;"
        date3 = method.execute_fetchone_query(sql)
        z1 = date3[0]

        modify_window = tk.Toplevel(search_window)
        modify_window.title("修改数据")
        modify_window.geometry("300x300")

        # Create five entry fields for modification

        entry_label = tk.Label(modify_window, text="订单编号")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 1), anchor=tk.CENTER)

        entry_field1 = tk.Entry(modify_window)
        entry_field1.place(relx=0.3, rely=0.2 + (0.1 * 1))

        entry_label = tk.Label(modify_window, text="订单价格")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 2), anchor=tk.CENTER)

        entry_field2 = tk.Entry(modify_window)
        entry_field2.place(relx=0.3, rely=0.2 + (0.1 * 2))

        entry_label = tk.Label(modify_window, text="创建日期")
        entry_label.place(relx=0.2, rely=0.2 + (0.1 * 3), anchor=tk.CENTER)

        entry_field3 = tk.Entry(modify_window)
        entry_field3.place(relx=0.3, rely=0.2 + (0.1 * 3))

        def confirm_modification():
            x1 = entry_field1.get()
            x2 = entry_field2.get()
            x3 = entry_field3.get()
            sql = "UPDATE finance.game_orders SET goid='" + x1 + "',price=" + x2 + ",creation_time='" + x3 + "' WHERE goid='" + z1 + "';"
            print(sql)
            date0 = method.execute_insert_query(sql)

            messagebox.showinfo("修改成功", "数据修改成功！")
            modify_window.destroy()

        confirm_button = tk.Button(modify_window, text="确认", command=confirm_modification)
        confirm_button.place(relx=0.4, rely=0.7)

        cancel_button = tk.Button(modify_window, text="取消", command=modify_window.destroy)
        cancel_button.place(relx=0.6, rely=0.7)

    modify_button = tk.Button(search_window, text="修改", command=modify_data)
    modify_button.pack()

    delete_button = tk.Button(search_window, text="删除", command=delete_data)
    delete_button.pack()


def open_main1_window():
    root1 = tk.Tk()
    root1.title("管理员界面")
    root1.geometry("500x500")

    welcome_label = tk.Label(root1, text="欢迎回来！管理员", font=("Arial", 20))
    welcome_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Create four buttons
    buttons = ["管理游戏", "管理玩家", "管理厂商", "管理订单"]

    button = tk.Button(root1, text="管理游戏", command=open_search_window1)
    button.place(relx=0.5, rely=0.3 + 1 * 0.1, anchor=tk.CENTER)

    button = tk.Button(root1, text="管理玩家", command=open_search_window2)
    button.place(relx=0.5, rely=0.3 + 2 * 0.1, anchor=tk.CENTER)

    button = tk.Button(root1, text="管理厂商", command=open_search_window3)
    button.place(relx=0.5, rely=0.3 + 3 * 0.1, anchor=tk.CENTER)

    button = tk.Button(root1, text="管理订单", command=open_search_window4)
    button.place(relx=0.5, rely=0.3 + 4 * 0.1, anchor=tk.CENTER)

    root1.mainloop()


if __name__ =="__main__":# Start the application by opening the main window
 open_main1_window()