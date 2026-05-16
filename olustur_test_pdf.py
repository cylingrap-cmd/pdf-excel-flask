from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

doc = SimpleDocTemplate("test_tablo.pdf", pagesize=A4)

veri = [
    ["İsim", "Yaş", "Şehir", "Maaş"],
    ["Ahmet", "25", "İstanbul", "15000"],
    ["Ayşe", "30", "Ankara", "18000"],
    ["Mehmet", "28", "İzmir", "12000"],
    ["Fatma", "35", "Bursa", "20000"],
]

tablo = Table(veri)
tablo.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
]))

doc.build([tablo])
print("PDF oluşturuldu: test_tablo.pdf")