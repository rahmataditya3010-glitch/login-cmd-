import mysql.connector
import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Mahasiswa - SIAKAD")
        self.root.geometry("380x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "siakad"
        }

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(
            expand=True,
            fill=tk.BOTH,
            padx=20,
            pady=20
        )

        lbl_title = tk.Label(
            main_frame,
            text="SIAKAD LOGIN MAHASISWA",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="black"
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
            anchor="e"
        ).grid(row=0, column=0, padx=5, pady=6)

        self.entry_nim = tk.Entry(
            form_frame,
            font=("Arial", 10),
            width=22,
            relief=tk.SOLID,
            bd=1
        )
        self.entry_nim.grid(row=0, column=1, padx=5, pady=6)
        self.entry_nim.focus()

        tk.Label(
            form_frame,
            text="Password (Email):",
            font=("Arial", 10),
            bg="#f0f0f0",
            width=12,
            anchor="e"
        ).grid(row=1, column=0, padx=5, pady=6)

        self.entry_email = tk.Entry(
            form_frame,
            font=("Arial", 10),
            width=22,
            show="*",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_email.grid(row=1, column=1, padx=5, pady=6)

        btn_login = tk.Button(
            main_frame,
            text="Login",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.proses_login
        )
        btn_login.pack(pady=(20, 0))

        self.root.bind(
            "<Return>",
            lambda event: self.proses_login()
        )

    def proses_login(self):
        nim = self.entry_nim.get().strip()
        email = self.entry_email.get().strip()

        if not nim or not email:
            messagebox.showwarning(
                "Peringatan",
                "NIM dan email wajib diisi!"
            )
            return

        conn = None
        cursor = None

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

            if user:
                messagebox.showinfo(
                    "Berhasil",
                    f"Login berhasil!\n"
                    f"Selamat datang, {user['nama_lengkap']}."
                )
                self.buka_dashboard(user)
            else:
                messagebox.showerror(
                    "Login Gagal",
                    "NIM atau email salah!"
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Koneksi database bermasalah:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    def buka_dashboard(self, user):
        self.root.destroy()

        dashboard = tk.Tk()
        dashboard.title("Dashboard Mahasiswa - SIAKAD")
        dashboard.geometry("450x300")
        dashboard.configure(bg="#f0f0f0")

        tk.Label(
            dashboard,
            text="DASHBOARD MAHASISWA",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2E7D32"
        ).pack(pady=25)

        tk.Label(
            dashboard,
            text=f"Selamat datang, {user['nama_lengkap']}!",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=10)

        tk.Label(
            dashboard,
            text=f"NIM: {user['nim']}",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(pady=5)

        tk.Label(
            dashboard,
            text=f"Email: {user['email']}",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(pady=5)

        tk.Button(
            dashboard,
            text="Keluar",
            font=("Arial", 10, "bold"),
            bg="#e53935",
            fg="white",
            width=12,
            command=dashboard.destroy
        ).pack(pady=25)

        dashboard.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()