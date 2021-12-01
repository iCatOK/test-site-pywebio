import sqlite3

db = sqlite3.connect('db.db')

# клиент бд
sql = db.cursor()

name = input('Name: ')
username = input('Username: ')
password = input('Password: ')

sql.execute(f"select username from user where username = '{username}'")

if sql.fetchone() is None:
    sql.execute(f"""insert into user (name, username, password)
        values (?, ?, ?)
    """, (name, username, password))
    db.commit()
    print('Пользователь успешно добавлен')
else:
    print("Пользователь уже существует")