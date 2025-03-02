import os
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Veri seti yolu
path = "../karakterseti4/"
siniflar = os.listdir(path)
urls = []
sinifs = []
data_Set = 0
for sinif in siniflar:
    resimler = os.listdir(path + sinif)
    for resim in resimler:
        urls.append(path + sinif + "/" + resim)
        sinifs.append(sinif)
        data_Set += 1

df = pd.DataFrame({"adres": urls, "sinif": sinifs})

# Özellik çıkarma fonksiyonu
def islem(img):
    if img.shape == (200, 200, 1):
        img = img.squeeze()  # (200, 200, 1) -> (200, 200)
    assert img.shape == (200, 200), f"Yanlış boyut: {img.shape}"
    yeni_boy = img.reshape((1600, 5, 5))  # 200x200'lük resim olmalı
    orts = []
    for parca in yeni_boy:
        ort = np.mean(parca)
        orts.append(ort)
    return np.array(orts).reshape(1600,)

# Ön işleme fonksiyonu
def on_isle(img):
    return img / 255

# Hiperparametreler
target_size = (200, 200)
batch_size = data_Set

# ImageDataGenerator kullanarak veri seti oluşturma
train_gen = tf.keras.preprocessing.image.ImageDataGenerator(preprocessing_function=on_isle)

train_set = train_gen.flow_from_dataframe(
    df, x_col="adres", y_col="sinif",
    target_size=target_size,
    color_mode="grayscale",
    shuffle=True,
    class_mode='sparse',
    batch_size=batch_size
)

# Görüntüleri ve etiketleri elde et
images, train_y = next(train_set)

# Görüntüleri özelliklere dönüştürme
train_x = np.array(list(map(islem, images))).astype("float32")
train_y = train_y.astype(int)

# Veriyi eğitim ve test setine ayırma
train_x, test_x, train_y, test_y = train_test_split(train_x, train_y, test_size=0.2, random_state=42)

# Random Forest modelini eğitme
print("Random Forest eğitiliyor...")
rfc = RandomForestClassifier(n_estimators=100, criterion="entropy")
rfc.fit(train_x, train_y)

# Modeli test etme
pred = rfc.predict(test_x)
acc = accuracy_score(pred, test_y)
print("Başarı:", acc)

# Modeli kaydetme
dosya = "rfc_model2.rfc"
pickle.dump(rfc, open(dosya, "wb"))

# Modeli doğrulama
loaded_rfc = pickle.load(open(dosya, "rb"))
print("Model başarıyla kaydedildi ve yüklendi.")