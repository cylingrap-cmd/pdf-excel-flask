from flask import Flask, render_template, request, send_file
import os
import pdfplumber
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/donustur', methods=['POST'])
def donustur():
    # 1. Kullanıcının HTML formundan gönderdiği dosyayı alıyoruz
    dosya = request.files['pdf_dosya']
    
    # Eğer dosya seçilmemişse uyarı verelim
    if dosya.filename == '':
        return "Lütfen bir PDF dosyası seçin!"
        
    # 2. Gelen PDF dosyasını geçici olarak "uploads" klasörüne kaydediyoruz
    pdf_yolu = os.path.join(UPLOAD_FOLDER, dosya.filename)
    dosya.save(pdf_yolu)
    
    # 3. Çıktı olarak vereceğimiz Excel dosyasının adını ve yerini belirliyoruz
    excel_yolu = os.path.join(UPLOAD_FOLDER, "sonuc.xlsx")
    
    # 4. Çok Sayfalı PDF Desteği: Tüm sayfaları gezip tabloları birleştireceğiz
    tum_satirlar = []
    basliklar = None

    with pdfplumber.open(pdf_yolu) as pdf:
        for sayfa in pdf.pages:
            tablo = sayfa.extract_table()
            if not tablo:
                continue # Bu sayfada tablo yoksa diğer sayfaya geç
                
            # İlk sayfada başlıkları belirliyoruz
            if basliklar is None:
                basliklar = [str(h).replace('\n', ' ').strip() if h is not None else "" for h in tablo[0]]
                baslangic_index = 1 # İlk satırı başlık yaptık, veriye 2. satırdan başla
            else:
                # Diğer sayfalarda PDF bazen başlığı tekrar yazar, aynıysa onu atlıyoruz
                ilk_satir = [str(h).replace('\n', ' ').strip() if h is not None else "" for h in tablo[0]]
                if ilk_satir == basliklar:
                    baslangic_index = 1
                else:
                    baslangic_index = 0
            
            # Verileri satır satır temizleyip genel listeye ekliyoruz
            for satir in tablo[baslangic_index:]:
                temiz_satir = [str(h).replace('\n', ' ').strip() if h is not None else "" for h in satir]
                
                # Sadece tamamen boş olmayan ve sütun sayısı başlıkla eşleşen satırları al (temiz çıktı)
                if any(temiz_satir) and len(temiz_satir) == len(basliklar):
                    tum_satirlar.append(temiz_satir)

    # 5. Pandas ile birleştirilmiş veriyi Excel'e çeviriyoruz
    if basliklar and tum_satirlar:
        df = pd.DataFrame(tum_satirlar, columns=basliklar)
        df.to_excel(excel_yolu, index=False)
    else:
        return "Bu PDF'in içinde okunabilir bir tablo bulunamadı."
        
    # 6. Son adım: Oluşan Excel dosyasını tarayıcıdan kullanıcıya indirtiyoruz
    return send_file(excel_yolu, as_attachment=True, download_name="donusturulmus_tablo.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
