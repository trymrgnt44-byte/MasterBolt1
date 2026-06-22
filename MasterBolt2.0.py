import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import hashlib
from datetime import datetime
import sys
import random

# Цветовые темы
THEMES = {
    "Светлая": {
        "bg": "#f0f0f5",
        "fg": "#2c3e50",
        "header_bg": "#2c3e50",
        "header_fg": "#e74c3c",
        "button_bg": "#e74c3c",
        "button_fg": "white",
        "entry_bg": "white",
        "entry_fg": "#2c3e50",
        "tree_bg": "white",
        "tree_fg": "#2c3e50",
        "frame_bg": "#f0f0f5",
        "label_fg": "#2c3e50",
        "select_bg": "#e74c3c",
        "select_fg": "white"
    },
    "Тёмная": {
        "bg": "#1a1a2e",
        "fg": "#ecf0f1",
        "header_bg": "#0f3460",
        "header_fg": "#e94560",
        "button_bg": "#e94560",
        "button_fg": "white",
        "entry_bg": "#16213e",
        "entry_fg": "#ecf0f1",
        "tree_bg": "#16213e",
        "tree_fg": "#ecf0f1",
        "frame_bg": "#1a1a2e",
        "label_fg": "#ecf0f1",
        "select_bg": "#e94560",
        "select_fg": "white"
    }
}


class Database:
    def __init__(self):
        self.users_file = "users.json"
        self.products_file = "products.json"
        self.settings_file = "settings.json"
        self.consent_file = "consent.json"
        self.current_user = None
        self.current_theme = "Светлая"
        self.load_settings()
        self.load_data()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get("theme", "Светлая")
            except:
                pass

    def save_settings(self, theme):
        self.current_theme = theme
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump({"theme": theme}, f, ensure_ascii=False, indent=2)

    def has_consent(self):
        if os.path.exists(self.consent_file):
            try:
                with open(self.consent_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("consent", False)
            except:
                return False
        return False

    def save_consent(self, consent):
        with open(self.consent_file, 'w', encoding='utf-8') as f:
            json.dump({"consent": consent, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False,
                      indent=2)

    def load_data(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {
                "admin": {
                    "password": hashlib.sha256("admin123".encode()).hexdigest(),
                    "role": "admin",
                    "name": "Администратор",
                    "registered": "2024-01-01"
                },
                "user1": {
                    "password": hashlib.sha256("user123".encode()).hexdigest(),
                    "role": "user",
                    "name": "Иван Петров",
                    "registered": "2024-01-15"
                }
            }
            self.save_users()

        if os.path.exists(self.products_file):
            with open(self.products_file, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
        else:
            self.products = self.generate_200_products()
            self.save_products()

    def get_real_options(self):
        return [
            "Li-Ion аккумулятор 2.0 Ач",
            "Li-Ion аккумулятор 4.0 Ач",
            "Li-Ion аккумулятор 5.0 Ач",
            "Быстрая зарядка 30 мин",
            "LED подсветка рабочей зоны",
            "Автоматическая блокировка шпинделя",
            "Электронная регулировка оборотов",
            "Быстрозажимной патрон",
            "Пластиковый кейс в комплекте",
            "Защита от перегрузки",
            "Защита от перегрева",
            "Низкий уровень шума",
            "Магнитный держатель для бит",
            "Реверс",
            "Ударный механизм",
            "Точная фиксация крутящего момента",
            "LED дисплей заряда",
            "Сумка или рюкзак в комплекте",
            "Набор бит 32 шт",
            "Зарядное устройство",
            "Система Anti-Vibration",
            "Электронный тормоз двигателя",
            "Индикатор уровня заряда",
            "Металлический редуктор",
            "Система охлаждения двигателя"
        ]

    def generate_200_products(self):
        brands = ['Makita', 'Bosch', 'DeWALT', 'Metabo', 'Интерскол', 'Bort', 'Greenworks',
                  'Ryobi', 'Hitachi', 'AEG', 'Milwaukee', 'Sparky', 'Einhell', 'Black+Decker',
                  'CROWN', 'Xiaomi', 'Kolner', 'TROUVER', 'Zubr', 'Caliber']

        types = ['Бесщеточный', 'Щеточный']
        power_types = ['Аккумуляторный', 'Сетевой']
        chucks = ['6.35 мм (HEX)', '10 мм', '13 мм', '16 мм', '1/4"']
        voltages = ['10.8 В', '12 В', '14.4 В', '18 В', '20 В', '21 В', '24 В', '36 В', '40 В']
        max_torques = ['20 Н·м', '30 Н·м', '40 Н·м', '45 Н·м', '50 Н·м', '56 Н·м', '60 Н·м', '70 Н·м', '80 Н·м',
                       '100 Н·м', '120 Н·м', '150 Н·м']
        speeds = ['0-400 об/мин', '0-500/0-1800 об/мин', '0-450/0-1500 об/мин', '0-500/0-1900 об/мин',
                  '0-600/0-2000 об/мин', '0-650 об/мин']

        products = []

        for i in range(1, 201):
            brand = random.choice(brands)
            model_num = random.randint(100, 999)
            name = f"{brand} {model_num}{random.choice(['X', 'R', 'L', 'F', 'G', 'PRO', 'MAX', 'Plus', 'Ultra'])}"

            all_options = self.get_real_options()
            num_options = random.randint(2, 6)
            selected_options = random.sample(all_options, num_options)

            product = {
                "id": i,
                "Модель": name,
                "Производитель": brand,
                "Тип питания": random.choice(power_types),
                "Тип двигателя": random.choice(types),
                "Размер патрона": random.choice(chucks),
                "Дополнительные опции": '; '.join(selected_options),
                "Количество": random.randint(0, 50),
                "Цена": random.randint(3000, 35000),
                "in_stock": random.choice([True, True, True, False]),
                "Напряжение": random.choice(voltages),
                "Макс. момент": random.choice(max_torques),
                "Скорость вращения": random.choice(speeds),
                "Вес": f"{random.randint(8, 35) / 10:.1f} кг",
                "Описание": f"{brand} - {random.choice(['профессиональный', 'полупрофессиональный', 'бытовой'])} шуруповерт. {random.choice(['Высокая надежность', 'Отличная производительность', 'Долговечность', 'Эргономичный дизайн'])}. Подходит для {random.choice(['строительства', 'ремонта', 'монтажных работ', 'сборки мебели'])}."
            }
            products.append(product)

        return products

    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def save_products(self):
        with open(self.products_file, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)

    def authenticate(self, username, password):
        if username in self.users:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            if self.users[username]["password"] == hashed:
                self.current_user = {"username": username, "role": self.users[username]["role"],
                                     "name": self.users[username]["name"]}
                return True
        return False

    def register_user(self, username, password, name):
        if username in self.users:
            return False, "Пользователь уже существует"
        if len(password) < 4:
            return False, "Пароль должен быть не менее 4 символов"

        self.users[username] = {
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "role": "user",
            "name": name,
            "registered": datetime.now().strftime("%Y-%m-%d")
        }
        self.save_users()
        return True, "Регистрация успешна"

    def add_product(self, product):
        product["id"] = max([p["id"] for p in self.products], default=0) + 1
        self.products.append(product)
        self.save_products()

    def update_product(self, product_id, updated_data):
        for i, p in enumerate(self.products):
            if p["id"] == product_id:
                self.products[i].update(updated_data)
                self.save_products()
                return True
        return False

    def delete_product(self, product_id):
        self.products = [p for p in self.products if p["id"] != product_id]
        self.save_products()

    def get_product_by_id(self, product_id):
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None


class CopyPasteEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)
        self.bind("<Control-x>", self.cut)
        self.bind("<Button-3>", self.show_context_menu)

    def copy(self, event=None):
        self.clipboard_clear()
        try:
            text = self.selection_get()
            self.clipboard_append(text)
        except:
            pass
        return "break"

    def paste(self, event=None):
        try:
            text = self.clipboard_get()
            self.insert(tk.INSERT, text)
        except:
            pass
        return "break"

    def cut(self, event=None):
        self.copy()
        try:
            self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            pass
        return "break"

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Копировать", command=self.copy)
        menu.add_command(label="Вставить", command=self.paste)
        menu.add_command(label="Вырезать", command=self.cut)
        menu.post(event.x_root, event.y_root)


class CopyPasteText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)
        self.bind("<Control-x>", self.cut)
        self.bind("<Button-3>", self.show_context_menu)

    def copy(self, event=None):
        self.clipboard_clear()
        try:
            text = self.selection_get()
            self.clipboard_append(text)
        except:
            pass
        return "break"

    def paste(self, event=None):
        try:
            text = self.clipboard_get()
            self.insert(tk.INSERT, text)
        except:
            pass
        return "break"

    def cut(self, event=None):
        self.copy()
        try:
            self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            pass
        return "break"

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Копировать", command=self.copy)
        menu.add_command(label="Вставить", command=self.paste)
        menu.add_command(label="Вырезать", command=self.cut)
        menu.post(event.x_root, event.y_root)


class ConsentWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("Согласие на обработку персональных данных")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        theme = THEMES["Светлая"]
        self.window.configure(bg=theme["bg"])

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def create_widgets(self):
        theme = THEMES["Светлая"]

        main_frame = tk.Frame(self.window, bg=theme["bg"])
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        title = tk.Label(main_frame, text="СОГЛАСИЕ НА ОБРАБОТКУ ПЕРСОНАЛЬНЫХ ДАННЫХ",
                         font=("Arial", 14, "bold"), bg=theme["bg"], fg=theme["fg"])
        title.pack(pady=(0, 20))

        text_frame = tk.Frame(main_frame, bg=theme["bg"])
        text_frame.pack(fill="both", expand=True)

        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 10),
                              bg=theme["entry_bg"], fg=theme["entry_fg"],
                              relief="solid", bd=1, height=15)
        text_widget.pack(fill="both", expand=True, side="left")

        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        consent_text = """
Уважаемый пользователь!

Программа "МастерБолт" (далее - Программа) собирает и обрабатывает следующие персональные данные:

1. Имя пользователя (указывается при регистрации)
2. Логин для входа в систему
3. Дата регистрации
4. Роль пользователя (администратор/пользователь)

Цель сбора персональных данных:
- Идентификация пользователя при входе в систему
- Разграничение прав доступа (администратор/пользователь)
- Ведение истории действий в системе

Ваши персональные данные хранятся в зашифрованном виде в локальном файле users.json
на вашем устройстве. Программа не передает ваши данные третьим лицам.

Вы имеете право:
- Отказаться от предоставления персональных данных
- Запросить удаление ваших данных
- Изменить свои данные

Согласие на обработку персональных данных может быть отозвано в любое время
путем удаления файла users.json.

Нажимая "Принимаю", вы подтверждаете, что ознакомлены с условиями обработки
персональных данных и даете согласие на их обработку.

Если вы не принимаете условия, программа будет закрыта.
"""

        text_widget.insert("1.0", consent_text)
        text_widget.config(state="disabled")

        button_frame = tk.Frame(main_frame, bg=theme["bg"])
        button_frame.pack(pady=20)

        accept_btn = tk.Button(button_frame, text="ПРИНИМАЮ", command=self.accept,
                               bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                               padx=30, pady=10, cursor="hand2", relief="flat")
        accept_btn.pack(side="left", padx=10)

        decline_btn = tk.Button(button_frame, text="НЕ ПРИНИМАЮ", command=self.decline,
                                bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                                padx=30, pady=10, cursor="hand2", relief="flat")
        decline_btn.pack(side="left", padx=10)

    def accept(self):
        self.window.destroy()
        self.callback(True)

    def decline(self):
        self.window.destroy()
        self.callback(False)

    def on_close(self):
        self.window.destroy()
        self.callback(False)


class MasterBoltApp:
    def __init__(self):
        self.db = Database()

        if not self.db.has_consent():
            self.show_consent_window()
        else:
            self.start_app()

    def show_consent_window(self):
        consent_window = ConsentWindow(None, self.on_consent_result)
        consent_window.window.wait_window()

    def on_consent_result(self, consent):
        if consent:
            self.db.save_consent(True)
            self.start_app()
        else:
            messagebox.showwarning("Внимание",
                                   "Вы не дали согласие на обработку персональных данных. Программа будет закрыта.")
            sys.exit(0)

    def start_app(self):
        self.window = tk.Tk()
        self.window.title("МастерБолт - Шуруповерты")
        self.window.geometry("1400x800")
        self.apply_theme()

        self.show_main_menu()
        self.window.mainloop()

    def apply_theme(self):
        theme = THEMES[self.db.current_theme]
        self.window.configure(bg=theme["bg"])

    def show_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        theme = THEMES[self.db.current_theme]
        self.window.configure(bg=theme["bg"])

        main_container = tk.Frame(self.window, bg=theme["bg"])
        main_container.pack(fill="both", expand=True)

        left_panel = tk.Frame(main_container, bg=theme["header_bg"], width=450)
        left_panel.pack(side="left", fill="both", expand=True)
        left_panel.pack_propagate(False)

        left_content = tk.Frame(left_panel, bg=theme["header_bg"])
        left_content.place(relx=0.5, rely=0.5, anchor="center")

        logo = tk.Label(left_content, text="🔧", font=("Arial", 60), bg=theme["header_bg"], fg=theme["header_fg"])
        logo.pack()

        title = tk.Label(left_content, text="МАСТЕРБОЛТ", font=("Arial", 36, "bold"),
                         bg=theme["header_bg"], fg=theme["header_fg"])
        title.pack(pady=(10, 5))

        subtitle = tk.Label(left_content, text="ШУРУПОВЕРТЫ", font=("Arial", 20),
                            bg=theme["header_bg"], fg="white")
        subtitle.pack()

        slogan_frame = tk.Frame(left_content, bg=theme["header_bg"])
        slogan_frame.pack(pady=40)

        slogan1 = tk.Label(slogan_frame, text="ЗАВЕРТЕЛ", font=("Arial", 26, "bold"),
                           bg=theme["header_bg"], fg=theme["header_fg"])
        slogan1.pack()

        slogan2 = tk.Label(slogan_frame, text="И ДЕЛО", font=("Arial", 26, "bold"),
                           bg=theme["header_bg"], fg=theme["header_fg"])
        slogan2.pack()

        slogan3 = tk.Label(slogan_frame, text="В ШЛЯПЕ", font=("Arial", 26, "bold"),
                           bg=theme["header_bg"], fg=theme["header_fg"])
        slogan3.pack()

        right_panel = tk.Frame(main_container, bg=theme["bg"])
        right_panel.pack(side="right", fill="both", expand=True)

        welcome = tk.Label(right_panel, text="Добро пожаловать!", font=("Arial", 26, "bold"),
                           bg=theme["bg"], fg=theme["fg"])
        welcome.pack(pady=(60, 10))

        welcome_sub = tk.Label(right_panel, text="Войдите в свой аккаунт", font=("Arial", 14),
                               bg=theme["bg"], fg="#7f8c8d")
        welcome_sub.pack(pady=(0, 40))

        login_frame = tk.Frame(right_panel, bg=theme["bg"])
        login_frame.pack(pady=10)

        tk.Label(login_frame, text="Логин", font=("Arial", 12), bg=theme["bg"], fg=theme["fg"]).pack(anchor="w",
                                                                                                     pady=(0, 5))
        self.login_entry = CopyPasteEntry(login_frame, font=("Arial", 12), width=30, bg=theme["entry_bg"],
                                          fg=theme["entry_fg"],
                                          relief="solid", bd=1, highlightthickness=0)
        self.login_entry.pack(pady=(0, 20), ipady=8)

        tk.Label(login_frame, text="Пароль", font=("Arial", 12), bg=theme["bg"], fg=theme["fg"]).pack(anchor="w",
                                                                                                      pady=(0, 5))
        self.password_entry = CopyPasteEntry(login_frame, font=("Arial", 12), width=30, bg=theme["entry_bg"],
                                             fg=theme["entry_fg"],
                                             relief="solid", bd=1, highlightthickness=0, show="*")
        self.password_entry.pack(pady=(0, 30), ipady=8)

        login_btn = tk.Button(login_frame, text="ВОЙТИ", command=self.login,
                              bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 12, "bold"),
                              width=25, height=1, cursor="hand2", relief="flat")
        login_btn.pack(pady=5)

        register_btn = tk.Button(login_frame, text="СОЗДАТЬ АККАУНТ", command=self.show_register_form,
                                 bg=theme["bg"], fg=theme["button_bg"], font=("Arial", 11, "bold"),
                                 width=25, height=1, cursor="hand2", relief="solid", bd=1)
        register_btn.pack(pady=10)

        info = tk.Label(right_panel, text="Тестовые аккаунты:\nАдмин: admin / admin123\nПользователь: user1 / user123",
                        font=("Arial", 9), bg=theme["bg"], fg="#95a5a6", justify="center")
        info.pack(pady=(30, 0))

        settings_btn = tk.Button(right_panel, text="НАСТРОЙКИ", command=self.show_settings,
                                 bg=theme["header_bg"], fg="white", font=("Arial", 10),
                                 cursor="hand2", relief="flat", padx=15, pady=5)
        settings_btn.pack(pady=(10, 0))

    def show_settings(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Настройки")
        settings_window.geometry("500x450")
        settings_window.configure(bg=THEMES[self.db.current_theme]["bg"])
        settings_window.resizable(False, False)
        settings_window.transient(self.window)
        settings_window.grab_set()

        theme = THEMES[self.db.current_theme]

        tk.Label(settings_window, text="НАСТРОЙКИ", font=("Arial", 20, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(20, 30))

        theme_frame = tk.Frame(settings_window, bg=theme["bg"])
        theme_frame.pack(pady=10, padx=30, fill="x")

        tk.Label(theme_frame, text="Тема оформления:", font=("Arial", 12),
                 bg=theme["bg"], fg=theme["fg"]).pack(side="left", padx=(0, 20))

        theme_var = tk.StringVar(value=self.db.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=["Светлая", "Тёмная"],
                                   state="readonly", width=15)
        theme_combo.pack(side="left")

        def change_theme():
            new_theme = theme_var.get()
            if new_theme != self.db.current_theme:
                if messagebox.askyesno("Подтверждение",
                                       f"Вы хотите изменить тему на '{new_theme}'?\nДля применения изменений потребуется перезапуск программы."):
                    self.db.save_settings(new_theme)
                    messagebox.showinfo("Успех", f"Тема изменена на '{new_theme}'\nПриложение будет перезапущено.")
                    settings_window.destroy()
                    self.window.destroy()
                    MasterBoltApp()
                else:
                    theme_var.set(self.db.current_theme)

        apply_btn = tk.Button(theme_frame, text="ПРИМЕНИТЬ", command=change_theme,
                              bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 10, "bold"),
                              padx=15, pady=5, cursor="hand2", relief="flat")
        apply_btn.pack(side="left", padx=(20, 0))

        info_frame = tk.Frame(settings_window, bg=theme["bg"], relief="groove", bd=2)
        info_frame.pack(pady=30, padx=30, fill="both", expand=True)

        tk.Label(info_frame, text="ИНФОРМАЦИЯ О ПРОГРАММЕ", font=("Arial", 12, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(15, 10))

        tk.Label(info_frame, text="Разработчик:", font=("Arial", 10, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack()
        tk.Label(info_frame, text="Куколь Александра Владимировна", font=("Arial", 10),
                 bg=theme["bg"], fg=theme["fg"]).pack()

        tk.Label(info_frame, text="Группа:", font=("Arial", 10, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(10, 0))
        tk.Label(info_frame, text="ИС-941", font=("Arial", 10),
                 bg=theme["bg"], fg=theme["fg"]).pack()

        tk.Label(info_frame, text="2024 МастерБолт", font=("Arial", 9),
                 bg=theme["bg"], fg="#7f8c8d").pack(pady=(15, 10))

        close_btn = tk.Button(settings_window, text="ЗАКРЫТЬ", command=settings_window.destroy,
                              bg="#7f8c8d", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, cursor="hand2", relief="flat")
        close_btn.pack(pady=20)

    def show_register_form(self):
        theme = THEMES[self.db.current_theme]
        reg_window = tk.Toplevel(self.window)
        reg_window.title("Регистрация")
        reg_window.geometry("450x550")
        reg_window.configure(bg=theme["bg"])
        reg_window.resizable(False, False)
        reg_window.transient(self.window)
        reg_window.grab_set()

        tk.Label(reg_window, text="Создать аккаунт", font=("Arial", 20, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(30, 20))

        form_frame = tk.Frame(reg_window, bg=theme["bg"])
        form_frame.pack(pady=10, padx=40)

        tk.Label(form_frame, text="Ваше имя", font=("Arial", 11), bg=theme["bg"], fg=theme["fg"]).pack(anchor="w",
                                                                                                       pady=(0, 5))
        name_entry = CopyPasteEntry(form_frame, font=("Arial", 11), width=30, bg=theme["entry_bg"],
                                    fg=theme["entry_fg"], relief="solid", bd=1)
        name_entry.pack(pady=(0, 15), ipady=8)

        tk.Label(form_frame, text="Логин", font=("Arial", 11), bg=theme["bg"], fg=theme["fg"]).pack(anchor="w",
                                                                                                    pady=(0, 5))
        login_entry = CopyPasteEntry(form_frame, font=("Arial", 11), width=30, bg=theme["entry_bg"],
                                     fg=theme["entry_fg"], relief="solid", bd=1)
        login_entry.pack(pady=(0, 15), ipady=8)

        tk.Label(form_frame, text="Пароль (мин. 4 символа)", font=("Arial", 11), bg=theme["bg"], fg=theme["fg"]).pack(
            anchor="w", pady=(0, 5))
        password_entry = CopyPasteEntry(form_frame, font=("Arial", 11), width=30, bg=theme["entry_bg"],
                                        fg=theme["entry_fg"], relief="solid", bd=1, show="*")
        password_entry.pack(pady=(0, 25), ipady=8)

        def register():
            name = name_entry.get()
            login = login_entry.get()
            password = password_entry.get()

            if not all([name, login, password]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            success, msg = self.db.register_user(login, password, name)
            if success:
                messagebox.showinfo("Успех", msg)
                reg_window.destroy()
            else:
                messagebox.showerror("Ошибка", msg)

        register_btn = tk.Button(form_frame, text="ЗАРЕГИСТРИРОВАТЬСЯ", command=register,
                                 bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 11, "bold"),
                                 width=25, height=1, cursor="hand2", relief="flat")
        register_btn.pack(pady=10)

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return

        if self.db.authenticate(username, password):
            self.window.destroy()
            if self.db.current_user["role"] == "admin":
                panel = AdminPanel(self.db)
            else:
                panel = UserPanel(self.db)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")


class UserPanel:
    def __init__(self, db):
        self.db = db
        self.all_products = db.products
        self.filtered_products = self.all_products.copy()

        self.window = tk.Tk()
        self.window.title(f"МастерБолт - {db.current_user['name']}")
        self.window.geometry("1400x800")
        self.apply_theme()

        self.setup_ui()
        self.window.mainloop()

    def apply_theme(self):
        theme = THEMES[self.db.current_theme]
        self.window.configure(bg=theme["bg"])
        # Применяем тему ко всем дочерним виджетам
        for widget in self.window.winfo_children():
            self.apply_theme_to_widget(widget, theme)

    def apply_theme_to_widget(self, widget, theme):
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.Label, tk.Button, tk.Entry, tk.Text, ttk.Combobox)):
                if isinstance(widget, tk.LabelFrame):
                    widget.configure(bg=theme["bg"], fg=theme["fg"])
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=theme["bg"], fg=theme["fg"])
                elif isinstance(widget, tk.Button):
                    if widget.cget("bg") not in ["#27ae60", "#3498db", "#e74c3c", "#9b59b6", "#7f8c8d"]:
                        widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
                elif isinstance(widget, (tk.Entry, tk.Text)):
                    widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
        except:
            pass
        for child in widget.winfo_children():
            self.apply_theme_to_widget(child, theme)

    def setup_ui(self):
        theme = THEMES[self.db.current_theme]

        header = tk.Frame(self.window, bg=theme["header_bg"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="МАСТЕРБОЛТ", font=("Arial", 20, "bold"),
                 bg=theme["header_bg"], fg=theme["header_fg"]).pack(side="left", padx=30, pady=20)

        settings_btn = tk.Button(header, text="Настройки", command=self.show_settings,
                                 bg=theme["header_bg"], fg="white", font=("Arial", 12),
                                 cursor="hand2", relief="flat")
        settings_btn.pack(side="left", padx=10)

        user_frame = tk.Frame(header, bg=theme["header_bg"])
        user_frame.pack(side="right", padx=30)

        tk.Label(user_frame, text=f"Пользователь: {self.db.current_user['name']}",
                 font=("Arial", 12), bg=theme["header_bg"], fg="white").pack(side="left")

        logout_btn = tk.Button(user_frame, text="Выйти", command=self.logout,
                               bg=theme["button_bg"], fg="white", cursor="hand2", relief="flat", padx=15)
        logout_btn.pack(side="left", padx=(15, 0))

        # Панель поиска
        filter_frame = tk.LabelFrame(self.window, text="ПОИСК И ФИЛЬТРАЦИЯ",
                                     font=("Arial", 12, "bold"), bg=theme["bg"],
                                     fg=theme["fg"], padx=15, pady=15)
        filter_frame.pack(fill="x", padx=20, pady=15)

        row1 = tk.Frame(filter_frame, bg=theme["bg"])
        row1.pack(fill="x", pady=5)

        tk.Label(row1, text="Модель:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left", padx=5)
        self.model_entry = CopyPasteEntry(row1, width=20, font=("Arial", 10), bg=theme["entry_bg"],
                                          fg=theme["entry_fg"], relief="solid", bd=1)
        self.model_entry.pack(side="left", padx=5)

        tk.Label(row1, text="Производитель:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                       padx=(20, 5))
        self.brand_combo = ttk.Combobox(row1, width=15, state="readonly")
        brands = sorted(list(set([p.get("Производитель", "") for p in self.all_products])))
        self.brand_combo['values'] = ['Все'] + brands
        self.brand_combo.set('Все')
        self.brand_combo.pack(side="left", padx=5)

        tk.Label(row1, text="Тип питания:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                     padx=(20, 5))
        self.power_combo = ttk.Combobox(row1, width=15, state="readonly")
        self.power_combo['values'] = ['Все', 'Аккумуляторный', 'Сетевой']
        self.power_combo.set('Все')
        self.power_combo.pack(side="left", padx=5)

        row2 = tk.Frame(filter_frame, bg=theme["bg"])
        row2.pack(fill="x", pady=5)

        tk.Label(row2, text="Тип двигателя:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                       padx=5)
        self.motor_combo = ttk.Combobox(row2, width=15, state="readonly")
        self.motor_combo['values'] = ['Все', 'Бесщеточный', 'Щеточный']
        self.motor_combo.set('Все')
        self.motor_combo.pack(side="left", padx=5)

        tk.Label(row2, text="Размер патрона:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                        padx=(20, 5))
        self.chuck_combo = ttk.Combobox(row2, width=15, state="readonly")
        chucks = sorted(list(set([p.get("Размер патрона", "") for p in self.all_products])))
        self.chuck_combo['values'] = ['Все'] + chucks
        self.chuck_combo.set('Все')
        self.chuck_combo.pack(side="left", padx=5)

        tk.Label(row2, text="Напряжение:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                    padx=(20, 5))
        self.voltage_combo = ttk.Combobox(row2, width=12, state="readonly")
        voltages = sorted(list(set([p.get("Напряжение", "") for p in self.all_products])))
        self.voltage_combo['values'] = ['Все'] + voltages
        self.voltage_combo.set('Все')
        self.voltage_combo.pack(side="left", padx=5)

        row3 = tk.Frame(filter_frame, bg=theme["bg"])
        row3.pack(fill="x", pady=5)

        tk.Label(row3, text="Макс. момент:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                      padx=5)
        self.torque_combo = ttk.Combobox(row3, width=12, state="readonly")
        torques = sorted(list(set([p.get("Макс. момент", "") for p in self.all_products])))
        self.torque_combo['values'] = ['Все'] + torques
        self.torque_combo.set('Все')
        self.torque_combo.pack(side="left", padx=5)

        tk.Label(row3, text="Дополнительные опции:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(
            side="left", padx=5)
        self.options_entry = CopyPasteEntry(row3, width=25, font=("Arial", 10), bg=theme["entry_bg"],
                                            fg=theme["entry_fg"], relief="solid", bd=1)
        self.options_entry.pack(side="left", padx=5)

        tk.Label(row3, text="Цена от:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                 padx=(20, 5))
        self.price_from = CopyPasteEntry(row3, width=8, font=("Arial", 10), bg=theme["entry_bg"], fg=theme["entry_fg"],
                                         relief="solid", bd=1)
        self.price_from.pack(side="left", padx=5)

        tk.Label(row3, text="до:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left", padx=5)
        self.price_to = CopyPasteEntry(row3, width=8, font=("Arial", 10), bg=theme["entry_bg"], fg=theme["entry_fg"],
                                       relief="solid", bd=1)
        self.price_to.pack(side="left", padx=5)

        btn_frame = tk.Frame(filter_frame, bg=theme["bg"])
        btn_frame.pack(fill="x", pady=(15, 5))

        search_btn = tk.Button(btn_frame, text="ПОИСК", command=self.search_products,
                               bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 10, "bold"),
                               padx=25, pady=8, cursor="hand2", relief="flat")
        search_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(btn_frame, text="СБРОСИТЬ", command=self.reset_filters,
                              bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                              padx=25, pady=8, cursor="hand2", relief="flat")
        reset_btn.pack(side="left", padx=5)

        show_all_btn = tk.Button(btn_frame, text="ПОКАЗАТЬ ВСЕ", command=self.show_all,
                                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                 padx=25, pady=8, cursor="hand2", relief="flat")
        show_all_btn.pack(side="left", padx=5)

        export_btn = tk.Button(btn_frame, text="ЭКСПОРТ EXCEL", command=self.export_excel,
                               bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                               padx=25, pady=8, cursor="hand2", relief="flat")
        export_btn.pack(side="right", padx=5)

        # Таблица
        table_frame = tk.Frame(self.window, bg=theme["bg"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ('Модель', 'Производитель', 'Тип питания', 'Тип двигателя',
                   'Размер патрона', 'Напряжение', 'Макс. момент', 'Дополнительные опции', 'Цена')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background=theme["tree_bg"],
                        foreground=theme["tree_fg"],
                        fieldbackground=theme["tree_bg"],
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background=theme["header_bg"],
                        foreground="white",
                        font=("Arial", 10, "bold"))
        style.map('Treeview', background=[('selected', theme["select_bg"])])

        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20, style="Treeview")

        col_widths = {'Модель': 180, 'Производитель': 100, 'Тип питания': 90,
                      'Тип двигателя': 100, 'Размер патрона': 90, 'Напряжение': 80,
                      'Макс. момент': 80, 'Дополнительные опции': 200, 'Цена': 100}

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), anchor='center')

        self.tree.column('Модель', anchor='w')
        self.tree.column('Дополнительные опции', anchor='w')
        self.tree.column('Цена', anchor='e')

        self.tree.bind("<Control-c>", self.copy_from_tree)
        self.tree.bind("<Button-3>", self.show_tree_context_menu)

        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        bottom_frame = tk.Frame(self.window, bg=theme["bg"], height=40)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        self.count_label = tk.Label(bottom_frame, text="", font=("Arial", 10),
                                    bg=theme["bg"], fg="#7f8c8d")
        self.count_label.pack(side="left")

        buy_btn = tk.Button(bottom_frame, text="КУПИТЬ", command=self.buy_product,
                            bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 11, "bold"),
                            padx=30, pady=8, cursor="hand2", relief="flat")
        buy_btn.pack(side="right", padx=5)

        details_btn = tk.Button(bottom_frame, text="ПОДРОБНЕЕ", command=self.show_details,
                                bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                                padx=30, pady=8, cursor="hand2", relief="flat")
        details_btn.pack(side="right", padx=5)

        self.tree.bind("<Double-1>", lambda e: self.show_details())

        self.load_products(self.filtered_products)

    def copy_from_tree(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        text_to_copy = []
        for item in selected:
            values = self.tree.item(item, 'values')
            text_to_copy.append('\t'.join(str(v) for v in values))
        self.window.clipboard_clear()
        self.window.clipboard_append('\n'.join(text_to_copy))

    def show_tree_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.window, tearoff=0)
            menu.add_command(label="Копировать строку", command=self.copy_from_tree)
            menu.add_command(label="Копировать всё", command=self.copy_all_from_tree)
            menu.post(event.x_root, event.y_root)

    def copy_all_from_tree(self):
        text_to_copy = []
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            text_to_copy.append('\t'.join(str(v) for v in values))
        self.window.clipboard_clear()
        self.window.clipboard_append('\n'.join(text_to_copy))
        messagebox.showinfo("Копирование", f"Скопировано {len(text_to_copy)} строк")

    def show_settings(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Настройки")
        settings_window.geometry("500x450")
        settings_window.configure(bg=THEMES[self.db.current_theme]["bg"])
        settings_window.resizable(False, False)
        settings_window.transient(self.window)
        settings_window.grab_set()

        theme = THEMES[self.db.current_theme]

        tk.Label(settings_window, text="НАСТРОЙКИ", font=("Arial", 20, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(20, 30))

        theme_frame = tk.Frame(settings_window, bg=theme["bg"])
        theme_frame.pack(pady=10, padx=30, fill="x")

        tk.Label(theme_frame, text="Тема оформления:", font=("Arial", 12),
                 bg=theme["bg"], fg=theme["fg"]).pack(side="left", padx=(0, 20))

        theme_var = tk.StringVar(value=self.db.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=["Светлая", "Тёмная"],
                                   state="readonly", width=15)
        theme_combo.pack(side="left")

        def change_theme():
            new_theme = theme_var.get()
            if new_theme != self.db.current_theme:
                if messagebox.askyesno("Подтверждение",
                                       f"Вы хотите изменить тему на '{new_theme}'?\nДля применения изменений потребуется перезапуск программы."):
                    self.db.save_settings(new_theme)
                    messagebox.showinfo("Успех", f"Тема изменена на '{new_theme}'\nПриложение будет перезапущено.")
                    settings_window.destroy()
                    self.window.destroy()
                    MasterBoltApp()
                else:
                    theme_var.set(self.db.current_theme)

        apply_btn = tk.Button(theme_frame, text="ПРИМЕНИТЬ", command=change_theme,
                              bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 10, "bold"),
                              padx=15, pady=5, cursor="hand2", relief="flat")
        apply_btn.pack(side="left", padx=(20, 0))

        info_frame = tk.Frame(settings_window, bg=theme["bg"], relief="groove", bd=2)
        info_frame.pack(pady=30, padx=30, fill="both", expand=True)

        tk.Label(info_frame, text="ИНФОРМАЦИЯ О ПРОГРАММЕ", font=("Arial", 12, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(15, 10))

        tk.Label(info_frame, text="Разработчик:", font=("Arial", 10, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack()
        tk.Label(info_frame, text="Куколь Александра Владимировна", font=("Arial", 10),
                 bg=theme["bg"], fg=theme["fg"]).pack()

        tk.Label(info_frame, text="Группа:", font=("Arial", 10, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(10, 0))
        tk.Label(info_frame, text="ИС-941", font=("Arial", 10),
                 bg=theme["bg"], fg=theme["fg"]).pack()

        tk.Label(info_frame, text="2024 МастерБолт", font=("Arial", 9),
                 bg=theme["bg"], fg="#7f8c8d").pack(pady=(15, 10))

        close_btn = tk.Button(settings_window, text="ЗАКРЫТЬ", command=settings_window.destroy,
                              bg="#7f8c8d", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, cursor="hand2", relief="flat")
        close_btn.pack(pady=20)

    def search_products(self):
        model = self.model_entry.get().lower()
        brand = self.brand_combo.get()
        power = self.power_combo.get()
        motor = self.motor_combo.get()
        chuck = self.chuck_combo.get()
        voltage = self.voltage_combo.get()
        torque = self.torque_combo.get()
        options = self.options_entry.get().lower()
        price_from = self.price_from.get()
        price_to = self.price_to.get()

        filtered = []
        for p in self.all_products:
            if model and model not in p.get('Модель', '').lower():
                continue
            if brand != 'Все' and p.get('Производитель', '') != brand:
                continue
            if power != 'Все' and p.get('Тип питания', '') != power:
                continue
            if motor != 'Все' and p.get('Тип двигателя', '') != motor:
                continue
            if chuck != 'Все' and p.get('Размер патрона', '') != chuck:
                continue
            if voltage != 'Все' and p.get('Напряжение', '') != voltage:
                continue
            if torque != 'Все' and p.get('Макс. момент', '') != torque:
                continue
            if options and options not in p.get('Дополнительные опции', '').lower():
                continue
            if price_from:
                try:
                    if p.get('Цена', 0) < int(price_from):
                        continue
                except:
                    pass
            if price_to:
                try:
                    if p.get('Цена', 0) > int(price_to):
                        continue
                except:
                    pass
            filtered.append(p)

        self.filtered_products = filtered
        self.load_products(filtered)

    def reset_filters(self):
        self.model_entry.delete(0, tk.END)
        self.brand_combo.set('Все')
        self.power_combo.set('Все')
        self.motor_combo.set('Все')
        self.chuck_combo.set('Все')
        self.voltage_combo.set('Все')
        self.torque_combo.set('Все')
        self.options_entry.delete(0, tk.END)
        self.price_from.delete(0, tk.END)
        self.price_to.delete(0, tk.END)
        self.search_products()

    def show_all(self):
        self.reset_filters()

    def load_products(self, products):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in products:
            options = p.get('Дополнительные опции', '')
            if len(options) > 50:
                options = options[:47] + '...'

            self.tree.insert('', 'end', values=(
                p.get('Модель', ''),
                p.get('Производитель', ''),
                p.get('Тип питания', ''),
                p.get('Тип двигателя', ''),
                p.get('Размер патрона', ''),
                p.get('Напряжение', ''),
                p.get('Макс. момент', ''),
                options,
                f"{p.get('Цена', 0):,} руб"
            ))

        self.count_label.config(text=f"Найдено товаров: {len(products)} из {len(self.all_products)}")

    def buy_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите товар для покупки")
            return

        item = self.tree.item(selection[0])
        model = item['values'][0]
        product = next((p for p in self.filtered_products if p.get('Модель') == model), None)

        if product and product.get('Количество', 0) > 0:
            msg = f"Товар добавлен в корзину!\n\n"
            msg += f"Модель: {product.get('Модель')}\n"
            msg += f"Производитель: {product.get('Производитель')}\n"
            msg += f"Цена: {product.get('Цена'):,} руб"
            messagebox.showinfo("Корзина", msg)
        else:
            messagebox.showerror("Ошибка", "Товар временно недоступен")

    def show_details(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите товар для просмотра")
            return

        item = self.tree.item(selection[0])
        model = item['values'][0]
        product = next((p for p in self.filtered_products if p.get('Модель') == model), None)

        if product:
            self.show_product_details(product)

    def show_product_details(self, product):
        theme = THEMES[self.db.current_theme]
        detail = tk.Toplevel(self.window)
        detail.title(f"Детали - {product.get('Модель')}")
        detail.geometry("650x750")
        detail.configure(bg=theme["bg"])

        header = tk.Frame(detail, bg=theme["header_bg"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=product.get('Модель'), font=("Arial", 16, "bold"),
                 bg=theme["header_bg"], fg="white").pack(pady=20)

        info_frame = tk.Frame(detail, bg=theme["bg"], padx=30, pady=20)
        info_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(info_frame, bg=theme["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme["bg"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        specs = [
            ("Производитель", product.get('Производитель')),
            ("Тип питания", product.get('Тип питания')),
            ("Тип двигателя", product.get('Тип двигателя')),
            ("Размер патрона", product.get('Размер патрона')),
            ("Напряжение", product.get('Напряжение', '—')),
            ("Макс. момент", product.get('Макс. момент', '—')),
            ("Скорость вращения", product.get('Скорость вращения', '—')),
            ("Вес", product.get('Вес', '—')),
            ("Дополнительные опции", product.get('Дополнительные опции', '—')),
            ("Количество", f"{product.get('Количество')} шт."),
            ("Цена", f"{product.get('Цена'):,} руб")
        ]

        for label, value in specs:
            row = tk.Frame(scrollable_frame, bg=theme["bg"])
            row.pack(fill="x", pady=8)

            tk.Label(row, text=f"{label}:", font=("Arial", 11, "bold"),
                     bg=theme["bg"], fg=theme["fg"], width=20, anchor="w").pack(side="left")

            if label == "Дополнительные опции" and len(str(value)) > 50:
                text_widget = CopyPasteText(row, font=("Arial", 10), bg=theme["entry_bg"], fg=theme["entry_fg"],
                                            height=4, width=35, wrap="word", relief="solid", bd=1)
                text_widget.insert("1.0", str(value))
                text_widget.config(state="disabled")
                text_widget.pack(side="left", padx=(10, 0))
            else:
                label_widget = tk.Label(row, text=str(value), font=("Arial", 11),
                                        bg=theme["bg"], fg=theme["entry_fg"], wraplength=350,
                                        anchor="w", justify="left")
                label_widget.pack(side="left", padx=(10, 0))
                label_widget.bind("<Button-3>", lambda e, t=str(value): self.copy_text(t))

        tk.Label(scrollable_frame, text="Описание:", font=("Arial", 11, "bold"),
                 bg=theme["bg"], fg=theme["fg"], anchor="w").pack(anchor="w", pady=(15, 5))

        desc_text = CopyPasteText(scrollable_frame, font=("Arial", 10), bg=theme["entry_bg"],
                                  fg=theme["entry_fg"], height=6, width=55, wrap="word",
                                  relief="solid", bd=1)
        desc_text.insert("1.0", product.get('Описание', 'Нет описания'))
        desc_text.config(state="disabled")
        desc_text.pack(pady=(0, 10))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if product.get('Количество', 0) > 0:
            buy_btn = tk.Button(detail, text="КУПИТЬ", command=lambda: self.buy_product_by_id(product),
                                bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 12, "bold"),
                                padx=30, pady=8, cursor="hand2", relief="flat")
            buy_btn.pack(pady=20)

    def copy_text(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("Копирование", "Текст скопирован в буфер обмена")

    def buy_product_by_id(self, product):
        messagebox.showinfo("Покупка",
                            f"Товар '{product.get('Модель')}' добавлен в корзину!\nСумма: {product.get('Цена'):,} руб")

    def export_excel(self):
        try:
            import pandas as pd
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"catalog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                df = pd.DataFrame(self.filtered_products)
                df.to_excel(filename, index=False)
                messagebox.showinfo("Успех", f"Экспорт выполнен успешно!\n{filename}")
        except ImportError:
            messagebox.showerror("Ошибка", "Библиотека pandas не установлена. Установите: pip install pandas")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {e}")

    def logout(self):
        self.window.destroy()
        MasterBoltApp()


class AdminPanel(UserPanel):
    def __init__(self, db):
        self.db = db
        self.all_products = db.products
        self.filtered_products = self.all_products.copy()

        self.window = tk.Tk()
        self.window.title(f"МастерБолт - Админ панель - {db.current_user['name']}")
        self.window.geometry("1400x800")
        self.apply_theme()

        self.setup_ui()
        self.window.mainloop()

    def apply_theme(self):
        theme = THEMES[self.db.current_theme]
        self.window.configure(bg=theme["bg"])

    def setup_ui(self):
        theme = THEMES[self.db.current_theme]

        header = tk.Frame(self.window, bg=theme["header_bg"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="МАСТЕРБОЛТ - АДМИНИСТРАТОР", font=("Arial", 20, "bold"),
                 bg=theme["header_bg"], fg=theme["header_fg"]).pack(side="left", padx=30, pady=20)

        settings_btn = tk.Button(header, text="Настройки", command=self.show_settings,
                                 bg=theme["header_bg"], fg="white", font=("Arial", 12),
                                 cursor="hand2", relief="flat")
        settings_btn.pack(side="left", padx=10)

        user_frame = tk.Frame(header, bg=theme["header_bg"])
        user_frame.pack(side="right", padx=30)

        tk.Label(user_frame, text=f"Администратор: {self.db.current_user['name']}",
                 font=("Arial", 12), bg=theme["header_bg"], fg="white").pack(side="left")

        logout_btn = tk.Button(user_frame, text="Выйти", command=self.logout,
                               bg=theme["button_bg"], fg="white", cursor="hand2", relief="flat", padx=15)
        logout_btn.pack(side="left", padx=(15, 0))

        # Панель управления администратора
        admin_control_frame = tk.LabelFrame(self.window, text="УПРАВЛЕНИЕ ТОВАРАМИ (АДМИНИСТРАТОР)",
                                            font=("Arial", 12, "bold"), bg=theme["bg"], fg=theme["fg"],
                                            padx=15, pady=10)
        admin_control_frame.pack(fill="x", padx=20, pady=(10, 5))

        add_btn = tk.Button(admin_control_frame, text="ДОБАВИТЬ ТОВАР", command=self.add_product,
                            bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                            padx=20, pady=8, cursor="hand2", relief="flat")
        add_btn.pack(side="left", padx=10, pady=5)

        edit_btn = tk.Button(admin_control_frame, text="РЕДАКТИРОВАТЬ", command=self.edit_product,
                             bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                             padx=20, pady=8, cursor="hand2", relief="flat")
        edit_btn.pack(side="left", padx=10, pady=5)

        delete_btn = tk.Button(admin_control_frame, text="УДАЛИТЬ", command=self.delete_product,
                               bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=8, cursor="hand2", relief="flat")
        delete_btn.pack(side="left", padx=10, pady=5)

        refresh_btn = tk.Button(admin_control_frame, text="ОБНОВИТЬ", command=self.refresh_products,
                                bg="#9b59b6", fg="white", font=("Arial", 10, "bold"),
                                padx=20, pady=8, cursor="hand2", relief="flat")
        refresh_btn.pack(side="left", padx=10, pady=5)

        # Панель поиска
        filter_frame = tk.LabelFrame(self.window, text="ПОИСК И ФИЛЬТРАЦИЯ",
                                     font=("Arial", 12, "bold"), bg=theme["bg"],
                                     fg=theme["fg"], padx=15, pady=15)
        filter_frame.pack(fill="x", padx=20, pady=15)

        row1 = tk.Frame(filter_frame, bg=theme["bg"])
        row1.pack(fill="x", pady=5)

        tk.Label(row1, text="Модель:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left", padx=5)
        self.model_entry = CopyPasteEntry(row1, width=20, font=("Arial", 10), bg=theme["entry_bg"],
                                          fg=theme["entry_fg"], relief="solid", bd=1)
        self.model_entry.pack(side="left", padx=5)

        tk.Label(row1, text="Производитель:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                       padx=(20, 5))
        self.brand_combo = ttk.Combobox(row1, width=15, state="readonly")
        brands = sorted(list(set([p.get("Производитель", "") for p in self.all_products])))
        self.brand_combo['values'] = ['Все'] + brands
        self.brand_combo.set('Все')
        self.brand_combo.pack(side="left", padx=5)

        tk.Label(row1, text="Тип питания:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                     padx=(20, 5))
        self.power_combo = ttk.Combobox(row1, width=15, state="readonly")
        self.power_combo['values'] = ['Все', 'Аккумуляторный', 'Сетевой']
        self.power_combo.set('Все')
        self.power_combo.pack(side="left", padx=5)

        row2 = tk.Frame(filter_frame, bg=theme["bg"])
        row2.pack(fill="x", pady=5)

        tk.Label(row2, text="Тип двигателя:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                       padx=5)
        self.motor_combo = ttk.Combobox(row2, width=15, state="readonly")
        self.motor_combo['values'] = ['Все', 'Бесщеточный', 'Щеточный']
        self.motor_combo.set('Все')
        self.motor_combo.pack(side="left", padx=5)

        tk.Label(row2, text="Размер патрона:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                        padx=(20, 5))
        self.chuck_combo = ttk.Combobox(row2, width=15, state="readonly")
        chucks = sorted(list(set([p.get("Размер патрона", "") for p in self.all_products])))
        self.chuck_combo['values'] = ['Все'] + chucks
        self.chuck_combo.set('Все')
        self.chuck_combo.pack(side="left", padx=5)

        tk.Label(row2, text="Напряжение:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                    padx=(20, 5))
        self.voltage_combo = ttk.Combobox(row2, width=12, state="readonly")
        voltages = sorted(list(set([p.get("Напряжение", "") for p in self.all_products])))
        self.voltage_combo['values'] = ['Все'] + voltages
        self.voltage_combo.set('Все')
        self.voltage_combo.pack(side="left", padx=5)

        row3 = tk.Frame(filter_frame, bg=theme["bg"])
        row3.pack(fill="x", pady=5)

        tk.Label(row3, text="Макс. момент:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                      padx=5)
        self.torque_combo = ttk.Combobox(row3, width=12, state="readonly")
        torques = sorted(list(set([p.get("Макс. момент", "") for p in self.all_products])))
        self.torque_combo['values'] = ['Все'] + torques
        self.torque_combo.set('Все')
        self.torque_combo.pack(side="left", padx=5)

        tk.Label(row3, text="Дополнительные опции:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(
            side="left", padx=5)
        self.options_entry = CopyPasteEntry(row3, width=25, font=("Arial", 10), bg=theme["entry_bg"],
                                            fg=theme["entry_fg"], relief="solid", bd=1)
        self.options_entry.pack(side="left", padx=5)

        tk.Label(row3, text="Цена от:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left",
                                                                                                 padx=(20, 5))
        self.price_from = CopyPasteEntry(row3, width=8, font=("Arial", 10), bg=theme["entry_bg"], fg=theme["entry_fg"],
                                         relief="solid", bd=1)
        self.price_from.pack(side="left", padx=5)

        tk.Label(row3, text="до:", bg=theme["bg"], font=("Arial", 10), fg=theme["fg"]).pack(side="left", padx=5)
        self.price_to = CopyPasteEntry(row3, width=8, font=("Arial", 10), bg=theme["entry_bg"], fg=theme["entry_fg"],
                                       relief="solid", bd=1)
        self.price_to.pack(side="left", padx=5)

        btn_frame = tk.Frame(filter_frame, bg=theme["bg"])
        btn_frame.pack(fill="x", pady=(15, 5))

        search_btn = tk.Button(btn_frame, text="ПОИСК", command=self.search_products,
                               bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 10, "bold"),
                               padx=25, pady=8, cursor="hand2", relief="flat")
        search_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(btn_frame, text="СБРОСИТЬ", command=self.reset_filters,
                              bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                              padx=25, pady=8, cursor="hand2", relief="flat")
        reset_btn.pack(side="left", padx=5)

        show_all_btn = tk.Button(btn_frame, text="ПОКАЗАТЬ ВСЕ", command=self.show_all,
                                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                 padx=25, pady=8, cursor="hand2", relief="flat")
        show_all_btn.pack(side="left", padx=5)

        export_btn = tk.Button(btn_frame, text="ЭКСПОРТ EXCEL", command=self.export_excel,
                               bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                               padx=25, pady=8, cursor="hand2", relief="flat")
        export_btn.pack(side="right", padx=5)

        # Таблица
        table_frame = tk.Frame(self.window, bg=theme["bg"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ('Модель', 'Производитель', 'Тип питания', 'Тип двигателя',
                   'Размер патрона', 'Напряжение', 'Макс. момент', 'Дополнительные опции', 'Цена')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background=theme["tree_bg"],
                        foreground=theme["tree_fg"],
                        fieldbackground=theme["tree_bg"],
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background=theme["header_bg"],
                        foreground="white",
                        font=("Arial", 10, "bold"))
        style.map('Treeview', background=[('selected', theme["select_bg"])])

        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20, style="Treeview")

        col_widths = {'Модель': 180, 'Производитель': 100, 'Тип питания': 90,
                      'Тип двигателя': 100, 'Размер патрона': 90, 'Напряжение': 80,
                      'Макс. момент': 80, 'Дополнительные опции': 200, 'Цена': 100}

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), anchor='center')

        self.tree.column('Модель', anchor='w')
        self.tree.column('Дополнительные опции', anchor='w')
        self.tree.column('Цена', anchor='e')

        self.tree.bind("<Control-c>", self.copy_from_tree)
        self.tree.bind("<Button-3>", self.show_tree_context_menu)

        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        bottom_frame = tk.Frame(self.window, bg=theme["bg"], height=40)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        self.count_label = tk.Label(bottom_frame, text="", font=("Arial", 10),
                                    bg=theme["bg"], fg="#7f8c8d")
        self.count_label.pack(side="left")

        self.load_products(self.filtered_products)

    # Методы админа
    def refresh_products(self):
        self.all_products = self.db.products
        self.filtered_products = self.all_products.copy()
        self.load_products(self.filtered_products)
        messagebox.showinfo("Успех", "Список товаров обновлен")

    def add_product(self):
        theme = THEMES[self.db.current_theme]
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавить товар")
        add_window.geometry("650x850")
        add_window.configure(bg=theme["bg"])

        canvas = tk.Canvas(add_window, bg=theme["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme["bg"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        fields = {}
        labels = [
            ("Модель*", "Модель"), ("Производитель*", "Производитель"),
            ("Тип питания*", "Тип питания"), ("Тип двигателя*", "Тип двигателя"),
            ("Размер патрона*", "Размер патрона"), ("Напряжение", "Напряжение"),
            ("Макс. момент", "Макс. момент"), ("Скорость вращения", "Скорость вращения"),
            ("Вес", "Вес"), ("Количество*", "Количество"), ("Цена*", "Цена"),
            ("Дополнительные опции", "Дополнительные опции"), ("Описание", "Описание")
        ]

        power_types = ['Аккумуляторный', 'Сетевой']
        motor_types = ['Бесщеточный', 'Щеточный']
        chucks = ['6.35 мм (HEX)', '10 мм', '13 мм', '16 мм', '1/4"']
        voltages = ['10.8 В', '12 В', '14.4 В', '18 В', '20 В', '21 В', '24 В', '36 В', '40 В']
        torques = ['20 Н·м', '30 Н·м', '40 Н·м', '45 Н·м', '50 Н·м', '56 Н·м', '60 Н·м', '70 Н·м', '80 Н·м', '100 Н·м']
        speeds = ['0-400 об/мин', '0-500/0-1800 об/мин', '0-450/0-1500 об/мин', '0-500/0-1900 об/мин',
                  '0-600/0-2000 об/мин']

        for label, key in labels:
            frame = tk.Frame(scrollable_frame, bg=theme["bg"])
            frame.pack(fill="x", pady=5, padx=20)

            tk.Label(frame, text=label, font=("Arial", 10),
                     bg=theme["bg"], fg=theme["fg"], width=18, anchor="w").pack(side="left")

            if key in ["Тип питания", "Тип двигателя", "Размер патрона", "Напряжение", "Макс. момент",
                       "Скорость вращения"]:
                values_map = {
                    "Тип питания": power_types,
                    "Тип двигателя": motor_types,
                    "Размер патрона": chucks,
                    "Напряжение": voltages,
                    "Макс. момент": torques,
                    "Скорость вращения": speeds
                }
                combo = ttk.Combobox(frame, values=values_map.get(key, []), width=30, state="readonly")
                combo.pack(side="left", padx=(10, 0))
                fields[key] = combo
            elif key in ["Дополнительные опции", "Описание"]:
                text_widget = CopyPasteText(frame, font=("Arial", 10), width=35,
                                            height=4 if key == "Дополнительные опции" else 5,
                                            bg=theme["entry_bg"], fg=theme["entry_fg"],
                                            relief="solid", bd=1)
                text_widget.pack(side="left", padx=(10, 0))
                fields[key] = text_widget
            else:
                entry = CopyPasteEntry(frame, font=("Arial", 10), width=35,
                                       bg=theme["entry_bg"], fg=theme["entry_fg"],
                                       relief="solid", bd=1)
                entry.pack(side="left", padx=(10, 0))
                fields[key] = entry

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def save():
            try:
                new_product = {
                    "id": 0,
                    "Модель": fields["Модель"].get(),
                    "Производитель": fields["Производитель"].get(),
                    "Тип питания": fields["Тип питания"].get(),
                    "Тип двигателя": fields["Тип двигателя"].get(),
                    "Размер патрона": fields["Размер патрона"].get(),
                    "Напряжение": fields["Напряжение"].get(),
                    "Макс. момент": fields["Макс. момент"].get(),
                    "Скорость вращения": fields["Скорость вращения"].get(),
                    "Вес": fields["Вес"].get(),
                    "Дополнительные опции": fields["Дополнительные опции"].get("1.0", "end-1c"),
                    "Количество": int(fields["Количество"].get() or 0),
                    "Цена": int(fields["Цена"].get() or 0),
                    "Описание": fields["Описание"].get("1.0", "end-1c"),
                    "in_stock": True
                }
                self.db.add_product(new_product)
                self.all_products = self.db.products
                self.filtered_products = self.all_products
                self.load_products(self.filtered_products)
                add_window.destroy()
                messagebox.showinfo("Успех", "Товар добавлен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка: {e}")

        btn_frame = tk.Frame(add_window, bg=theme["bg"])
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="СОХРАНИТЬ", command=save,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=10, cursor="hand2", relief="flat").pack(side="left", padx=10)

        tk.Button(btn_frame, text="ОТМЕНА", command=add_window.destroy,
                  bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=10, cursor="hand2", relief="flat").pack(side="left", padx=10)

    def edit_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите товар для редактирования")
            return

        item = self.tree.item(selection[0])
        model = item['values'][0]
        product = next((p for p in self.all_products if p.get('Модель') == model), None)

        if not product:
            return

        self.show_edit_dialog(product)

    def show_edit_dialog(self, product):
        theme = THEMES[self.db.current_theme]
        edit_window = tk.Toplevel(self.window)
        edit_window.title(f"Редактировать - {product.get('Модель')}")
        edit_window.geometry("650x850")
        edit_window.configure(bg=theme["bg"])

        canvas = tk.Canvas(edit_window, bg=theme["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme["bg"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        fields = {}
        keys = ['Модель', 'Производитель', 'Тип питания', 'Тип двигателя', 'Размер патрона',
                'Напряжение', 'Макс. момент', 'Скорость вращения', 'Вес', 'Количество', 'Цена',
                'Дополнительные опции', 'Описание']

        power_types = ['Аккумуляторный', 'Сетевой']
        motor_types = ['Бесщеточный', 'Щеточный']
        chucks = ['6.35 мм (HEX)', '10 мм', '13 мм', '16 мм', '1/4"']
        voltages = ['10.8 В', '12 В', '14.4 В', '18 В', '20 В', '21 В', '24 В', '36 В', '40 В']
        torques = ['20 Н·м', '30 Н·м', '40 Н·м', '45 Н·м', '50 Н·м', '56 Н·м', '60 Н·м', '70 Н·м', '80 Н·м', '100 Н·м']
        speeds = ['0-400 об/мин', '0-500/0-1800 об/мин', '0-450/0-1500 об/мин', '0-500/0-1900 об/мин',
                  '0-600/0-2000 об/мин']

        for key in keys:
            frame = tk.Frame(scrollable_frame, bg=theme["bg"])
            frame.pack(fill="x", pady=5, padx=20)

            tk.Label(frame, text=key, font=("Arial", 10),
                     bg=theme["bg"], fg=theme["fg"], width=18, anchor="w").pack(side="left")

            if key in ["Тип питания", "Тип двигателя", "Размер патрона", "Напряжение", "Макс. момент",
                       "Скорость вращения"]:
                values_map = {
                    "Тип питания": power_types,
                    "Тип двигателя": motor_types,
                    "Размер патрона": chucks,
                    "Напряжение": voltages,
                    "Макс. момент": torques,
                    "Скорость вращения": speeds
                }
                combo = ttk.Combobox(frame, values=values_map.get(key, []), width=30, state="readonly")
                combo.set(str(product.get(key, '')))
                combo.pack(side="left", padx=(10, 0))
                fields[key] = combo
            elif key in ["Дополнительные опции", "Описание"]:
                text_widget = CopyPasteText(frame, font=("Arial", 10), width=35,
                                            height=4 if key == "Дополнительные опции" else 5,
                                            bg=theme["entry_bg"], fg=theme["entry_fg"],
                                            relief="solid", bd=1)
                text_widget.insert("1.0", str(product.get(key, '')))
                text_widget.pack(side="left", padx=(10, 0))
                fields[key] = text_widget
            else:
                entry = CopyPasteEntry(frame, font=("Arial", 10), width=35,
                                       bg=theme["entry_bg"], fg=theme["entry_fg"],
                                       relief="solid", bd=1)
                entry.insert(0, str(product.get(key, '')))
                entry.pack(side="left", padx=(10, 0))
                fields[key] = entry

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def save():
            try:
                updated = {}
                for key in keys:
                    if key in ["Дополнительные опции", "Описание"]:
                        updated[key] = fields[key].get("1.0", "end-1c")
                    elif key in ["Тип питания", "Тип двигателя", "Размер патрона", "Напряжение", "Макс. момент",
                                 "Скорость вращения"]:
                        updated[key] = fields[key].get()
                    else:
                        updated[key] = fields[key].get()

                updated['Количество'] = int(updated['Количество'] or 0)
                updated['Цена'] = int(updated['Цена'] or 0)
                updated['in_stock'] = updated['Количество'] > 0
                self.db.update_product(product['id'], updated)
                self.all_products = self.db.products
                self.filtered_products = self.all_products
                self.load_products(self.filtered_products)
                edit_window.destroy()
                messagebox.showinfo("Успех", "Товар обновлен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка: {e}")

        btn_frame = tk.Frame(edit_window, bg=theme["bg"])
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="СОХРАНИТЬ", command=save,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=10, cursor="hand2", relief="flat").pack(side="left", padx=10)

        tk.Button(btn_frame, text="ОТМЕНА", command=edit_window.destroy,
                  bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=10, cursor="hand2", relief="flat").pack(side="left", padx=10)

    def delete_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите товар для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот товар?"):
            item = self.tree.item(selection[0])
            model = item['values'][0]
            product = next((p for p in self.all_products if p.get('Модель') == model), None)
            if product:
                self.db.delete_product(product['id'])
                self.all_products = self.db.products
                self.filtered_products = self.all_products
                self.load_products(self.filtered_products)
                messagebox.showinfo("Успех", "Товар удален")

    # Копируем остальные методы из UserPanel
    def search_products(self):
        model = self.model_entry.get().lower()
        brand = self.brand_combo.get()
        power = self.power_combo.get()
        motor = self.motor_combo.get()
        chuck = self.chuck_combo.get()
        voltage = self.voltage_combo.get()
        torque = self.torque_combo.get()
        options = self.options_entry.get().lower()
        price_from = self.price_from.get()
        price_to = self.price_to.get()

        filtered = []
        for p in self.all_products:
            if model and model not in p.get('Модель', '').lower():
                continue
            if brand != 'Все' and p.get('Производитель', '') != brand:
                continue
            if power != 'Все' and p.get('Тип питания', '') != power:
                continue
            if motor != 'Все' and p.get('Тип двигателя', '') != motor:
                continue
            if chuck != 'Все' and p.get('Размер патрона', '') != chuck:
                continue
            if voltage != 'Все' and p.get('Напряжение', '') != voltage:
                continue
            if torque != 'Все' and p.get('Макс. момент', '') != torque:
                continue
            if options and options not in p.get('Дополнительные опции', '').lower():
                continue
            if price_from:
                try:
                    if p.get('Цена', 0) < int(price_from):
                        continue
                except:
                    pass
            if price_to:
                try:
                    if p.get('Цена', 0) > int(price_to):
                        continue
                except:
                    pass
            filtered.append(p)

        self.filtered_products = filtered
        self.load_products(filtered)

    def reset_filters(self):
        self.model_entry.delete(0, tk.END)
        self.brand_combo.set('Все')
        self.power_combo.set('Все')
        self.motor_combo.set('Все')
        self.chuck_combo.set('Все')
        self.voltage_combo.set('Все')
        self.torque_combo.set('Все')
        self.options_entry.delete(0, tk.END)
        self.price_from.delete(0, tk.END)
        self.price_to.delete(0, tk.END)
        self.search_products()

    def show_all(self):
        self.reset_filters()

    def load_products(self, products):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in products:
            options = p.get('Дополнительные опции', '')
            if len(options) > 50:
                options = options[:47] + '...'

            self.tree.insert('', 'end', values=(
                p.get('Модель', ''),
                p.get('Производитель', ''),
                p.get('Тип питания', ''),
                p.get('Тип двигателя', ''),
                p.get('Размер патрона', ''),
                p.get('Напряжение', ''),
                p.get('Макс. момент', ''),
                options,
                f"{p.get('Цена', 0):,} руб"
            ))

        self.count_label.config(text=f"Найдено товаров: {len(products)} из {len(self.all_products)}")

    def copy_from_tree(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        text_to_copy = []
        for item in selected:
            values = self.tree.item(item, 'values')
            text_to_copy.append('\t'.join(str(v) for v in values))
        self.window.clipboard_clear()
        self.window.clipboard_append('\n'.join(text_to_copy))

    def show_tree_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.window, tearoff=0)
            menu.add_command(label="Копировать строку", command=self.copy_from_tree)
            menu.add_command(label="Копировать всё", command=self.copy_all_from_tree)
            menu.post(event.x_root, event.y_root)

    def copy_all_from_tree(self):
        text_to_copy = []
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            text_to_copy.append('\t'.join(str(v) for v in values))
        self.window.clipboard_clear()
        self.window.clipboard_append('\n'.join(text_to_copy))
        messagebox.showinfo("Копирование", f"Скопировано {len(text_to_copy)} строк")

    def show_settings(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Настройки")
        settings_window.geometry("500x450")
        settings_window.configure(bg=THEMES[self.db.current_theme]["bg"])
        settings_window.resizable(False, False)
        settings_window.transient(self.window)
        settings_window.grab_set()

        theme = THEMES[self.db.current_theme]

        tk.Label(settings_window, text="НАСТРОЙКИ", font=("Arial", 20, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(20, 30))

        theme_frame = tk.Frame(settings_window, bg=theme["bg"])
        theme_frame.pack(pady=10, padx=30, fill="x")

        tk.Label(theme_frame, text="Тема оформления:", font=("Arial", 12),
                 bg=theme["bg"], fg=theme["fg"]).pack(side="left", padx=(0, 20))

        theme_var = tk.StringVar(value=self.db.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=["Светлая", "Тёмная"],
                                   state="readonly", width=15)
        theme_combo.pack(side="left")

        def change_theme():
            new_theme = theme_var.get()
            if new_theme != self.db.current_theme:
                if messagebox.askyesno("Подтверждение",
                                       f"Вы хотите изменить тему на '{new_theme}'?\nДля применения изменений потребуется перезапуск программы."):
                    self.db.save_settings(new_theme)
                    messagebox.showinfo("Успех", f"Тема изменена на '{new_theme}'\nПриложение будет перезапущено.")
                    settings_window.destroy()
                    self.window.destroy()
                    MasterBoltApp()
                else:
                    theme_var.set(self.db.current_theme)

        apply_btn = tk.Button(theme_frame, text="ПРИМЕНИТЬ", command=change_theme,
                              bg=theme["button_bg"], fg=theme["button_fg"], font=("Arial", 10, "bold"),
                              padx=15, pady=5, cursor="hand2", relief="flat")
        apply_btn.pack(side="left", padx=(20, 0))

        info_frame = tk.Frame(settings_window, bg=theme["bg"], relief="groove", bd=2)
        info_frame.pack(pady=30, padx=30, fill="both", expand=True)

        tk.Label(info_frame, text="ИНФОРМАЦИЯ О ПРОГРАММЕ", font=("Arial", 12, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(15, 10))

        tk.Label(info_frame, text="Разработчик:", font=("Arial", 10, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack()
        tk.Label(info_frame, text="Куколь Александра Владимировна", font=("Arial", 10),
                 bg=theme["bg"], fg=theme["fg"]).pack()

        tk.Label(info_frame, text="Группа:", font=("Arial", 10, "bold"),
                 bg=theme["bg"], fg=theme["fg"]).pack(pady=(10, 0))
        tk.Label(info_frame, text="ИС-941", font=("Arial", 10),
                 bg=theme["bg"], fg=theme["fg"]).pack()

        tk.Label(info_frame, text="2024 МастерБолт", font=("Arial", 9),
                 bg=theme["bg"], fg="#7f8c8d").pack(pady=(15, 10))

        close_btn = tk.Button(settings_window, text="ЗАКРЫТЬ", command=settings_window.destroy,
                              bg="#7f8c8d", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, cursor="hand2", relief="flat")
        close_btn.pack(pady=20)

    def export_excel(self):
        try:
            import pandas as pd
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"catalog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                df = pd.DataFrame(self.filtered_products)
                df.to_excel(filename, index=False)
                messagebox.showinfo("Успех", f"Экспорт выполнен успешно!\n{filename}")
        except ImportError:
            messagebox.showerror("Ошибка", "Библиотека pandas не установлена. Установите: pip install pandas")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {e}")

    def logout(self):
        self.window.destroy()
        MasterBoltApp()


if __name__ == "__main__":
    app = MasterBoltApp()