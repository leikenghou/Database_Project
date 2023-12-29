import tkinter as tk
from tkinter import messagebox
import method
import login

class UserProfileUI:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("用户个人信息界面")

        # 用户信息
        self.user_id = tk.StringVar()
        self.user_name = tk.StringVar()
        self.user_email = tk.StringVar()
        self.user_balance = tk.StringVar()
        self.user_profile = tk.StringVar()
        self.owned_games = tk.Listbox(root, selectmode=tk.SINGLE, exportselection=0)

        # 初始化用户ID（不可修改）
        self.user_id.set(user_id)

        # 查询并展示用户信息
        self.show_user_info()

        # 标签和输入框
        label_id = tk.Label(root, text="用户ID:")
        label_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_id = tk.Entry(root, textvariable=self.user_id, state='readonly')
        entry_id.grid(row=0, column=1, padx=10, pady=10)

        label_name = tk.Label(root, text="用户名字:")
        label_name.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_name = tk.Entry(root, textvariable=self.user_name)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        label_email = tk.Label(root, text="用户Email:")
        label_email.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_email = tk.Entry(root, textvariable=self.user_email)
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        label_balance = tk.Label(root, text="用户余额:")
        label_balance.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_balance = tk.Entry(root, textvariable=self.user_balance, state='readonly')
        entry_balance.grid(row=3, column=1, padx=10, pady=10)

        label_profile = tk.Label(root, text="用户个人简介:")
        label_profile.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_profile = tk.Entry(root, textvariable=self.user_profile)
        entry_profile.grid(row=4, column=1, padx=10, pady=10)

        label_games = tk.Label(root, text="拥有的游戏:")
        label_games.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.owned_games.grid(row=5, column=1, padx=10, pady=10)

        # 按钮
        button_save = tk.Button(root, text="保存", command=self.save_user_info)
        button_save.grid(row=6, column=0, pady=20)

        button_refund = tk.Button(root, text="退款", command=self.process_refund)
        button_refund.grid(row=6, column=1, pady=20)

        button_charge = tk.Button(root, text="充值", command=self.charge)
        button_charge.grid(row=6, column=2, pady=20)

        self.root.mainloop()

    def show_user_info(self):
        """
        展示用户信息
        """
        # 清空游戏列表
        self.owned_games.delete(0, tk.END)

        # 查询用户信息
        user_id = self.user_id.get()
        sql = "SELECT * FROM finance.players WHERE pid = %s;"
        user_data = method.execute_fetchone_query(sql, (user_id,))

        if user_data:
            self.user_id.set(user_data[0])
            self.user_name.set(user_data[1])
            self.user_email.set(user_data[2])
            self.user_balance.set(user_data[3])
            self.user_profile.set(user_data[4])

            # 查询用户拥有的游戏
            game_sql = "SELECT gname FROM finance.player1_games WHERE pid = %s;"
            owned_games_data = method.execute_fetchall_query(game_sql, (user_id,))

            for game in owned_games_data:
                self.owned_games.insert(tk.END, game[0])

    def save_user_info(self):
        """
        保存用户信息
        """
        # 更新用户信息
        user_id = self.user_id.get()
        user_name = self.user_name.get()
        user_email = self.user_email.get()
        user_profile = self.user_profile.get()

        user_id = user_id[0]
        user_id = str(user_id)
        user_id = user_id.strip()
        print(user_id)

        # 将修改后的用户信息写入数据库
        sql = "UPDATE finance.players SET pname = %s, email = %s, personal_profile = %s WHERE pid = %s;"
        method.execute_insert_query(sql, (user_name, user_email, user_profile, user_id))

        # 刷新用户信息
        self.show_user_info()

        messagebox.showinfo("保存成功", "用户信息保存成功！")

    def process_refund(self):
        selected_game_index = self.owned_games.curselection()
        s = selected_game_index[0]
        sql1="SELECT gid FROM finance.game_library WHERE pid = %s LIMIT %s,1;"
        gid_sql2 = method.execute_fetchone_query(sql1, (self.user_id.get(), s))
        gid_sql2 = gid_sql2[0]
        # 去掉字符串中的空格
        gid_sql2 = gid_sql2.strip()
        sql2="select price from finance.games where gid = %s;"
        gid_sql3 = method.execute_fetchone_query(sql2, (gid_sql2,))
        if selected_game_index:
            selected_game = self.owned_games.get(selected_game_index)

            # Ask for confirmation before refunding
            result = messagebox.askquestion("确认退款", f"确定退款游戏：{selected_game}？")

            if result == 'yes':
                

                # Remove the game from the list
                self.owned_games.delete(selected_game_index)

                # Add your database deletion logic here
                user_id = self.user_id.get()
                gid_sql = "SELECT gid FROM finance.game_library WHERE pid = %s;"
                method.execute_insert_query(gid_sql, (user_id,))
                game_sql = "DELETE FROM finance.game_library WHERE pid = %s AND gid = %s;"
                method.execute_insert_query(game_sql, (user_id, gid_sql2))
                
                moneyback = gid_sql3[0]
                sql3="update finance.players set account_balance = account_balance + %s where pid = %s;"
                method.execute_insert_query(sql3, (moneyback, user_id))

                # 减少厂商余额
                sql_get_mid = "SELECT mid FROM finance.games WHERE gid = %s;"
                mid = method.execute_fetchone_query(sql_get_mid, gid_sql2)[0]
                mid = int(mid)
                sql = "update finance.manufacturers set income = income - %s where mid = %s;"
                method.execute_insert_query(sql, (moneyback, mid))

                # refresh the user info
                self.show_user_info()
                
                # Refund logic here
                messagebox.showinfo("退款成功", f"成功退款游戏：{selected_game}")
            
            else:
                messagebox.showinfo("取消操作", "取消退款")

        else:
            messagebox.showwarning("退款失败", "请选择要退款的游戏！")

    def charge(self):
        """
        充值
        """
        # 弹出充值窗口
        charge_window = tk.Toplevel()
        charge_window.title("充值")
        charge_window.geometry("300x100")
        charge_window.resizable(0, 0)
        
        # 充值金额输入框
        entry_amount = tk.Entry(charge_window)
        entry_amount.pack(pady=10)

        def confirm_charge():
            # 获取充值金额
            amount = entry_amount.get()

            # 检查输入的是否是数字
            try:
                amount = int(amount)
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字金额。")
                return

            # 获取玩家ID（示例中使用固定ID，您需要根据实际情况获取）
            user_id = login.get_player_id()[0]

            # 更新数据库中的账户余额
            sql = "UPDATE finance.players SET account_balance = account_balance + %s WHERE pid = %s;"
            method.execute_insert_query(sql, (amount, user_id))

            # 刷新用户信息
            self.show_user_info()

            messagebox.showinfo("充值成功", f"成功充值 {amount} 元。")

        # 确定按钮
        button_confirm = tk.Button(charge_window, text="确定", command=confirm_charge)
        button_confirm.pack(pady=10)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UserProfileUI(root, user_id="1")
#     root.mainloop()
