import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from sympy import isprime

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Комбинированный генератор ПСП (RC4 + BBS)")
        
        # Параметры для RC4
        self.rc4_key = [61, 60, 23, 22, 21, 20]
        self.rc4_key_length = 6
        
        # Параметры для BBS
        self.bbs_p = 24672462467892469787
        self.bbs_q = 396736894567834589803
        self.bbs_modulus = self.bbs_p * self.bbs_q
        self.bbs_n = 256
        
        # Создание интерфейса
        self.create_main_window()
        self.create_rc4_params_window()
        self.create_bbs_params_window()
        self.create_output_window()
        self.create_benchmark_window()
    
    def create_main_window(self):
        """Создание главного окна управления"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Ноутбук с вкладками
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Вкладка RC4
        self.rc4_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rc4_tab, text="RC4")
        self.create_rc4_tab()
        
        # Вкладка BBS
        self.bbs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.bbs_tab, text="BBS")
        self.create_bbs_tab()
        
        # Кнопки для окон параметров
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(buttons_frame, text="Параметры RC4", command=self.show_rc4_params_window).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Параметры BBS", command=self.show_bbs_params_window).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Тест производительности", command=self.show_benchmark_window).grid(row=0, column=2, padx=5)
    
    def create_rc4_tab(self):
        """Создание вкладки RC4"""
        # Поле для ввода сообщения
        ttk.Label(self.rc4_tab, text="Сообщение:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.rc4_message_entry = scrolledtext.ScrolledText(self.rc4_tab, width=60, height=5, wrap=tk.WORD)
        self.rc4_message_entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.rc4_message_entry.insert(tk.END, "Пример текста для шифрования")
        
        # Поле для зашифрованного сообщения
        ttk.Label(self.rc4_tab, text="Зашифрованное/расшифрованное сообщение:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.rc4_encrypted_entry = scrolledtext.ScrolledText(self.rc4_tab, width=60, height=5, wrap=tk.WORD)
        self.rc4_encrypted_entry.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Поле для количества байт ПСП
        ttk.Label(self.rc4_tab, text="Количество байт ПСП:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.rc4_bytes_entry = ttk.Entry(self.rc4_tab, width=10)
        self.rc4_bytes_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.rc4_bytes_entry.insert(0, "256")
        
        # Кнопки
        buttons_frame = ttk.Frame(self.rc4_tab)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="Зашифровать", command=self.rc4_encrypt).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Расшифровать", command=self.rc4_decrypt).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Сгенерировать ПСП", command=self.rc4_generate_sequence).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Показать результаты", command=self.show_output_window).grid(row=0, column=3, padx=5)
    
    def create_bbs_tab(self):
        """Создание вкладки BBS"""
        # Поле для ввода начального значения
        ttk.Label(self.bbs_tab, text="Начальное значение (seed):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bbs_seed_entry = ttk.Entry(self.bbs_tab, width=30)
        self.bbs_seed_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.bbs_seed_entry.insert(0, str(int(time.time())))
        
        # Поле для количества бит
        ttk.Label(self.bbs_tab, text="Количество бит:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bbs_bits_entry = ttk.Entry(self.bbs_tab, width=10)
        self.bbs_bits_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.bbs_bits_entry.insert(0, str(self.bbs_n))
        
        # Кнопки
        buttons_frame = ttk.Frame(self.bbs_tab)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="Сгенерировать ПСП", command=self.bbs_generate_sequence).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Показать результаты", command=self.show_output_window).grid(row=0, column=1, padx=5)
    
    def create_rc4_params_window(self):
        """Создание окна с параметрами RC4"""
        self.rc4_params_window = tk.Toplevel(self.root)
        self.rc4_params_window.title("Параметры алгоритма RC4")
        self.rc4_params_window.withdraw()
        
        frame = ttk.Frame(self.rc4_params_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Параметры алгоритма RC4", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        ttk.Label(frame, text="Длина ключа:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, text=f"{self.rc4_key_length} байт").grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Ключ (десятичные числа):").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, text=', '.join(map(str, self.rc4_key))).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Ключ (шестнадцатеричный):").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, text=', '.join([f"0x{byte:02X}" for byte in self.rc4_key])).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Button(frame, text="Закрыть", command=self.rc4_params_window.withdraw).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_bbs_params_window(self):
        """Создание окна с параметрами BBS"""
        self.bbs_params_window = tk.Toplevel(self.root)
        self.bbs_params_window.title("Параметры алгоритма BBS")
        self.bbs_params_window.withdraw()
        
        frame = ttk.Frame(self.bbs_params_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Параметры алгоритма BBS", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        ttk.Label(frame, text="p:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.bbs_p)).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="q:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.bbs_q)).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Модуль (n = p*q):").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.bbs_modulus)).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Длина выходного блока:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(frame, text=str(self.bbs_n)).grid(row=4, column=1, sticky=tk.W)
        
        ttk.Button(frame, text="Закрыть", command=self.bbs_params_window.withdraw).grid(row=5, column=0, columnspan=2, pady=10)
    
    def create_output_window(self):
        """Создание окна для вывода результатов"""
        self.output_window = tk.Toplevel(self.root)
        self.output_window.title("Результаты генерации ПСП")
        self.output_window.withdraw()
        
        frame = ttk.Frame(self.output_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.output_notebook = ttk.Notebook(frame)
        self.output_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Вкладка для RC4
        self.rc4_output_tab = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.rc4_output_tab, text="RC4")
        
        self.rc4_output_text = scrolledtext.ScrolledText(self.rc4_output_tab, wrap=tk.WORD, width=80, height=20)
        self.rc4_output_text.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка для BBS
        self.bbs_output_tab = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.bbs_output_tab, text="BBS")
        
        self.bbs_output_text = scrolledtext.ScrolledText(self.bbs_output_tab, wrap=tk.WORD, width=80, height=20)
        self.bbs_output_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frame, text="Закрыть", command=self.output_window.withdraw).grid(row=1, column=0, pady=10)
    
    def create_benchmark_window(self):
        """Создание окна для тестирования производительности"""
        self.benchmark_window = tk.Toplevel(self.root)
        self.benchmark_window.title("Тест производительности")
        self.benchmark_window.withdraw()
        
        frame = ttk.Frame(self.benchmark_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Тест производительности алгоритмов", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        self.benchmark_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
        self.benchmark_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(frame, text="Запустить тест RC4", command=self.run_rc4_benchmark).grid(row=2, column=0, pady=5)
        ttk.Button(frame, text="Запустить тест BBS", command=self.run_bbs_benchmark).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Закрыть", command=self.benchmark_window.withdraw).grid(row=4, column=0, pady=5)
    
    def show_rc4_params_window(self):
        """Показать окно параметров RC4"""
        self.rc4_params_window.deiconify()
    
    def show_bbs_params_window(self):
        """Показать окно параметров BBS"""
        self.bbs_params_window.deiconify()
    
    def show_output_window(self):
        """Показать окно вывода"""
        self.output_window.deiconify()
    
    def show_benchmark_window(self):
        """Показать окно тестирования"""
        self.benchmark_window.deiconify()
    
    def rc4_init(self):
        """Инициализация S-блока для RC4"""
        S = list(range(256))
        j = 0
        
        # Повторяем ключ, если он короче 256 байт
        key = self.rc4_key * (256 // len(self.rc4_key)) + self.rc4_key[:256 % len(self.rc4_key)]
        
        for i in range(256):
            j = (j + S[i] + key[i]) % 256
            S[i], S[j] = S[j], S[i]
        
        return S
    
    def rc4_generate(self, S, length):
        """Генерация псевдослучайной последовательности RC4"""
        i = j = 0
        result = []
        
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            result.append(K)
        
        return result
    
    def rc4_encrypt(self):
        """Шифрование сообщения с использованием RC4"""
        message = self.rc4_message_entry.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Инициализация RC4
        S = self.rc4_init()
        
        # Генерация ключевого потока
        key_stream = self.rc4_generate(S, len(message))
        
        # Шифрование (XOR с ключевым потоком)
        encrypted = []
        for i in range(len(message)):
            encrypted.append(ord(message[i]) ^ key_stream[i])
        
        # Отображение зашифрованного сообщения
        self.rc4_encrypted_entry.delete(1.0, tk.END)
        self.rc4_encrypted_entry.insert(tk.END, ' '.join([f"{byte:02X}" for byte in encrypted]))
        
        # Сохранение результатов для окна вывода
        self.rc4_output_text.delete(1.0, tk.END)
        self.rc4_output_text.insert(tk.END, "Исходное сообщение:\n")
        self.rc4_output_text.insert(tk.END, message + "\n\n")
        self.rc4_output_text.insert(tk.END, "Зашифрованное сообщение (HEX):\n")
        self.rc4_output_text.insert(tk.END, ' '.join([f"{byte:02X}" for byte in encrypted]) + "\n\n")
        self.rc4_output_text.insert(tk.END, "Ключевой поток (первые 256 байт):\n")
        self.rc4_output_text.insert(tk.END, ' '.join([f"{byte:02X}" for byte in key_stream[:256]]))
    
    def rc4_decrypt(self):
        """Дешифрование сообщения с использованием RC4"""
        encrypted_hex = self.rc4_encrypted_entry.get("1.0", tk.END).strip()
        if not encrypted_hex:
            return
        
        try:
            # Преобразование HEX строки в байты
            encrypted = [int(hex_byte, 16) for hex_byte in encrypted_hex.split()]
        except ValueError:
            self.rc4_encrypted_entry.delete(1.0, tk.END)
            self.rc4_encrypted_entry.insert(tk.END, "Ошибка: некорректный HEX формат")
            return
        
        # Инициализация RC4
        S = self.rc4_init()
        
        # Генерация ключевого потока
        key_stream = self.rc4_generate(S, len(encrypted))
        
        # Дешифрование (XOR с ключевым потоком)
        decrypted = []
        for i in range(len(encrypted)):
            decrypted.append(chr(encrypted[i] ^ key_stream[i]))
        
        # Отображение расшифрованного сообщения
        self.rc4_message_entry.delete(1.0, tk.END)
        self.rc4_message_entry.insert(tk.END, ''.join(decrypted))
        
        # Сохранение результатов для окна вывода
        self.rc4_output_text.delete(1.0, tk.END)
        self.rc4_output_text.insert(tk.END, "Зашифрованное сообщение (HEX):\n")
        self.rc4_output_text.insert(tk.END, encrypted_hex + "\n\n")
        self.rc4_output_text.insert(tk.END, "Расшифрованное сообщение:\n")
        self.rc4_output_text.insert(tk.END, ''.join(decrypted) + "\n\n")
        self.rc4_output_text.insert(tk.END, "Ключевой поток (первые 256 байт):\n")
        self.rc4_output_text.insert(tk.END, ' '.join([f"{byte:02X}" for byte in key_stream[:256]]))
    
    def rc4_generate_sequence(self):
        """Генерация ПСП с использованием RC4"""
        try:
            length = int(self.rc4_bytes_entry.get())
        except ValueError:
            self.rc4_output_text.delete(1.0, tk.END)
            self.rc4_output_text.insert(tk.END, "Ошибка: введите корректное число байт")
            self.show_output_window()
            return
        
        # Инициализация RC4
        S = self.rc4_init()
        
        # Генерация последовательности
        sequence = self.rc4_generate(S, length)
        
        # Сохранение результатов для окна вывода
        self.rc4_output_text.delete(1.0, tk.END)
        self.rc4_output_text.insert(tk.END, f"Сгенерированная ПСП (первые 1024 байта из {length}):\n\n")
        
        # Форматированный вывод (16 байт в строке)
        hex_sequence = [f"{byte:02X}" for byte in sequence[:1024]]
        for i in range(0, len(hex_sequence), 16):
            line = ' '.join(hex_sequence[i:i+16])
            self.rc4_output_text.insert(tk.END, line + '\n')
        
        self.show_output_window()
        self.output_notebook.select(0)  # Выбрать вкладку RC4
    
    def bbs_generate_sequence(self):
        """Генерация ПСП с использованием BBS"""
        try:
            seed = int(self.bbs_seed_entry.get())
            bits = int(self.bbs_bits_entry.get())
        except ValueError:
            self.bbs_output_text.delete(1.0, tk.END)
            self.bbs_output_text.insert(tk.END, "Ошибка: введите корректные числовые значения")
            self.show_output_window()
            return
        
        if seed <= 1 or seed >= self.bbs_modulus:
            self.bbs_output_text.delete(1.0, tk.END)
            self.bbs_output_text.insert(tk.END, f"Ошибка: seed должен быть 1 < seed < {self.bbs_modulus}")
            self.show_output_window()
            return
        
        # Генерация последовательности
        x = (seed * seed) % self.bbs_modulus
        sequence = []
        
        for _ in range(bits):
            x = (x * x) % self.bbs_modulus
            bit = x % 2
            sequence.append(str(bit))
        
        # Преобразование в 32-битные блоки для удобства чтения
        binary_str = ''.join(sequence)
        
        # Сохранение результатов для окна вывода
        self.bbs_output_text.delete(1.0, tk.END)
        self.bbs_output_text.insert(tk.END, f"Параметры генерации:\n")
        self.bbs_output_text.insert(tk.END, f"Начальное значение (seed): {seed}\n")
        self.bbs_output_text.insert(tk.END, f"Модуль (n): {self.bbs_modulus}\n")
        self.bbs_output_text.insert(tk.END, f"Количество бит: {bits}\n\n")
        self.bbs_output_text.insert(tk.END, "Сгенерированная последовательность:\n\n")
        
        for i in range(0, len(binary_str), 32):
            self.bbs_output_text.insert(tk.END, binary_str[i:i+32] + "\n")
        
        self.show_output_window()
        self.output_notebook.select(1)  # Выбрать вкладку BBS
    
    def run_rc4_benchmark(self):
        """Тестирование производительности RC4"""
        self.benchmark_text.delete(1.0, tk.END)
        self.benchmark_text.insert(tk.END, "Запуск теста производительности RC4...\n")
        self.benchmark_window.update()
        
        test_sizes = [100, 1000, 10000, 100000, 1000000]
        results = []
        
        for size in test_sizes:
            start_time = time.time()
            
            # Инициализация RC4
            S = self.rc4_init()
            
            # Генерация последовательности
            self.rc4_generate(S, size)
            
            elapsed = time.time() - start_time
            speed = size / elapsed  # байт/сек
            results.append((size, elapsed, speed))
            
            self.benchmark_text.insert(tk.END, 
                f"Размер: {size} байт, Время: {elapsed:.6f} сек, Скорость: {speed:,.0f} байт/сек\n")
            self.benchmark_window.update()
        
        self.benchmark_text.insert(tk.END, "\nТест RC4 завершен\n")
    
    def run_bbs_benchmark(self):
        """Тестирование производительности BBS"""
        self.benchmark_text.delete(1.0, tk.END)
        self.benchmark_text.insert(tk.END, "Запуск теста производительности BBS...\n")
        self.benchmark_window.update()
        
        test_sizes = [100, 1000, 10000, 100000, 1000000]
        results = []
        seed = int(time.time()) % self.bbs_modulus
        
        for size in test_sizes:
            start_time = time.time()
            
            # Генерация последовательности
            x = (seed * seed) % self.bbs_modulus
            for _ in range(size):
                x = (x * x) % self.bbs_modulus
                _ = x % 2
            
            elapsed = time.time() - start_time
            speed = size / elapsed  # бит/сек
            results.append((size, elapsed, speed))
            
            self.benchmark_text.insert(tk.END, 
                f"Размер: {size} бит, Время: {elapsed:.6f} сек, Скорость: {speed:,.0f} бит/сек\n")
            self.benchmark_window.update()
        
        self.benchmark_text.insert(tk.END, "\nТест BBS завершен\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()