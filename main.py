import tkinter as tk
from tkinter import ttk
import  sqlite3

# клас главного окна

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
    def open_search_dialog(self):
        Search()

    # удаление записи

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute("""DELETE FROM db WHERE
            id=?""", (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

    # изменение записи

    def update_record(self, name, number, email, salary):
        self.db.c.execute('''UPDATE db SET name=?, number=?, email=?, salary=? WHERE ID=?''',
                          (name, number, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    # Вывод данных в виджет таблицы
    def view_records(self):
        self.db.c.execute("""SELECT * FROM db""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def records(self, name, number, email, salary):
        self.db.insert_data(name, number, email, salary)
        self.view_records()

    def open_dialog(self):
        Child()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добавления
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # виджет Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'number', 'email', 'salary'), height=45, show='headings')

        # параметры колонок
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("number", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=100, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("number", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)

        # кнопка изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0',bd=0,
                                    image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # кнопка удаления записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                              image=self.search_img,
                              command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

# класс дочернего окна

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_sal = tk.Label(self, text='Зарплата')
        label_sal.place(x=50, y=140)

        # строки ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_number.get(),
                                                                       self.entry_salary.get()))

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                        self.entry_email.get(),
                        self.entry_number.get(),
                        self.entry_salary.get()))
        # закрытие окна редактирования
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # доступ к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_number.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# класс базы данных

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('employees.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS db(
        id INTEGER PRIMARY KEY,
        name TEXT,
        number TEXT,
        email TEXT,
        salary TEXT);
        """)
        self.conn.commit()

    def insert_data(self, name, number, email, salary):
        self.c.execute("""INSERT INTO db(name, number, email, salary)
        VALUES (?, ?, ?, ?)
        """, (name, number, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компаний')
    root.geometry('740x450')
    root.resizable(False, False)
    root.mainloop()