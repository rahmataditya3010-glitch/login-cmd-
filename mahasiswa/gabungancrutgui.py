import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk


class SIAKADApp:

    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD - Sistem Informasi Akademik")
        self.root.geometry("380x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "siakad",
        }

        # Jalankan Tampilan Login Pertama Kali
        self.buat_tampilan_login()

    # ==================== MODUL LOGIN ====================
    def buat_tampilan_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("380x250")
        self.root.title("Login Mahasiswa - SIAKAD")

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(
            expand=True, fill=tk.BOTH, padx=20, pady=20
        )

        lbl_title = tk.Label(
            main_frame,
            text="SIAKAD LOGIN MAHASISWA",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="black",
        )
        lbl_title.pack(pady=(0, 20))

        form_frame = tk.Frame(main_frame, bg="#f0f0f0")
        form_frame.pack()

        tk.Label(
            form_frame,
            text="Username (NIM):",
            font=("Arial", 10),
            bg="#f0f0f0",
            width=12,
            anchor="e",
        ).grid(row=0, column=0, padx=5, pady=6)

        self.entry_nim_login = tk.Entry(
            form_frame, font=("Arial", 10), width=22, relief=tk.SOLID, bd=1
        )
        self.entry_nim_login.grid(row=0, column=1, padx=5, pady=6)
        self.entry_nim_login.focus()

        tk.Label(
            form_frame,
            text="Password (Email):",
            font=("Arial", 10),
            bg="#f0f0f0",
            width=12,
            anchor="e",
        ).grid(row=1, column=0, padx=5, pady=6)

        self.entry_email_login = tk.Entry(
            form_frame,
            font=("Arial", 10),
            width=22,
            show="*",
            relief=tk.SOLID,
            bd=1,
        )
        self.entry_email_login.grid(row=1, column=1, padx=5, pady=6)

        btn_login = tk.Button(
            main_frame,
            text="Login",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.proses_login,
        )
        btn_login.pack(pady=(20, 0))

        self.root.bind("<Return>", lambda event: self.proses_login())

    def proses_login(self):
        nim = self.entry_nim_login.get().strip()
        email = self.entry_email_login.get().strip()

        if not nim or not email:
            messagebox.showwarning(
                "Peringatan", "NIM dan email wajib diisi!"
            )
            return

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT nim, nama_lengkap, email 
                FROM mahasiswa 
                WHERE nim = %s AND email = %s
            """
            cursor.execute(query, (nim, email))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                messagebox.showinfo(
                    "Berhasil",
                    f"Login berhasil!\nSelamat datang, {user['nama_lengkap']}.",
                )
                self.root.unbind("<Return>")
                self.buka_dashboard(user)
            else:
                messagebox.showerror(
                    "Login Gagal", "NIM atau email salah!"
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error", f"Koneksi database bermasalah:\n{err}"
            )

    # ==================== MODUL DASHBOARD & CRUD ====================
    def buka_dashboard(self, user):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("950x600")
        self.root.title("Dashboard & Kelola Data Mahasiswa - SIAKAD")

        # --- Frame Form Input ---
        frame_form = tk.LabelFrame(
            self.root, text=" Form Data Mahasiswa ", padx=10, pady=10
        )
        frame_form.pack(fill="x", padx=15, pady=10)

        labels = [
            "NIM",
            "Nama Lengkap",
            "Jenis Kelamin",
            "Jurusan",
            "Alamat",
            "No Telepon",
            "Email",
        ]
        for i, label_text in enumerate(labels):
            tk.Label(frame_form, text=label_text).grid(
                row=i // 2, column=(i % 2) * 2, sticky="w", padx=5, pady=3
            )

        # Input Fields
        self.entry_nim = tk.Entry(frame_form)
        self.entry_nim.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

        self.entry_nama = tk.Entry(frame_form)
        self.entry_nama.grid(row=0, column=3, padx=5, pady=3, sticky="ew")

        self.combo_jk = ttk.Combobox(
            frame_form, values=["Laki-laki", "Perempuan"], state="readonly"
        )
        self.combo_jk.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

        self.entry_jurusan = tk.Entry(frame_form)
        self.entry_jurusan.grid(row=1, column=3, padx=5, pady=3, sticky="ew")

        self.entry_alamat = tk.Entry(frame_form)
        self.entry_alamat.grid(row=2, column=1, padx=5, pady=3, sticky="ew")

        self.entry_tlp = tk.Entry(frame_form)
        self.entry_tlp.grid(row=2, column=3, padx=5, pady=3, sticky="ew")

        self.entry_email = tk.Entry(frame_form)
        self.entry_email.grid(row=3, column=1, padx=5, pady=3, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        # --- Frame Tombol Aksi ---
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(fill="x", padx=15, pady=5)

        tk.Button(
            frame_btn,
            text="Tambah",
            bg="#4CAF50",
            fg="white",
            command=self.tambah_data,
            width=12,
        ).pack(side="left", padx=5)
        tk.Button(
            frame_btn,
            text="Edit",
            bg="#2196F3",
            fg="white",
            command=self.edit_data,
            width=12,
        ).pack(side="left", padx=5)
        tk.Button(
            frame_btn,
            text="Hapus",
            bg="#f44336",
            fg="white",
            command=self.hapus_data,
            width=12,
        ).pack(side="left", padx=5)
        tk.Button(
            frame_btn,
            text="Clear",
            bg="#9E9E9E",
            fg="white",
            command=self.clear_fields,
            width=12,
        ).pack(side="left", padx=5)
        tk.Button(
            frame_btn,
            text="Logout",
            bg="#FF9800",
            fg="white",
            command=self.buat_tampilan_login,
            width=12,
        ).pack(side="right", padx=5)

        # --- Frame Tabel (Treeview) ---
        frame_table = tk.Frame(self.root)
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = (
            "nim",
            "nama_lengkap",
            "jenis_kelamin",
            "jurusan",
            "alamat",
            "no_telepon",
            "email",
        )
        self.tree = ttk.Treeview(
            frame_table, columns=columns, show="headings"
        )

        self.tree.heading("nim", text="NIM")
        self.tree.heading("nama_lengkap", text="Nama Lengkap")
        self.tree.heading("jenis_kelamin", text="Jenis Kelamin")
        self.tree.heading("jurusan", text="Jurusan")
        self.tree.heading("alamat", text="Alamat")
        self.tree.heading("no_telepon", text="No Telepon")
        self.tree.heading("email", text="Email")

        self.tree.column("nim", width=80)
        self.tree.column("nama_lengkap", width=150)
        self.tree.column("jenis_kelamin", width=100)
        self.tree.column("jurusan", width=120)
        self.tree.column("alamat", width=150)
        self.tree.column("no_telepon", width=100)
        self.tree.column("email", width=150)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar = ttk.Scrollbar(
            frame_table, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

    # --- Fungsi-Fungsi Operasi Database (CRUD) ---
    def connect_db(self):
        return mysql.connector.connect(**self.db_config)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM mahasiswa")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Gagal mengambil data: {e}"
            )

    def tambah_data(self):
        nim = self.entry_nim.get()
        nama = self.entry_nama.get()
        jk = self.combo_jk.get()
        jurusan = self.entry_jurusan.get()
        alamat = self.entry_alamat.get()
        tlp = self.entry_tlp.get()
        email = self.entry_email.get()

        if not nim or not nama:
            messagebox.showwarning(
                "Warning", "NIM dan Nama Lengkap wajib diisi!"
            )
            return

        try:
            db = self.connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO mahasiswa (nim, nama_lengkap, jenis_kelamin, jurusan, alamat, no_telepon, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nim, nama, jk, jurusan, alamat, tlp, email)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Pilih data di tabel yang ingin diubah!"
            )
            return

        nim = self.entry_nim.get()
        nama = self.entry_nama.get()
        jk = self.combo_jk.get()
        jurusan = self.entry_jurusan.get()
        alamat = self.entry_alamat.get()
        tlp = self.entry_tlp.get()
        email = self.entry_email.get()

        try:
            db = self.connect_db()
            cursor = db.cursor()
            sql = """UPDATE mahasiswa SET nama_lengkap=%s, jenis_kelamin=%s, jurusan=%s, 
                     alamat=%s, no_telepon=%s, email=%s WHERE nim=%s"""
            val = (nama, jk, jurusan, alamat, tlp, email, nim)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Pilih data di tabel yang ingin dihapus!"
            )
            return

        nim = self.entry_nim.get()
        confirm = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus mahasiswa NIM {nim}?"
        )
        if confirm:
            try:
                db = self.connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_nim.insert(0, values[0])
            self.entry_nama.insert(0, values[1])
            self.combo_jk.set(values[2])
            self.entry_jurusan.insert(0, values[3])
            self.entry_alamat.insert(0, values[4])
            self.entry_tlp.insert(0, values[5])
            self.entry_email.insert(0, values[6])

    def clear_fields(self):
        self.entry_nim.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.combo_jk.set("")
        self.entry_jurusan.delete(0, tk.END)
        self.entry_alamat.delete(0, tk.END)
        self.entry_tlp.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SIAKADApp(root)
    root.mainloop()