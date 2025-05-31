import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

class ModuleD:
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
            text="Gramática 1: S → a A | a B, A → b, B → c", 
            variable=self.grammar_var, 
            value="grammar1",
            command=self.setup_grammar1
        )
        self.grammar1_rb.pack(anchor=tk.W)
        
        self.grammar2_rb = ttk.Radiobutton(
            grammar_frame, 
            text="Gramática 2: E → E | Ea | Fb | F, F → (E) | Bbe | Bba, B → Ba | C | b, C → a | CbC", 
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
        
        # Frame para opciones
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.backtrack_var = tk.BooleanVar(value=True)
        backtrack_cb = ttk.Checkbutton(
            options_frame, 
            text="Usar Backtracking", 
            variable=self.backtrack_var
        )
        backtrack_cb.pack(side=tk.LEFT, padx=5)
        
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
        self.console_callback("Gramática 1 seleccionada: S → a A | a B, A → b, B → c")
    
    def setup_grammar2(self):
        self.current_grammar = "grammar2"
        self.grammar_var.set("grammar2")
        self.console_callback("Gramática 2 seleccionada: E → E | Ea | Fb | F, F → (E) | Bbe | Bba, B → Ba | C | b, C → a | CbC")
    
    def analyze_input(self):
        input_text = self.input_entry.get().strip()
        if not input_text:
            messagebox.showerror("Error", "Por favor ingrese una expresión para analizar")
            return
        
        self.console_callback(f"\nAnalizando entrada: '{input_text}'")
        
        # Tokenizar la entrada
        self.tokens = list(input_text)  # Para estas gramáticas simples, cada carácter es un token
        self.current_token = 0
        
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        
        try:
            if self.current_grammar == "grammar1":
                if self.backtrack_var.get():
                    success = self.S_with_backtracking()
                else:
                    success = self.S_no_backtracking()
                
                if success and self.current_token == len(self.tokens):
                    self.result_text.insert(tk.END, "Análisis exitoso: La entrada es válida\n")
                    self.console_callback("Análisis exitoso")
                else:
                    self.result_text.insert(tk.END, f"Error de sintaxis en el token: {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}\n")
                    self.console_callback("Error de sintaxis")
            else:
                if self.backtrack_var.get():
                    success = self.E_with_backtracking()
                else:
                    success = self.E_no_backtracking()
                
                if success and self.current_token == len(self.tokens):
                    self.result_text.insert(tk.END, "Análisis exitoso: La entrada es válida\n")
                    self.console_callback("Análisis exitoso")
                else:
                    self.result_text.insert(tk.END, f"Error de sintaxis en el token: {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}\n")
                    self.console_callback("Error de sintaxis")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error inesperado: {str(e)}\n")
            self.console_callback(f"Error inesperado: {str(e)}")
        
        self.result_text.config(state='disabled')
    
    def match(self, expected):
        if self.current_token < len(self.tokens) and self.tokens[self.current_token] == expected:
            self.current_token += 1
            return True
        return False
    
    # Gramática 1: S → a A | a B
    # A → b
    # B → c
    
    # Versión sin backtracking (solo prueba la primera opción)
    def S_no_backtracking(self):
        self.console_callback(f"Llamando a S() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        if self.match('a'):
            return self.A_no_backtracking()  # Solo prueba A, nunca prueba B
        return False
    
    def A_no_backtracking(self):
        self.console_callback(f"Llamando a A() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.match('b')
    
    def B_no_backtracking(self):
        self.console_callback(f"Llamando a B() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.match('c')
    
    # Versión con backtracking manual
    def S_with_backtracking(self):
        self.console_callback(f"Llamando a S() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        save_pos = self.current_token
        
        # Prueba la primera opción: a A
        if self.match('a') and self.A_with_backtracking():
            return True
        
        # Si falla, retrocede y prueba la segunda opción
        self.current_token = save_pos
        
        # Prueba la segunda opción: a B
        if self.match('a') and self.B_with_backtracking():
            return True
        
        # Si ambas fallan, retrocede completamente
        self.current_token = save_pos
        return False
    
    def A_with_backtracking(self):
        self.console_callback(f"Llamando a A() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.match('b')
    
    def B_with_backtracking(self):
        self.console_callback(f"Llamando a B() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        return self.match('c')
    
    # Gramática 2: E → E | Ea | Fb | F
    # F → (E) | Bbe | Bba
    # B → Ba | C | b
    # C → a | CbC
    
    # Versión sin backtracking (solo prueba la primera opción)
    def E_no_backtracking(self):
        self.console_callback(f"Llamando a E() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        # Solo prueba la primera opción: E
        return self.E_no_backtracking()  # Esto causará recursión infinita
    
    def F_no_backtracking(self):
        self.console_callback(f"Llamando a F() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        # Solo prueba la primera opción: (E)
        if self.match('('):
            success = self.E_no_backtracking()
            return success and self.match(')')
        return False
    
    def B_no_backtracking(self):
        self.console_callback(f"Llamando a B() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        # Solo prueba la primera opción: Ba
        return self.B_no_backtracking() and self.match('a')  # Esto causará recursión infinita
    
    def C_no_backtracking(self):
        self.console_callback(f"Llamando a C() sin backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        # Solo prueba la primera opción: a
        return self.match('a')
    
    # Versión con backtracking manual
    def E_with_backtracking(self):
        self.console_callback(f"Llamando a E() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        save_pos = self.current_token
        
        # Opción 1: E
        if self.E_with_backtracking():
            return True
        self.current_token = save_pos
        
        # Opción 2: Ea
        if self.E_with_backtracking() and self.match('a'):
            return True
        self.current_token = save_pos
        
        # Opción 3: Fb
        if self.F_with_backtracking() and self.match('b'):
            return True
        self.current_token = save_pos
        
        # Opción 4: F
        if self.F_with_backtracking():
            return True
        self.current_token = save_pos
        
        return False
    
    def F_with_backtracking(self):
        self.console_callback(f"Llamando a F() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        save_pos = self.current_token
        
        # Opción 1: (E)
        if self.match('('):
            if self.E_with_backtracking() and self.match(')'):
                return True
            self.current_token = save_pos
        else:
            self.current_token = save_pos
        
        # Opción 2: Bbe
        if self.B_with_backtracking() and self.match('b') and self.match('e'):
            return True
        self.current_token = save_pos
        
        # Opción 3: Bba
        if self.B_with_backtracking() and self.match('b') and self.match('a'):
            return True
        self.current_token = save_pos
        
        return False
    
    def B_with_backtracking(self):
        self.console_callback(f"Llamando a B() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        save_pos = self.current_token
        
        # Opción 1: Ba
        if self.B_with_backtracking() and self.match('a'):
            return True
        self.current_token = save_pos
        
        # Opción 2: C
        if self.C_with_backtracking():
            return True
        self.current_token = save_pos
        
        # Opción 3: b
        if self.match('b'):
            return True
        self.current_token = save_pos
        
        return False
    
    def C_with_backtracking(self):
        self.console_callback(f"Llamando a C() con backtracking en token {self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'EOF'}")
        save_pos = self.current_token
        
        # Opción 1: a
        if self.match('a'):
            return True
        self.current_token = save_pos
        
        # Opción 2: CbC
        if self.C_with_backtracking() and self.match('b') and self.C_with_backtracking():
            return True
        self.current_token = save_pos
        
        return False