import sqlite3
from datetime import datetime

#funkcja do dodawania wydatku
def add_expense(amount, category, month, year):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, month, year) VALUES (?, ?, ?, ?)",
              (amount, category, month, year))
    conn.commit()
    conn.close()

#funkcja do dodawania przychodu
def add_income(amount, month, year):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("INSERT INTO incomes (amount, month, year) VALUES (?, ?, ?)",
              (amount, month, year))
    conn.commit()
    conn.close()

#funkcja do pobierania kategorii wydatku
def get_expenses_categories():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM expenses")
    categories = c.fetchall()

    category_list = [category[0] for category in categories]
    predefined_categories = ["Jedzenie", "Transport", "Opłaty", "Rozrywka", "Inne"]
    combined_categories = set(category_list + predefined_categories)
    sorted_category_list = sorted(combined_categories)
    conn.close()

    return sorted_category_list

#funkcja do wyświetlania zawrtości BD
def display_table(table_name):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("Table is empty.")
    else:
        print(f"Content of the '{table_name}' table:")
        for row in rows:
            print(row)

#funkcja do łączenia tabel
def join_tables():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    query = '''SELECT 'Wydatek' AS Typ, amount, category, month, year FROM expenses
                   UNION ALL
                   SELECT 'Przychód' AS Typ, amount, 'Przychód' AS category, month, year FROM incomes
                   ORDER BY year, month'''
    c.execute(query)
    data = c.fetchall()
    return data

#funkcja potrzebna do tworzenia wykresu, pobiera dane
def for_chart( month, year):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    query = '''SELECT category, SUM(amount) FROM expenses WHERE month = ? AND year = ? GROUP BY category'''
    c.execute(query, (month, year))
    data = c.fetchall()
    conn.close()
    return data

#funkcja do dodawania celu oszczednosciowego
def add_goal(name, target_amount):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("INSERT INTO savings_goals (name, target_amount, saved_amount) VALUES (?, ?, ?)",
              (name, target_amount, 0))
    conn.commit()
    conn.close()

#funkcja do dodawania wplaty na cel oszczednosciowy
def add_contribution(goal_id, amount):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO savings_contributions (goal_id, amount, date) VALUES (?, ?, ?)", (goal_id, amount, date))
    c.execute("UPDATE savings_goals SET saved_amount = saved_amount + ? WHERE id = ?", (amount, goal_id))
    conn.commit()
    conn.close()

#funkcja do pobierania celów
def get_goals():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM savings_goals")
    rows = c.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1], 'target_amount': row[2], 'saved_amount': row[3]} for row in rows]

#funkcja do obliczania salda ogólnego
def get_balance():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = c.fetchone()[0]
    if total_expenses is None:
        total_expenses = 0

    c.execute("SELECT SUM(amount) FROM incomes")
    total_incomes = c.fetchone()[0]
    if total_incomes is None:
        total_incomes = 0

    conn.close()
    balance = total_incomes - total_expenses
    return balance

#funkcja do obliczania salda bez oszczednosci
def get_available():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM savings_contributions")
    suma = c.fetchone()[0]
    if suma is None:
        suma = 0

    available = get_balance() - suma
    conn.close()
    return available

#funkcja do usuwania celu oszczednosciowego
def remove_goal(goal_id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM savings_contributions WHERE goal_id=?", (goal_id,))
    total_contributed = c.fetchone()[0]
    if total_contributed is None:
        total_contributed = 0

    c.execute("DELETE FROM savings_goals WHERE id=?", (goal_id,))
    c.execute("DELETE FROM savings_contributions WHERE goal_id=?", (goal_id,))

    conn.commit()
    conn.close()

    available = get_available() + total_contributed
    return available

#DO TESTÓW
# Wyświetlanie zawartości tabeli expenses
display_table('expenses')

# Wyświetlanie zawartości tabeli incomes
display_table('incomes')