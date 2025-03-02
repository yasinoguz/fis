import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import cv2
import tanima
import fis_no_kesim
from PIL import Image, ImageTk  # Fotoğraf gösterimi için PIL kullanıyoruz

def run_recognition():
    # Dosya yolunu al
    file_path = entry.get()
    if not file_path:
        result_label.config(text="Lütfen bir dosya yolu giriniz!", fg="red")
        return

    try:
        # harf_tanıma fonksiyonunu çağır
        char_list = tanima.harf_tanima(file_path)
        # Sonuçları birleştir ve ekrana yazdır
        result_text = ''.join(char_list)
        result_label.config(text=result_text, fg="black")
        
        # Fotoğraf döndürme işlemini başlat
        rotated_image = fis_no_kesim.fis_donder(file_path)  # Fotoğrafı döndürüyoruz
        display_image(rotated_image)  # Döndürülen fotoğrafı gösteriyoruz
    except Exception as e:
        result_label.config(text=f"Hata: {e}", fg="red")

def browse_file():
    # Dosya seçme penceresi aç
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry.delete(0, tk.END)  # Önceki metni sil
        entry.insert(0, file_path)  # Yeni dosya yolunu yerleştir

def clear_entry():
    entry.delete(0, tk.END)
    result_label.config(text="", fg="black")
    image_label.config(image="")  # Görüntüyü temizle

def display_image(image):
    # OpenCV görüntüsünü tkinter'e uygun hale getirin
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR'den RGB'ye dönüştür
    pil_image = Image.fromarray(image_rgb)  # Numpy dizisinden PIL image'a dönüştür
    pil_image = pil_image.resize((350, 200))  # Görüntüyü yeniden boyutlandır
    tk_image = ImageTk.PhotoImage(pil_image)  # Tkinter için uygun formata dönüştür
    
    # Görüntüyü Tkinter label'ında göster
    image_label.config(image=tk_image)
    image_label.image = tk_image  # Referans tutmak için ekleme

# Tkinter arayüzünü oluştur
window = tk.Tk()
window.title("Harf Tanıma ve Fotoğraf Döndürme")
window.geometry("800x600")

# Dosya yolu girişi
entry_label = tk.Label(window, text="Dosya Yolu:")
entry_label.pack(pady=10)
entry = tk.Entry(window, width=70)
entry.pack(pady=5)

# Gözat butonu
browse_button = tk.Button(window, text="Gözat", command=browse_file)
browse_button.pack(pady=5)

# Çalıştır butonu
run_button = tk.Button(window, text="tanimla", command=run_recognition)
run_button.pack(pady=20)

# Silme butonu
clear_button = tk.Button(window, text="Sil", command=clear_entry)
clear_button.pack(pady=5)

# Sonuç label'ı
result_label = tk.Label(window, text="", font=("Helvetica", 20))
result_label.pack(pady=10)

# Döndürülen fotoğrafı göstermek için bir label
image_label = tk.Label(window)
image_label.pack(pady=10)

# Tkinter döngüsünü başlat
window.mainloop()
