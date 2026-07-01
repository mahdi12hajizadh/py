import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core.canvas_manager import CanvasManager
from core.event_handler import EventHandler
from core.state_manager import StateManager
from engine.code_generator import CodeGenerator
from engine.code_runner import CodeRunner
from models.flowchart import Flowchart
from theme.theme_manager import ThemeManager
from storage.file_manager import FileManager

class FlowPyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FlowPy Studio")
        self.root.geometry("1200x800")
        
        # Initialize core components
        self.flowchart = Flowchart()
        self.canvas_manager = CanvasManager(self.flowchart)
        self.event_handler = EventHandler(self.canvas_manager, self.flowchart)
        self.event_handler.set_ui(self)
        self.state_manager = StateManager(self.flowchart)
        
        # connect state_manager to canvas_manager for Undo/Redo
        self.canvas_manager.state_manager = self.state_manager
        print("state_manager connected to canvas_manager!")
        
        self.theme_manager = ThemeManager()
        self.file_manager = FileManager()
        self.code_generator = CodeGenerator()
        self.code_runner = CodeRunner()
        
        self.setup_ui()
        self.setup_menu()
        self.apply_theme()
        
    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar
        self.toolbar = ttk.Frame(main_container)
        self.toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # Tool buttons
        btn_select = ttk.Button(self.toolbar, text="Select", command=lambda: self.set_tool("select"))
        btn_select.pack(side=tk.LEFT, padx=2)
        
        btn_start = ttk.Button(self.toolbar, text="Start", command=lambda: self.set_tool("start"))
        btn_start.pack(side=tk.LEFT, padx=2)
        
        btn_process = ttk.Button(self.toolbar, text="Process", command=lambda: self.set_tool("process"))
        btn_process.pack(side=tk.LEFT, padx=2)
        
        btn_decision = ttk.Button(self.toolbar, text="Decision", command=lambda: self.set_tool("decision"))
        btn_decision.pack(side=tk.LEFT, padx=2)
        
        btn_io = ttk.Button(self.toolbar, text="IO", command=lambda: self.set_tool("io"))
        btn_io.pack(side=tk.LEFT, padx=2)
        
        btn_arrow = ttk.Button(self.toolbar, text="Arrow", command=lambda: self.set_tool("arrow"))
        btn_arrow.pack(side=tk.LEFT, padx=2)
        
        #btn_text = ttk.Button(self.toolbar, text="Text", command=lambda: self.set_tool("text"))
        #btn_text.pack(side=tk.LEFT, padx=2)
        
        # Test button
        #test_btn = ttk.Button(self.toolbar, text="TEST", command=self.test_draw)
        #test_btn.pack(side=tk.LEFT, padx=10)
        
        # Undo/Redo buttons
        btn_undo = ttk.Button(self.toolbar, text="Undo", command=self.undo)
        btn_undo.pack(side=tk.LEFT, padx=2)
        
        btn_redo = ttk.Button(self.toolbar, text="Redo", command=self.redo)
        btn_redo.pack(side=tk.LEFT, padx=2)
            
        # Canvas area
        canvas_frame = tk.Frame(main_container, relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#000000", width=800, height=600, 
                               highlightthickness=2, highlightbackground="#333333")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.canvas_manager.set_canvas(self.canvas)
        
        # Bind events
        self.canvas.bind("<Button-1>", self.event_handler.on_click)
        self.canvas.bind("<B1-Motion>", self.event_handler.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.event_handler.on_release)
        self.canvas.bind("<KeyPress>", self.event_handler.on_keypress)
        self.canvas.bind("<Double-Button-1>", self.event_handler.on_double_click)
        self.canvas.focus_set()
        
        # Right panel
        right_panel = ttk.Frame(main_container, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        code_label = ttk.Label(right_panel, text="Generated Code:", foreground="black", background="#FFFFFF")
        code_label.pack(anchor=tk.W)
        
        self.code_text = tk.Text(right_panel, height=15, bg="#000000", fg="#FFFFFF")
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        output_label = ttk.Label(right_panel, text="Output:", foreground="black", background="#FFFFFF")
        output_label.pack(anchor=tk.W)
        
        self.output_text = tk.Text(right_panel, height=10, bg="#000000", fg="#FFFFFF")
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.Frame(right_panel)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Generate Code", command=self.generate_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Run Code", command=self.run_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=2)
        
        self.status_bar = ttk.Label(self.root, text="Ready - Click on canvas to draw", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def set_tool(self, tool):
        """تغییر ابزار"""
        print(f"Setting tool to: {tool}")
        self.event_handler.current_tool = tool
        
        if tool != "arrow":
            self.canvas_manager.arrow_start = None
            
        self.status_bar.config(text=f"Tool: {tool} - Click on canvas to draw")
        
    def test_draw(self):
        """تست کانواس"""
        print("TEST button clicked!")
        self.canvas.create_oval(50, 50, 150, 150, fill="red", outline="white", width=3)
        self.canvas.create_text(100, 100, text="TEST", fill="white", font=("Arial", 14, "bold"))
        self.status_bar.config(text="Test shape drawn!")
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Export PNG", command=self.export_png)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=self.clear_all)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def undo(self):
        print("Undo called")
        if self.state_manager.undo():
            self.canvas_manager.render()
            self.status_bar.config(text="Undo done")
            print("Undo successful!")
        else:
            self.status_bar.config(text="Nothing to undo")
            print("Nothing to undo")
            
    def redo(self):
        print("Redo called")
        if self.state_manager.redo():
            self.canvas_manager.render()
            self.status_bar.config(text="Redo done")
            print("Redo successful!")
        else:
            self.status_bar.config(text="Nothing to redo")
            print("Nothing to redo")
        
    def generate_code(self):
        try:
            code = self.code_generator.generate(self.flowchart)
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(1.0, code)
            self.status_bar.config(text="Code generated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code: {str(e)}")
            
    def run_code(self):
        code = self.code_text.get(1.0, tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "No code to run. Generate code first.")
            return
        try:
            output = self.code_runner.run(code)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, output)
            self.status_bar.config(text="Code executed successfully")
        except Exception as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, f"Error: {str(e)}")
            self.status_bar.config(text="Code execution failed")
            
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        
    def new_project(self):
        if messagebox.askyesno("New Project", "Clear current project?"):
            self.flowchart.clear()
            self.canvas.delete("all")
            self.code_text.delete(1.0, tk.END)
            self.output_text.delete(1.0, tk.END)
            self.state_manager.clear()
            self.status_bar.config(text="New project created")
            
    def save_project(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".flowpy",
            filetypes=[("FlowPy Project", "*.flowpy"), ("All Files", "*.*")]
        )
        if filename:
            try:
                self.file_manager.save_project(self.flowchart, filename)
                self.status_bar.config(text=f"Project saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save project: {str(e)}")
                
    def load_project(self):
        filename = filedialog.askopenfilename(
            filetypes=[("FlowPy Project", "*.flowpy"), ("All Files", "*.*")]
        )
        if filename:
            try:
                self.flowchart = self.file_manager.load_project(filename)
                self.canvas_manager.flowchart = self.flowchart
                self.event_handler.flowchart = self.flowchart
                self.state_manager.flowchart = self.flowchart
                self.canvas_manager.render()
                self.status_bar.config(text=f"Project loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project: {str(e)}")
                
    def export_png(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            try:
                self.file_manager.export_png(self.canvas, filename)
                self.status_bar.config(text=f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
                
    def clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all shapes and arrows?"):
            self.flowchart.clear()
            self.canvas.delete("all")
            self.state_manager.clear()
            self.status_bar.config(text="Cleared all")
            
    def toggle_theme(self):
        self.theme_manager.toggle_theme()
        self.apply_theme()
        self.status_bar.config(text=f"Theme: {self.theme_manager.current_theme}")
        
    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        self.canvas.config(bg="#000000")
        self.code_text.config(bg="#000000", fg="#ffffff")
        self.output_text.config(bg="#000000", fg="#ffffff")
        self.root.config(bg="#000000")
        
    def show_about(self):
        messagebox.showinfo("About FlowPy Studio", 
                           "FlowPy Studio v1.0\n\n"
                           "A flowchart-based Python development environment\n"
                           "Design -> Generate -> Run\n\n"
                           "Created by Mahdi_Hajizadh with Python")