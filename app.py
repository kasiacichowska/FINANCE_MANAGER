import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

import database
from database import add_expense, add_income, get_balance, join_tables, for_chart, get_expenses_categories, get_available

miesiace = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
current_year = datetime.now().year


#okno bazowe aplikacji, inne klasy okien po niej dziedziczą
class BaseFrame:
    def __init__(self, root):
        self.root = root

    # Metoda do przełączania między ramkami
    def switch_frame(self, frame_class):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame_class(self.root)


#-----------------------Główny ekran----------------------

class GlownyEkran(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Finance Manager")
        root.geometry("1100x600")

        # Nagłówek aplikacji
        label = tk.Label(root, text="MANAGER FINANSÓW", font=("Arial", 64))
        label.pack(expand=True)

        # Etykieta do wpisywania hasła
        self.password_label = tk.Label(root, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=10)

        # Pole do wpisywania hasła
        self.password_entry = tk.Entry(root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=10)

        # Przycisk do zatwierdzenia hasła
        self.submit_button = tk.Button(root, text="Submit", command=self.check_password, font=("Arial", 14))
        self.submit_button.pack(pady=10)

    #funkcja do sprawdzania poprawności hasła
    def check_password(self):
        password = self.password_entry.get()
        if password == "1234":
            messagebox.showinfo("Powodzenie", "Hasło prawidłowe.")
            self.password_entry.delete(0, tk.END)
            self.switch_frame(GlowneMenu)
        else:
            messagebox.showerror("Error", "Niepoprawne hasło. Spróbuj ponownie")
            self.password_entry.delete(0, tk.END)

#-----------------------Główne menu----------------------
class GlowneMenu(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Finance Manager")
        root.geometry("1100x600")

        # Górna ramka na powitanie
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill=tk.X, pady=20)

        # Etykieta powitania
        welcome_label = tk.Label(self.top_frame, text="Witamy w Managerze Finansów!", font=("Arial", 24))
        welcome_label.pack(side=tk.TOP)

        # Wyświetlanie dostępnych środków, czyli bez pieniedzy wplaconych na cele oszczednosciowe
        self.available = get_available()
        self.available_label = tk.Label(root, text=f"Dostępne środki: {self.available} PLN", font=("Arial", 18))
        self.available_label.pack(pady=10)

        # Wyświetlanie ogólnego stanu konta
        self.balance = get_balance()
        self.balance_label = tk.Label(root, text=f"Ogólny stan konta: {self.balance} PLN", font=("Arial", 15))
        self.balance_label.pack(pady=20)

        # Ramka na przyciski akcji
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Przycisk do dodania przychodu
        self.add_income_button = tk.Button(self.button_frame, command=lambda: self.switch_frame(oknoPrzychod), text="Dodaj Przychód", font=("Arial", 14))
        self.add_income_button.grid(row=0, column=0, padx=10)

        # Przycisk do dodania wydatku
        self.add_expense_button = tk.Button(self.button_frame, command=lambda: self.switch_frame(oknoWydatek), text="Dodaj Wydatek", font=("Arial", 14))
        self.add_expense_button.grid(row=0, column=1, padx=10)

        # Przycisk do wyświetlania historii
        self.view_history_button = tk.Button(self.button_frame, command=lambda: self.switch_frame(oknoHistoria), text="Zobacz Historię", font=("Arial", 14))
        self.view_history_button.grid(row=1, column=0, padx=10, pady=10)

        # Przycisk do przejścia do oszczędności
        self.exit_button = tk.Button(self.button_frame, command=lambda: self.switch_frame(oknoOszczednosci), text="Przejdź do oszczędności", font=("Arial", 14))
        self.exit_button.grid(row=1, column=1, padx=10, pady=10)


#-----------------------Okno przychodu----------------------
class oknoPrzychod(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Finance Manager")
        root.geometry("800x450")

        # Etykieta
        info_label = tk.Label(root, text="Wprowadź kwotę i datę transakcji", font=("Arial", 24))
        info_label.pack(pady=20)

        # funkcja do sprawdzania poprawności wprowadzonego przychodu
        def zatwierdz_przychod():
            kwota = kwota_entry.get()
            day = day_var.get()
            miesiac = month_var.get()
            rok = year_var.get()

            if kwota == '':
                messagebox.showwarning("Błąd", "Proszę wpisać kwotę")
            elif float(kwota) <= 0:
                messagebox.showwarning("Błąd", "Proszę wpisać poprawną kwotę")
            elif float(kwota) > 0:
                add_income(kwota, miesiac, rok)
                messagebox.showinfo("Zatwierdzenie", f"Transakcja o wartości: {kwota} PLN została zatwierdzona")
                self.switch_frame(GlowneMenu)

        # Pole do wpisywania kwoty
        kwota_label = tk.Label(root, text="Wpisz kwotę:")
        kwota_label.pack(pady=5)

        kwota_entry = tk.Entry(root)
        kwota_entry.pack(pady=5)

        data_frame = tk.Frame(root)
        data_frame.pack(pady=5)

        # Lista rozwijana do wyboru dnia
        day_label = tk.Label(data_frame, text="Dzień:")
        day_label.grid(row=0, column=0, padx=5)

        day_var = tk.StringVar()
        day_combobox = ttk.Combobox(data_frame, textvariable=day_var, width=4)
        day_combobox['values'] = [str(i) for i in range(1, 32)]
        day_combobox.current(datetime.now().day - 1)
        day_combobox.grid(row=0, column=1, padx=5)

        # Lista rozwijana do wyboru miesiąca
        month_label = tk.Label(data_frame, text="Miesiąc:")
        month_label.grid(row=0, column=2, padx=5)

        month_var = tk.StringVar()
        month_combobox = ttk.Combobox(data_frame, textvariable=month_var, width=15)
        month_combobox['values'] = miesiace
        month_combobox.current(datetime.now().month - 1)
        month_combobox.grid(row=0, column=3, padx=5)

        # Lista rozwijana do wyboru roku
        year_label = tk.Label(data_frame, text="Rok:")
        year_label.grid(row=0, column=4, padx=5)

        year_var = tk.StringVar()
        year_combobox = ttk.Combobox(data_frame, textvariable=year_var, width=10)
        current_year = datetime.now().year
        year_combobox['values'] = [str(i) for i in range(current_year - 4, current_year + 1)]
        year_combobox.current(4)
        year_combobox.grid(row=0, column=5, padx=5)

        # Przycisk zatwierdzenia transakcji
        zatwierdz_button = tk.Button(root, text="Zatwierdź transakcję", command=zatwierdz_przychod)
        zatwierdz_button.pack(pady=5)

        # Przycisk powrotu do głównego menu
        back_button = tk.Button(root, text="Powrót do głównego menu", command=lambda: self.switch_frame(GlowneMenu))
        back_button.pack(pady=10)

#---------------------Okno wydatki-----------------------
class oknoWydatek(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Finance Manager")
        root.geometry("800x450")

        # Etykieta
        info_label = tk.Label(root, text="Wprowadź kwotę i datę transakcji", font=("Arial", 24))
        info_label.pack(pady=20)

        # funkcja do sprawdzania poprawności wprowadzonego wydatku
        def zatwierdz_wydatek():
            kwota = kwota_entry.get()
            miesiac = month_var.get()
            rok = year_var.get()
            kategoria=expense_category.get()

            if kwota=='':
                messagebox.showwarning("Błąd", "Proszę wpisać kwotę")
            elif float(kwota)<=0:
                messagebox.showwarning("Błąd", "Proszę wpisać poprawną kwotę")
            elif float(kwota)>0 :
                add_expense(kwota,kategoria,miesiac,rok)
                messagebox.showinfo("Zatwierdzenie", f"Transakcja o wartości: {kwota} PLN została zatwierdzona")
                self.switch_frame(GlowneMenu)


        # Pole do wpisywania kwoty
        kwota_label = tk.Label(root, text="Wpisz kwotę:")
        kwota_label.pack(pady=5)

        kwota_entry = tk.Entry(root)
        kwota_entry.pack(pady=5)

        # Ramka dla etykiety i listy rozwijanej
        category_frame = tk.Frame(root)
        category_frame.pack(side=tk.TOP)

        # Etykieta kategoria
        expense_category_label = tk.Label(category_frame, text="Category:")
        expense_category_label.pack(side=tk.LEFT)

        # Lista rozwijana kategorii
        lista= get_expenses_categories()
        expense_category = ttk.Combobox(category_frame,
                                        values=lista)
        expense_category.pack(side=tk.LEFT)
        expense_category.set(" ")

        data_frame = tk.Frame(root)
        data_frame.pack(pady=5)

        # Lista rozwijana do wyboru dnia
        day_label = tk.Label(data_frame, text="Dzień:")
        day_label.grid(row=0, column=0, padx=5)

        day_var = tk.StringVar()
        day_combobox = ttk.Combobox(data_frame, textvariable=day_var,width=4)
        day_combobox['values'] = [str(i) for i in range(1, 32)]
        day_combobox.current(datetime.now().day-1)
        day_combobox.grid(row=0, column=1, padx=5)

        # Lista rozwijana do wyboru miesiąca
        month_label = tk.Label(data_frame, text="Miesiąc:")
        month_label.grid(row=0, column=2, padx=5)

        month_var = tk.StringVar()
        month_combobox = ttk.Combobox(data_frame, textvariable=month_var,width=15)
        month_combobox['values'] = miesiace
        month_combobox.current(datetime.now().month - 1)
        month_combobox.grid(row=0, column=3, padx=5)

        # Lista rozwijana do wyboru roku
        year_label = tk.Label(data_frame, text="Rok:")
        year_label.grid(row=0, column=4, padx=5)

        year_var = tk.StringVar()
        year_combobox = ttk.Combobox(data_frame, textvariable=year_var,width=10)
        current_year = datetime.now().year
        year_combobox['values'] = [str(i) for i in range(current_year-4, current_year+1)]
        year_combobox.current(4)
        year_combobox.grid(row=0, column=5, padx=5)

        # Przycisk do zatwierdzania transakcji
        zatwierdz_button = tk.Button(root, text="Zatwierdź transakcję", command=zatwierdz_wydatek)
        zatwierdz_button.pack(pady=5)

        # przycisk powrotu
        back_button = tk.Button(root, text="Powrót do głównego menu", command=lambda: self.switch_frame(GlowneMenu))
        back_button.pack(pady=10)

#---------------------Okno historia-----------------------
class oknoHistoria(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Historia finansów")
        root.geometry("800x460")
        self.display_data()

    #funkcja do tworzenia okna wykresu
    def oknowykres(self):
        new_window = tk.Toplevel(self.root)
        oknoWykres(new_window)

    #funkcja do wyświetlania danych
    def display_data(self):
        data = join_tables()

        headers = ["Typ", "Kwota", "Kategoria", "Miesiąc", "Rok"]
        for col_index, header in enumerate(headers):
            label = tk.Label(self.root, text=header, font=("Arial", 20, "bold"))
            label.grid(row=0, column=col_index, sticky="nsew")
            self.root.grid_columnconfigure(col_index, weight=1)  # Rozciągnij kolumny

        # Wyświetlenie danych w oknie
        for index, row in enumerate(data, start=1):
            for col_index, value in enumerate(row):
                label = tk.Label(self.root, text=value)
                label.grid(row=index, column=col_index, sticky="nsew")
                self.root.grid_columnconfigure(col_index, weight=1)

        #przycisk do okna wykresu
        button = tk.Button(self.root, command=self.oknowykres, text="Utwórz wykres")
        button.grid(row=100, column=0, columnspan=6, pady=10)

        #przycisk powrotu
        back_button = tk.Button(self.root, text="Powrót do menu", command=lambda: self.switch_frame(GlowneMenu))
        back_button.grid(row=100, column=0,padx=10, pady=10)


#---------------------Okno wykres-----------------------
class oknoWykres(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Wykresy finansów")
        root.geometry("600x600")

        # Pola wejściowe dla miesiąca i roku
        self.month1_label = tk.Label(root, text="Miesiąc 1:")
        self.month1_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.month1 = ttk.Combobox(root, values=miesiace)
        self.month1.grid(row=0, column=1, padx=10, pady=5)

        self.year1_label = tk.Label(root, text="Rok 1:")
        self.year1_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.year1 = ttk.Combobox(root, values=[str(i) for i in range(2020, 2025)])
        self.year1.grid(row=0, column=3, padx=10, pady=5)

        self.month2_label = tk.Label(root, text="Miesiąc 2:")
        self.month2_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.month2 = ttk.Combobox(root, values=miesiace)
        self.month2.grid(row=1, column=1, padx=10, pady=5)

        self.year2_label = tk.Label(root, text="Rok 2:")
        self.year2_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.year2 = ttk.Combobox(root, values=[str(i) for i in range(2020, 2025)])
        self.year2.grid(row=1, column=3, padx=10, pady=5)

        #przycisk generowania wykresu
        self.generate_button = tk.Button(root, text="Generuj wykres", command=self.generate_chart)
        self.generate_button.grid(row=2, column=0, columnspan=4, pady=10)

    #funkcja do tworzenia wykresu
    def generate_chart(self):
        month1 = self.month1.get()
        year1 = self.year1.get()
        month2 = self.month2.get()
        year2 = self.year2.get()

        if not (month1 and year1 and month2 and year2):
            messagebox.showerror("Błąd", "Proszę wprowadzić wszystkie wartości.")
            return

        data1 = for_chart(month1, year1)
        data2 = for_chart(month2, year2)

        if not data1 or not data2:
            messagebox.showerror("Błąd", "Brak danych dla wybranych okresów.")
            return

        categories1 = [row[0] for row in data1]
        amounts1 = [row[1] for row in data1]

        categories2 = [row[0] for row in data2]
        amounts2 = [row[1] for row in data2]

        # Synchronizacja długości danych
        all_categories = list(set(categories1) | set(categories2))
        amounts1_dict = dict(zip(categories1, amounts1))
        amounts2_dict = dict(zip(categories2, amounts2))

        amounts1_synced = [amounts1_dict.get(category, 0) for category in all_categories]
        amounts2_synced = [amounts2_dict.get(category, 0) for category in all_categories]

        fig, ax = plt.subplots()
        bar_width = 0.35
        index = range(len(all_categories))

        bar1 = ax.bar(index, amounts1_synced, bar_width, label=f'{month1} {year1}')
        bar2 = ax.bar([i + bar_width for i in index], amounts2_synced, bar_width, label=f'{month2} {year2}')

        ax.set_xlabel('Kategoria')
        ax.set_ylabel('Suma pieniędzy')
        ax.set_title('Wydatki w poszczególnych kategoriach')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(all_categories)
        ax.legend()

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().grid_forget()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=4)

#---------------------Okno oszczędności-----------------------
class oknoOszczednosci(BaseFrame):
    def __init__(self, root):
        self.root = root
        root.title("Finance Manager - Oszczędności")
        root.geometry("800x600")

        #etykieta
        info_label = tk.Label(root, text="Oszczędności", font=("Arial", 24))
        info_label.pack(pady=10)

        self.goals = self.get_goals()
        self.display_goals()

        #przycisk do dodawania celu
        style = ttk.Style()
        style.configure('Dodaj.TButton', font=('Arial', 14))

        add_goal_button = ttk.Button(root, text="Dodaj nowy cel", style='Dodaj.TButton',
                                         command=self.add_goal_window)
        add_goal_button.pack(pady=20, padx=40, ipadx=20, ipady=10)

        self.total_savings_label = tk.Label(root,
                                                text=f"Łączna kwota oszczędności: {self.calculate_total_savings()} PLN",
                                                font=("Arial", 18))
        self.total_savings_label.pack(pady=10)

        #przycisk powrotu
        back_button = tk.Button(root, text="Powrót do głównego menu", command=lambda: self.switch_frame(GlowneMenu))
        back_button.pack(pady=10)

    # funkcja do pobierania celów oszczędnościowych
    def get_goals(self):
        return database.get_goals()

    # funkcja do wyświetlania celów oszczędnościowych
    def display_goals(self):
        for goal in self.goals:
            goal_frame = tk.Frame(self.root)
            goal_frame.pack(pady=5, padx=10, fill=tk.X)

            goal_label = tk.Label(goal_frame,
                                      text=f"Cel: {goal['name']}, Kwota docelowa: {goal['target_amount']} PLN, Wpłacono: {goal['saved_amount']} PLN")
            goal_label.grid(row=0, column=0, sticky='w')

            #przycisk wplac
            add_funds_button = ttk.Button(goal_frame, text="Wpłać", command=lambda g=goal: self.add_funds_window(g))
            add_funds_button.grid(row=0, column=1, padx=10, sticky='e')

            #przycisk usuń
            remove_goal_button = ttk.Button(goal_frame, text="Usuń", command=lambda g=goal: self.remove_goal(g))
            remove_goal_button.grid(row=0, column=2, padx=10, sticky='e')

            # Dodanie poziomej linii
            separator = ttk.Separator(self.root, orient='horizontal')
            separator.pack(fill='x', pady=10)

    #funkcja do tworzenia okienka do nowego celu
    def add_goal_window(self):
        new_window = tk.Toplevel(self.root)
        DodajCelOszczednosciowy(new_window, self)

    #funkcja do tworzenia okienka do wplaty na cel
    def add_funds_window(self, goal):
        new_window = tk.Toplevel(self.root)
        WplataNaCelOszczednosciowy(new_window, goal, self)

    #funkcja do odświeżania celów
    def refresh_goals(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    #funkcja do obliczenia sumy oszczędności
    def calculate_total_savings(self):
        return sum(goal['saved_amount'] for goal in self.goals)

    #funkcja do usuwania celu
    def remove_goal(self, goal):
        confirm = messagebox.askyesno("Potwierdzenie usunięcia", f"Czy na pewno chcesz usunąć cel: {goal['name']}?")
        if confirm:
            database.remove_goal(goal['id'])
            messagebox.showinfo("Sukces",
                                f"Cel {goal['name']} został usunięty, a {goal['saved_amount']} PLN zostało zwrócone do dostępnych środków.")
            self.refresh_goals()
            self.switch_frame(oknoOszczednosci)

    #funkcja do sprawdzenia, czy cel został osiągnięty
    def check_goal_completion(self, goal):
        if goal['saved_amount'] >= goal['target_amount']:
            messagebox.showinfo("Gratulacje!", f"Cel oszczędnościowy '{goal['name']}' został osiągnięty!")



#---------------------Okno wprowadzania nowego celu-----------------------
class DodajCelOszczednosciowy:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        root.title("Dodaj Cel Oszczędnościowy")
        root.geometry("400x300")

        #do wprowadzenia nazwy
        name_label = ttk.Label(root, text="Nazwa Celu:")
        name_label.pack(pady=5)
        self.name_entry = ttk.Entry(root)
        self.name_entry.pack(pady=5)

        # do wprowadzenia kwoty
        target_label = ttk.Label(root, text="Kwota Docelowa:")
        target_label.pack(pady=5)
        self.target_entry = ttk.Entry(root)
        self.target_entry.pack(pady=5)

        # przycisk zatwierdzenia
        add_button = ttk.Button(root, text="Dodaj Cel", command=self.add_goal)
        add_button.pack(pady=10)

    #funkcja do dodania celu
    def add_goal(self):
        name = self.name_entry.get()
        target_amount = self.target_entry.get()

        if not name or not target_amount:
            messagebox.showwarning("Błąd", "Proszę wpisać nazwę celu i kwotę docelową")
            self.root.destroy()
            self.parent.root.lift()
            return

        try:
            target_amount = float(target_amount)
            if target_amount <= 0:
                messagebox.showwarning("Błąd", "Kwota docelowa musi być większa od zera")
                self.root.destroy()
                self.parent.root.lift()
                return
        except ValueError:
            messagebox.showwarning("Błąd", "Proszę wpisać poprawną kwotę docelową")
            self.root.destroy()
            self.parent.root.lift()
            return

        database.add_goal(name, target_amount)
        messagebox.showinfo("Sukces", "Cel oszczędnościowy został dodany.")
        self.parent.refresh_goals()
        self.root.destroy()
        self.parent.root.lift()


#---------------------Okno wplaty na cel-----------------------
class WplataNaCelOszczednosciowy:
    def __init__(self, root, goal, parent):
        self.root = root
        self.goal = goal
        self.parent = parent
        root.title("Wpłać na Cel")
        root.geometry("400x300")

        #etykieta
        info_label = ttk.Label(root, text=f"Wpłata na cel: {goal['name']}")
        info_label.pack(pady=5)

        #do wpisania kwoty
        amount_label = ttk.Label(root, text="Kwota Wpłaty:")
        amount_label.pack(pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.pack(pady=5)

        #przycisk zatwierdzenia
        add_button = ttk.Button(root, text="Wpłać", command=self.add_funds)
        add_button.pack(pady=10)

    #funkcja do dodania wplaty
    def add_funds(self):
        amount = self.amount_entry.get()

        if not amount:
            messagebox.showwarning("Błąd", "Proszę wpisać kwotę wpłaty")
            self.root.destroy()
            self.parent.root.lift()
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showwarning("Błąd", "Kwota wpłaty musi być większa od zera")
                self.root.destroy()
                self.parent.root.lift()
                return
        except ValueError:
            messagebox.showwarning("Błąd", "Proszę wpisać poprawną kwotę wpłaty")
            self.root.destroy()
            self.parent.root.lift()
            return

        if amount <= get_available():
            database.add_contribution(self.goal['id'], amount)

            self.goal['saved_amount'] += amount

            if self.goal['saved_amount'] >= self.goal['target_amount']:
                messagebox.showinfo("Gratulacje!", f"Cel oszczędnościowy '{self.goal['name']}' został osiągnięty!")

            messagebox.showinfo("Sukces", "Wpłata została dodana.")
            self.parent.refresh_goals()
            self.root.destroy()
            self.parent.root.lift()
        else:
            messagebox.showwarning("Błąd", "Brak dostępnych środków.")
            self.root.destroy()
            self.parent.root.lift()

# odpalenie aplikacji
root = tk.Tk()
app = (GlownyEkran(root))
root.mainloop()

