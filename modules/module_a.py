import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

class ModuleA:
    def __init__(self, parent, console_callback):
        self.parent = parent
        self.console_callback = console_callback
        self.current_grammar = None
        self.tokens = []
        self.current_token = 0
        
        self.create_widgets()
        self.setup_grammar1()
    
    def create_widgets(self):
        # Frame para selección de gramática
        grammar_frame = ttk.LabelFrame(self.parent, text="Selección de Gramática")
        grammar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.grammar_var = tk.StringVar()
        self.grammar1_rb = ttk.Radiobutton(
            grammar_frame, 
            text="Gramática 1: E → E + T | T, T → T * F | F, F → (E) | id", 
            variable=self.grammar_var, 
            value="grammar1",
            command=self.setup_grammar1
        )
        self.grammar1_rb.pack(anchor=tk.W)
        
        self.grammar2_rb = ttk.Radiobutton(
            grammar_frame, 
            text="Gramática 2: L → A | F, F → (S), S → SL | L, A → num | id", 
            variable=self.grammar_var, 
            value="grammar2",
            command=self.setup_grammar2
        )
        self.grammar2_rb.pack(anchor=tk.W)
        
        # Frame para entrada de texto
        input_frame = ttk.LabelFrame(self.parent, text="Entrada a Analizar")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Botón de análisis
        analyze_button = ttk.Button(
            input_frame, 
            text="Analizar", 
            command=self.analyze_input
        )
        analyze_button.pack(pady=5)
        
        # Frame para resultados
        result_frame = ttk.LabelFrame(self.parent, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, state='disabled')
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_grammar1(self):
        self.current_grammar = "grammar1"
        self.grammar_var.set("grammar1")
        self.console_callback("Gramática 1 seleccionada: E → E + T | T, T → T * F | F, F → (E) | id")
    
    def setup_grammar2(self):
        self.current_grammar = "grammar2"
        self.grammar_var.set("grammar2")
        self.console_callback("Gramática 2 seleccionada: L → A | F, F → (S), S → SL | L, A → num | id")
    
    def analyze_input(self):
        input_text = self.input_entry.get().strip()
        if not input_text:
            messagebox.showerror("Error", "Por favor ingrese una expresión para analizar")
            return
        
        self.console_callback(f"\nAnalizando entrada: '{input_text}'")
        
        # Tokenizar la entrada
        self.tokens = self.tokenize(input_text)
        self.current_token = 0
        
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        
        try:
            if self.current_grammar == "grammar1":
                success = self.E()
                if success and self.current_token == len(self.tokens):
                    self.result_text.insert(tk.END, "Análisis exitoso: La entrada es válida\n")
                    self.console_callback("Análisis exitoso")
                else:
                    self.result_text.insert(tk.END, f"Error de sintaxis en el token: {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}\n")
                    self.console_callback("Error de sintaxis")
            else:
                success = self.L()
                if success and self.current_token == len(self.tokens):
                    self.result_text.insert(tk.END, "Análisis exitoso: La entrada es válida\n")
                    self.console_callback("Análisis exitoso")
                else:
                    self.result_text.insert(tk.END, f"Error de sintaxis en el token: {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}\n")
                    self.console_callback("Error de sintaxis")
        except RecursionError:
            self.result_text.insert(tk.END, "Error: Recursión infinita detectada (problema de recursión izquierda)\n")
            self.console_callback("Error: Recursión infinita (problema de recursión izquierda)")
        
        self.result_text.config(state='disabled')
    
    def tokenize(self, input_text):
        # Tokenización simple
        tokens = []
        i = 0
        n = len(input_text)
        
        while i < n:
            if input_text[i].isspace():
                i += 1
            elif input_text[i] in '()+*':
                tokens.append(input_text[i])
                i += 1
            else:
                # Identificador o palabra clave
                start = i
                while i < n and (input_text[i].isalnum() or input_text[i] == '_'):
                    i += 1
                tokens.append(input_text[start:i])
        
        return tokens
    
    def match(self, expected):
        if self.current_token < len(self.tokens) and self.tokens[self.current_token] == expected:
            self.current_token += 1
            return True
        return False
    
    # Gramática 1: E → E + T | T
    # T → T * F | F
    # F → (E) | id
    def E(self):
        self.console_callback(f"Llamando a E() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.E() and self.match('+') and self.T() or self.T()
    
    def T(self):
        self.console_callback(f"Llamando a T() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.T() and self.match('*') and self.F() or self.F()
    
    def F(self):
        self.console_callback(f"Llamando a F() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        if self.match('('):
            success = self.E()
            return success and self.match(')')
        else:
            token = self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'
            if token.isalpha() or token == 'id':
                self.current_token += 1
                return True
            return False
    
    # Gramática 2: L → A | F
    # F → (S)
    # S → SL | L
    # A → num | id
    def L(self):
        self.console_callback(f"Llamando a L() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.A() or self.F()
    
    def F(self):
        self.console_callback(f"Llamando a F() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        if self.match('('):
            success = self.S()
            return success and self.match(')')
        return False
    
    def S(self):
        self.console_callback(f"Llamando a S() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return (self.S() and self.L()) or self.L()
    
    def A(self):
        self.console_callback(f"Llamando a A() en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        token = self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'
        if token == 'num' or token == 'id':
            self.current_token += 1
            return True
        return False