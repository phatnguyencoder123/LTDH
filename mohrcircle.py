import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk




class MohrsCircleApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.file_path = "D:/NetworkAutomation/LTDH/assets.txt"
        self.assets = {}
        self.load_assets_from_text(self.file_path)  # Load dữ liệu từ file


        # Label hiển thị kết quả
        self.result_label = tk.Label(self, text="", fg="black", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Vùng vẽ đồ thị
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)

        # Toolbar để phóng to/thu nhỏ
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack()

    



    def load_assets_from_text(self, file_path):
        """Đọc dữ liệu từ file assets.txt"""
        self.assets = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                try:
                    name, value = line.split(":")
                    self.assets[name.strip()] = float(value.strip())
                except ValueError:
                   pass

    def calculate(self):
        """Tính toán ứng suất và vẽ các vòng tròn Mohr"""
        self.load_assets_from_text(self.file_path)  # Cập nhật dữ liệu mới nhất

        # Lấy dữ liệu ứng suất từ file
        sigma_x = self.assets.get("sigma_x", 0.0)
        sigma_y = self.assets.get("sigma_y", 0.0)
        sigma_z = self.assets.get("sigma_z", 0.0)
        tau_xy = self.assets.get("tau_xy", 0.0)
        tau_yz = self.assets.get("tau_yz", 0.0)
        tau_xz = self.assets.get("tau_xz", 0.0)

        # Tính toán các vòng tròn Mohr
        circles = [
            ("XY Plane", sigma_x, sigma_y, tau_xy),
            ("YZ Plane", sigma_y, sigma_z, tau_yz),
            ("ZX Plane", sigma_z, sigma_x, tau_xz)
        ]

        self.ax.clear()  # Xóa đồ thị cũ

        result_text = "Ứng suất chính:\n"
        for name, sigma_1, sigma_2, tau in circles:
            center = (sigma_1 + sigma_2) / 2
            radius = np.sqrt(((sigma_1 - sigma_2) / 2) ** 2 + tau ** 2)
            sigma_max, sigma_min = center + radius, center - radius

            # Vẽ vòng tròn Mohr
            theta = np.linspace(0, 2*np.pi, 100)
            circle_x = center + radius * np.cos(theta)
            circle_y = radius * np.sin(theta)

            self.ax.plot(circle_x, circle_y, label=f"{name} Circle")
            self.ax.scatter([sigma_1, sigma_2], [tau, -tau], marker="o", color="red")

            result_text += f"{name}: σmax = {sigma_max:.2f}, σmin = {sigma_min:.2f}\n"

        self.ax.axhline(0, color="black", linestyle="--")
        self.ax.set_xlabel("Normal Stress (σ)")
        self.ax.set_ylabel("Shear Stress (τ)")
        self.ax.legend(draggable=True)  # Cho phép di chuyển legend bằng chuột
        self.ax.grid()

        # Hiển thị kết quả và vẽ lại đồ thị
        self.result_label.config(text=result_text, bg="white")
        self.canvas.draw()
