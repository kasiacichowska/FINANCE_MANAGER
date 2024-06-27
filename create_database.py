import sqlite3

# Nawiązanie połączenia z bazą danych (lub jej utworzenie, jeśli nie istnieje)
conn = sqlite3.connect('finance.db')
c = conn.cursor()

# Utworzenie tabeli wydatków
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY,
              amount REAL,
              category TEXT,
              month INTEGER,
              year INTEGER)''')

# Utworzenie tabeli przychodów
c.execute('''CREATE TABLE IF NOT EXISTS incomes
             (id INTEGER PRIMARY KEY,
              amount REAL,
              month INTEGER,
              year INTEGER)''')

# Utworzenie tabeli celów oszczędnościowych
c.execute('''CREATE TABLE IF NOT EXISTS savings_goals
             (id INTEGER PRIMARY KEY,
              name TEXT,
              target_amount REAL,
              saved_amount REAL)''')

# Utworzenie tabeli wpłat na cele oszczędnościowe
c.execute('''CREATE TABLE IF NOT EXISTS savings_contributions
             (id INTEGER PRIMARY KEY,
              goal_id INTEGER,
              amount REAL,
              date TEXT,
              FOREIGN KEY(goal_id) REFERENCES savings_goals(id))''')

# Zamknięcie połączenia z bazą danych
conn.commit()
conn.close()

#funkcja do usuwania wydatkow
def delete_all_expenses():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()

#funkcja do usuwania przychodow
def delete_all_incomes():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("DELETE FROM incomes")
    conn.commit()
    conn.close()

# Usuwanie wszystkich wydatkow i przychodow
#delete_all_expenses()
#delete_all_incomes()

#funkcja do usuwania oszczednosci
def delete_all_savings():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("DELETE FROM savings_goals")
    conn.commit()
    conn.close()

#funkcja do usuwania wplat
def delete_all_contributions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("DELETE FROM savings_contributions")
    conn.commit()
    conn.close()

#delete_all_savings()
#delete_all_contributions()