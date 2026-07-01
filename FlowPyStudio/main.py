import tkinter as tk
from ui import FlowPyUI

def main():
    root = tk.Tk()
    app = FlowPyUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()