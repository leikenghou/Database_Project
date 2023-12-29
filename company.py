import tkinter as tk
from tkinter import messagebox
import method

class ManufacturerProfileUI:
    def __init__(self, root, manufacturer_id):
        self.root = root
        self.root.title("厂商个人信息界面")

        # 厂商信息
        self.manufacturer_id = tk.StringVar()
        self.manufacturer_name = tk.StringVar()
        self.official_web = tk.StringVar()
        self.income = tk.StringVar()
        self.manufacturers_profile = tk.StringVar()
        self.published_games = tk.Listbox(root, selectmode=tk.SINGLE, exportselection=0)

        # 初始化厂商ID（不可修改）
        self.manufacturer_id.set(manufacturer_id)

        # 查询并展示厂商信息
        self.show_manufacturer_info()

        # 标签和输入框
        label_id = tk.Label(root, text="厂商ID:")
        label_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_id = tk.Entry(root, textvariable=self.manufacturer_id, state='readonly')
        entry_id.grid(row=0, column=1, padx=10, pady=10)

        label_name = tk.Label(root, text="厂商名字:")
        label_name.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_name = tk.Entry(root, textvariable=self.manufacturer_name)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        label_web = tk.Label(root, text="厂商官网:")
        label_web.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_web = tk.Entry(root, textvariable=self.official_web)
        entry_web.grid(row=2, column=1, padx=10, pady=10)

        label_income = tk.Label(root, text="厂商收入:")
        label_income.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_income = tk.Entry(root, textvariable=self.income, state='readonly')
        entry_income.grid(row=3, column=1, padx=10, pady=10)

        label_profile = tk.Label(root, text="厂商公司简介:")
        label_profile.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_profile = tk.Entry(root, textvariable=self.manufacturers_profile)
        entry_profile.grid(row=4, column=1, padx=10, pady=10)

        label_games = tk.Label(root, text="发行的游戏:")
        label_games.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.published_games.grid(row=5, column=1, padx=10, pady=10)

        # 按钮
        button_save = tk.Button(root, text="保存", command=self.save_manufacturer_info)
        button_save.grid(row=6, column=0, pady=20)

        button_remove_game = tk.Button(root, text="下架游戏", command=self.remove_published_game)
        button_remove_game.grid(row=6, column=1, pady=20)

        button_add_game = tk.Button(root, text="发行新游戏", command=self.launch_add_game_window)
        button_add_game.grid(row=7, column=0, columnspan=2, pady=20)

    def show_manufacturer_info(self):
        """
        展示厂商信息
        """
        # 查询厂商信息
        manufacturer_id = self.manufacturer_id.get()
        sql = "SELECT * FROM finance.manufacturers WHERE mid = %s;"
        manufacturer_data = method.execute_fetchone_query(sql, (manufacturer_id,))

        if manufacturer_data:
            self.manufacturer_id.set(manufacturer_data[0])
            self.manufacturer_name.set(manufacturer_data[1])
            self.official_web.set(manufacturer_data[2])
            self.income.set(manufacturer_data[3])
            self.manufacturers_profile.set(manufacturer_data[4])

            # 查询厂商发行的游戏
            game_sql = "SELECT gname FROM finance.manufacturers_games WHERE mid = %s;"
            published_games_data = method.execute_fetchall_query(game_sql, (manufacturer_id,))

            for game in published_games_data:
                self.published_games.insert(tk.END, game[0])

    def save_manufacturer_info(self):
        """
        保存厂商信息
        """
        # 更新厂商信息
        manufacturer_id = self.manufacturer_id.get()
        manufacturer_name = self.manufacturer_name.get()
        official_web = self.official_web.get()
        manufacturers_profile = self.manufacturers_profile.get()

        # 将修改后的厂商信息写入数据库
        sql = "UPDATE finance.manufacturers SET mname = %s, official_web = %s, manufacturers_profile = %s WHERE mid = %s;"
        method.execute_insert_query(sql, (manufacturer_name, official_web, manufacturers_profile, manufacturer_id))

        messagebox.showinfo("保存成功", "厂商信息保存成功！")

    def remove_published_game(self):
        """
        下架游戏操作
        """
        selected_game_index = self.published_games.curselection()
        if selected_game_index:
            selected_game = self.published_games.get(selected_game_index)

            # 弹出确定视窗
            result = messagebox.askquestion("下架游戏", f"确定下架游戏：{selected_game}？")

            if result == 'yes':
                # 从厂商发行的游戏列表中移除游戏
                self.published_games.delete(selected_game_index)
                
                # 获取厂商ID
                manufacturer_id = self.manufacturer_id.get()

                # 从数据库中删除游戏数据
                game_sql = "DELETE FROM finance.games WHERE mid = %s AND gname = %s   ;"
                method.execute_insert_query(game_sql, (manufacturer_id, selected_game))

                messagebox.showinfo("下架成功", f"成功下架游戏：{selected_game}")   
            else:
                messagebox.showinfo("取消操作", "取消下架游戏")

        else:
            messagebox.showwarning("下架失败", "请选择要下架的游戏！")


    def launch_add_game_window(self):
        """
        打开发行新游戏的窗口
        """
        add_game_window = tk.Toplevel(self.root)
        add_game_window.title("发行新游戏")

        # 标签和输入框
        label_name = tk.Label(add_game_window, text="游戏名字:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_name = tk.Entry(add_game_window)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        label_price = tk.Label(add_game_window, text="游戏价格:")
        label_price.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_price = tk.Entry(add_game_window)
        entry_price.grid(row=1, column=1, padx=10, pady=10)

        label_release_date = tk.Label(add_game_window, text="发行时间:")
        label_release_date.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_release_date = tk.Entry(add_game_window)
        entry_release_date.grid(row=2, column=1, padx=10, pady=10)

        label_publisher = tk.Label(add_game_window, text="发行商:")
        label_publisher.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_publisher = tk.Entry(add_game_window)
        entry_publisher.grid(row=3, column=1, padx=10, pady=10)

        label_discount = tk.Label(add_game_window, text="折扣:")
        label_discount.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_discount = tk.Entry(add_game_window)
        entry_discount.grid(row=4, column=1, padx=10, pady=10)

        label_profile = tk.Label(add_game_window, text="游戏简介:")
        label_profile.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        entry_profile = tk.Entry(add_game_window)
        entry_profile.grid(row=5, column=1, padx=10, pady=10)

        # 保存按钮
        button_save = tk.Button(add_game_window, text="保存", command=lambda: self.save_new_game(add_game_window,
                                                                                               entry_name.get(),
                                                                                               entry_price.get(),
                                                                                               entry_release_date.get(),
                                                                                               entry_publisher.get(),
                                                                                               entry_discount.get(),
                                                                                               entry_profile.get()))
        button_save.grid(row=6, column=0, columnspan=2, pady=20)

    def save_new_game(self, add_game_window, gname, price, release_date, publisher, discount, game_profile):
        """
        保存新游戏信息到数据库
        """
        # 获取厂商ID
        manufacturer_id = self.manufacturer_id.get()

        # 将新游戏信息写入数据库
        sql = "SELECT MAX(gid) FROM finance.games;"
        gid = method.execute_fetchone_query(sql)[0]
        if gid == None:
            gid = 1
        else:
            gid = int(method.execute_fetchone_query(sql)[0].strip()) + 1

        # 转换为char类型
        gid = str(gid)
        print(gid)
        sql = "INSERT INTO finance.games (gid, gname, price, release_date, publisher, discount, game_profile, mid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        
        method.execute_insert_query(sql, (gid, gname, price, release_date, publisher, discount, game_profile, manufacturer_id))

        # 刷新发行的游戏列表
        self.refresh_published_games()

        # 关闭添加游戏的窗口
        add_game_window.destroy()

    def refresh_published_games(self):
        """
        刷新发行的游戏列表
        """
        # 清空游戏列表
        self.published_games.delete(0, tk.END)

        # 查询厂商发行的游戏
        manufacturer_id = self.manufacturer_id.get()
        game_sql = "SELECT gname FROM finance.manufacturers_games WHERE mid = %s;"
        published_games_data = method.execute_fetchall_query(game_sql, (manufacturer_id,))
        print(published_games_data)

        for game in published_games_data:
            # 将游戏名称添加到游戏列表中
            self.published_games.insert(tk.END, game[0])



# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ManufacturerProfileUI(root, manufacturer_id="1")
#     root.mainloop()
