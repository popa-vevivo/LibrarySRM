import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta

# книги и количество
books = {
    "Алгебра": 3,
    "Физика": 2,
    "История": 1,
    "Информатика": 4,
    "Химия": 3,
    "Биология": 2,
    "География": 2,
    "Литература": 5,
    "Английский язык": 3,
    "Программирование на Python": 4,
    "Математический анализ": 2,
    "Философия": 2,
    "Экономика": 3
}

# кто какую книгу взял (текущие выдачи)
# формат: имя -> {"book": книга, "phone": телефон, "date": дата выдачи, "deadline": срок возврата}
taken_books = {}

# база данных студентов (имя -> телефон)
students = {}

# история операций
history = []


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Библиотека")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Заголовок
        title_label = tk.Label(root, text="Система управления библиотекой",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Фрейм для кнопок
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Кнопки действий
        tk.Button(button_frame, text="Показать книги", command=self.show_books_window,
                  width=20, height=2, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Взять книгу", command=self.take_book_window,
                  width=20, height=2, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Вернуть книгу", command=self.return_book_window,
                  width=20, height=2, bg="#FF9800", fg="white").grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Текущие выдачи", command=self.show_taken_books,
                  width=20, height=2, bg="#9C27B0", fg="white").grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="История студента", command=self.student_history_window,
                  width=20, height=2, bg="#795548", fg="white").grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Вся история", command=self.show_all_history,
                  width=20, height=2, bg="#607D8B", fg="white").grid(row=1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Просроченные книги", command=self.show_overdue_books,
                  width=20, height=2, bg="#F44336", fg="white").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Продлить книгу", command=self.extend_book_window,
                  width=20, height=2, bg="#00BCD4", fg="white").grid(row=2, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Список студентов", command=self.show_students_list,
                  width=20, height=2, bg="#3F51B5", fg="white").grid(row=2, column=2, padx=5, pady=5)

        # Область вывода информации
        self.output_text = scrolledtext.ScrolledText(root, width=100, height=25, font=("Courier", 10))
        self.output_text.pack(pady=10, padx=10)

        # Приветственное сообщение
        self.update_output("Добро пожаловать в библиотеку!\nВыберите действие из меню выше.\n")
        self.update_books_list()

    def validate_phone(self, phone):
        """Проверяет корректность номера телефона"""
        # Удаляем пробелы, скобки и дефисы
        cleaned = phone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

        # Проверяем, что номер состоит из цифр и имеет длину от 10 до 11 цифр
        if not cleaned.isdigit():
            return False, "Номер телефона должен содержать только цифры"

        if len(cleaned) < 10 or len(cleaned) > 12:
            return False, "Номер телефона должен содержать от 10 до 12 цифр"

        return True, cleaned

    def update_output(self, text):
        """Обновляет текст в области вывода"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)

    def add_history_record(self, student, book, action, phone=""):
        """Добавляет запись в историю"""
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        record = {
            "student": student,
            "book": book,
            "action": action,
            "time": timestamp,
            "phone": phone
        }
        history.append(record)

    def update_books_list(self):
        """Обновляет список книг в основном окне"""
        text = "=== СПИСОК КНИГ В БИБЛИОТЕКЕ ===\n\n"
        for book, qty in books.items():
            status = f"{qty} шт"
            if qty == 0:
                status += " (нет в наличии)"
            text += f"{book:30} - {status}\n"
        self.update_output(text)

    def show_books_window(self):
        """Показывает окно со списком книг"""
        self.update_books_list()

    def take_book_window(self):
        """Окно для выдачи книги"""
        window = tk.Toplevel(self.root)
        window.title("Взять книгу")
        window.geometry("500x500")

        # Имя студента
        tk.Label(window, text="Введите имя студента:", font=("Arial", 12)).pack(pady=10)
        name_entry = tk.Entry(window, width=40, font=("Arial", 11))
        name_entry.pack(pady=5)

        # Номер телефона
        tk.Label(window, text="Введите номер телефона:", font=("Arial", 12)).pack(pady=10)
        tk.Label(window, text="(формат: +7 XXX XXX XX XX)", font=("Arial", 9), fg="gray").pack()
        phone_entry = tk.Entry(window, width=40, font=("Arial", 11))
        phone_entry.pack(pady=5)

        tk.Label(window, text="Доступные книги:", font=("Arial", 12)).pack(pady=10)

        # Список доступных книг
        listbox_frame = tk.Frame(window)
        listbox_frame.pack(pady=5)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        book_listbox = tk.Listbox(listbox_frame, width=50, height=10,
                                  yscrollcommand=scrollbar.set, font=("Arial", 10))
        book_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=book_listbox.yview)

        # Заполняем список доступных книг
        available_books = [(book, qty) for book, qty in books.items() if qty > 0]
        for book, qty in available_books:
            book_listbox.insert(tk.END, f"{book} - {qty} шт")

        def take_book():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()

            if not name:
                messagebox.showerror("Ошибка", "Введите имя студента!")
                return

            if not phone:
                messagebox.showerror("Ошибка", "Введите номер телефона!")
                return

            # Проверяем номер телефона
            is_valid, result = self.validate_phone(phone)
            if not is_valid:
                messagebox.showerror("Ошибка", result)
                return
            cleaned_phone = result

            selection = book_listbox.curselection()
            if not selection:
                messagebox.showerror("Ошибка", "Выберите книгу из списка!")
                return

            selected_book = available_books[selection[0]][0]

            if name in taken_books:
                messagebox.showerror("Ошибка",
                                     f"Студент {name} уже взял книгу '{taken_books[name]['book']}'.\nСначала верните её.")
                return

            if books[selected_book] > 0:
                books[selected_book] -= 1

                # Сохраняем информацию о выдаче
                issue_date = datetime.now()
                deadline = issue_date + timedelta(days=14)

                taken_books[name] = {
                    "book": selected_book,
                    "phone": cleaned_phone,
                    "date": issue_date,
                    "deadline": deadline
                }

                # Сохраняем студента в базе
                students[name] = cleaned_phone

                self.add_history_record(name, selected_book, "ВЗЯЛ", cleaned_phone)

                deadline_str = deadline.strftime("%d.%m.%Y")
                messagebox.showinfo("Успех",
                                    f"Книга '{selected_book}' выдана студенту {name}\n"
                                    f"Телефон: {cleaned_phone}\n"
                                    f"Срок возврата: {deadline_str} (через 14 дней)")
                self.update_books_list()
                window.destroy()
            else:
                messagebox.showerror("Ошибка", "Книга закончилась!")

        tk.Button(window, text="Взять книгу", command=take_book,
                  width=20, height=2, bg="#2196F3", fg="white").pack(pady=20)

    def return_book_window(self):
        """Окно для возврата книги"""
        window = tk.Toplevel(self.root)
        window.title("Вернуть книгу")
        window.geometry("400x300")

        tk.Label(window, text="Введите имя студента:", font=("Arial", 12)).pack(pady=20)
        name_entry = tk.Entry(window, width=40, font=("Arial", 11))
        name_entry.pack(pady=10)

        def return_book():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите имя студента!")
                return

            if name in taken_books:
                book_info = taken_books[name]
                book = book_info["book"]
                books[book] += 1

                # Проверяем просрочку
                today = datetime.now()
                deadline = book_info["deadline"]
                days_overdue = (today - deadline).days

                overdue_message = ""
                if days_overdue > 0:
                    overdue_message = f"\nВНИМАНИЕ: Книга просрочена на {days_overdue} дней!"

                self.add_history_record(name, book, "ВЕРНУЛ", book_info["phone"])
                del taken_books[name]

                messagebox.showinfo("Успех",
                                    f"Книга '{book}' возвращена. Спасибо, {name}!{overdue_message}")
                self.update_books_list()
                window.destroy()
            else:
                messagebox.showerror("Ошибка", f"Студент {name} не брал книгу")

        tk.Button(window, text="Вернуть книгу", command=return_book,
                  width=20, height=2, bg="#FF9800", fg="white").pack(pady=20)

    def show_taken_books(self):
        """Показывает текущие выдачи"""
        if not taken_books:
            text = "Нет выданных книг"
        else:
            text = "=== ТЕКУЩИЕ ВЫДАЧИ КНИГ ===\n\n"
            today = datetime.now()

            for student, info in taken_books.items():
                deadline = info["deadline"]
                days_left = (deadline - today).days

                status = ""
                if days_left < 0:
                    status = f" [ПРОСРОЧЕНО на {abs(days_left)} дн.]"
                elif days_left <= 3:
                    status = f" [осталось {days_left} дн.]"
                else:
                    status = f" [осталось {days_left} дн.]"

                text += f"{student:20} - {info['book']:25} - тел: {info['phone']}{status}\n"
                text += f"  Взято: {info['date'].strftime('%d.%m.%Y')} | "
                text += f"Вернуть до: {deadline.strftime('%d.%m.%Y')}\n\n"

        self.update_output(text)

    def show_overdue_books(self):
        """Показывает просроченные книги"""
        if not taken_books:
            text = "Нет выданных книг"
        else:
            today = datetime.now()
            overdue_found = False
            text = "=== ПРОСРОЧЕННЫЕ КНИГИ ===\n\n"

            for student, info in taken_books.items():
                deadline = info["deadline"]
                days_overdue = (today - deadline).days

                if days_overdue > 0:
                    overdue_found = True
                    text += f"СТУДЕНТ: {student}\n"
                    text += f"Телефон: {info['phone']}\n"
                    text += f"Книга: {info['book']}\n"
                    text += f"Просрочено на: {days_overdue} дней\n"
                    text += f"Взято: {info['date'].strftime('%d.%m.%Y')}\n"
                    text += f"Должен был вернуть: {deadline.strftime('%d.%m.%Y')}\n"
                    text += "-" * 40 + "\n\n"

            if not overdue_found:
                text = "Нет просроченных книг"

        self.update_output(text)

    def extend_book_window(self):
        """Окно для продления книги"""
        window = tk.Toplevel(self.root)
        window.title("Продлить книгу")
        window.geometry("400x250")

        tk.Label(window, text="Введите имя студента:", font=("Arial", 12)).pack(pady=20)
        name_entry = tk.Entry(window, width=40, font=("Arial", 11))
        name_entry.pack(pady=10)

        def extend_book():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите имя студента!")
                return

            if name in taken_books:
                book_info = taken_books[name]

                # Продлеваем на 7 дней
                new_deadline = book_info["deadline"] + timedelta(days=7)
                book_info["deadline"] = new_deadline

                self.add_history_record(name, book_info["book"], "ПРОДЛИЛ", book_info["phone"])

                messagebox.showinfo("Успех",
                                    f"Книга '{book_info['book']}' продлена на 7 дней\n"
                                    f"Новый срок возврата: {new_deadline.strftime('%d.%m.%Y')}")

                self.update_books_list()
                window.destroy()
            else:
                messagebox.showerror("Ошибка", f"Студент {name} не брал книгу")

        tk.Button(window, text="Продлить книгу", command=extend_book,
                  width=20, height=2, bg="#00BCD4", fg="white").pack(pady=20)

    def show_students_list(self):
        """Показывает список всех студентов"""
        if not students:
            text = "Список студентов пуст"
        else:
            text = "=== СПИСОК СТУДЕНТОВ ===\n\n"
            for name, phone in students.items():
                has_book = " (есть книга)" if name in taken_books else ""
                text += f"{name:20} - {phone}{has_book}\n"

        self.update_output(text)

    def student_history_window(self):
        """Окно для просмотра истории студента"""
        window = tk.Toplevel(self.root)
        window.title("История студента")
        window.geometry("600x400")

        tk.Label(window, text="Введите имя студента:", font=("Arial", 12)).pack(pady=20)
        name_entry = tk.Entry(window, width=40, font=("Arial", 11))
        name_entry.pack(pady=10)

        def show_history():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите имя студента!")
                return

            student_records = [r for r in history if r["student"].lower() == name.lower()]

            if not student_records:
                messagebox.showinfo("Информация", f"Студент {name} не совершал операций с книгами")
                return

            history_window = tk.Toplevel(window)
            history_window.title(f"История студента {name}")
            history_window.geometry("700x500")

            text_widget = scrolledtext.ScrolledText(history_window, width=80, height=25, font=("Courier", 10))
            text_widget.pack(pady=10, padx=10)

            # Показываем информацию о студенте
            phone = students.get(name, "не указан")
            text = f"=== ИСТОРИЯ ОПЕРАЦИЙ СТУДЕНТА ===\n"
            text += f"Имя: {name}\n"
            text += f"Телефон: {phone}\n"
            text += "=" * 50 + "\n\n"

            for record in student_records:
                text += f"[{record['time']}] {record['action']}: {record['book']}\n"

            text_widget.insert(1.0, text)
            text_widget.config(state=tk.DISABLED)

        tk.Button(window, text="Показать историю", command=show_history,
                  width=20, height=2, bg="#795548", fg="white").pack(pady=20)

    def show_all_history(self):
        """Показывает всю историю"""
        if not history:
            text = "История операций пуста"
        else:
            text = "=== ПОЛНАЯ ИСТОРИЯ ОПЕРАЦИЙ ===\n\n"
            for record in history:
                text += f"[{record['time']}] {record['student']:20} {record['action']}: {record['book']}\n"
        self.update_output(text)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()