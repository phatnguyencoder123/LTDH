import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MohrsCircleApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.file_path = "C:/HCMUT Learn/NetworkAutomation/LTDH/assets.txt"
        self.assets = {}
        self.load_assets_from_text(self.file_path)

        self.result_frame = tk.Frame(self, bg="white", padx=10, pady=10, bd=2, relief="solid")
        self.result_frame.pack(pady=10)
        self.result_frame.pack_forget()

        self.result_label = tk.Label(self.result_frame, text="", fg="black", bg="white", justify="left")
        self.result_label.pack()


        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack()

    def load_assets_from_text(self, file_path):
        """đọc giá trị các biến từ file assest.txt"""
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
        self.load_assets_from_text(self.file_path)

        sigma_x = self.assets.get("sigma_x", 0.0)
        sigma_y = self.assets.get("sigma_y", 0.0)
        tau_xy = self.assets.get("tau_xy", 0.0)

        center = (sigma_x + sigma_y) / 2
        radius = np.sqrt(((sigma_x - sigma_y) / 2) ** 2 + tau_xy ** 2)
        sigma_max, sigma_min = center + radius, center - radius

        # xóa đồ thị trước đó
        self.ax.clear()
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = center + radius * np.cos(theta)
        circle_y = radius * np.sin(theta)

        # Draw Mohr's Circle
        self.ax.plot(circle_x, circle_y, label="Vòng tròn Mohr", color="blue", linewidth=2)
        self.ax.scatter([sigma_x, sigma_y], [tau_xy, -tau_xy], marker="o", color="black", label="Ứng suất trong mặt xy")
        self.ax.scatter([sigma_max, sigma_min], [0, 0], marker="o", color="red", label="Ứng suất pháp max min trong mặt xy")
        self.ax.scatter([center, center], [radius, -radius], marker="o", color="green", label="ứng suất tiếp max min trong mặt xy")

        # Axes and labels
        self.ax.axhline(0, color="black", linestyle="--")
        self.ax.axvline(center, color="green", linestyle="dashed")
        self.ax.set_xlabel("ứng suất pháp (σ)", fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Ứng suất tiếp (τ)", fontsize=12, fontweight='bold')
        self.ax.set_title("Vòng tròn Mohr xét trong mặt phẳng xy", fontsize=14, fontweight='bold')
        self.ax.legend(loc="upper right", frameon=True, facecolor='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)

        # Display results
        result_text = (
            "Ứng suất max min trong mặt phẳng xy\n"
            "-------------------------\n"
            f"σ_max: {sigma_max:.4f}\n"
            f"σ_min: {sigma_min:.4f}\n"
            "-------------------------\n"
            "Lưu ý rằng ứng suất này không phải ứng suất chính"
        )

        self.ax.legend().set_draggable(True)
        self.result_label.config(text=result_text, bg="lightyellow",justify="center")
        self.result_frame.config(bg="lightyellow")
        self.result_frame.pack(pady=10)
        self.canvas.draw()
