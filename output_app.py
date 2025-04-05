import tkinter as tk
from math import *
import numpy as np
import ast
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class OutputApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.file_path = "C:/HCMUT Learn/NetworkAutomation/LTDH/assets.txt"
        self.assets = {}  
        self.load_assets_from_text(self.file_path) 


        self.result_label = tk.Label(self, text="Kết quả sẽ được hiển thị ở đây", 
                                     bg="white", fg="black")
        self.result_label.pack(pady=10, padx=10, fill="both")



    def load_assets_from_text(self, file_path):
        """lấy giá trị các biến từ file assest.txt"""
        self.assets = {}  
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or ":" not in line:
                    continue  
                
                try:
                    name, value = line.split(": ", 1)  
                    
                    if "[" in value and "]" in value:
                        self.assets[name.strip()] = ast.literal_eval(value.strip()) 
                    else:
                        self.assets[name.strip()] = float(value.strip()) 
                    
                except Exception as e:
                    print(f"Lỗi khi đọc dòng: {line} - {e}") 

    def principal_stress(self):
        """Tính ứng suất chính, phương chính và vector ứng suất tương ứng hướng được nhập."""

        self.load_assets_from_text(self.file_path)


        sigma_x = self.assets.get("sigma_x", 0.0)
        tau_xy = self.assets.get("tau_xy", 0.0)
        tau_xz = self.assets.get("tau_xz", 0.0)
        sigma_y = self.assets.get("sigma_y", 0.0)
        tau_yz = self.assets.get("tau_yz", 0.0)
        sigma_z = self.assets.get("sigma_z", 0.0)

        # Tạo tensor ứng suất
        stress_tensor = np.array([
            [sigma_x, tau_xy, tau_xz],
            [tau_xy, sigma_y, tau_yz],
            [tau_xz, tau_yz, sigma_z]
        ])

        # Tính ứng suất chính và phương chính
        self.principal_stresses, self.eigenvectors = np.linalg.eig(stress_tensor)
        sorted_indices = np.argsort(self.principal_stresses)[::-1]
        self.principal_stresses = self.principal_stresses[sorted_indices]
        self.eigenvectors = self.eigenvectors[:, sorted_indices]

        # Lấy giá trị cosin chỉ phưởng
        vx = self.assets.get("vx", 0.0)
        vy = self.assets.get("vy", 0.0)
        vz = self.assets.get("vz", 0.0)
        velocity_vector = np.array([vx/sqrt(vx**2 + vy**2 +vz**2), vy/sqrt(vx**2 + vy**2 +vz**2), vz/sqrt(vx**2 + vy**2 +vz**2)])

        # Nhân tensor ứng suất với vector vận tốc
        stress_velocity_result = np.dot(stress_tensor, velocity_vector)

        # Hiển thị kết quả
        result_text = "Ứng suất chính:\n" 
        result_text += "\n".join([f"Ứng suất chính thứ {i+1}: {stress:.4f}" for i, stress in enumerate(self.principal_stresses)])
        result_text += "\n\nPhương chính:\n" 
        for i, vector in enumerate(self.eigenvectors.T, start=1):
            result_text += f"Phướng chính thứ {i}: [{', '.join([f'{v:.4f}' for v in vector])}]\n"

        result_text += "\nVector ứng suất tương ứng với cosin chỉ phương được nhập\n" 
        result_text += f"[{', '.join([f'{v:.4f}' for v in stress_velocity_result])}]"

        self.result_label.config(text=result_text)

        # Ghi kết quả vào file
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write("\nKết quả tính toán\n")
            for i, stress in enumerate(self.principal_stresses, start=1):
                file.write(f"principal_stress_{i}: {stress:.4f}\n")
            file.write("Phương chính\n")
            for i, vector in enumerate(self.eigenvectors.T, start=1):
                vector_str = ", ".join([f"{v:.4f}" for v in vector])
                file.write(f"principal_direction_{i}: [{vector_str}]\n")
            file.write("Vector ứng suất tương ứng với cosin chỉ phương được nhập\n")
            file.write(f"stress_vector: [{', '.join([f'{v:.4f}' for v in stress_velocity_result])}]\n")

        print("Output đã được ghi")
