import random
import smtplib
import tkinter as tk
from tkinter import messagebox

def generate_security_code():
    """
    Bu fonksiyon, 6 haneli bir rastgele güvenlik kodu üretir.
    """
    security_code = ""
    for i in range(6):
        security_code += str(random.randint(1, 9))
    return security_code


def send_email(receiver_email, security_code):
    """
    Bu fonksiyon, verilen e-posta adresine belirtilen güvenlik kodunu içeren bir e-posta gönderir.
    """
    sender_email = "GONDEREN_EPOSTA_ADRESINIZ"
    sender_password = "GONDEREN_EPOSTA_SIFRENIZ"

    message = f"Konu: Şifre Yenileme Güvenlik Kodu\n\nGüvenlik Kodunuz: {security_code}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        messagebox.showinfo("Başarılı", "Güvenlik kodunuz e-posta adresinize gönderildi.")
    except:
        messagebox.showerror("Hata", "E-posta gönderilirken bir hata oluştu.")

def validate_password(password):
    # Şifrenin doğru formatta olup olmadığı burada kontrol edilebilir
    # Bu örnekte sadece şifrenin 6 basamaklı bir sayı olması kontrol edilecek
    if len(password) != 6 or not password.isdigit():
        return False
    else:
        return True

def reset_password():
    email = email_entry.get()

    if email == "":
        show_error("Lütfen bir e-posta adresi girin.")
    else:
        security_code = generate_security_code()
        send_email(email, security_code)
        security_code_entry.delete(0, tk.END)
        security_code_entry.insert(0, security_code)

def perform_password_reset():
    email = email_entry.get()
    security_code = security_code_entry.get()
    new_password = new_password_entry.get()
    new_password_again = new_password_again_entry.get()

    # Gerekli doğrulama kontrollerini yapma
    if email == "":
        show_error("Lütfen bir e-posta adresi girin.")
    elif security_code == "":
        show_error("Lütfen doğrulama kodunu girin.")
    elif new_password == "":
        show_error("Lütfen yeni şifrenizi girin.")
    elif new_password != new_password_again:
        show_error("Yeni şifreniz uyuşmuyor. Lütfen tekrar deneyin.")
    elif not validate_password(new_password):
        show_error("Yeni şifre 6 basamaklı bir sayı olmalıdır.")
    else:
        # Burada şifrenin sıfırlanması ve veritabanına kaydedilmesi işlemleri gerçekleştirilir
        messagebox.showinfo("Başarılı", "Şifreniz başarıyla sıfırlandı.")

def show_error(message):
    error_label.config(text=message)

window = tk.Tk()
window.title("Şifre Yenileme Formu")
window.geometry("400x300")
window.resizable(False, False)



# E-posta giriş kutusunu oluşturma
email_label = tk.Label(window, text="E-posta:")
email_label.pack(pady=10)
email_entry = tk.Entry(window, width=30)
email_entry.pack()

# Güvenlik kodu giriş kutusunu oluşturma
security_code_label = tk.Label(window, text="Güvenlik Kodu:")
security_code_label.pack(pady=10)
security_code_entry = tk.Entry(window, width=30)
security_code_entry.pack()

# Yeni şifre giriş kutusunu oluşturma
new_password_label = tk.Label(window, text="Yeni Şifre:")
new_password_label.pack(pady=10)
new_password_entry = tk.Entry(window, show="*")
new_password_entry.pack()

# Yeni şifre tekrar giriş kutusunu oluşturma
new_password_again_label = tk.Label(window, text="Yeni Şifre (Tekrar):")
new_password_again_label.pack(pady=10)
new_password_again_entry = tk.Entry(window, show="*")
new_password_again_entry.pack()

error_label = tk.Label(window, fg="red")
error_label.pack()

def generate_security_code():
    """
    Bu fonksiyon, 6 haneli bir rastgele güvenlik kodu üretir.
    """
    security_code = ""
    for i in range(6):
        security_code += str(random.randint(1, 9))
    return security_code


def send_security_code():
    """
    Bu fonksiyon, kullanıcının e-posta adresine güvenlik kodunu gönderir.
    """
    email = email_entry.get()

    if email == "":
        show_error("Lütfen bir e-posta adresi girin.")
        return

    security_code = generate_security_code()
    send_email(email, security_code)
    show_info("Güvenlik kodu e-posta adresinize gönderildi.")


    # Yeni şifrenin kaydedilmesi
    # Burada yeni şifrenin veritabanına kaydedilmesi gerekiyor

    messagebox.showinfo("Başarılı", "Şifreniz başarıyla güncellendi.")
def verify_security_code():
    """
    Bu fonksiyon, kullanıcının girdiği güvenlik kodunu doğrular.
    """
    entered_code = security_code_entry.get()

    if entered_code == "":
        show_error("Lütfen bir güvenlik kodu girin.")
        return False

    if entered_code == security_code:
        return True
    else:
        show_error("Girilen güvenlik kodu yanlış.")
        return False
    
def perform_password_reset():
    """
    Bu fonksiyon, kullanıcının girdiği yeni şifreyi kaydeder ve ekrana mesaj gösterir.
    """
    email = email_entry.get()
    new_password = new_password_entry.get()
    new_password_again = new_password_again_entry.get()

    if email == "":
        show_error("Lütfen bir e-posta adresi girin.")
        return

    if not verify_security_code():
        return

    if new_password == "":
        show_error("Lütfen yeni şifrenizi girin.")
        return

    if new_password != new_password_again:
        show_error("Yeni şifreniz uyuşmuyor. Lütfen tekrar deneyin.")
        return

    if not validate_password(new_password):
        show_error("Yeni şifre 6 basamaklı bir sayı olmalıdır.")
        return

    # Yeni şifrenin kaydedilmesi
    # Burada yeni şifrenin veritabanına kaydedilmesi gerekiyor

    messagebox.showinfo("Başarılı", "Şifreniz başarıyla güncellendi.")

# Ana pencereyi oluşturma
window = tk.Tk()
window.title("Şifre Yenileme Formu")
window.geometry("500x400")
window.resizable(False, False)

# E-posta giriş kutusunu oluşturma
email_label = tk.Label(window, text="E-posta:")
email_label.pack(pady=10)
email_entry = tk.Entry(window, width=30)
email_entry.pack()

# Güvenlik kodu giriş kutusunu oluşturma
security_code_label = tk.Label(window, text="Güvenlik Kodu:")
security_code_label.pack(pady=10)
security_code_entry = tk.Entry(window, width=30)
security_code_entry.pack()

# Yeni şifre giriş kutusunu oluşturma
new_password_label = tk.Label(window, text="Yeni Şifre:")
new_password_label.pack(pady=10)
new_password_entry = tk.Entry(window, show="*")
new_password_entry.pack()

# Yeni şifre tekrar giriş kutusunu oluşturma
new_password_again_label = tk.Label(window, text="Yeni Şifre (Tekrar):")
new_password_again_label.pack(pady=10)
new_password_again_entry = tk.Entry(window, show="*")
new_password_again_entry.pack()

# Şifre sıfırla butonunu oluşturma
reset_button = tk.Button(window, text="Şifremi Sıfırla", command=perform_password_reset)
reset_button.pack(pady=10)

send_security_code_button = tk.Button(window, text="Kod Gönder", command=send_security_code)
send_security_code_button.pack(pady=10)


# Hata etiketi
error_label = tk.Label(window, fg="red")
error_label.pack()

window.mainloop()

