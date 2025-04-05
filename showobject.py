import tkinter as tk
import numpy as np
import ast
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class ShowObjectApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = "C:/HCMUT Learn/NetworkAutomation/LTDH/assets.txt"
        self.assets = {}
        self.principal_directions = []
        self.fig = None
        self.ax = None
        self.canvas = None
        self.toolbar = None

    def load_assets_from_text(self):
        """lấy giá trị các biến từ file assest.txt"""
        self.assets = {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
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
        except FileNotFoundError:
            print("Không tìm thấy file assets.txt")

    def load_vectors(self):
        """đọc số liệu từ file text"""
        self.load_assets_from_text()
        self.principal_directions = [
            np.array(self.assets.get(f"principal_direction_{i}", [0, 0, 0])) for i in range(1, 4)
        ]
        self.velocity_vector = np.array([
            self.assets.get("vx", 0.0),
            self.assets.get("vy", 0.0),
            self.assets.get("vz", 0.0)
        ])


        self.stress_velocity_result = np.array(self.assets.get("stress_vector", [0.0, 0.0, 0.0]))

    def update_3d_object(self):
        
        """vẽ lại trường hợp mới"""
        self.load_vectors()

        # Kiểm tra có đủ dữ liệu để vẽ không
        if len(self.principal_directions) != 3:
            print("Chưa đủ 3 vector phương chính, không thể vẽ")
            return

        # Xóa canvas và toolbar cũ nếu có
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.toolbar:
            self.toolbar.destroy()

        # Tính độ dài trung bình của vector phương chính
        principal_lengths = [np.linalg.norm(vec) for vec in self.principal_directions]
        avg_principal_length = np.mean(principal_lengths)

        # Hàm chuẩn hóa vector về độ dài tương tự vector phương chính
        def normalize_vector(vec, target_length):
            norm = np.linalg.norm(vec)
            return (vec * target_length / norm) if norm > 0 else vec

        # Chuẩn hóa vector vận tốc và stress_velocity_result
        self.velocity_vector = normalize_vector(self.velocity_vector, avg_principal_length)
        self.stress_velocity_result = normalize_vector(self.stress_velocity_result, avg_principal_length)

        # Tạo Figure mới
        self.fig = plt.figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.view_init(elev=20, azim=30)  # Góc nhìn mặc định

        # Giới hạn tọa độ khối lập phương
        r = np.array([-1, 1])
        X, Y = np.meshgrid(r, r)

        # Vẽ các mặt khối lập phương
        self.ax.plot_surface(X, Y, np.full_like(X, 1), alpha=0.5, color='red')    
        self.ax.plot_surface(X, Y, np.full_like(X, -1), alpha=0.5, color='blue')   
        self.ax.plot_surface(X, np.full_like(X, -1), Y, alpha=0.5, color='green')  
        self.ax.plot_surface(X, np.full_like(X, 1), Y, alpha=0.5, color='yellow')  
        self.ax.plot_surface(np.full_like(X, -1), X, Y, alpha=0.5, color='purple') 
        self.ax.plot_surface(np.full_like(X, 1), X, Y, alpha=0.5, color='orange')  

        # Gốc tọa độ xuất phát từ (-1, -1, -1)
        start_x, start_y, start_z = 0, 0, 0  
        self.ax.set_ylim(-1, 1)  

        # Vẽ 3 vector phương chính
        colors = ['red', 'green', 'blue']
        for i, direction in enumerate(self.principal_directions):
            self.ax.quiver(start_x, start_y, start_z,  
                            direction[0], direction[1], direction[2],  
                            color=colors[i], arrow_length_ratio=0.2, linewidth=2, label=f"Phương chính thứ {i+1}")

        # Vẽ cosin chỉ phương (màu tím)
        self.ax.quiver(start_x, start_y, start_z,  
                        self.velocity_vector[0], self.velocity_vector[1], self.velocity_vector[2],  
                        color='purple', arrow_length_ratio=0.2, linewidth=2, label="cosin chỉ phương")

        # Vẽ vector ứng suất ứng với cosin chỉ phương (màu đen)
        self.ax.quiver(start_x, start_y, start_z,  
                        self.stress_velocity_result[0], self.stress_velocity_result[1], self.stress_velocity_result[2],  
                        color='black', arrow_length_ratio=0.2, linewidth=2, label="vector ứng suất ứng với cosin chỉ phương")
        
        
        

        
        # Cấu hình trục
        self.ax.set_xlabel("X",fontsize = 14, fontweight='bold')
        self.ax.set_ylabel("Y",fontsize = 14, fontweight='bold')
        self.ax.set_zlabel("Z",fontsize = 14, fontweight='bold')
        self.ax.set_title("Hiển thị hướng các vector tương ứng tại phân tố đang xét",fontweight='bold')
        self.ax.legend().set_draggable(True)

        # Hiển thị trên giao diện Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Thêm thanh công cụ tương tác
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack()

        self.canvas.draw()
        print(f"Đã vẽ xong tất cả vector tại gốc tọa độ ({start_x}, {start_y}, {start_z}) với độ dài chuẩn hóa")

