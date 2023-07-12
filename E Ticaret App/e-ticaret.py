# Doğuş Üniversitesi Büt Projesi E Ticaret Sitesi Kodları

# Database bağlama
import sqlite3 # sqlite3 modülüni içeri aktarıyoruz
baglanti = sqlite3.connect("eticaret.db") # eticaret.db adlı database  ile bağlantı kurma
imlec = baglanti.cursor() 

# Eğer yoksa kullanıcılar tablosu oluşturuyoruz
imlec.execute("""CREATE TABLE IF NOT EXISTS kullanıcılar (
    isim TEXT,
    sifre TEXT,
    tip TEXT
)""")

# Eğer yoksa ürünler tablosu oluşturuluyor
imlec.execute("""CREATE TABLE IF NOT EXISTS urunler (
    isim TEXT,
    fiyat REAL
)""")

# Database üzerindeki kullanıcıları ve ürünleri listeler halinde almak için fonksiyonlar
def kullanici_listesi():
    imlec.execute("SELECT * FROM kullanıcılar") # tüm kullanıcıları seçme
    return imlec.fetchall() # Tüm kullanıcıları liste olarak döndürme

def urun_listesi():
    imlec.execute("SELECT * FROM urunler") # Tüm ürünleri seçme
    return imlec.fetchall() # Tüm ürünleri liste olarak döndürme

# Kullanıcı sınıfı tanımlama
class Kullanici:
    def __init__(self, isim, sifre, tip):
        self.isim = isim # Kullanıcı adı
        self.sifre = sifre # Kullanıcı şifresi
        self.tip = tip # Kullanıcı tipi (admin veya standart)
        self.sepet = [] # kullanıcının sepetindeki ürünler
        self.rapor = [] # kullanıcının yaptığı işlemlerin kaydı

    # Kullanıcıya özel rapor almak için fonksiyon
    def rapor_al(self):
        import csv # csv modülü aktif etme
        dosya_adi = self.isim + "_rapor.csv" # rapor dosyasının adını belirliyoruz
        with open(dosya_adi, "w", newline="") as dosya: # Dosyayı yazma modunda açma
            yazici = csv.writer(dosya) # csv yazıcı oluşturma
            yazici.writerow(["İşlem Tarihi", "İşlem Tipi", "İşlem Detayı"]) 
            for islem in self.rapor: 
                yazici.writerow(islem) # işlemi csv dosyasına yazma
        print(f"{dosya_adi} dosyasına raporunuz kaydedildi.") # raporun kaydedildiğini bildirmek için konsola yazı yazdırma

    # Sepete ürün ekleme fonksiyonu
    def sepete_ekle(self, urun):
        self.sepet.append(urun) # sepete ürünü ekleme
        print(f"{urun} sepetinize eklendi.") # sepete eklendiğini bildirme
        from datetime import datetime # datetime ı aktif etme
        tarih = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # İşlem tarihi alınması
        tip = "Sepete Ekleme" 
        detay = urun 
        self.rapor.append([tarih, tip, detay]) # rapora işlemi ekleme

    # Sepetten ürün çıkarma fonksiyonu
    def sepetten_cikar(self, urun):
        if urun in self.sepet: # eğer ürün sepette varsa
            self.sepet.remove(urun) # sepetten ürünü çıkarma
            print(f"{urun} sepetinizden çıkarıldı.") # sepetten çıkarıldığını bildirme
            from datetime import datetime 
            tarih = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
            tip = "Sepetten Çıkarma" 
            detay = urun 
            self.rapor.append([tarih, tip, detay]) # rapora işlemi ekleme
        else: # eğer ürün sepette yoksa
            print(f"{urun} sepetinizde bulunmuyor.") # Ürünün sepette bulunmadığını bildirmek için konsola yazılan yazı

    # Sipariş verme fonksiyonu
    def siparis_ver(self):
        if len(self.sepet) > 0: # eğer sepet boş değilse
            print("Siparişiniz verildi. Sepetinizdeki ürünler:")
            for urun in self.sepet: # sepetteki her ürün için
                print(urun) # ürünü yazdırma
            self.sepet.clear() # sepeti boşaltma
            from datetime import datetime # datetime modülü import etme
            tarih = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # işlem tarihi
            tip = "Sipariş Verme" # işlem tipi
            detay = "Sipariş verildi." # işlem detayı
            self.rapor.append([tarih, tip, detay]) # rapora işlemi ekleme
        else: # eğer sepet boşsa
            print("Sepetiniz boş. Sipariş vermek için önce sepetinize ürün ekleyin.") # sepetin boş olduğunu bildirme

# Admin sınıfı tanımlama 
class Admin(Kullanici):
    def __init__(self, isim, sifre):
        super().__init__(isim, sifre, "admin") # üst sınıfın fonksiyonunu çağırma

    # Tüm kullanıcıların raporlarını almak için fonksiyon
    def tum_raporlari_al(self):
        import csv # csv modülü import etme
        dosya_adi = "tum_raporlar.csv" # rapor dosyasının adı
        with open(dosya_adi, "w", newline="") as dosya: # dosyayı yazma modunda açma
            yazici = csv.writer(dosya) # csv yazıcı oluşturma
            yazici.writerow(["Kullanıcı Adı", "İşlem Tarihi", "İşlem Tipi", "İşlem Detayı"]) # başlık satırı yazma
            for kullanici in kullanici_listesi(): # database üzerindeki her kullanıcı için
                isim = kullanici[0] # kullanıcı adı
                imlec.execute(f"SELECT * FROM {isim}_rapor") # kullanıcının rapor tablosunu seçme
                rapor = imlec.fetchall() # kullanıcının raporunu liste olarak alma
                for islem in rapor: # kullanıcının raporundaki her işlem için
                    yazici.writerow([isim] + list(islem)) # kullanıcı adı ve işlemi csv dosyasına yazma
        print(f"{dosya_adi} dosyasına tüm raporlar kaydedildi.") # raporun kaydedildiğini bildirme

# Programın tanıtım yazısı
print("""
Merhaba, bu bir e-ticaret programıdır. Proje Olarak Tasarladım
Bu programda yönetici veya standart kullanıcı olarak giriş yapabilir,
Sepetinize ürün ekleyip çıkarabilir,
Sipariş verebilir ve rapor alabilirsiniz.
""")

# Programın ana menüsü 
while True:
    print("""
    Ana menü:
    1- Giriş yap
    2- Yeni kullanıcı oluştur
    3- Çıkış yap (programdan çıkış)
    """)
    secim = input("Lütfen yapmak istediğiniz işlemi seçin: ") # kullanıcıdan seçim alma

    if secim == "1": # giriş yapma seçeneği

        isim = input("Lütfen kullanıcı adınızı girin: ") # kullanıcı adı alma
        sifre = input("Lütfen şifrenizi girin: ") # şifre alma
        imlec.execute(f"SELECT * FROM kullanıcılar WHERE isim = '{isim}' AND sifre = '{sifre}'") # database üzerinde kullanıcı adı ve şifreye göre arama yapma
        sonuc = imlec.fetchone() # arama sonucunu almak
        if sonuc: # eğer arama sonucu varsa (giriş başarılıysa)
            tip = sonuc[2] # kullanıcı tipini alma
            if tip == "admin": # eğer kullanıcı tipi admin ise
                kullanici = Admin(isim, sifre) 
                print(f"Merhaba {isim}, yönetici olarak giriş yaptınız.") # giriş mesajı verme
            else: # eğer kullanıcı tipi standart ise
                kullanici = Kullanici(isim, sifre, tip) # Kullanici sınıfından bir nesne oluşturma
                print(f"Merhaba {isim}, standart kullanıcı olarak giriş yaptınız.") # giriş mesajı verme

            # Kullanıcının rapor tablosu oluşturma (eğer yoksa)
            imlec.execute(f"""CREATE TABLE IF NOT EXISTS {isim}_rapor (
                tarih TEXT,
                tip TEXT,
                detay TEXT
            )""")

            # Kullanıcının rapor tablosundaki verileri rapor listesine aktarma
            imlec.execute(f"SELECT * FROM {isim}_rapor") # rapor tablosunu seçme
            rapor = imlec.fetchall() # rapor tablosundaki verileri liste olarak alma
            for islem in rapor: # her işlem için
                kullanici.rapor.append(list(islem)) # işlemi rapor listesine ekleme

            # Kullanıcının sepet tablosu oluşturma 
            imlec.execute(f"""CREATE TABLE IF NOT EXISTS {isim}_sepet (
                urun TEXT,
                fiyat REAL
            )""")

            # Kullanıcının sepet tablosundaki verileri sepet listesine aktarma
            imlec.execute(f"SELECT * FROM {isim}_sepet") # sepet tablosunu seçme
            sepet = imlec.fetchall() # sepet tablosundaki verileri liste olarak alma
            for urun in sepet: # her ürün için
                kullanici.sepet.append(urun[0]) # ürünü sepet listesine ekleme

            # Kullanıcı menüsü 
            while True:
                print("""
                Kullanıcı menüsü:
                1- Ürünleri görüntüle
                2- Sepete ürün ekle
                3- Sepetten ürün çıkar
                4- Sepeti görüntüle
                5- Sipariş ver
                6- Rapor al
                7- Çıkış yap (ana menüye dön)
                """)
                if tip == "admin": # eğer kullanıcı tipi admin ise
                    print("8- Tüm raporları al") # ekstra seçenek gösterme

                secim = input("Lütfen yapmak istediğiniz işlemi seçin: ") # kullanıcıdan seçim almak
                if secim == "1": # ürünleri görüntüleme seçeneği

                    print("Ürünler:")
                    for urun in urun_listesi(): # database üzerindeki her ürün için
                        isim = urun[0] 
                        fiyat = urun[1] 
                        print(f"{isim} - {fiyat} TL") # ürünü ve fiyatını yazdırma

                elif secim == "2": # sepete ürün ekleme seçeneği

                    urun = input("Lütfen sepetinize eklemek istediğiniz ürünü girin: ") # kullanıcıdan ürün almak
                    imlec.execute(f"SELECT * FROM urunler WHERE isim = '{urun}'") # database üzerinde ürüne göre arama yapmak
                    sonuc = imlec.fetchone() # arama sonucunu almak
                    if sonuc: # eğer arama sonucu varsa (ürün mevcutsa)
                        kullanici.sepete_ekle(urun) # kullanıcının sepete ekleme fonksiyonunu çağırmak
                        imlec.execute(f"INSERT INTO {isim}_sepet VALUES (?, ?)", sonuc) # sepet tablosuna ürünü ve fiyatını eklemek
                        baglanti.commit() # database üzerinde değişiklik yapmak
                    else: # eğer arama sonucu yoksa (ürün mevcut değilse)
                        print(f"{urun} adlı bir ürün bulunamadı.") # bulunamadığını bildirme

                elif secim == "3": # sepetten ürün çıkarma seçeneği

                    urun = input("Lütfen sepetinizden çıkarmak istediğiniz ürünü girin: ") # kullanıcıdan ürün almak
                    imlec.execute(f"SELECT * FROM urunler WHERE isim = '{urun}'") # database üzerinde ürüne göre arama yapmak
                    sonuc = imlec.fetchone() # arama sonucunu almak
                    if sonuc: # eğer arama sonucu varsa (ürün mevcutsa)
                        kullanici.sepetten_cikar(urun) # kullanıcının sepetten çıkarma fonksiyonunu çağırmak
                        imlec.execute(f"DELETE FROM {isim}_sepet WHERE urun = '{urun}'") # sepet tablosundan ürünü silmek
                        baglanti.commit() # database üzerinde değişiklik yapmak
                    else: # eğer arama sonucu yoksa (ürün mevcut değilse)
                        print(f"{urun} adlı bir ürün bulunamadı.") # bulunamadığını bildirme

                elif secim == "4": # sepeti görüntüleme seçeneği

                    if len(kullanici.sepet) > 0: # eğer sepet boş değilse
                        print("Sepetinizdeki ürünler:")
                        for urun in kullanici.sepet: # sepetteki her ürün için
                            print(urun) # ürünü yazdırma
                    else: # eğer sepet boşsa
                        print("Sepetiniz boş.") # sepetin boş olduğunu bildirme

                elif secim == "5": # sipariş verme seçeneği

                    kullanici.siparis_ver() # kullanıcının sipariş verme fonksiyonunu çağırmak
                    imlec.execute(f"DELETE FROM {isim}_sepet") # sepet tablosunu boşaltmak
                    baglanti.commit() # database üzerinde değişiklik yapmak

                elif secim == "6": # rapor alma seçeneği

                    kullanici.rapor_al() # kullanıcının rapor alma fonksiyonunu çağırmak

                elif secim == "7": # çıkış yapma seçeneği

                    print("Çıkış yaptınız. Ana menüye dönülüyor.") # çıkış mesajı vermek
                    break # kullanıcı menüsünden çıkmak

                elif secim == "8" and tip == "admin": # tüm raporları alma seçeneği (eğer kullanıcı tipi admin ise)

                    kullanici.tum_raporlari_al() # adminin tüm raporları alma fonksiyonunu çağırmak

                else: # geçersiz seçim

                    print("Lütfen geçerli bir seçim yapın.") # geçersiz seçim mesajı vermek

        else: # eğer arama sonucu yoksa (giriş başarısızsa)
            print("Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.") # hata mesajı vermek

    elif secim == "2": # yeni kullanıcı oluşturma seçeneği

        isim = input("Lütfen kullanıcı adınızı girin: ") # kullanıcı adı almak
        sifre = input("Lütfen şifrenizi girin: ") # şifre almak
        tip = input("Lütfen kullanıcı tipinizi girin (admin veya standart): ") # kullanıcı tipi almak
        if tip not in ["admin", "standart"]: # eğer kullanıcı tipi geçerli değilse
            print("Lütfen geçerli bir kullanıcı tipi girin.") # hata mesajı vermek
            continue # ana menüye dönmek
        imlec.execute(f"SELECT * FROM kullanıcılar WHERE isim = '{isim}'") # database üzerinde kullanıcı adına göre arama yapmak
        sonuc = imlec.fetchone() # arama sonucunu almak
        if sonuc: # eğer arama sonucu varsa (kullanıcı adı zaten mevcutsa)
            print(f"{isim} adlı bir kullanıcı zaten var. Lütfen başka bir kullanıcı adı seçin.") # hata mesajı vermek
            continue # ana menüye dönmek
        else: # eğer arama sonucu yoksa (kullanıcı adı mevcut değilse)
            imlec.execute(f"INSERT INTO kullanıcılar VALUES (?, ?, ?)", (isim, sifre, tip)) # kullanıcıları tablosuna yeni kullanıcıyı eklemek
            baglanti.commit() # database üzerinde değişiklik yapmak
            print(f"{isim} adlı yeni bir kullanıcı oluşturuldu.") # başarı mesajı vermek

    elif secim == "3": # çıkış yapma seçeneği 

        print("Programdan çıkılıyor. İyi günler.") # çıkış mesajı vermek
        baglanti.close() # database bağlantısını kapatmak
        break # programdan çıkmak

    else: # geçersiz seçim

        print("Lütfen geçerli bir seçim yapın.") # geçersiz seçim mesajı vermek
