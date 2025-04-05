import tkinter as tk
from input_app import InputApp
from output_app  import OutputApp
from mohrcircle  import MohrsCircleApp
from showobject  import ShowObjectApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stress Manager")
        self.geometry("800x400")

        # Tạo Frame chứa tất cả giao diện
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        # Khởi tạo InputApp trước để có thể lấy dữ liệu đầu vào
        self.input_app = InputApp(container, self)
        self.input_app.grid(row=0, column=0, padx=30, pady=10)

        # Khởi tạo OutputApp, truyền dữ liệu từ InputApp vào
        self.output_app = OutputApp(container, self)
        self.output_app.grid(row=0, column=1, padx=30, pady=10)

        self.mohrcircle = MohrsCircleApp(container, self)  # <-- Kiểm tra kỹ tên biến!
        self.mohrcircle.grid(row=0, column=2, padx=30, pady=10)

        self.showobject = ShowObjectApp(container, self)
        self.showobject.grid(row=0, column=3, padx=30, pady=10)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()






























