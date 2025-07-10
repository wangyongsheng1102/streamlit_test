import sqlite3
from streamlit_authenticator.utilities.hasher import Hasher


# 初始化数据库，创建菜单表和用户表
def init_db():
    conn = sqlite3.connect("data.db")
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()

    try:
        # 创建菜单表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                route TEXT NOT NULL UNIQUE
            )
        """)

        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # 初始化默认菜单
        cursor.execute("SELECT COUNT(*) FROM menus")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO menus (name, route) VALUES (?, ?)
            """, [
                ("首页", "home"),
                ("文件上传", "upload"),
                ("比较", "compare")
            ])

        # 初始化默认用户（使用加密密码存储）
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            hashed_password = Hasher.hash("admin123")  # 加密密码
            cursor.execute("""
                INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)
            """, ("管理员", "admin", hashed_password, "admin"))
    except sqlite3.OperationalError as e:
        print("SQLite error:", e)
    finally:
        cursor.close()
        conn.close()


# 从数据库中加载菜单数据
def get_menus():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, route FROM menus")
    menus = [{"id": row[0], "name": row[1], "route": row[2]} for row in cursor.fetchall()]
    conn.close()
    print("menus : ", menus)
    return menus


# 从数据库中加载用户数据
def get_users():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, password FROM users")
    users = [{"name": row[0], "username": row[1], "password": row[2]} for row in cursor.fetchall()]
    conn.close()
    return users
