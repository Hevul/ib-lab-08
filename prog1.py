import tkinter as tk
from tkinter import ttk
import math
import time
from sympy import isprime

class BBSGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор ПСП - алгоритм BBS")
        
        # Основные параметры
        self.n = 256
        self.p = 24672462467892469787
        self.q = 396736894567834589803
        self.modulus = self.p * self.q
        
        # Создание главного окна
        self.create_main_window()
        
        # Создание окна с информацией о параметрах
        self.create_params_window()
        
        # Создание окна для вывода последовательности
        self.create_output_window()
    
    def create_main_window(self):
        """Создание главного окна управления"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Поле для ввода начального значения (seed)
        ttk.Label(self.main_frame, text="Начальное значение (seed):").grid(row=0, column=0, sticky=tk.W)
        self.seed_entry = ttk.Entry(self.main_frame, width=40)
        self.seed_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.seed_entry.insert(0, str(int(time.time())))
        
        # Поле для выбора количества бит
        ttk.Label(self.main_frame, text="Количество бит:").grid(row=1, column=0, sticky=tk.W)
        self.bits_entry = ttk.Entry(self.main_frame, width=10)
        self.bits_entry.grid(row=1, column=1, sticky=tk.W)
        self.bits_entry.insert(0, str(self.n))
        
        # Кнопка генерации
        self.generate_button = ttk.Button(self.main_frame, text="Сгенерировать ПСП", command=self.generate_sequence)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Кнопка для показа окна параметров
        self.params_button = ttk.Button(self.main_frame, text="Параметры алгоритма", command=self.show_params_window)
        self.params_button.grid(row=3, column=0, columnspan=2)
        
        # Кнопка для показа окна вывода
        self.output_button = ttk.Button(self.main_frame, text="Показать вывод", command=self.show_output_window)
        self.output_button.grid(row=4, column=0, columnspan=2)
    
    def create_params_window(self):
        """Создание окна с информацией о параметрах"""
        self.params_window = tk.Toplevel(self.root)
        self.params_window.title("Параметры алгоритма BBS")
        self.params_window.withdraw()
        
        frame = ttk.Frame(self.params_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Информация о параметрах
        ttk.Label(frame, text="Параметры алгоритма BBS", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(frame, text="p:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.p)).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="q:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.q)).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Модуль (n = p*q):").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.modulus)).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Длина выходного блока:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.n)).grid(row=4, column=1, sticky=tk.W)
        
        # Проверка параметров
        ttk.Label(frame, text="Проверка параметров:", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Проверка p ≡ 3 mod 4
        p_check = self.p % 4 == 3
        ttk.Label(frame, text="p ≡ 3 mod 4:").grid(row=6, column=0, sticky=tk.W)
        ttk.Label(frame, text="Да" if p_check else "Нет").grid(row=6, column=1, sticky=tk.W)
        
        # Проверка q ≡ 3 mod 4
        q_check = self.q % 4 == 3
        ttk.Label(frame, text="q ≡ 3 mod 4:").grid(row=7, column=0, sticky=tk.W)
        ttk.Label(frame, text="Да" if q_check else "Нет").grid(row=7, column=1, sticky=tk.W)
        
        # Проверка что (p-1)/2 простое
        p_half = (self.p - 1) // 2
        p_half_check = isprime(p_half)
        ttk.Label(frame, text="(p-1)/2 простое:").grid(row=8, column=0, sticky=tk.W)
        ttk.Label(frame, text="Да" if p_half_check else "Нет").grid(row=8, column=1, sticky=tk.W)
        
        # Проверка что (q-1)/2 простое
        q_half = (self.q - 1) // 2
        q_half_check = isprime(q_half)
        ttk.Label(frame, text="(q-1)/2 простое:").grid(row=9, column=0, sticky=tk.W)
        ttk.Label(frame, text="Да" if q_half_check else "Нет").grid(row=9, column=1, sticky=tk.W)
        
        ttk.Button(frame, text="Закрыть", command=self.params_window.withdraw).grid(row=10, column=0, columnspan=2, pady=10)
    
    def create_output_window(self):
        """Создание окна для вывода последовательности"""
        self.output_window = tk.Toplevel(self.root)
        self.output_window.title("Сгенерированная ПСП")
        self.output_window.withdraw()
        
        frame = ttk.Frame(self.output_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Текстовое поле с прокруткой
        self.output_text = tk.Text(frame, wrap=tk.WORD, width=80, height=20)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.output_text['yscrollcommand'] = scrollbar.set
        
        ttk.Button(frame, text="Закрыть", command=self.output_window.withdraw).grid(row=1, column=0, pady=10)
    
    def show_params_window(self):
        """Показать окно параметров"""
        self.params_window.deiconify()
    
    def show_output_window(self):
        """Показать окно вывода"""
        self.output_window.deiconify()
    
    def generate_sequence(self):
        """Генерация псевдослучайной последовательности"""
        try:
            seed = int(self.seed_entry.get())
            bits = int(self.bits_entry.get())
        except ValueError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Ошибка: введите корректные числовые значения для seed и количества бит")
            self.show_output_window()
            return
        
        if seed <= 1 or seed >= self.modulus:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Ошибка: seed должен быть 1 < seed < {self.modulus}")
            self.show_output_window()
            return
        
        # Генерация последовательности
        x = (seed * seed) % self.modulus
        sequence = []
        
        for _ in range(bits):
            x = (x * x) % self.modulus
            bit = x % 2
            sequence.append(str(bit))
        
        # Преобразование в 32-битные блоки для удобства чтения
        binary_str = ''.join(sequence)
        formatted_output = ""
        for i in range(0, len(binary_str), 32):
            formatted_output += binary_str[i:i+32] + "\n"
        
        # Вывод результатов
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Параметры генерации:\n")
        self.output_text.insert(tk.END, f"Начальное значение (seed): {seed}\n")
        self.output_text.insert(tk.END, f"Модуль (n): {self.modulus}\n")
        self.output_text.insert(tk.END, f"Количество бит: {bits}\n\n")
        self.output_text.insert(tk.END, "Сгенерированная последовательность:\n\n")
        self.output_text.insert(tk.END, formatted_output)
        
        self.show_output_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = BBSGeneratorApp(root)
    root.mainloop()