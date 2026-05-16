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
    
    # 4. pdfplumber ile PDF'i açıp içindeki tabloyu okuyoruz
    with pdfplumber.open(pdf_yolu) as pdf:
        sayfa = pdf.pages[0]           # İlk sayfayı al
        tablo = sayfa.extract_table()  # Tabloyu çıkart
        
    # 5. Eğer PDF içinde tablo bulduysak, pandas ile bunu Excel'e çeviriyoruz
    if tablo:
        df = pd.DataFrame(tablo[1:], columns=tablo[0])  # İlk satır başlıklar (columns), kalanı veri
        df.to_excel(excel_yolu, index=False)
    else:
        return "Bu PDF'in içinde okunabilir bir tablo bulunamadı."
        
    # 6. Son adım: Oluşan Excel dosyasını tarayıcıdan kullanıcıya indirtiyoruz
    return send_file(excel_yolu, as_attachment=True, download_name="donusturulmus_tablo.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
