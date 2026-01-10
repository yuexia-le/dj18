import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='vocab_master'
    )
    print("Database connection successful")
    
    # 记得操作完关闭连接
    conn.close()
    
except mysql.connector.Error as err:
    # 修复了这里的语法问题
    print(f"Error: {err.errno} {err.msg}")