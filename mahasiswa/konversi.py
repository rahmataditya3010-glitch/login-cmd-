# Mengimpor modul tkinter untuk membuat antarmuka grafis (GUI)
import tkinter as tk
# Mengimpor modul os untuk mengelola alur path/direktori file sistem
import os

# Memunculkan jendela utama aplikasi Tkinter
root = tk.Tk()
# Mengatur teks pada judul jendela aplikasi
root.title("Database Mahasiswa")
# Menentukan ukuran resolusi jendela aplikasi (lebar 300px, tinggi 180px)
root.geometry("300x260")

# Mengambil lokasi path folder dari file skrip Python ini berada
base_dir = os.path.dirname(__file__)
# Menggabungkan direktori utama dengan nama file ikon 'calc.ico'
icon_path = os.path.join(base_dir, "calc.ico")

# Mengecek apakah file ikon 'calc.ico' tersedia sebelum dimuat ke title bar
if os.path.exists(icon_path):
    # Mengganti ikon default Tkinter pada title bar menggunakan file .ico
    root.iconbitmap(icon_path)

# --- FUNGSI LOGIKA DATABASE MAHASISWA ---
def simpan():
    try:
        # Mengambil nilai masukan dari Entry NIM dan Nama
        nim = entry_nim.get()
        nama = entry_nama.get()
        # Mengecek apakah kedua field sudah diisi
        if nim == "" or nama == "":
            # Menampilkan pesan error jika ada field yang kosong
            label_hasil.config(text="NIM dan Nama wajib diisi!", fg="red")
            return
        # Menyimpan data mahasiswa ke dalam file teks 'data_mahasiswa.txt'
        with open(os.path.join(base_dir, "data_mahasiswa.txt"), "a") as f:
            f.write(f"{nim} - {nama}\n")
        # Memperbarui teks hasil penyimpanan pada label dengan warna hijau
        label_hasil.config(text=f"Tersimpan: {nim} - {nama}", fg="green")
    except Exception:
        # Menampilkan pesan error jika terjadi kesalahan tak terduga
        label_hasil.config(text="Gagal menyimpan data!", fg="red")

# Membuat dan menampilkan label petunjuk "NIM:"
tk.Label(root, text="NIM:", font=('Arial', 11)).pack(pady=(15, 5))

# Membuat kotak input teks untuk NIM dengan teks berada di tengah (justify="center")
entry_nim = tk.Entry(root, font=('Arial', 12), justify="center")
# Menampilkan kotak input NIM di jendela
entry_nim.pack(pady=5)

# Membuat dan menampilkan label petunjuk "Nama:"
tk.Label(root, text="Nama:", font=('Arial', 11)).pack(pady=(5, 5))

# Membuat kotak input teks untuk Nama dengan teks berada di tengah (justify="center")
entry_nama = tk.Entry(root, font=('Arial', 12), justify="center")
# Menampilkan kotak input Nama di jendela
entry_nama.pack(pady=5)

# Membuat tombol untuk mengeksekusi fungsi simpan() saat diklik
btn_simpan = tk.Button(root, text="Simpan Data Mahasiswa", command=simpan, font=('Arial', 10, 'bold'))
# Menampilkan tombol simpan
btn_simpan.pack(pady=10)

# Membuat label untuk menampilkan teks status atau hasil penyimpanan
label_hasil = tk.Label(root, text="Status: -", font=('Arial', 11, 'bold'))
# Menampilkan label hasil
label_hasil.pack(pady=5)

# Memulai event loop utama agar GUI tetap berjalan dan dapat berinteraksi
root.mainloop()