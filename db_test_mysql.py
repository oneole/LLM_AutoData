import mysql.connector
import os

# --- 配置数据库连接信息 ---
# 建议使用环境变量来存储敏感信息，例如：
# export DB_HOST='your_host'
# export DB_USER='your_user'
# export DB_PASSWORD='your_password'
# export DB_NAME='your_database'
#
# 如果不使用环境变量，请直接替换下面的占位符值。

# 替换 'localhost' 为您的 MySQL 主机名或 IP 地址
db_host = os.getenv('DB_HOST', '152.136.150.40')    #端口3306
db_user = os.getenv('DB_USER', 'llmauto')       # 替换 'root' 为您的 MySQL 用户名
# 替换 'your_password' 为您的 MySQL 密码
db_password = os.getenv('DB_PASSWORD', 'mariadb_zMWZZk')
db_name = os.getenv('DB_NAME', None)         # 可选：替换 None 为您要连接的特定数据库名称

# --- 尝试连接 ---
connection = None
try:
    print(f"正在尝试连接到 MySQL 主机: {db_host}...")
    connection_config = {
        'host': db_host,
        'user': db_user,
        'password': db_password,
        'connect_timeout': 5  # 设置连接超时时间（秒）
    }
    # 如果指定了数据库名称，则添加到配置中
    if db_name:
        connection_config['database'] = db_name
        print(f"目标数据库: {db_name}")

    connection = mysql.connector.connect(**connection_config)

    if connection.is_connected():
        print("\033[92m连接成功！\033[0m")  # 绿色表示成功
        db_info = connection.get_server_info()
        print(f"服务器信息: {db_info}")

        # 可选：执行简单查询验证
        # cursor = connection.cursor()
        # cursor.execute("SELECT DATABASE();")
        # current_db = cursor.fetchone()
        # print(f"当前数据库: {current_db[0] if current_db else '未选择'}")
        # cursor.execute("SELECT VERSION();")
        # version = cursor.fetchone()
        # print(f"数据库版本: {version[0]}")
        # cursor.close()

    else:
        print("\033[91m连接失败。\033[0m")  # 红色表示失败

except mysql.connector.Error as err:
    print(f"\033[91m连接时发生错误: {err}\033[0m")  # 红色表示失败
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
        print("错误详情：用户名或密码不正确。请检查您的凭据。")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print(f"错误详情：数据库 '{db_name}' 不存在。请检查数据库名称。")
    elif 'timed out' in str(err).lower():
        print("错误详情：连接超时。请检查主机名/IP地址、端口以及网络连接和防火墙设置。")
    elif 'connection refused' in str(err).lower():
        print("错误详情：连接被拒绝。请确保 MySQL 服务器正在运行，并且监听指定的主机和端口。")
    else:
        print(f"错误代码: {err.errno}")

finally:
    # --- 关闭连接 ---
    if connection and connection.is_connected():
        connection.close()
        print("数据库连接已关闭。")
    elif connection is None and 'err' not in locals():
        print("\033[91m未能建立连接。\033[0m")
