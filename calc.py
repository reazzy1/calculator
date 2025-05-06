import tkinter as tk
from tkinter import font as tkfont

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Красивый калькулятор")
        self.root.geometry("320x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Стили
        self.button_font = tkfont.Font(family="Arial", size=14, weight="bold")
        self.display_font = tkfont.Font(family="Arial", size=24)
        
        # Переменные
        self.current_input = ""
        self.total = 0
        self.operation = None
        self.reset_input = False
        
        # Создание интерфейса
        self.create_display()
        self.create_buttons()
    
    def create_display(self):
        # Фрейм для дисплея
        display_frame = tk.Frame(self.root, height=100, bg="#f0f0f0")
        display_frame.pack(expand=True, fill="both", padx=10, pady=(20, 10))
        
        # Верхний дисплей (история)
        self.history_label = tk.Label(
            display_frame, 
            text="", 
            anchor="e", 
            bg="#f0f0f0", 
            fg="#666", 
            font=tkfont.Font(family="Arial", size=12)
        )
        self.history_label.pack(expand=True, fill="both")
        
        # Нижний дисплей (текущий ввод)
        self.display_label = tk.Label(
            display_frame, 
            text="0", 
            anchor="e", 
            bg="#f0f0f0", 
            fg="#333", 
            font=self.display_font
        )
        self.display_label.pack(expand=True, fill="both")
    
    def create_buttons(self):
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Расположение кнопок
        buttons = [
            ("C", "⌫", "%", "/"),
            ("7", "8", "9", "×"),
            ("4", "5", "6", "-"),
            ("1", "2", "3", "+"),
            ("±", "0", ".", "=")
        ]
        
        # Создание кнопок
        for i, row in enumerate(buttons):
            button_frame.rowconfigure(i, weight=1)
            for j, text in enumerate(row):
                button_frame.columnconfigure(j, weight=1)
                
                # Определение цвета кнопки
                if text in {"C", "⌫", "±", "%"}:
                    bg = "#e0e0e0"
                    fg = "black"
                elif text in {"/", "×", "-", "+", "="}:
                    bg = "#ff9500"
                    fg = "white"
                else:
                    bg = "#f8f8f8"
                    fg = "black"
                
                # Создание кнопки
                btn = tk.Button(
                    button_frame, 
                    text=text, 
                    font=self.button_font,
                    bg=bg,
                    fg=fg,
                    activebackground="#d0d0d0" if bg != "#ff9500" else "#e68a00",
                    activeforeground=fg,
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
    
    def on_button_click(self, text):
        if text.isdigit() or text == ".":
            self.handle_digit(text)
        elif text in {"+", "-", "×", "/"}:
            self.handle_operator(text)
        elif text == "=":
            self.handle_equals()
        elif text == "C":
            self.handle_clear()
        elif text == "⌫":
            self.handle_backspace()
        elif text == "±":
            self.handle_negate()
        elif text == "%":
            self.handle_percentage()
        
        self.update_display()
    
    def handle_digit(self, digit):
        if self.reset_input:
            self.current_input = ""
            self.reset_input = False
        
        if digit == "." and "." in self.current_input:
            return
        
        self.current_input += digit
    
    def handle_operator(self, operator):
        if self.current_input:
            current_num = float(self.current_input)
            
            if self.operation:
                self.calculate()
            
            self.total = current_num
            self.operation = operator
            self.reset_input = True
            self.history_label.config(text=f"{self.total} {self.operation}")
    
    def handle_equals(self):
        if self.operation and self.current_input:
            self.calculate()
            self.operation = None
            self.history_label.config(text="")
    
    def handle_clear(self):
        self.current_input = ""
        self.total = 0
        self.operation = None
        self.reset_input = False
        self.history_label.config(text="")
    
    def handle_backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
    
    def handle_negate(self):
        if self.current_input:
            if self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
    
    def handle_percentage(self):
        if self.current_input:
            num = float(self.current_input) / 100
            self.current_input = str(num)
            if "." in self.current_input and self.current_input.endswith("0"):
                self.current_input = self.current_input[:-2]
    
    def calculate(self):
        current_num = float(self.current_input)
        
        if self.operation == "+":
            self.total += current_num
        elif self.operation == "-":
            self.total -= current_num
        elif self.operation == "×":
            self.total *= current_num
        elif self.operation == "/":
            self.total /= current_num
        
        self.current_input = str(self.total)
        if "." in self.current_input and self.current_input.endswith("0"):
            self.current_input = self.current_input[:-2]
        
        self.reset_input = True
    
    def update_display(self):
        if not self.current_input:
            self.display_label.config(text="0")
        else:
            self.display_label.config(text=self.current_input)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()