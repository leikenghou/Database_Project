# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import method
import New_Market
import ck
import company
# 连接到数据库
method.initialize_database()

# 检查用户是否存在的方法
def check_user_exists(username):
    query = "SELECT * FROM finance.players_account WHERE paccount=%s;"
    result = method.execute_fetchone_query(query, (username,))
    return result is not None
def login():
    username = entry_username.get()
    password = entry_password.get()
    if (username=='admin') and (password=='admin'):
        ck.open_main1_window()
    else:
     matched_user=check_user_exists(username)

     if matched_user:
        # 验证用户密码是否匹配
        query = "SELECT * FROM finance.players_account WHERE paccount=%s AND ppassword=%s;"
        result = method.execute_fetchone_query(query, (username, password))

        if result:
            messagebox.showinfo("登录成功", "欢迎回来，" + username + "!")
            # 创建一个新的Toplevel窗口用于市场页面
            market_window = tk.Toplevel(root)
            market_window.title("游戏商城")
            market_page = New_Market.GameListWindow(market_window)
            market_window.mainloop()
        else:
            messagebox.showerror("登录失败", "用户名或密码不正确")

     else:
        messagebox.showerror("登录失败", "用户名或密码不正确")

def register():
    username = entry_username.get()
    password = entry_password.get()

    existing_user = check_user_exists(username)

    if existing_user:
        messagebox.showwarning("注册失败", "用户名已存在，请选择其他用户名！")
    else:
        # 使用 askstring 弹出对话框，获取玩家信息
        pname = simpledialog.askstring("玩家信息", "请输入您的姓名:")
        email = simpledialog.askstring("玩家信息", "请输入您的邮箱:")
        personal_profile = simpledialog.askstring("玩家信息", "请输入您的个人简介:")
        pid = int(method.CheckDatabasePlayerNumber()) + 1
        pid = str(pid)

         # 执行插入操作
        query = "INSERT INTO finance.players_account (pid, paccount, ppassword) VALUES (%s, %s, %s);"
        params = (pid, username, password)
        method.execute_insert_query(query, params)

        query = "INSERT INTO finance.players (pid, pname, email, account_balance, personal_profile) VALUES (%s, %s, %s, %s, %s);"
        account_balance = 0
        params = (pid, pname, email, account_balance,personal_profile)
        method.execute_insert_query(query, params)

       
        # player 也要增加 pid
        sql = "INSERT INTO finance.players (pid) VALUES (%s);"
        method.execute_insert_query(sql, (pid,))

        # 提示用户注册成功
        messagebox.showinfo("注册成功", "账户 " + username + " 注册成功!")

def check_vendor_exists(maccount):
    '''
    检查厂商是否存在
    :param vendor_name: 厂商名称
    :return: 如果厂商存在，返回True，否则返回False
    '''
    query = "SELECT * FROM finance.manufacturers_account WHERE maccount=%s;"
    result = method.execute_fetchone_query(query, (maccount,))
    return result is not None

def vendor_register():
    '''
    厂商注册
    '''
    maccount = entry_username.get()
    vendor_password = entry_password.get()

    existing_vendor=check_vendor_exists(maccount)

    if existing_vendor:
        messagebox.showwarning("注册失败", "厂商已存在，请选择其他厂商名称！")
    else:
        # 使用 askstring 弹出对话框，获取厂商信息
        mname = simpledialog.askstring("厂商信息", "请输入厂商名称:")
        official_web = simpledialog.askstring("厂商信息", "请输入厂商官网:")
        manufacturers_profile = simpledialog.askstring("厂商信息", "请输入厂商简介:")
        mid = method.CheckDatabaseVendorNumber() + 1
        mid = str(mid)

        # 优先插入到manufacturers表中
        income = 0
        sql = "INSERT INTO finance.manufacturers (mid, mname, official_web, income, manufacturers_profile) VALUES (%s, %s, %s, %s, %s);"
        method.execute_insert_query(sql, (mid,mname,official_web,income,manufacturers_profile))


        # 插入到manufacturers_account表中
        query = "INSERT INTO finance.manufacturers_account (mid, maccount, mpassword) VALUES (%s, %s, %s);"
        params = (mid, maccount, vendor_password)
        method.execute_insert_query(query, params)

       
        # 提示厂商注册成功
        messagebox.showinfo("注册成功", "厂商 " + maccount + " 注册成功!")

def vendor_login():
    '''
    厂商登录
    '''
    m_account = entry_username.get()
    m_password = entry_password.get()

    matched_vendor=check_vendor_exists(m_account)

    if matched_vendor:
        # 验证厂商密码是否匹配
        query = "SELECT * FROM finance.manufacturers_account WHERE maccount=%s AND mpassword=%s;"
        result = method.execute_fetchone_query(query, (m_account, m_password))

        if result:
            messagebox.showinfo("登录成功", "欢迎回来，" + m_account + "!")
            # 创建一个新的Toplevel窗口用于厂商资讯页面
            company_window = tk.Toplevel(root)
            company_window.title("厂商讯息")
            m_id = get_vendor_id()
            company_page = company.ManufacturerProfileUI(company_window, m_id)
            company_window.mainloop()

        else:
            messagebox.showerror("登录失败", "用户名或密码不正确")

    else:
        messagebox.showerror("登录失败", "用户名或密码不正确")

def get_player_id():
    """
    获取玩家 ID
    """
    pname = entry_username.get()
    sql = "Select pid FROM finance.players_account where paccount = %s;"
    player_id = method.execute_fetchone_query(sql, (pname,))
    return player_id

def get_vendor_id():
    """
    获取厂商 ID
    """
    # 从数据库获取厂商数据
    sql = "SELECT * FROM finance.manufacturers_account where maccount=%s;"
    vendor_id = method.execute_fetchone_query(sql, (entry_username.get(),))
    vendor_id = vendor_id[0]
    vendor_id = str(vendor_id)
    return vendor_id


# 创建主窗口
root = tk.Tk()
root.title("用户登录界面")

# 创建用户名标签和输入框
label_username = tk.Label(root, text="用户名:", font=('Arial', 16))
label_username.grid(row=0, column=0, padx=70, pady=10, sticky="e")
entry_username = tk.Entry(root, width=20, font=('Arial', 16))
entry_username.grid(row=0, column=1, padx=10, pady=10)

# 创建密码标签和输入框
label_password = tk.Label(root, text="密码:", font=('Arial', 16))
label_password.grid(row=1, column=0, padx=70, pady=10, sticky="e")
entry_password = tk.Entry(root, show="*", width=20, font=('Arial', 16))
entry_password.grid(row=1, column=1, padx=10, pady=10)

# 创建登录按钮
button_login = tk.Button(root, text="登录", command=login, font=('Arial', 16), width=20, height=2)
button_login.grid(row=2, column=0, pady=20, sticky='ew')

# 创建注册按钮
button_register = tk.Button(root, text="注册", command=register, font=('Arial', 16), width=20, height=2)
button_register.grid(row=3, column=0, pady=10, sticky='ew')

# 创建厂商注册按钮
button_vendor_register = tk.Button(root, text="厂商注册", command=vendor_register, font=('Arial', 16), width=20, height=2)
button_vendor_register.grid(row=3, column=1, pady=5, sticky='ew')

# 创建厂商登录按钮
button_vendor_login = tk.Button(root, text="厂商登录",command=vendor_login, font=('Arial', 16), width=20, height=2)
button_vendor_login.grid(row=2, column=1, pady=5, sticky='ew')
# 运行主循环

root.mainloop()
