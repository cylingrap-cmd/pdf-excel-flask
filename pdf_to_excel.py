import pdfplumber
import pandas as pd

with pdfplumber.open("test_tablo.pdf") as pdf:
    sayfa = pdf.pages[0]
    tablo = sayfa.extract_table()

df = pd.DataFrame(tablo[1:], columns=tablo[0])
df.to_excel("sonuc.xlsx", index=False)
print("Dönüştürme tamamlandı: sonuc.xlsx")