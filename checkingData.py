import sqlite3

connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute(
    """
  SELECT DailyTime from users;
  """
)
print(cursor.fetchone()[0])
connection.commit()
cursor.close()
connection.close()
