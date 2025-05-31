import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from modules.module_a import ModuleA
from modules.module_b import ModuleB
from modules.module_d import ModuleD

class ParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico Recursivo")
        self.root.geometry("900x700")
        
        self.create_widgets()
        self.setup_modules()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook para los módulos
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el módulo A
        self.tab_a = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_a, text="Parser Recursivo Directo")
        
        # Frame para el módulo B
        self.tab_b = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_b, text="Parser con Gramática Transformada")
        
        # Frame para el módulo D
        self.tab_d = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_d, text="Parser con Backtracking")
        
        # Consola de salida
        self.console_frame = ttk.Frame(self.main_frame)
        self.console_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.console_label = ttk.Label(self.console_frame, text="Consola de Salida:")
        self.console_label.pack(anchor=tk.W)
        
        self.console = scrolledtext.ScrolledText(
            self.console_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=10,
            state='disabled'
        )
        self.console.pack(fill=tk.BOTH, expand=True)
    
    def setup_modules(self):
        # Inicializar cada módulo con su frame y la consola
        self.module_a = ModuleA(self.tab_a, self.print_to_console)
        self.module_b = ModuleB(self.tab_b, self.print_to_console)
        self.module_d = ModuleD(self.tab_d, self.print_to_console)
    
    def print_to_console(self, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ParserApp(root)
    root.mainloop()