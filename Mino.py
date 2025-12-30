import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc
import tkinter.messagebox as messagebox
import datetime
import pypyodbc

class LoginForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Giriş")
        self.master.geometry("500x400+500+250")
        self.master.iconbitmap('assets/mino.ico')
        self.master.resizable(False, False)
        
        self.username_label = ttk.Label(self.master, text="Kullanıcı Adı:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.username_entry = ttk.Entry(self.master, width=15)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.username_entry.focus()
        
        self.password_label = ttk.Label(self.master, text="Şifre:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.password_entry = ttk.Entry(self.master, width=15, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.show_password_var = tk.BooleanVar(value=False)
        self.show_password_checkbutton = ttk.Checkbutton(
            self.master, text="Şifreyi Göster/Gizle", variable=self.show_password_var, command=self.show_password
        )
        self.show_password_checkbutton.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.remember_me_var = tk.BooleanVar(value=False)
        self.remember_me_checkbutton = ttk.Checkbutton(
            self.master, text="Beni Hatırla", variable=self.remember_me_var
        )
        self.remember_me_checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.password_forgot_button = ttk.Button(
            self.master, text="Şifremi Unuttum", command=self.forgot_password
        )
        self.password_forgot_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.login_button = ttk.Button(self.master, text="Giriş Yap", command=self.login)
        self.login_button.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        
        self.register_button = ttk.Button(self.master, text="Kayıt Ol", command=self.register)
        self.register_button.grid(row=4, column=1, padx=5, pady=5, sticky="e")
        
        self.status_label = ttk.Label(self.master, text="", foreground="red")
        self.status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
    def show_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def forgot_password(self):
        self.status_label.config(text="Şifrenizi sıfırlamak için sistem yöneticinize başvurun.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Veritabanı kontrolü
        conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/Kullanicikayitlari.accdb;")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Kayitlar WHERE KullaniciAdi=? AND Sifre=?", (username, password))
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")
        else:
            if self.remember_me_var.get():
                print("Beni Hatırla seçildi.")
                self.status_label.config(text="Giriş Başarılı!")
                self.master.withdraw()  # Ana pencereyi gizle
                self.open_new_form()  # Yeni formu aç
            else:
                messagebox.showinfo("Bilgi", "Giriş Başarılı!")
                self.master.withdraw()  # Ana pencereyi gizle
                self.open_new_form()  # Yeni formu aç

        if len(username) > 12 or not username.isalpha():
            self.status_label.config(text="Kullanıcı adı en fazla 12 karakter olmalı ve yalnızca harf içermelidir.")
        elif len(password) > 6 or not password.isnumeric():
            self.status_label.config(text="Şifre en fazla 6 karakter olmalı ve yalnızca rakam içermelidir.")
    def register(self):
        register_window = tk.Toplevel(self.master)
        register_window.title("Kayıt Ol")
        register_window.geometry("500x400+500+250")
        register_window.iconbitmap("assets/mino.ico")
        
        username_label = ttk.Label(register_window, text="Kullanıcı Adı:")
        username_label.pack()
        
        username_entry = ttk.Entry(register_window)
        username_entry.pack()
        
        email_label = ttk.Label(register_window, text="E-posta Adresi:")
        email_label.pack()
        
        email_entry = ttk.Entry(register_window)
        email_entry.pack()
        
        password_label = ttk.Label(register_window, text="Şifre:")
        password_label.pack()
        
        password_entry = ttk.Entry(register_window, show="*")
        password_entry.pack()
        
        password_confirm_label = ttk.Label(register_window, text="Şifre Tekrar:")
        password_confirm_label.pack()
        
        password_confirm_entry = ttk.Entry(register_window, show="*")
        password_confirm_entry.pack()
        
        show_password = tk.BooleanVar()
        show_password.set(False)
        
        def toggle_password_visibility():
            if show_password.get():
                password_entry.config(show="")
                password_confirm_entry.config(show="")
            else:
                password_entry.config(show="*")
                password_confirm_entry.config(show="*")
        
        show_password_checkbox = ttk.Checkbutton(register_window, text="Şifreleri Göster", variable=show_password, command=toggle_password_visibility)
        show_password_checkbox.pack()
        self.master.withdraw()
        def perform_register():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            password_confirm = password_confirm_entry.get()
        
            # Kullanıcı adı doğrulama
            if not username.isalpha():
                messagebox.showerror("Hata", "Kullanıcı adı sadece harflerden oluşmalıdır.")
                return False
            if len(username) < 3 or len(username) > 12:
                messagebox.showerror("Hata", "Kullanıcı adı 3 ila 12 karakter arasında olmalıdır.")
                return False
        
            # E-posta doğrulama
            if "@" not in email or "." not in email:
                messagebox.showerror("Hata", "Geçerli bir e-posta adresi girin.")
                return False
        
            # Şifre doğrulama
            if password != password_confirm:
                messagebox.showerror("Hata", "Şifreler uyuşmuyor.")
                return False
            if len(password) < 6:
                messagebox.showerror("Hata", "Şifre en az 6 karakter olmalıdır.")
                return False
        
            # Kaydetme işlemi
            conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/Kullanicikayitlari.accdb;")

            cursor = conn.cursor()
            cursor.execute("INSERT INTO Kayitlar (KullaniciAdi, Email, Sifre) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            conn.close()
        
            messagebox.showinfo("Bilgi", "Kayıt başarıyla tamamlandı.")
            register_window.destroy()
            self.master.deiconify()  # Ana pencereyi tekrar görünür hale getir
        
        register_button = ttk.Button(register_window, text="Kaydol", command=perform_register)
        register_button.pack()
            
    def open_new_form(self):
        def ilac_kayit_formunu_ac():
            def kaydet():
                # Kullanıcının girdiği bilgileri al
                ilac_adi = entry_ilac_adi.get()
                ilac_seri_no = entry_ilac_seri_no.get()
                ilac_adeti = entry_ilac_adeti.get()
                ilac_fiyati = entry_ilac_fiyati.get()
                ilac_son_k_tarihi = entry_ilac_son_k_tarihi.get()
                ilac_alindigi_firma = entry_ilac_alindigi_firma.get()
        
                # Gerekli bilgilerin hepsinin girildiğini ve ilac_adeti ve ilac_fiyati'nın sayı olduğunu kontrol et
                if ilac_adi == "" or ilac_seri_no == "" or ilac_adeti == "" or ilac_fiyati == "" or ilac_son_k_tarihi == "" or ilac_alindigi_firma == "":
                    # Hata mesajı göster
                    messagebox.showerror("Hata", "Lütfen tüm bilgileri girin.")
                    return
        
                if not ilac_adeti.isdigit() or not ilac_fiyati.isdigit():
                    # Hata mesajı göster
                    messagebox.showerror("Hata", "İlaç adeti ve fiyatı sayısal değer olmalıdır.")
                    return
        
                try:
                    # ilac_son_k_tarihi'nin doğru bir tarih formatına sahip olup olmadığını kontrol et
                    tarih = datetime.datetime.strptime(ilac_son_k_tarihi, "%d.%m.%Y").date()
    
                    # Bugünkü tarihi al
                    bugun = datetime.datetime.now().date()
    
                    # Girilen tarihin bugünkü tarihten büyük veya eşit olduğunu kontrol et
                    if tarih < bugun:
                        # Hata mesajı göster
                        messagebox.showerror("Hata", "Geçersiz tarih. Lütfen bugünkü tarihten ileri bir tarih girin.")
                        return
                except ValueError:
                    # Hata mesajı göster
                    messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen tarihi 'gün.ay.yıl' formatında girin.")
                    return
        
                try:
                    # Veritabanına bağlan
                    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/ilacverileri.accdb;")

                    cursor = conn.cursor()
    
                    # Veritabanına kaydetme işlemi
                    cursor.execute("INSERT INTO ilaclar (ilac_adi, ilac_seri_no, ilac_adeti, ilac_fiyati, ilac_son_k_tarihi, ilac_alindigi_firma) VALUES (?, ?, ?, ?, ?, ?)",
                               ilac_adi, ilac_seri_no, ilac_adeti, ilac_fiyati, ilac_son_k_tarihi, ilac_alindigi_firma)
                    conn.commit()
    
                    # Bağlantıyı kapat
                    conn.close()
    
                    # Kullanıcıya kaydedildi mesajını göster
                    messagebox.showinfo("Başarılı", "İlaç kaydedildi!")
                except Exception as e:
                    # Hata mesajı göster
                    messagebox.showerror("Hata", str(e))
            
        
            # İlaç kayıt formunu oluşturma
            ilac_kayit_form = tk.Toplevel(root)
            ilac_kayit_form.geometry("300x250+1000+250")
            ilac_kayit_form.iconbitmap("assets/mino.ico")
            ilac_kayit_form.title("İlaç Kayıt Formu")
    
            # İlaç adı etiketi ve metin kutusu
            label_ilac_adi = tk.Label(ilac_kayit_form, text="İlaç Adı:")
            label_ilac_adi.grid(row=0, column=0, padx=5, pady=5)
            entry_ilac_adi = tk.Entry(ilac_kayit_form)
            entry_ilac_adi.grid(row=0, column=1, padx=5, pady=5)
    
            # İlaç seri no etiketi ve metin kutusu
            label_ilac_seri_no = tk.Label(ilac_kayit_form, text="İlaç Seri No:")
            label_ilac_seri_no.grid(row=1, column=0, padx=5, pady=5)
            entry_ilac_seri_no = tk.Entry(ilac_kayit_form)
            entry_ilac_seri_no.grid(row=1, column=1, padx=5, pady=5)
    
            # İlaç adeti etiketi ve metin kutusu
            label_ilac_adeti = tk.Label(ilac_kayit_form, text="İlaç Adeti:")
            label_ilac_adeti.grid(row=2, column=0, padx=5, pady=5)
            entry_ilac_adeti = tk.Entry(ilac_kayit_form)
            entry_ilac_adeti.grid(row=2, column=1, padx=5, pady=5)
    
            # İlaç fiyatı etiketi ve metin kutusu
            label_ilac_fiyati = tk.Label(ilac_kayit_form, text="İlaç Fiyatı:")
            label_ilac_fiyati.grid(row=3, column=0, padx=5, pady=5)
            entry_ilac_fiyati = tk.Entry(ilac_kayit_form)
            entry_ilac_fiyati.grid(row=3, column=1, padx=5, pady=5)
    
            # İlaçın son kullanma tarihi etiketi ve metin kutusu
            label_ilac_son_k_tarihi = tk.Label(ilac_kayit_form, text="Son Kullanma Tarihi:")
            label_ilac_son_k_tarihi.grid(row=4, column=0, padx=5, pady=5)
            entry_ilac_son_k_tarihi = tk.Entry(ilac_kayit_form)
            entry_ilac_son_k_tarihi.grid(row=4, column=1, padx=5, pady=5)
    
            # İlacın alındığı firma etiketi ve metin kutusu
            label_ilac_alindigi_firma = tk.Label(ilac_kayit_form, text="Alındığı Firma:")
            label_ilac_alindigi_firma.grid(row=5, column=0, padx=5, pady=5)
            entry_ilac_alindigi_firma = tk.Entry(ilac_kayit_form)
            entry_ilac_alindigi_firma.grid(row=5, column=1, padx=5, pady=5)
    
            # Kaydet butonu
            button_kaydet = tk.Button(ilac_kayit_form, text="Kaydet", command=kaydet)
            button_kaydet.grid(row=6, column=1, padx=5, pady=5)
    
        def show_ilac_listesi():
            # Yeni pencere oluştur
            liste_pencere = tk.Toplevel()
            liste_pencere.geometry("800x400+700+250")
            liste_pencere.iconbitmap("assets/mino.ico")
            liste_pencere.title("İlaç Listesi")
            
            # Veritabanına bağlan
            conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/ilacverileri.accdb;")

            cursor = conn.cursor()
            
            # İlaç listesini sorgula
            cursor.execute("SELECT * FROM ilaclar")
            ilac_listesi = cursor.fetchall()
    
            def sil():
                # Seçili satırı al
                selected_item = treeview_ilac_listesi.selection()
    
                if selected_item:
                    deleted_indices = []  # Silinen satırların indislerini tutacak liste
                    for item in selected_item:
                        # Satırın ID değerini al
                        ilac_id = treeview_ilac_listesi.item(item)['values'][0]
        
                        # Veritabanından ilacı sil
                        cursor.execute("DELETE FROM İlaclar WHERE ilac_id LIKE ? OR ilac_seri_no LIKE ?", (ilac_id, ilac_id))
                        conn.commit()
        
                        # Silinen satırın sıra numarasını kaydet
                        deleted_indices.append(int(ilac_id))
        
                        # Satırı sil
                        treeview_ilac_listesi.delete(item)
    
                    # Sıra numaralarını güncelle
                    for i, item in enumerate(treeview_ilac_listesi.get_children(), start=1):
                        if i in deleted_indices:
                            continue  # Silinen satırı atla
                        new_index = i - sum([1 for index in deleted_indices if index < i])
                        treeview_ilac_listesi.item(item, values=(str(new_index), *treeview_ilac_listesi.item(item)['values'][1:]))
            
                        # Veritabanında sıra numarasını güncelle
                        ilac_id = treeview_ilac_listesi.item(item)['values'][0]
                        cursor.execute("UPDATE İlaclar SET sira_no = ? WHERE ilac_id = ?", (new_index, ilac_id))
                        conn.commit()
    
                    conn.close()
    
                else:
                    messagebox.showwarning("Uyarı", "Lütfen silmek için bir ilaç seçin.")
            
    
        
            # Treeview oluştur
            treeview_ilac_listesi = ttk.Treeview(liste_pencere)
        
            # Sütunlar tanımla
            treeview_ilac_listesi["columns"] = ("id", "ad", "seri_no", "adet", "fiyat", "son_k_tarihi", "firma")
        
            # Sütun özelliklerini ayarla
            treeview_ilac_listesi.column("#0", width=0, stretch=tk.NO)  # İlk sütunu gizle
            treeview_ilac_listesi.column("id", width=50, anchor=tk.CENTER)
            treeview_ilac_listesi.column("ad", width=150, anchor=tk.W)
            treeview_ilac_listesi.column("seri_no", width=100, anchor=tk.CENTER)
            treeview_ilac_listesi.column("adet", width=50, anchor=tk.CENTER)
            treeview_ilac_listesi.column("fiyat", width=70, anchor=tk.CENTER)
            treeview_ilac_listesi.column("son_k_tarihi", width=120, anchor=tk.CENTER)
            treeview_ilac_listesi.column("firma", width=150, anchor=tk.W)
        
            # Sütun başlıklarını ayarla
            treeview_ilac_listesi.heading("id", text="ID")
            treeview_ilac_listesi.heading("ad", text="İlaç Adı")
            treeview_ilac_listesi.heading("seri_no", text="Seri No")
            treeview_ilac_listesi.heading("adet", text="Adet")
            treeview_ilac_listesi.heading("fiyat", text="Fiyat")
            treeview_ilac_listesi.heading("son_k_tarihi", text="Son Kullanma Tarihi")
            treeview_ilac_listesi.heading("firma", text="Alındığı Firma")
    
            # Arama fonksiyonunu tanımla
            def ilac_ara():
                seri_no = arama_entry.get().strip().lower()  # Seri numarası değerini al ve küçük harflere çevir
    
                # Seri numarasının boş olup olmadığını kontrol et
                if seri_no == "":
                    messagebox.showwarning("Uyarı", "Lütfen seri numarası girin.")
                    return
    
                # İlaç listesini temizle
                treeview_ilac_listesi.delete(*treeview_ilac_listesi.get_children())
    
                # Seri numarasına göre arama yap
                for ilac in ilac_listesi:
                    if ilac[2].lower() == seri_no:
                        treeview_ilac_listesi.insert("", tk.END, values=(ilac[0], ilac[1], ilac[2], ilac[3], ilac[4], ilac[5], ilac[6]))
                        break
                else:
                    messagebox.showinfo("Bilgi", "Seri numarası bulunamadı.")
    
            # Arama giriş kutusunu oluştur
            arama_label = tk.Label(liste_pencere, text="Seri No")
            arama_label.pack()
            arama_entry = tk.Entry(liste_pencere)
            arama_entry.pack(pady=5)
        
            # Arama düğmesini oluştur
            arama_butonu = tk.Button(liste_pencere, text="Ara", command=ilac_ara)
            arama_butonu.pack(pady=5)
        
            # İlaç listesini ekle
            for i, ilac in enumerate(ilac_listesi, start=0):
                treeview_ilac_listesi.insert("", tk.END, values=(ilac[0], ilac[1], ilac[2], ilac[3], ilac[4], ilac[5], ilac[6]))
        
            # Sütun genişliklerini otomatik ayarla
            for column in treeview_ilac_listesi["columns"]:
                treeview_ilac_listesi.column(column, width=100, anchor=tk.CENTER)
        
            # Treeview'i yerleştir
            treeview_ilac_listesi.pack(padx=10, pady=10)
        
            # Silme düğmesini oluştur
            sil_butonu = tk.Button(liste_pencere, text="Sil", command=sil)
            sil_butonu.pack(pady=5)
    
        
    
        root = tk.Tk()
        root.geometry("500x300+450+250")
        root.iconbitmap('assets/mino.ico')
        root.title("Mino")
    
    
        def open_ilac_listeleme_formu():
            show_ilac_listesi()
        
        def musteri_kayit_formunu_ac():
            def clear_entries():
                owner_name_entry.delete(0, "end")
                owner_surname_entry.delete(0, "end")
                owner_phone_entry.delete(0, "end")
                owner_email_entry.delete(0, "end")
                owner_address_entry.delete(0, "end")
                pet_name_entry.delete(0, "end")
                pet_color_entry.delete(0, "end")
                pet_gender_entry.delete(0, "end")
                pet_weight_entry.delete(0, "end")
                pet_species_entry.delete(0, "end")
                pet_breed_entry.delete(0, "end")
                pet_age_entry.delete(0, "end")
                pet_allergy_entry.delete(0, "end")
                notes_entry.delete("1.0", "end")
    
            def musteri_kaydet():
                veteriner = vet_combobox.get()
                sahip_adi = owner_name_entry.get()
                sahip_soyadi = owner_surname_entry.get()
                sahip_telefon = owner_phone_entry.get()
                sahip_email = owner_email_entry.get()
                sahip_adres = owner_address_entry.get()
                hayvan_adi = pet_name_entry.get()
                hayvan_renk = pet_color_entry.get()
                hayvan_cinsiyet = pet_gender_entry.get()
                hayvan_agirlik = pet_weight_entry.get()
                hayvan_tur = pet_species_entry.get()
                hayvan_irki = pet_breed_entry.get()
                hayvan_yas = pet_age_entry.get()
                hayvan_alerji = pet_allergy_entry.get()
                notlar = notes_entry.get("1.0", "end")
        
                # Bağlantı dizesi
                conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/musteriverileri.accdb;")
        
                # Veritabanına bağlan
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
    
                # Verileri ekleme
                ekleme_sorgu = """
                INSERT INTO Musteriler (
                    Veteriner,
                    SahipAdi,
                    SahipSoyadi,
                    SahipTelefon,
                    SahipEmail,
                    SahipAdres,
                    HayvanAdi,
                    HayvanRenk,
                    HayvanCinsiyet,
                    HayvanAgirlik,
                    HayvanTur,
                    HayvanIrki,
                    HayvanYas,
                    HayvanAlerji,
                    Notlar
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                degerler = (
                    veteriner,
                    sahip_adi,
                    sahip_soyadi,
                    sahip_telefon,
                    sahip_email,
                    sahip_adres,
                    hayvan_adi,
                    hayvan_renk,
                    hayvan_cinsiyet,
                    hayvan_agirlik,
                    hayvan_tur,
                    hayvan_irki,
                    hayvan_yas,
                    hayvan_alerji,
                    notlar
                )
                cursor.execute(ekleme_sorgu, degerler)
                conn.commit()
                # Bağlantıyı kapat
                cursor.close()
                conn.close()
    
                messagebox.showinfo("Başarılı", "Müşteri kaydedildi.")
    
                clear_entries()
    
            # Ana pencereyi oluştur
            window = tk.Tk()
            window.geometry("600x700+800+50")
            window.iconbitmap('assets/mino.ico')
            window.title("Müşteri Kayıt")
        
            # Vet seçimi oluştur
            vet_label = tk.Label(window, text="Veteriner Seçin:")
            vet_label.pack()
            vet_combobox = ttk.Combobox(window, values=["Dr. Ahmet", "Dr. Selin", "Dr. Mehmet"])
            vet_combobox.pack()
        
            # Sahip bilgilerini oluştur
            owner_frame = tk.Frame(window)
            owner_frame.pack()
        
            owner_label = tk.Label(owner_frame, text="Sahip Bilgileri")
            owner_label.grid(row=0, column=0, columnspan=2, pady=5)
        
            owner_name_label = tk.Label(owner_frame, text="Ad:")
            owner_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
            owner_name_entry = tk.Entry(owner_frame)
            owner_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
            owner_surname_label = tk.Label(owner_frame, text="Soyad:")
            owner_surname_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
            owner_surname_entry = tk.Entry(owner_frame)
            owner_surname_entry.grid(row=2, column=1, padx=5, pady=5)
        
            owner_phone_label = tk.Label(owner_frame, text="Telefon:")
            owner_phone_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
            owner_phone_entry = tk.Entry(owner_frame)
            owner_phone_entry.grid(row=3, column=1, padx=5, pady=5)
        
            owner_email_label = tk.Label(owner_frame, text="E-posta:")
            owner_email_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
            owner_email_entry = tk.Entry(owner_frame)
            owner_email_entry.grid(row=4, column=1, padx=5, pady=5)
        
            owner_address_label = tk.Label(owner_frame, text="Adres:")
            owner_address_label.grid(row=5, column=0, padx=5, pady=5, sticky="E")
            owner_address_entry = tk.Entry(owner_frame)
            owner_address_entry.grid(row=5, column=1, padx=5, pady=5)
        
            # Evcil hayvan bilgilerini oluştur
            pet_frame = tk.Frame(window)
            pet_frame.pack()
        
            pet_label = tk.Label(pet_frame, text="Evcil Hayvan Bilgileri")
            pet_label.grid(row=0, column=0, columnspan=2, pady=5)
        
            pet_name_label = tk.Label(pet_frame, text="Ad:")
            pet_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
            pet_name_entry = tk.Entry(pet_frame)
            pet_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
            pet_color_label = tk.Label(pet_frame, text="Renk:")
            pet_color_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
            pet_color_entry = tk.Entry(pet_frame)
            pet_color_entry.grid(row=2, column=1, padx=5, pady=5)
        
            pet_gender_label = tk.Label(pet_frame, text="Cinsiyet:")
            pet_gender_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
            pet_gender_entry = tk.Entry(pet_frame)
            pet_gender_entry.grid(row=3, column=1, padx=5, pady=5)
        
            pet_weight_label = tk.Label(pet_frame, text="Ağırlık:")
            pet_weight_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
            pet_weight_entry = tk.Entry(pet_frame)
            pet_weight_entry.grid(row=4, column=1, padx=5, pady=5)
        
            pet_species_label = tk.Label(pet_frame, text="Tür:")
            pet_species_label.grid(row=5, column=0, padx=5, pady=5, sticky="E")
            pet_species_entry = tk.Entry(pet_frame)
            pet_species_entry.grid(row=5, column=1, padx=5, pady=5)
        
            pet_breed_label = tk.Label(pet_frame, text="Cins:")
            pet_breed_label.grid(row=6, column=0, padx=5, pady=5, sticky="E")
            pet_breed_entry = tk.Entry(pet_frame)
            pet_breed_entry.grid(row=6, column=1, padx=5, pady=5)
        
            pet_age_label = tk.Label(pet_frame, text="Yaş:")
            pet_age_label.grid(row=7, column=0, padx=5, pady=5, sticky="E")
            pet_age_entry = tk.Entry(pet_frame)
            pet_age_entry.grid(row=7, column=1, padx=5, pady=5)
        
            pet_allergy_label = tk.Label(pet_frame, text="Alerji:")
            pet_allergy_label.grid(row=8, column=0, padx=5, pady=5, sticky="E")
            pet_allergy_entry = tk.Entry(pet_frame)
            pet_allergy_entry.grid(row=8, column=1, padx=5, pady=5)
        
            pet_race_label = tk.Label(pet_frame, text="Irk:")
            pet_race_label.grid(row=9, column=0, padx=5, pady=5, sticky="E")
            pet_race_entry = tk.Entry(pet_frame)
            pet_race_entry.grid(row=9, column=1, padx=5, pady=5)
        
            # Notları oluştur
            notes_label = tk.Label(window, text="Notlar:")
            notes_label.pack()
            notes_entry = tk.Text(window, height=5)
            notes_entry.pack()
        
            # Düğmeleri oluştur
            button_frame = tk.Frame(window)
            button_frame.pack()
        
            save_button = tk.Button(button_frame, text="Müşteri Kaydet", command=musteri_kaydet)
            save_button.grid(row=0, column=0, padx=5, pady=5)
        
            clear_button = tk.Button(button_frame, text="Temizle", command=clear_entries)
            clear_button.grid(row=0, column=1, padx=5, pady=5)
    
        def musteri_listeleme_formunu_ac():
            class MusteriKayitListesi:
                def __init__(self):
                    self.pencere = tk.Toplevel()
                    self.pencere.geometry("500x480+1000+250")
                    self.pencere.iconbitmap('assets/mino.ico')
                    self.pencere.title("Müşteri Kayıt Listesi")
        
                    self.musteri_listesi_yazi_alani = tk.Text(self.pencere, width=40, height=20)
                    self.musteri_listesi_yazi_alani.pack()
        
                    self.arama_etiketi = tk.Label(self.pencere, text="Müşteri Adı:")
                    self.arama_etiketi.pack()
        
                    self.arama_girdisi = tk.Entry(self.pencere)
                    self.arama_girdisi.pack()
        
                    self.arama_butonu = tk.Button(self.pencere, text="Ara", command=self.musteri_ara)
                    self.arama_butonu.pack()
        
                    self.silme_etiketi = tk.Label(self.pencere, text="Silinecek Müşteri Adı:")
                    self.silme_etiketi.pack()
        
                    self.silme_girdisi = tk.Entry(self.pencere)
                    self.silme_girdisi.pack()
        
                    self.silme_butonu = tk.Button(self.pencere, text="Sil", command=self.musteri_sil)
                    self.silme_butonu.pack()
        
                    self.musteri_kayitlarini_listele()
    
                def musteri_kayitlarini_listele(self):
                    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/musteriverileri.accdb")
                    cursor = conn.cursor()
    
                    # Müşteri kayıtlarını listeleme
                    cursor.execute("SELECT Veteriner, SahipAdi, SahipSoyadi, SahipTelefon, SahipEmail, SahipAdres, HayvanAdi, HayvanRenk, HayvanCinsiyet, HayvanAgirlik, HayvanTur, HayvanIrki, HayvanYas, HayvanAlerji, Notlar FROM Musteriler")
                    kayitlar = cursor.fetchall()
    
                    self.musteri_listesi_yazi_alani.delete(1.0, tk.END)
    
                    if kayitlar:
                        for kayit in kayitlar:
                            musteri_bilgisi = f"Veteriner: {kayit.Veteriner}\nMüşteri Adı: {kayit.SahipAdi}\nSoyadı: {kayit.SahipSoyadi}\nTelefon: {kayit.SahipTelefon}\nEmail: {kayit.SahipEmail}\nAdres: {kayit.SahipAdres}\nHayvan Adı: {kayit.HayvanAdi}\nHayvan Renk: {kayit.HayvanRenk}\nHayvan Cinsiyet: {kayit.HayvanCinsiyet}\nHayvan Agirlik: {kayit.HayvanAgirlik}\nHayvan Tur: {kayit.HayvanTur}\nHayvan Irki: {kayit.HayvanIrki}\nHayvan Yas: {kayit.HayvanYas}\nHayvan Alerji: {kayit.HayvanAlerji}\nNotlar: {kayit.Notlar}\n---\n"
                            self.musteri_listesi_yazi_alani.insert(tk.END, musteri_bilgisi)
                    else:
                        self.musteri_listesi_yazi_alani.insert(tk.END, "Kayıtlı müşteri bulunamadı.")
    
                    conn.close()            
    
                def musteri_ara(self):
                    aranan_musteri = self.arama_girdisi.get()
                    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/musteriverileri.accdb")
                    cursor = conn.cursor()
    
                    # Müşteri arama
                    cursor.execute(f"SELECT * FROM Musteriler WHERE SahipAdi LIKE ? OR SahipSoyadi LIKE ?", (f'%{aranan_musteri}%', f'%{aranan_musteri}%'))
                    bulunan_musteriler = cursor.fetchall()
    
                    self.musteri_listesi_yazi_alani.delete(1.0, tk.END)
        
                    if bulunan_musteriler:
                        for kayit in bulunan_musteriler:
                            musteri_bilgisi = f"Veteriner: {kayit[1]}\nMüşteri Adı: {kayit[2]}\nSoyadı: {kayit[3]}\nTelefon: {kayit[4]}\nEmail: {kayit[5]}\nAdres: {kayit[6]}\nHayvan Adı: {kayit[7]}\nHayvan Renk: {kayit[8]}\nHayvan Cinsiyet: {kayit[9]}\nHayvan Agirlik: {kayit[10]}\nHayvan Tur: {kayit[11]}\nHayvan Irki: {kayit[12]}\nHayvan Yas: {kayit[13]}\nHayvan Alerji: {kayit[14]}\nNotlar: {kayit[15]}\n---\n"
                            self.musteri_listesi_yazi_alani.insert(tk.END, musteri_bilgisi)
                    else:
                        self.musteri_listesi_yazi_alani.insert(tk.END, "Müşteri bulunamadı.")
    
                    conn.close()
    
                def musteri_sil(self):
                    silinecek_musteri = self.silme_girdisi.get()
                    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"r"DBQ=database/musteriverileri.accdb")
                    cursor = conn.cursor()
    
                    # Müşteri silme
                    cursor.execute(f"DELETE FROM Musteriler WHERE SahipAdi LIKE ? OR SahipSoyadi LIKE ?", (silinecek_musteri, silinecek_musteri))
                    conn.commit()
        
                    affected_rows = cursor.rowcount
        
                    self.musteri_listesi_yazi_alani.delete(1.0, tk.END)
    
                    if affected_rows > 0:
                        self.musteri_listesi_yazi_alani.insert(tk.END, f"{affected_rows} müşteri silindi.")
                    else:
                            self.musteri_listesi_yazi_alani.insert(tk.END, "Müşteri bulunamadı.")
    
                    conn.close()
    
            musteri_kayit_listesi = MusteriKayitListesi()
    
    
        # İlaç kayıt formu butonu
        ilac_kayit_btn = tk.Button(root, text="İlaç Kayıt", command=ilac_kayit_formunu_ac)
        ilac_kayit_btn.pack(pady=10)

        # İlaç listeleme formu butonu
        ilac_listeleme_formu_buton = tk.Button(root, text="İlaç Listeleme", command=open_ilac_listeleme_formu)
        ilac_listeleme_formu_buton.pack(pady=10)

        # Müşteri kayıt butonu
        musteri_kayit_btn = tk.Button(root, text="Müşteri Kayıt", command=musteri_kayit_formunu_ac)
        musteri_kayit_btn.pack(pady=10)

        # Müşteri listeleme butonu
        musteri_listele_btn = tk.Button(root, text="Müşteri Listeleme", command=musteri_listeleme_formunu_ac)
        musteri_listele_btn.pack(pady=10)

        # Ana uygulamayı başlat
        root.mainloop()

root = tk.Tk()
app = LoginForm(root)
root.mainloop()
