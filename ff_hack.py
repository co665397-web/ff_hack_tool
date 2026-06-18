# -*- coding: utf-8 -*-
import os
import sys
import json
import subprocess
import shutil
import random
import string

# Đường dẫn đến file cấu hình game Free Fire (thường nằm trong /data/data/com.dts.freefireth/)
# Để làm việc không cần root, cần quyền truy cập Android/data/ qua ADB hoặc Shizuku
GAME_DATA_PATH = "/storage/emulated/0/Android/data/com.dts.freefireth/files/"
TARGET_CONFIG = "app_data.json" # Ví dụ file cấu hình

def generate_fake_data():
    """Tạo chuỗi dữ liệu giả để mô phỏng 'dán data'."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

def create_hack_file():
    # 1. Kiểm tra thư mục tồn tại
    if not os.path.exists(GAME_DATA_PATH):
        print(f"Lỗi: Đường dẫn {GAME_DATA_PATH} không tồn tại. Hãy cấp quyền lưu trữ.")
        sys.exit(1)

    # 2. Tạo bản sao lưu file gốc (nếu có)
    backup_path = os.path.join(GAME_DATA_PATH, TARGET_CONFIG + ".bak")
    original_path = os.path.join(GAME_DATA_PATH, TARGET_CONFIG)
    if os.path.exists(original_path):
        shutil.copy2(original_path, backup_path)
        print(f"Đã tạo bản sao lưu tại {backup_path}")

    # 3. Ghi dữ liệu đã sửa đổi (mô phỏng "dán data")
    data_payload = generate_fake_data() + "_inject_aim"
    try:
        with open(original_path, 'w') as f:
            json.dump({"aim_assist": data_payload, "anti_ban": True}, f)
        print("Đã dán data thành công.")
    except Exception as e:
        print(f"Lỗi ghi: {e}")
        sys.exit(1)

def push_via_adb():
    # Phương thức thay thế qua ADB (cần bật gỡ lỗi USB)
    cmd = f"adb push {original_path} {GAME_DATA_PATH}"
    subprocess.run(cmd, shell=True, check=False)

def anti_ban_loop():
    # Khóa file log (mô phỏng cơ chế antiban)
    log_path = "/storage/emulated/0/Android/data/com.dts.freefireth/files/logs/"
    if os.path.exists(log_path):
        os.system(f"chmod 444 {log_path}*")

if __name__ == "__main__":
    print("Đang chạy FF Hack Patcher...")
    create_hack_file()
    anti_ban_loop()
    print("Script đã thực thi. Khởi động lại game để áp dụng.")
