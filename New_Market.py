import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import method
import login
import UserUi


class GameListWindow:
    def __init__(self, root):
        # self.user_id = tk.StringVar()
        self.root = root
        self.root.title("游戏列表")
        self.root.geometry("400x300")

        # 创建 Listbox
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 添加游戏数据到 Listbox
        self.display_game_list()

        # 添加选择按钮
        self.select_button = tk.Button(root, text="选择", command=self.show_selected_game)
        self.select_button.pack(pady=10)

        # 添加用户信息按钮
        self.user_info_button = tk.Button(root, text="用户信息", command=self.show_user_info)
        self.user_info_button.pack(pady=10)

    def display_game_list(self):
        """在 Listbox 中显示游戏列表"""
        # 从数据库获取游戏数据
        sql = "SELECT gname FROM finance.games;"
        games = method.execute_fetchall_query(sql)

        # 在 Listbox 中添加游戏名称
        for game in games:
            self.listbox.insert(tk.END, game[0])

    def show_selected_game(self):
        # 获取选中的游戏名称
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_game_name = self.listbox.get(selected_index)
            # 创建新窗口显示订单信息
            self.show_order_info(selected_game_name)
        else:
            messagebox.showwarning("警告", "请先选择一个游戏。")

    def show_order_info(self, game_name):
        # 计算订单号（示例中使用计数器，您可能需要根据实际需求修改）
        order_id = self.calculate_order_id()

        # 获取游戏信息
        game_info = self.get_game_info(game_name)

        # 创建新窗口
        order_window = tk.Toplevel(self.root)
        order_window.title("订单信息")

        # 显示订单信息
        tk.Label(order_window, text=f"订单号: {order_id}").pack()
        tk.Label(order_window, text=f"游戏名称: {game_info['gname']}").pack()
        tk.Label(order_window, text=f"厂商: {game_info['publisher']}").pack()
        tk.Label(order_window, text=f"游戏价格: {game_info['price']}").pack()
        tk.Label(order_window, text=f"目前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").pack()

        # 添加购买和取消按钮
        buy_button = tk.Button(order_window, text="购买", command=lambda: self.buy_game(game_info))
        buy_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(order_window, text="取消", command=order_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def calculate_order_id(self):
        # 这里使用简单的计数器，您可能需要根据实际需求进行调整
        if not hasattr(GameListWindow, 'order_id_counter'):
            GameListWindow.order_id_counter = 0
        GameListWindow.order_id_counter += 1
        return GameListWindow.order_id_counter

    def get_game_info(self, game_name):
        # 从数据库获取游戏信息
        sql = "SELECT * FROM finance.games WHERE gname = %s;"
        params = (game_name,)
        game_info = method.execute_fetchone_query(sql, params)
        return {
            'gname': game_info[1],
            'publisher': game_info[4],
            'price': game_info[2],
            'gid': game_info[0]
        }
    
    def buy_game(self, game_info):
        # 获取玩家ID（示例中使用固定ID，您需要根据实际情况获取）
        user_id = login.get_player_id()

        # 从数据库获取玩家余额
        sql_get_balance = "SELECT account_balance FROM finance.players WHERE pid = %s;"
        balance_result = method.execute_fetchone_query(sql_get_balance, (user_id,))

        # 检查余额是否足够购买游戏
        if balance_result is not None:
             
            balance = balance_result[0]

            if balance >= game_info['price']:
                # 扣除玩家余额
                new_balance = balance - game_info['price']
                sql_update_balance = "UPDATE finance.players SET account_balance = %s WHERE pid = %s;"
                method.execute_insert_query(sql_update_balance, (new_balance, user_id))

                # 增加厂商余额
                sql_get_mid = "SELECT mid FROM finance.games WHERE gid = %s;"
                mid = method.execute_fetchone_query(sql_get_mid, (game_info['gid'],))[0]
                mid = int(mid)
                sql = "update finance.manufacturers set income = income + %s where mid = %s;"
                method.execute_insert_query(sql, (game_info['price'], mid))

                # 向玩家游戏列表中添加游戏
                buy_time = datetime.now().strftime('%Y-%m-%d')
                sql_add_game = "INSERT INTO finance.game_library (pid, gid, storage_time) VALUES (%s, %s, %s);"
                method.execute_insert_query(sql_add_game, (user_id, game_info['gid'], buy_time))

                messagebox.showinfo("购买成功", f"您成功购买了游戏: {game_info['gname']}")
            else:
                messagebox.showwarning("余额不足", "您的余额不足以购买此游戏。")
        else:
         messagebox.showerror("错误", "无法获取玩家余额信息。")


    def show_user_info(self):
        # 打开用户信息窗口
        user = login.get_player_id()[0]
        print(user)
        user_info_window = tk.Toplevel()
        user_info_window = UserUi.UserProfileUI(user_info_window, user_id=user)
           

            
# # 创建主窗口
# root = tk.Tk()
# # 创建 GameListWindow 类的实例
# game_list_window = GameListWindow(root)
# # 运行主循环
# root.mainloop()
