import sqlite3

connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute(
    """
  CREATE TABLE heures(id INTEGER PRIMARY KEY AUTOINCREMENT,
  matricule VARCHAR(6),
  date_publication TEXT,
  duree INTEGER
  );
  """
)
connection.commit()
cursor.close()
connection.close()
