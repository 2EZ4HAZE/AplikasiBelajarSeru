# Nama file: appbs.py (Final V2 with Placeholder)
import ttkbootstrap as ttk
import os
from PIL import Image, ImageTk
from abc import ABC, abstractmethod
import random
import tkinter as tk
import tkinter.font as tkfont

# ==============================================================================
# == DATA SOAL (Tidak ada perubahan)
# ==============================================================================
SOAL_DATA = {
    "Bahasa Indonesia": {
        "🐝 Tebak Huruf Awal": {
            "Tebak huruf awal dari gambar APEL ini:": ("assets/apel.png", ("A", "B", "C", "A")),
            "Tebak huruf awal dari gambar BOLA ini:": ("assets/bola.png", ("D", "B", "C", "B")),
            "Tebak huruf awal dari gambar CICAK ini:": ("assets/cicak.png", ("C", "A", "D", "C")),
            "Tebak huruf awal dari gambar GAJAH ini:": ("assets/gajah.png", ("G", "J", "H", "G")),
            "Tebak huruf awal dari gambar IKAN ini:": ("assets/ikan.png", ("E", "I", "O", "I")),
        }
    },
    "Matematika": {
        "➕ Penjumlahan": {
            "2 + 3 = ?": ("4", "5", "6", "5"),
            "1 + 4 = ?": ("3", "5", "6", "5"),
            "3 + 3 = ?": ("5", "6", "7", "6"),
            "5 + 2 = ?": ("6", "7", "8", "7"),
            "4 + 0 = ?": ("0", "3", "4", "4")
        },
        "➖ Pengurangan": {
            "3 - 1 = ?": ("1", "2", "3", "2"),
            "5 - 2 = ?": ("2", "3", "4", "3"),
            "7 - 3 = ?": ("3", "4", "5", "4"),
            "6 - 4 = ?": ("1", "2", "3", "2"),
            "8 - 5 = ?": ("3", "4", "2", "3"),
        }
    },
    "IPA": {
        "🌳 Mengenal Alam & Tubuh": {
            "Bagian tubuh yang digunakan untuk melihat adalah...": ("Telinga", "Hidung", "Mata", "Mata"),
            "Kucing adalah contoh benda...": ("Hidup", "Tak Hidup", "Mainan", "Hidup"),
            "Suara 'Mooo' adalah suara hewan...": ("Ayam", "Sapi", "Kambing", "Sapi"),
            "Tumbuhan membutuhkan ... untuk membuat makanan.": ("Air", "Batu", "Plastik", "Air"),
            "Yang termasuk planet adalah...": ("Bulan", "Bumi", "Bintang", "Bumi"),
        }
    }
}

# ==============================================================================
# == KELAS-KELAS HALAMAN (Tidak ada perubahan)
# ==============================================================================
class Page(ABC):
    def __init__(self, parent_frame, app_controller):
        self.parent_frame = parent_frame
        self.app = app_controller
        self.frame = ttk.Frame(parent_frame, padding=10)

    @abstractmethod
    def _setup_widgets(self): pass

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self._setup_widgets()

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

class WelcomePage(Page):
    def _setup_widgets(self):
        ttk.Label(self.frame, text="Selamat Datang!", font=self.app.title_font, bootstyle="primary").pack(pady=40)
        ttk.Label(self.frame, text="Pilih pelajaran dari menu di sebelah kiri untuk memulai.").pack(pady=10)

class SubmenuPage(Page):
    def __init__(self, parent_frame, app_controller, subject):
        super().__init__(parent_frame, app_controller)
        self.subject = subject

    def _setup_widgets(self):
        ttk.Label(self.frame, text=f"Pilih Topik {self.subject}", font=self.app.title_font, bootstyle="primary").pack(pady=(20, 20))
        button_container = ttk.Frame(self.frame)
        button_container.pack()
        topics = self.app.SOAL_DATA.get(self.subject, {})

        if self.subject == "Matematika":
            ttk.Button(button_container, text="🔢 Mengenal Angka", width=20, bootstyle="secondary", command=lambda: self.app.show_page(MateriAngkaPage, self.subject)).grid(row=0, column=0, padx=10, pady=10, ipady=10)
            ttk.Button(button_container, text="🎨 Mengenal Bentuk", width=20, bootstyle="secondary", command=lambda: self.app.show_page(MateriBentukPage, self.subject)).grid(row=0, column=1, padx=10, pady=10, ipady=10)

        row_offset = 1 if self.subject == "Matematika" else 0
        quiz_styles = ["primary", "info", "success", "warning", "danger"]
        for i, topic_name in enumerate(topics.keys()):
            style = quiz_styles[i % len(quiz_styles)]
            ttk.Button(button_container, text=topic_name, width=20, bootstyle=style, command=lambda t=topic_name: self.app.start_quiz(self.subject, t)).grid(row=row_offset + (i // 2), column=i % 2, padx=10, pady=10, ipady=10)

        ttk.Button(self.frame, text="Kembali ke Menu Utama", bootstyle="secondary-link", command=lambda: self.app.show_page(WelcomePage)).pack(pady=30)

class MateriAngkaPage(Page):
    def __init__(self, parent_frame, app_controller, subject):
        super().__init__(parent_frame, app_controller)
        self.subject = subject

    def _setup_widgets(self):
        top_bar = ttk.Frame(self.frame)
        top_bar.pack(fill="x", padx=10, pady=(0,10))
        ttk.Button(top_bar, text="⬅️ Kembali", bootstyle="secondary-link", command=lambda: self.app.show_submenu(self.subject)).pack(side="left")
        ttk.Label(self.frame, text="Mengenal Angka (1-10)", font=self.app.title_font, bootstyle="primary").pack(pady=10)
        self._populate_angka_cards()

    def _populate_angka_cards(self):
        angka_data = [("1", "Satu Apel", "assets/apel.png"), ("2", "Dua Pisang", "assets/pisang.png"), ("3", "Tiga Mobil", "assets/mobil.png"), ("4", "Empat Bintang", "assets/bintang.png"), ("5", "Lima Balon", "assets/balon.png"), ("6", "Enam Kue", "assets/kue.png"), ("7", "Tujuh Ikan", "assets/ikan.png"), ("8", "Delapan Boneka", "assets/boneka.png"), ("9", "Sembilan Bola", "assets/bola.png"), ("10", "Sepuluh Pensil", "assets/pensil.png")]
        container = ttk.Frame(self.frame)
        container.pack(expand=True, pady=5)
        for i, (num, text, img_path) in enumerate(angka_data):
            card = ttk.Frame(container, bootstyle="light", padding=5)
            card_img = self.app.load_image(img_path, (90, 90))
            if card_img:
                img_label = ttk.Label(card, image=card_img)
                img_label.image = card_img
                img_label.pack(pady=(5,0), padx=10)
            ttk.Label(card, text=num, font=self.app.number_font).pack(pady=2)
            ttk.Label(card, text=text).pack(pady=(0,5))
            card.grid(row=i // 5, column=i % 5, padx=8, pady=8)
            container.grid_columnconfigure(i % 5, weight=1)

class MateriBentukPage(Page):
    def __init__(self, parent_frame, app_controller, subject):
        super().__init__(parent_frame, app_controller)
        self.subject = subject

    def _setup_widgets(self):
        top_bar = ttk.Frame(self.frame)
        top_bar.pack(fill="x", padx=10, pady=(0,10))
        ttk.Button(top_bar, text="⬅️ Kembali", bootstyle="secondary-link", command=lambda: self.app.show_submenu(self.subject)).pack(side="left")
        ttk.Label(self.frame, text="Mengenal Bentuk Dasar", font=self.app.title_font, bootstyle="primary").pack(pady=10)
        self._populate_bentuk_cards()

    def _populate_bentuk_cards(self):
        bentuk_data = [("Lingkaran", "#9575CD"), ("Persegi", "#7E57C2"), ("Segitiga", "#673AB7"), ("Bintang", "#FFCA28"), ("Hati", "#EF5350"), ("Oval", "#42A5F5"), ("Trapesium", "#26A69A"), ("Jajargenjang", "#FF7043"), ("Belah Ketupat", "#8D6E63"), ("Segi Lima", "#78909C"), ("Segi Enam", "#5C6BC0"), ("Layang-layang", "#66BB6A")]
        container = ttk.Frame(self.frame)
        container.pack(pady=20, expand=True)
        for i, (nama, warna) in enumerate(bentuk_data):
            card = ttk.Frame(container, bootstyle="light", padding=5)
            canvas = tk.Canvas(card, width=120, height=100, bg=self.app.root.cget('bg'), highlightthickness=0)
            if nama == "Lingkaran": canvas.create_oval(10, 10, 90, 90, fill=warna, outline=warna)
            elif nama == "Persegi": canvas.create_rectangle(10, 10, 90, 90, fill=warna, outline=warna)
            elif nama == "Segitiga": canvas.create_polygon(50, 10, 90, 90, 10, 90, fill=warna, outline=warna)
            elif nama == "Bintang": canvas.create_polygon([60, 10, 75, 45, 110, 45, 85, 65, 95, 95, 60, 75, 25, 95, 35, 65, 10, 45, 45, 45], fill=warna, outline=warna)
            elif nama == "Hati": canvas.create_polygon([60, 35, 75, 20, 90, 35, 60, 75, 30, 35, 45, 20], smooth=True, fill=warna, outline=warna)
            elif nama == "Oval": canvas.create_oval(10, 20, 110, 80, fill=warna, outline=warna)
            elif nama == "Trapesium": canvas.create_polygon([20, 20, 100, 20, 110, 80, 10, 80], fill=warna, outline=warna)
            elif nama == "Jajargenjang": canvas.create_polygon([10, 20, 80, 20, 110, 80, 40, 80], fill=warna, outline=warna)
            elif nama == "Belah Ketupat": canvas.create_polygon([60, 10, 110, 50, 60, 90, 10, 50], fill=warna, outline=warna)
            elif nama == "Segi Lima": canvas.create_polygon([60, 10, 110, 40, 90, 90, 30, 90, 10, 40], fill=warna, outline=warna)
            elif nama == "Segi Enam": canvas.create_polygon([30, 15, 90, 15, 110, 50, 90, 85, 30, 85, 10, 50], fill=warna, outline=warna)
            elif nama == "Layang-layang": canvas.create_polygon([60, 10, 100, 40, 60, 90, 20, 40], fill=warna, outline=warna)
            canvas.pack(pady=5)
            ttk.Label(card, text=nama).pack(pady=(0,10))
            card.grid(row=i // 6, column=i % 6, padx=10, pady=10)
            container.grid_columnconfigure(i % 6, weight=1)

class QuizPage(Page):
    def __init__(self, parent_frame, app_controller, subject, topic):
        super().__init__(parent_frame, app_controller)
        self.subject = subject
        self.topic = topic
        self._questions = list(self.app.SOAL_DATA[subject][topic].items())[:5]
        random.shuffle(self._questions)
        self._current_question_index = 0
        self._score = 0
        self._correct_answer = ""
        self._radio_buttons = []
        self._feedback_label = None
        self._score_label = None
        self._submit_button = None

    def _setup_widgets(self):
        self.clear()
        self.selected_answer = tk.StringVar(value="___UNSELECTED___")
        top_bar = ttk.Frame(self.frame)
        top_bar.pack(fill="x", padx=10, pady=(0,10))
        ttk.Button(top_bar, text="⬅️ Kembali", bootstyle="secondary-link", command=lambda: self.app.show_submenu(self.subject)).pack(side="left")

        if self._current_question_index < len(self._questions):
            ttk.Label(self.frame, text=self.topic, font=self.app.title_font, bootstyle="primary").pack(pady=5)
            self._score_label = ttk.Label(self.frame, text=f"Skor: {self._score}", font=self.app.subtitle_font)
            self._score_label.pack(pady=(0, 10))
            
            question_container = ttk.Frame(self.frame, bootstyle="light", padding=20)
            question_container.pack(pady=5, padx=10, fill="x")

            soal_text, question_data = self._questions[self._current_question_index]
            image_path, options = (question_data[0], question_data[1]) if isinstance(question_data, tuple) and len(question_data) == 2 and isinstance(question_data[0], str) else (None, question_data)

            if image_path:
                quiz_img = self.app.load_image(image_path, (120, 120))
                if quiz_img:
                    img_label = ttk.Label(question_container, image=quiz_img)
                    img_label.image = quiz_img
                    img_label.pack(pady=(0, 15))
            
            ttk.Label(question_container, text=soal_text, wraplength=700).pack()
            
            self._correct_answer = options[3]
            pilihan_jawaban = list(options[:3])
            random.shuffle(pilihan_jawaban)
            
            options_frame = ttk.Frame(self.frame)
            options_frame.pack(pady=15)
            
            self._radio_buttons.clear()
            for pilihan in pilihan_jawaban:
                rb = ttk.Radiobutton(options_frame, text=pilihan, value=pilihan, variable=self.selected_answer, bootstyle="toolbutton")
                self._radio_buttons.append(rb)
                rb.pack(side="left", padx=5, ipady=8, ipadx=12)
            
            self._feedback_label = ttk.Label(self.frame, text="", font=self.app.subtitle_font)
            self._feedback_label.pack(pady=5)
            
            self._submit_button = ttk.Button(self.frame, text="Jawab!", bootstyle="warning", command=self._check_answer)
            self._submit_button.pack(pady=5, ipady=8, ipadx=12)
        else:
            self._show_final_score()

    def _check_answer(self):
        user_answer = self.selected_answer.get()
        if user_answer == "___UNSELECTED___":
            self._feedback_label.config(text="Pilih jawaban dulu ya!", bootstyle="warning")
            return
        
        if self._submit_button: self._submit_button.pack_forget()
        is_correct = (user_answer == self._correct_answer)
        if is_correct:
            self._score += 1
            self._feedback_label.config(text="HEBAT! 🎉", bootstyle="success")
        else:
            self._feedback_label.config(text="Ayo Coba Lagi! 💪", bootstyle="danger")
        self._score_label.config(text=f"Skor: {self._score}")
        
        for rb in self._radio_buttons:
            rb.config(state="disabled")
            if rb['value'] == self._correct_answer: rb.config(bootstyle="success-toolbutton")
            elif rb['value'] == user_answer: rb.config(bootstyle="danger-toolbutton")
        
        self.app.root.after(1500, self._next_question)

    def _next_question(self):
        self._current_question_index += 1
        self._setup_widgets()

    def _show_final_score(self):
        self.clear()
        score = self._score
        total_questions = len(self._questions)
        
        if score == total_questions: feedback_style, feedback_title, feedback_message = "success", "Luar Biasa! ⭐⭐⭐⭐⭐", "Kamu menjawab semua soal dengan benar. Hebat!"
        elif score >= total_questions * 0.8: feedback_style, feedback_title, feedback_message = "info", "Bagus Sekali! ⭐⭐⭐⭐", "Hampir sempurna! Terus tingkatkan, ya."
        elif score >= total_questions * 0.6: feedback_style, feedback_title, feedback_message = "primary", "Cukup Bagus! ⭐⭐⭐", "Kamu sudah paham dasarnya. Terus berlatih!"
        else: feedback_style, feedback_title, feedback_message = "danger", "Ayo Coba Lagi! ⭐", "Jangan menyerah, belajar lagi pasti bisa!"

        ttk.Label(self.frame, text=feedback_title, font=self.app.title_font, bootstyle=feedback_style).pack(pady=(40, 10))
        final_text = f"Skor Akhir Kamu:\n{score} dari {total_questions} soal"
        ttk.Label(self.frame, text=final_text, font=self.app.subtitle_font, justify="center").pack(pady=20)
        ttk.Label(self.frame, text=feedback_message).pack(pady=10)
        ttk.Button(self.frame, text="Kembali ke Topik", bootstyle="secondary", command=lambda: self.app.show_submenu(self.subject)).pack(pady=20)

# ==============================================================================
# == KELAS APLIKASI UTAMA
# ==============================================================================
class AplikasiBelajarSeru:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Belajar Seru")
        self.root.geometry("950x750")

        style = ttk.Style()
        self.base_font_family = 'Comic Sans MS' if 'Comic Sans MS' in tkfont.families() else 'Arial'
        
        style.configure('.', font=(self.base_font_family, 12))
        style.configure('TButton', font=(self.base_font_family, 12))
        style.configure('TLabel', font=(self.base_font_family, 14))
        style.configure('AvatarOutline.TButton', font=(self.base_font_family, 24))
        style.configure('AvatarSelected.TButton', font=(self.base_font_family, 24))

        self.title_font = (self.base_font_family, 26, 'bold')
        self.subtitle_font = (self.base_font_family, 16, 'bold')
        self.number_font = (self.base_font_family, 32, 'bold')

        # Initialize instance variables
        self.player_name = tk.StringVar(value="")
        self.player_avatar = tk.StringVar(value="👧")
        self.image_cache = {}
        self.SOAL_DATA = SOAL_DATA
        self._current_page = None
        self.avatar_buttons = {}
        self.selected_avatar_button = None

        # --- PLACEHOLDER SETUP ---
        self.placeholder_text = "Masukkan namamu..."
        self.placeholder_color = 'grey' # Changed to grey for better visual cue
        
        self.create_login_screen()
    
    # --- BARU: Fungsi untuk menangani event focus pada entry nama ---
    def _on_entry_focus_in(self, event):
        """Function to remove placeholder text on focus."""
        if self.name_entry.get() == self.placeholder_text:
            self.name_entry.delete(0, "end")
            self.name_entry.config(foreground=self.default_fg_color)

    # --- BARU: Fungsi untuk menangani event focus-out pada entry nama ---
    def _on_entry_focus_out(self, event):
        """Function to add placeholder text if entry is empty."""
        # Jika entry kosong, tampilkan lagi placeholder
        if not self.name_entry.get():
            self.name_entry.insert(0, self.placeholder_text)
            self.name_entry.config(foreground=self.placeholder_color)

    def _on_avatar_select(self, avatar_value, button_widget):
        self.player_avatar.set(avatar_value)
        if self.selected_avatar_button and self.selected_avatar_button.winfo_exists():
            # Kembalikan tombol lama ke style outline
            self.selected_avatar_button.config(style="AvatarOutline.TButton")
        # Atur tombol baru ke style solid
        button_widget.config(style="AvatarSelected.TButton")
        self.selected_avatar_button = button_widget

    def create_login_screen(self):
        self.selected_avatar_button = None
        container = ttk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor="center")
        self.login_frame = ttk.Frame(container, padding=30, bootstyle="light")
        self.login_frame.pack()
        
        login_mascot_img = self.load_image("assets/kiko_maskot.png", (100, 100))
        if login_mascot_img:
            mascot_label = ttk.Label(self.login_frame, image=login_mascot_img)
            mascot_label.image = login_mascot_img
            mascot_label.pack(pady=(0, 15))
            
        ttk.Label(self.login_frame, text="Hai! Selamat Datang!", font=self.title_font, bootstyle="primary").pack()
        ttk.Label(self.login_frame, text="Siapa nama panggilanmu?").pack(pady=10)
        
        # --- PERUBAHAN LOGIKA PLACEHOLDER ---
        # 1. Simpan widget entry ke self.name_entry agar bisa diakses fungsi lain
        self.name_entry = ttk.Entry(self.login_frame, textvariable=self.player_name, width=25, justify="center")
        self.name_entry.pack(pady=5, ipady=5)
        
        # 2. Simpan warna teks default sebelum diubah
        self.default_fg_color = self.name_entry.cget("foreground")
        
        # 3. Panggil fungsi focus-out sekali di awal untuk mengatur state placeholder
        self._on_entry_focus_out(None)
        
        # 4. Ikat (bind) event FocusIn dan FocusOut ke fungsi yang sesuai
        self.name_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.name_entry.bind("<FocusOut>", self._on_entry_focus_out)
        # --- AKHIR PERUBAHAN ---

        ttk.Label(self.login_frame, text="Pilih avatarmu!").pack(pady=(20, 10))
        avatar_frame = ttk.Frame(self.login_frame, bootstyle="light")
        avatar_frame.pack(pady=10)
        
        avatars = ["👧", "👦", "👶", "👩", "👨"]
        self.avatar_buttons.clear()

        for avatar in avatars:
            btn = ttk.Button(avatar_frame, text=avatar, style='AvatarOutline.TButton', bootstyle="dark")
            btn.config(command=lambda av=avatar, b=btn: self._on_avatar_select(av, b))
            btn.pack(side="left", padx=5)
            self.avatar_buttons[avatar] = btn
        
        default_avatar = self.player_avatar.get()
        if default_avatar in self.avatar_buttons:
            self.avatar_buttons[default_avatar].config(style="AvatarSelected.TButton", bootstyle="success")
            self.selected_avatar_button = self.avatar_buttons[default_avatar]
        
        start_button = ttk.Button(self.login_frame, text="Mulai Petualangan!", bootstyle="success", command=self.login_and_start_app)
        start_button.pack(pady=30, ipady=10, ipadx=10)

    def load_image(self, path, size):
        try: 
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError: 
            script_dir = os.getcwd()
        abs_path = os.path.join(script_dir, path)
        cache_key = (abs_path, size)
        if cache_key in self.image_cache: 
            return self.image_cache[cache_key]
        if not os.path.exists(abs_path):
            print(f"Peringatan: File gambar tidak ditemukan di '{abs_path}'")
            return None
        try:
            image = Image.open(abs_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            self.image_cache[cache_key] = photo_image
            return photo_image
        except Exception as e:
            print(f"Error memuat gambar {abs_path}: {e}")
            return None

    def login_and_start_app(self):
        # Tambahan: Jika nama masih placeholder, ganti dengan nama default
        if self.player_name.get() == self.placeholder_text:
            self.player_name.set("Jagoan Cilik")

        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_main_layout()

    def logout(self):
        # Reset nama pemain saat logout
        self.player_name.set("")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_login_screen()

    def create_main_layout(self):
        self.header_frame = ttk.Frame(self.root, bootstyle="primary", padding=(20, 15))
        self.header_frame.pack(side="top", fill="x")
        
        self.sidebar_frame = ttk.Frame(self.root, bootstyle="light", padding=10, width=220)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        
        self.main_content_frame = ttk.Frame(self.root)
        self.main_content_frame.pack(side="right", fill="both", expand=True)
        
        self.create_header_widgets()
        self.create_sidebar_widgets()
        self.show_page(WelcomePage)

    def create_header_widgets(self):
        ttk.Label(self.header_frame, text="Aplikasi Belajar Seru 📚", font=self.subtitle_font, bootstyle="inverse-primary").pack(side="left")
        ttk.Label(self.header_frame, text=f"Halo, {self.player_name.get()} {self.player_avatar.get()}", style='Header.TLabel', bootstyle="inverse-primary").pack(side="right")

    def create_sidebar_widgets(self):
        ttk.Label(self.sidebar_frame, text="Pilih Pelajaran", font=self.subtitle_font, bootstyle="inverse-light").pack(pady=10, fill="x")
        
        buttons_data = [
            (" Halaman Utama", "assets/icon_home.png", "dark", lambda: self.show_page(WelcomePage)),
            (" B. Indonesia", "assets/icon_indonesia.png", "primary", lambda: self.show_submenu("Bahasa Indonesia")),
            (" Matematika", "assets/icon_matematika.png", "info", lambda: self.show_submenu("Matematika")),
            (" IPA", "assets/icon_ipa.png", "success", lambda: self.show_submenu("IPA"))
        ]

        for text, icon_path, style, command in buttons_data:
            icon_img = self.load_image(icon_path, (24, 24))
            btn = ttk.Button(self.sidebar_frame, text=text, image=icon_img, compound="left", bootstyle=style, command=command)
            btn.image = icon_img
            btn.pack(pady=5, fill="x", ipady=8)
        
        logout_icon = self.load_image("assets/icon_logout.png", (24, 24))
        logout_btn = ttk.Button(self.sidebar_frame, text=" Logout", image=logout_icon, compound="left", bootstyle="secondary-outline", command=self.logout)
        logout_btn.image = logout_icon
        logout_btn.pack(side="bottom", pady=20, fill="x")

    def show_page(self, page_class, *args):
        if self._current_page:
            self._current_page.frame.destroy()
        self._current_page = page_class(self.main_content_frame, self, *args)
        self._current_page.show()

    def show_submenu(self, subject):
        self.show_page(SubmenuPage, subject)

    def start_quiz(self, subject, topic):
        self.show_page(QuizPage, subject, topic)

# ==============================================================================
# == TITIK MASUK APLIKASI
# ==============================================================================
if __name__ == "__main__":
    root = ttk.Window(themename="minty") 
    app = AplikasiBelajarSeru(root)
    root.mainloop()
