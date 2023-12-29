import psycopg2

# 全局变量，用于保存数据库连接
db_connection = None

# 数据库连接信息
db_config = {
    'host': '172.20.10.3',
    'database': 'finance',
    'user': 'gaussdb',
    'password': 'Enmo@123',
    'port': '5432'
}

def create_connection():
    """
    创建数据库连接
    """
    try:
        connection = psycopg2.connect(**db_config)
        print("Database connection successful")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def initialize_database():
    """
    初始化数据库
    """
    global db_connection
    db_connection = create_connection()


def close_database():
    """
    关闭数据库
    """
    global db_connection
    if db_connection:
        db_connection.close()


# 初始化数据库
initialize_database()


def execute_fetchone_query(query, params=None):
    """
    查询一行
    :param query:
    :param params:
    :return: 返回一行数据
    """
    # 创建 cursor 对象
    with db_connection.cursor() as cursor:
        # 执行查询
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # 获取第一行数据
        row = cursor.fetchone()

    # 返回结果
    return row


def execute_insert_query(query, params=None):
    """
    向数据库插入数据。

    参数：
    - query (str): 要执行的 SQL INSERT 查询。
    - params (tuple, 可选): 包含插入数据的参数值的元组，默认为 None。

    返回：
    无返回值。

    示例：
    ```python
    execute_insert_query("INSERT INTO your_table (column1, column2) VALUES (%s, %s);", (value1, value2))
    ```

    注意：
    - 如果查询中有占位符，请使用 `params` 参数安全地传递参数值。
    - 插入操作后必须调用 `db_connection.commit()` 提交事务，以保存更改到数据库。
    """
    db_connection = create_connection()

    # 创建游标对象
    with db_connection.cursor() as cursor:
        try:
            # 执行插入
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        except Exception as e:
            # 处理异常
            print(f"插入数据时出错: {e}")
            raise

    # 提交事务
    db_connection.commit()
    print("Transaction committed successfully")

    


def execute_fetchall_query(query, params=None):
    """
    执行 SQL SELECT 查询并检索结果中的所有行。

    参数：
    - query (str): 要执行的 SQL SELECT 查询。
    - params (tuple, 可选): 包含查询参数值的元组，默认为 None。

    返回：
    list of tuple: 包含查询结果中所有行的列表。

    示例：
    ```python
    result = execute_fetchall_query("SELECT * FROM your_table WHERE column1 = %s;", (value,))
    for row in result:
        print(row)
    ```

    注意：
    如果查询中有占位符，请使用 `params` 参数安全地传递参数值。
    """

    # 创建游标对象
    with db_connection.cursor() as cursor:
        try:
            # 执行查询
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # 获取所有行的数据
            result = cursor.fetchall()
        except Exception as e:
            # 处理异常
            print(f"执行查询时出错: {e}")
            result = None
            raise

    # 返回结果
    return result

def update_user_balance(user_id, amount):
    """
    更新用户余额
    :param user_id: 用户 ID
    :param amount: 更新的金额
    """
    # 查询用户余额
    sql = "SELECT account_balance FROM finance.players WHERE pid = %s;"
    current_balance = execute_fetchone_query(sql, (user_id,))[0]

    # 计算新的余额
    new_balance = current_balance + amount

    # 更新用户余额
    sql = "UPDATE finance.players SET account_balance = %s WHERE pid = %s;"
    execute_insert_query(sql, (new_balance, user_id))

def CheckDatabasePlayerNumber():
    """
    查找数据库id最大值
    """
    sql = "SELECT MAX(pid) FROM finance.players_account;"
    max_id = execute_fetchone_query(sql)[0]
    return int(max_id)

def CheckDatabaseVendorNumber():
    """
    查找厂商id最大值
    """
    sql = "SELECT MAX(mid) FROM finance.manufacturers_account;"
    max_id = execute_fetchone_query(sql)[0]
    return int(max_id)