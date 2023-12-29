import tkinter as tk
from tkinter import messagebox
import psycopg2

class GameInfoApp:
    def __init__(self, root, game_id):
        self.root = root
        self.root.title("游戏资讯界面")

        # 游戏信息
        self.game_id = game_id
        self.game_name = tk.StringVar()
        self.game_intro = tk.StringVar()
        self.game_price = tk.StringVar()
        self.user_rating = tk.StringVar()

        # 标签和输入框
        label_game_name = tk.Label(root, text="游戏名字:")
        label_game_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_game_name = tk.Entry(root, textvariable=self.game_name, state='readonly')
        entry_game_name.grid(row=0, column=1, padx=10, pady=10)

        label_game_intro = tk.Label(root, text="游戏介绍:")
        label_game_intro.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_game_intro = tk.Entry(root, textvariable=self.game_intro, state='readonly')
        entry_game_intro.grid(row=1, column=1, padx=10, pady=10)

        label_game_price = tk.Label(root, text="游戏价格:")
        label_game_price.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_game_price = tk.Entry(root, textvariable=self.game_price, state='readonly')
        entry_game_price.grid(row=2, column=1, padx=10, pady=10)

        label_user_rating = tk.Label(root, text="用户评分:")
        label_user_rating.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_user_rating = tk.Entry(root, textvariable=self.user_rating, state='readonly')
        entry_user_rating.grid(row=3, column=1, padx=10, pady=10)

        # 初始化游戏信息
        self.show_game_info()

    def connect_to_database(self):
        """
        连接到数据库并返回连接对象和游标对象
        """
        db_config = {
            'host': 'localhost',
            'database': 'your_database',
            'user': 'your_user',
            'password': 'your_password',
            'port': 'your_port'
        }
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        return connection, cursor

    def close_database_connection(self, connection, cursor):
        """
        关闭数据库连接和游标对象
        """
        cursor.close()
        connection.close()

    def execute_query(self, query, params=None):
        """
        执行数据库查询
        """
        connection, cursor = self.connect_to_database()
        cursor.execute(query, params)
        result = cursor.fetchone()
        self.close_database_connection(connection, cursor)
        return result

    def show_game_info(self):
        # 连接到数据库
        query = "SELECT * FROM your_game_table WHERE game_id = %s"  # 替换为实际的表和字段名
        game_data = self.execute_query(query, (self.game_id,))  # 替换为实际的游戏ID

        if game_data:
            self.game_name.set(game_data[1])  # 假设游戏名字是第二列
            self.game_intro.set(game_data[2])  # 假设游戏介绍是第三列
            self.game_price.set(game_data[3])  # 假设游戏价格是第四列
            self.user_rating.set(game_data[4])  # 假设用户评分是第五列

if __name__ == "__main__":
    root = tk.Tk()
    game_info_app = GameInfoApp(root, game_id=1)  # 替换为实际的游戏ID
    root.mainloop()
