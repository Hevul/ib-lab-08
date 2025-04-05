import tkinter as tk
from tkinter import ttk, scrolledtext
import time

class RC4GeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор ПСП - алгоритм RC4")
        
        # Параметры алгоритма
        self.key = [61, 60, 23, 22, 21, 20]
        self.key_length = 6
        
        # Создание главного окна
        self.create_main_window()
        
        # Создание окна с информацией о параметрах
        self.create_params_window()
        
        # Создание окна для вывода результатов
        self.create_output_window()
        
        # Создание окна для оценки скорости
        self.create_benchmark_window()
    
    def create_main_window(self):
        """Создание главного окна управления"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Поле для ввода сообщения
        ttk.Label(self.main_frame, text="Сообщение для шифрования:").grid(row=0, column=0, sticky=tk.W)
        self.message_entry = scrolledtext.ScrolledText(self.main_frame, width=50, height=5, wrap=tk.WORD)
        self.message_entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.message_entry.insert(tk.END, "Пример текста для шифрования")
        
        # Поле для выбора количества байт
        ttk.Label(self.main_frame, text="Количество байт для генерации:").grid(row=2, column=0, sticky=tk.W)
        self.bytes_entry = ttk.Entry(self.main_frame, width=10)
        self.bytes_entry.grid(row=2, column=1, sticky=tk.W)
        self.bytes_entry.insert(0, "256")
        
        # Кнопки
        self.encrypt_button = ttk.Button(self.main_frame, text="Зашифровать сообщение", command=self.encrypt_message)
        self.encrypt_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.generate_button = ttk.Button(self.main_frame, text="Сгенерировать ПСП", command=self.generate_sequence)
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.params_button = ttk.Button(self.main_frame, text="Параметры алгоритма", command=self.show_params_window)
        self.params_button.grid(row=5, column=0, pady=5)
        
        self.benchmark_button = ttk.Button(self.main_frame, text="Тест производительности", command=self.show_benchmark_window)
        self.benchmark_button.grid(row=5, column=1, pady=5)
    
    def create_params_window(self):
        """Создание окна с информацией о параметрах"""
        self.params_window = tk.Toplevel(self.root)
        self.params_window.title("Параметры алгоритма RC4")
        self.params_window.withdraw()
        
        frame = ttk.Frame(self.params_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Параметры алгоритма RC4", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        ttk.Label(frame, text="Длина ключа:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, text=f"{self.key_length} байт").grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Ключ (десятичные числа):").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, text=', '.join(map(str, self.key))).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Ключ (шестнадцатеричный):").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, text=', '.join([f"0x{byte:02X}" for byte in self.key])).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Button(frame, text="Закрыть", command=self.params_window.withdraw).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_output_window(self):
        """Создание окна для вывода результатов"""
        self.output_window = tk.Toplevel(self.root)
        self.output_window.title("Результаты работы RC4")
        self.output_window.withdraw()
        
        frame = ttk.Frame(self.output_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Ноутбук с вкладками
        self.notebook = ttk.Notebook(frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Вкладка с исходным текстом
        self.original_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.original_tab, text="Исходное сообщение")
        self.original_text = scrolledtext.ScrolledText(self.original_tab, wrap=tk.WORD, width=70, height=15)
        self.original_text.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка с зашифрованным текстом
        self.encrypted_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.encrypted_tab, text="Зашифрованное сообщение")
        self.encrypted_text = scrolledtext.ScrolledText(self.encrypted_tab, wrap=tk.WORD, width=70, height=15)
        self.encrypted_text.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка с ПСП
        self.sequence_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sequence_tab, text="ПСП")
        self.sequence_text = scrolledtext.ScrolledText(self.sequence_tab, wrap=tk.WORD, width=70, height=15)
        self.sequence_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frame, text="Закрыть", command=self.output_window.withdraw).grid(row=1, column=0, pady=10)
    
    def create_benchmark_window(self):
        """Создание окна для оценки скорости"""
        self.benchmark_window = tk.Toplevel(self.root)
        self.benchmark_window.title("Тест производительности RC4")
        self.benchmark_window.withdraw()
        
        frame = ttk.Frame(self.benchmark_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Тест производительности алгоритма RC4", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        self.benchmark_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=15)
        self.benchmark_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(frame, text="Запустить тест", command=self.run_benchmark).grid(row=2, column=0, pady=5)
        ttk.Button(frame, text="Закрыть", command=self.benchmark_window.withdraw).grid(row=3, column=0, pady=5)
    
    def show_params_window(self):
        """Показать окно параметров"""
        self.params_window.deiconify()
    
    def show_output_window(self):
        """Показать окно вывода"""
        self.output_window.deiconify()
        self.notebook.select(0)  # Показать первую вкладку
    
    def show_benchmark_window(self):
        """Показать окно тестирования"""
        self.benchmark_window.deiconify()
    
    def rc4_init(self):
        """Инициализация S-блока (KSA)"""
        S = list(range(256))
        j = 0
        
        # Повторяем ключ, если он короче 256 байт
        key = self.key * (256 // len(self.key)) + self.key[:256 % len(self.key)]
        
        for i in range(256):
            j = (j + S[i] + key[i]) % 256
            S[i], S[j] = S[j], S[i]
        
        return S
    
    def rc4_generate(self, S, length):
        """Генерация псевдослучайной последовательности (PRGA)"""
        i = j = 0
        result = []
        
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            result.append(K)
        
        return result
    
    def encrypt_message(self):
        """Шифрование сообщения с использованием RC4"""
        message = self.message_entry.get("1.0", tk.END).strip()
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
        
        # Отображение результатов
        self.original_text.delete(1.0, tk.END)
        self.original_text.insert(tk.END, message)
        
        self.encrypted_text.delete(1.0, tk.END)
        self.encrypted_text.insert(tk.END, ' '.join([f"{byte:02X}" for byte in encrypted]))
        
        self.sequence_text.delete(1.0, tk.END)
        self.sequence_text.insert(tk.END, ' '.join([f"{byte:02X}" for byte in key_stream]))
        
        self.show_output_window()
    
    def generate_sequence(self):
        """Генерация ПСП заданной длины"""
        try:
            length = int(self.bytes_entry.get())
        except ValueError:
            self.sequence_text.delete(1.0, tk.END)
            self.sequence_text.insert(tk.END, "Ошибка: введите корректное число байт")
            self.show_output_window()
            return
        
        # Инициализация RC4
        S = self.rc4_init()
        
        # Генерация последовательности
        sequence = self.rc4_generate(S, length)
        
        # Отображение результатов
        self.original_text.delete(1.0, tk.END)
        self.original_text.insert(tk.END, "Генерация ПСП без исходного сообщения")
        
        self.encrypted_text.delete(1.0, tk.END)
        self.encrypted_text.insert(tk.END, "Не применимо")
        
        self.sequence_text.delete(1.0, tk.END)
        
        # Форматированный вывод (16 байт в строке)
        hex_sequence = [f"{byte:02X}" for byte in sequence]
        for i in range(0, len(hex_sequence), 16):
            line = ' '.join(hex_sequence[i:i+16])
            self.sequence_text.insert(tk.END, line + '\n')
        
        self.show_output_window()
    
    def run_benchmark(self):
        """Тестирование производительности алгоритма"""
        self.benchmark_text.delete(1.0, tk.END)
        self.benchmark_text.insert(tk.END, "Запуск теста производительности...\n")
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
        
        self.benchmark_text.insert(tk.END, "\nТест завершен\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RC4GeneratorApp(root)
    root.mainloop()