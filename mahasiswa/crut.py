# Mengimpor modul os untuk interaksi sistem operasi jika diperlukan
import os
# Mengimpor modul tkinter dasar untuk pembuatan komponen GUI
import tkinter as tk
# Mengimpor modul ttk untuk widget bertema (seperti Combobox & Treeview) dan messagebox untuk dialog pop-up
from tkinter import ttk, messagebox
# Mengimpor mysql.connector untuk mengendalikan koneksi dan operasi database MySQL
import mysql.connector

# --- KONEKSI DATABASE ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",       # Alamat host server MySQL
        user="root",            # Username untuk login ke MySQL
        password="",            # Password pengguna (kosongkan jika tidak ada password)
        database="siakad"       # Nama database yang dituju
    )

# --- FUNGSI CRUD MAHASISWA ---

# Fungsi untuk memuat dan menampilkan seluruh data dari tabel mahasiswa ke Treeview
def load_data():
    for row in tree.get_children():
        tree.delete(row)
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM mahasiswa")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        db.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

# Fungsi untuk menambahkan record mahasiswa baru ke database
def tambah_data():
    nim = entry_nim.get()
    nama = entry_nama.get()
    tgl_lahir = entry_tgl_lahir.get()
    jk = combo_jk.get()
    jurusan = entry_jurusan.get()
    alamat = entry_alamat.get()
    tlp = entry_tlp.get()
    email = entry_email.get()

    if not nim or not nama:
        messagebox.showwarning("Warning", "NIM dan Nama Lengkap wajib diisi!")
        return

    try:
        db = connect_db()
        cursor = db.cursor()
        # Query INSERT dengan tambahan kolom tanggal_lahir
        sql = """INSERT INTO mahasiswa 
                 (nim, nama_lengkap, tanggal_lahir, jenis_kelamin, jurusan, alamat, no_telepon, email) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (nim, nama, tgl_lahir, jk, jurusan, alamat, tlp, email)
        cursor.execute(sql, val)
        db.commit()
        db.close()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menambah data: {e}")

# Fungsi untuk memperbarui (update) data mahasiswa yang dipilih
def edit_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
        return

    nim = entry_nim.get()
    nama = entry_nama.get()
    tgl_lahir = entry_tgl_lahir.get()
    jk = combo_jk.get()
    jurusan = entry_jurusan.get()
    alamat = entry_alamat.get()
    tlp = entry_tlp.get()
    email = entry_email.get()

    try:
        db = connect_db()
        cursor = db.cursor()
        # Query UPDATE dengan tambahan tanggal_lahir
        sql = """UPDATE mahasiswa SET nama_lengkap=%s, tanggal_lahir=%s, jenis_kelamin=%s, 
                 jurusan=%s, alamat=%s, no_telepon=%s, email=%s WHERE nim=%s"""
        val = (nama, tgl_lahir, jk, jurusan, alamat, tlp, email, nim)
        cursor.execute(sql, val)
        db.commit()
        db.close()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

# Fungsi untuk menghapus record mahasiswa dari database
def hapus_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
        return

    nim = entry_nim.get()
    confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus mahasiswa NIM {nim}?")
    if confirm:
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

# Fungsi callback event saat baris pada Treeview diklik/dipilih
def select_item(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        clear_fields()
        entry_nim.insert(0, values[0])
        entry_nama.insert(0, values[1])
        entry_tgl_lahir.insert(0, values[2])
        combo_jk.set(values[3])
        entry_jurusan.insert(0, values[4])
        entry_alamat.insert(0, values[5])
        entry_tlp.insert(0, values[6])
        entry_email.insert(0, values[7])

# Fungsi helper untuk mengosongkan seluruh kotak input form
def clear_fields():
    entry_nim.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    entry_tgl_lahir.delete(0, tk.END)
    combo_jk.set("")
    entry_jurusan.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_tlp.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# --- GUI MAIN WINDOW ---
root = tk.Tk()
root.title("Aplikasi Data Mahasiswa - SIAKAD")
root.geometry("950x580")

# Frame Form Input
frame_form = tk.LabelFrame(root, text=" Form Data Mahasiswa ", padx=10, pady=10)
frame_form.pack(fill="x", padx=15, pady=10)

# Label untuk form (Total 8 field)
labels = [
    "NIM", "Nama Lengkap", 
    "Tanggal Lahir", "Jenis Kelamin", 
    "Jurusan", "Alamat", 
    "No Telepon", "Email"
]
for i, label_text in enumerate(labels):
    tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=3)

# Input Fields
entry_nim = tk.Entry(frame_form)
entry_nim.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

entry_nama = tk.Entry(frame_form)
entry_nama.grid(row=0, column=3, padx=5, pady=3, sticky="ew")

entry_tgl_lahir = tk.Entry(frame_form)  # Format: YYYY-MM-DD
entry_tgl_lahir.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

combo_jk = ttk.Combobox(frame_form, values=["Laki-laki", "Perempuan"], state="readonly")
combo_jk.grid(row=1, column=3, padx=5, pady=3, sticky="ew")

entry_jurusan = tk.Entry(frame_form)
entry_jurusan.grid(row=2, column=1, padx=5, pady=3, sticky="ew")

entry_alamat = tk.Entry(frame_form)
entry_alamat.grid(row=2, column=3, padx=5, pady=3, sticky="ew")

entry_tlp = tk.Entry(frame_form)
entry_tlp.grid(row=3, column=1, padx=5, pady=3, sticky="ew")

entry_email = tk.Entry(frame_form)
entry_email.grid(row=3, column=3, padx=5, pady=3, sticky="ew")

frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)

# Frame Tombol Aksi
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=15, pady=5)

tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

# Frame Tabel (Treeview)
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("nim", "nama_lengkap", "tanggal_lahir", "jenis_kelamin", "jurusan", "alamat", "no_telepon", "email")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

tree.heading("nim", text="NIM")
tree.heading("nama_lengkap", text="Nama Lengkap")
tree.heading("tanggal_lahir", text="Tanggal Lahir")
tree.heading("jenis_kelamin", text="Jenis Kelamin")
tree.heading("jurusan", text="Jurusan")
tree.heading("alamat", text="Alamat")
tree.heading("no_telepon", text="No Telepon")
tree.heading("email", text="Email")

tree.column("nim", width=70)
tree.column("nama_lengkap", width=140)
tree.column("tanggal_lahir", width=90)
tree.column("jenis_kelamin", width=90)
tree.column("jurusan", width=110)
tree.column("alamat", width=130)
tree.column("no_telepon", width=90)
tree.column("email", width=140)

tree.bind("<<TreeviewSelect>>", select_item)

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Muat data awal
load_data()

# Jalankan aplikasi
root.mainloop()