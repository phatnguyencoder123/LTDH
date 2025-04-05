import tkinter as tk
from tkinter import messagebox
import time 
import os
from output_app import OutputApp
from mohrcircle import MohrsCircleApp
from showobject import ShowObjectApp



class InputApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller  
        self.file_path =  "C:/HCMUT Learn/NetworkAutomation/LTDH/assets.txt"
        self.labels = [" sigma_x", "sigma_y", "sigma_z", "tau_xy", "tau_xz", "tau_yz","vx", "vy", "vz"]

        header_label = tk.Label(
            self,
            text="Nhập các giá trị ứng suất",
            fg="black",
            bg="white",
        )
        header_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Danh sách các ô nhập liệu để dễ chuyển tiếp
        self.entries = []

        # Tạo các ô nhập dữ liệu
        self.create_label_entry("σx:", 0)
        self.create_label_entry("σy:", 1)
        self.create_label_entry("σz:", 2)
        self.create_label_entry("τxy:", 3)
        self.create_label_entry("τxz:", 4)
        self.create_label_entry("τyz:", 5)
        self.create_label_entry("vx:", 6)
        self.create_label_entry("vy:", 7)
        self.create_label_entry("vz:", 8)





        # Gán sự kiện Enter cho từng ô nhập liệu
        for i, entry in enumerate(self.entries):
            entry.bind("<Return>", lambda event, idx=i: self.move_next_entry(idx, 1))  # Nhấn Enter = Xuống
            entry.bind("<Down>", lambda event, idx=i: self.move_next_entry(idx, 1))   # Nhấn ↓ = Xuống
            entry.bind("<Up>", lambda event, idx=i: self.move_next_entry(idx, -1))    # Nhấn ↑ = Lên

        self.load_entries()

        # Save button
        save_button = tk.Button(self, text="Tính toán", command=self.call_function, bg="lightblue")
        save_button.grid(row=len(self.labels) + 1, column=0, columnspan=2, pady=10)


    def call_function(self):
        '''gọi các hàm tính toán trong các file'''
        self.save_entries()
        time.sleep(0.1)

        self.controller.output_app.principal_stress()
        self.controller.mohrcircle.calculate()
        self.controller.update()  # Làm mới giao diện

        self.controller.showobject.update_3d_object()

        print("call_function")

        
    def create_label_entry(self, text, row):
        """Tạo nhãn và ô nhập liệu cho từng ô nhập liệu"""
        tk.Label(self, text=text, fg="black", bg="white").grid(row=row+1, column=0, padx=10, pady=10)
        entry = tk.Entry(self)
        entry.grid(row=row+1, column=1, padx=10, pady=5)
        self.entries.append(entry)

    def move_next_entry(self, index, direction):
        """
        Di chuyển đến ô nhập liệu tiếp theo hoặc trước đó.
        - index: Chỉ số hiện tại của ô nhập liệu.
        - direction: 1 (xuống), -1 (lên).
        """
        try:
            # Lấy giá trị nhập và kiểm tra số hợp lệ
            value = float(self.entries[index].get()) if self.entries[index].get() else 0.0
            print(f"Nhập thành công: {value}")

            # Xác định chỉ số ô nhập tiếp theo
            new_index = index + direction
            if 0 <= new_index < len(self.entries):  # Kiểm tra hợp lệ
                self.entries[new_index].focus()
        except ValueError:
            # Hiển thị thông báo lỗi nếu nhập sai
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập số hợp lệ!")
            self.entries[index].delete(0, tk.END)  # Xóa nội dung sai
            self.entries[index].focus()  # Giữ lại ô nhập lỗi để nhập lại
    
    def load_entries(self):
        """Tải dữ liệu từ file assets.txt nếu có"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    try:
                        parts = line.strip().split(": ")
                        if len(parts) == 2:  
                            value = parts[1].strip()
                            if i < len(self.entries):  
                                self.entries[i].insert(0, value)
                    except Exception as e:
                        print(f"Lỗi khi tải dòng {i + 1}: {e}")
        print("Đã tải dữ liệu từ file assets.txt")

    def save_entries(self):
        """Lưu dữ liệu vào file assets.txt"""
        values = [entry.get() if entry.get() else "0" for entry in self.entries] 
        with open(self.file_path, "w") as file:
            for label, value in zip(self.labels, values):
                file.write(f"{label}: {value}\n")
        print("Đã lưu dữ liệu vào file assets.txt")

    