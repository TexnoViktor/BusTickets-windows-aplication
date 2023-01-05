import tkinter as tk
from tkinter import ttk
import sqlite3
import random
import uuid


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='icons/add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Додати Квиток', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='icons/update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редагувати', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='icons/delete.gif')
        btn_delete = tk.Button(toolbar, text='Видалити Квиток', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='icons/search.gif')
        btn_search = tk.Button(toolbar, text='Пошук', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='icons/refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Оновити', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('idTicket', 'price', 'number_ticket', 'name', 'departure', 'arrival'), height=15, show='headings')

        self.tree.column('idTicket', width=30, anchor=tk.CENTER)
        self.tree.column('price', width=40, anchor=tk.CENTER)
        self.tree.column('number_ticket', width=100, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('departure', width=100, anchor=tk.CENTER)
        self.tree.column('arrival', width=100, anchor=tk.CENTER)

        self.tree.heading('idTicket', text='ID')
        self.tree.heading('price', text='Ціна')
        self.tree.heading('number_ticket', text='Номер білету')
        self.tree.heading('name', text='ПІБ')
        self.tree.heading('departure', text='Відправлення')
        self.tree.heading('arrival', text='Прибуття')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, surname, name, midlename, passcode, date, price, departure, arrival):
        self.db.insert_data(surname, name, midlename, passcode, date, price, departure, arrival)
        self.view_records()

    def update_record(self, surname, name, midlename, passcode, date, price, departure, arrival):
        self.db.c.execute('''UPDATE tickets SET price=?, time=? WHERE idTicket=?''',
                          (price, date, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.c.execute(
            '''UPDATE clients SET name=?, surname=?, midlename=?, passport=? WHERE id = (SELECT client_id FROM tickets WHERE idTicket=?)''',
        (surname, name, midlename, passcode, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.db.c.execute('''UPDATE tickets
               SET route_id = (SELECT id
                               FROM routes
                               WHERE departure=? AND arrival =?)
               WHERE idTicket=?''', (departure, arrival, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT idTicket, price, number_ticket, surname || " " || name || " " || midlename, departure, arrival
                                FROM tickets, clients, routes WHERE tickets.route_id = routes.id AND tickets.client_id = clients.id ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM tickets WHERE idTicket=?''', (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, number):
        number = ('%' + number + '%',)
        self.db.c.execute('''SELECT idTicket, price, number_ticket, surname || " " || name || " " || midlename, departure, arrival 
                                FROM tickets, clients, routes WHERE tickets.route_id = routes.id AND tickets.client_id = clients.id AND number_ticket LIKE ?''', number)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Додати Квиток')
        self.geometry('400x350+400+300')
        self.resizable(False, False)

        label_surname = tk.Label(self, text='Прізвище:')
        label_surname.place(x=50, y=50)
        label_name = tk.Label(self, text='Ім\'я:')
        label_name.place(x=50, y=80)
        label_midlename = tk.Label(self, text='Побатькові:')
        label_midlename.place(x=50, y=110)
        label_passcode = tk.Label(self, text='Код паспорта:')
        label_passcode.place(x=50, y=140)
        label_date = tk.Label(self, text='Дата відправлення:')
        label_date.place(x=50, y=170)
        label_departure = tk.Label(self, text='Відправлення:')
        label_departure.place(x=50, y=200)
        label_arrival = tk.Label(self, text='Прибуття:')
        label_arrival.place(x=50, y=230)
        label_price = tk.Label(self, text='Ціна:')
        label_price.place(x=50, y=260)

        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=200, y=50)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=80)

        self.entry_midlename = ttk.Entry(self)
        self.entry_midlename.place(x=200, y=110)

        self.entry_passcode = ttk.Entry(self)
        self.entry_passcode.place(x=200, y=140)

        self.entry_date = ttk.Entry(self)
        self.entry_date.place(x=200, y=170)

        self.combobox_dep = ttk.Combobox(self, values=[u'Kyiv', u'Lutsk', u'Cherkasy', u'Odesa', u'Kharkiv', u'Dnipro', u'Poltava'])
        self.combobox_dep.current(0)
        self.combobox_dep.place(x=200, y=200)

        self.combobox_arr = ttk.Combobox(self, values=[u'Kyiv', u'Lutsk', u'Cherkasy', u'Odesa', u'Kharkiv', u'Dnipro', u'Poltava'])
        self.combobox_arr.current(0)
        self.combobox_arr.place(x=200, y=230)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=200, y=260)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=300, y=300)

        self.btn_ok = ttk.Button(self, text='Додати')
        self.btn_ok.place(x=220, y=300)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_surname.get(),
                                                                       self.entry_name.get(),
                                                                       self.entry_midlename.get(),
                                                                       self.entry_passcode.get(),
                                                                       self.entry_date.get(),
                                                                       self.entry_price.get(),
                                                                       self.combobox_dep.get(),
                                                                       self.combobox_arr.get()))
        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db

    def init_edit(self):
        self.title('Редагувати Білет')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=205, y=300)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_surname.get(),
                                                                          self.entry_name.get(),
                                                                          self.entry_midlename.get(),
                                                                          self.entry_passcode.get(),
                                                                          self.entry_date.get(),
                                                                          self.entry_price.get(),
                                                                          self.combobox_dep.get(),
                                                                          self.combobox_arr.get()))

        self.btn_ok.destroy()


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Пошук')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Пошук')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Зачинити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

    def insert_data(self, surname, name, midlename, passcode, date, price, departure, arrival):
        self.c.execute('''INSERT INTO clients(name, midlename, surname, passport) VALUES (?, ?, ?, ?)''',
                       (name, midlename, surname, passcode))
        self.c.execute('''INSERT INTO tickets(price, number_ticket, tocken, time) VALUES (?, ?, ?, ?)''',
                       (price, random.randint(1000, 9999), str(uuid.uuid4()), date))
        self.c.execute(
            '''UPDATE tickets
               SET client_id = (SELECT id
                               FROM clients
                               WHERE name=? AND surname =?)
               WHERE idTicket = last_insert_rowid()''',
            (name, surname))
        self.c.execute(
            '''UPDATE tickets
               SET route_id = (SELECT id
                               FROM routes
                               WHERE departure=? AND arrival =?)
               WHERE idTicket = last_insert_rowid()''',
            (departure, arrival))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Bus tickets selling application")
    root.geometry("665x450+300+200")
    root.resizable(False, False)
    root.mainloop()