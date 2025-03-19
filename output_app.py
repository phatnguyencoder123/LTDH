import tkinter as tk
import numpy as np
import ast
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class OutputApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.file_path = "D:/NetworkAutomation/LTDH/assets.txt"
        self.assets = {}  # Initialize the assets dictionary
        self.load_assets_from_text(self.file_path)  # Load assets from the file

        # Add a label to display results
        self.result_label = tk.Label(self, text="Kết quả sẽ được hiển thị ở đây", bg="white", fg="black")
        self.result_label.pack(pady=10)


    def load_assets_from_text(self, file_path):
        """Load data from assets.txt, correctly handling numbers and lists."""
        self.assets = {}  
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or ":" not in line:
                    continue  # Skip empty or incorrect lines
                
                try:
                    name, value = line.split(": ", 1)  # Split only once
                    
                    # Detect and convert lists correctly
                    if "[" in value and "]" in value:
                        self.assets[name.strip()] = ast.literal_eval(value.strip())  # Convert list safely
                    else:
                        self.assets[name.strip()] = float(value.strip())  # Convert numbers to float
                    
                except Exception as e:
                    print(f"Error reading line: {line} - {e}")  # Debugging message

    def principal_stress(self):
        """Tính ứng suất chính, phương chính và nhân tensor ứng suất với vector vận tốc."""
        # Reload dữ liệu từ file
        self.load_assets_from_text(self.file_path)

        # Lấy các giá trị ứng suất từ assets
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
        sorted_indices = np.argsort(self.principal_stresses)
        self.principal_stresses = self.principal_stresses[sorted_indices]
        self.eigenvectors = self.eigenvectors[:, sorted_indices]

        # Lấy vector vận tốc
        vx = self.assets.get("vx", 0.0)
        vy = self.assets.get("vy", 0.0)
        vz = self.assets.get("vz", 0.0)
        velocity_vector = np.array([vx, vy, vz])

        # Nhân tensor ứng suất với vector vận tốc
        stress_velocity_result = np.dot(stress_tensor, velocity_vector)

        # Hiển thị kết quả
        result_text = "Ứng suất chính:\n" + ", ".join([f"{stress:.2f}" for stress in self.principal_stresses])
        result_text += "\n\nPhương chính:\n"
        for i, vector in enumerate(self.eigenvectors.T, start=1):
            result_text += f"Vector {i}: [{', '.join([f'{v:.2f}' for v in vector])}]\n"

        result_text += "\nTích tensor ứng suất với vận tốc:\n"
        result_text += f"[{', '.join([f'{v:.2f}' for v in stress_velocity_result])}]"

        self.result_label.config(text=result_text)

        # Ghi kết quả vào file
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write("\n# Kết quả tính toán\n")
            for i, stress in enumerate(self.principal_stresses, start=1):
                file.write(f"principal_stress_{i}: {stress:.2f}\n")
            file.write("# Phương chính\n")
            for i, vector in enumerate(self.eigenvectors.T, start=1):
                vector_str = ", ".join([f"{v:.2f}" for v in vector])
                file.write(f"principal_direction_{i}: [{vector_str}]\n")
            file.write("# Tích tensor ứng suất với vận tốc\n")
            file.write(f"stress_velocity_result: [{', '.join([f'{v:.2f}' for v in stress_velocity_result])}]\n")

        print("Đã lưu ứng suất chính, phương chính và kết quả nhân với vận tốc vào file assets.txt")
