import unittest
import coverage
import test_faktöriyel
from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze
import pandas as pd
import pyodbc

def connect_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=DESKTOP-7QC1A0N;'
                          'DATABASE=Ben;'
                          'Trusted_Connection=yes;')
    return conn

def insert_file(file_name):
    connection = connect_db()
    cursor = connection.cursor()

    # Files tablosuna dosya adını ekle
    cursor.execute("INSERT INTO Files (file_name) VALUES (?)", (file_name,))
    connection.commit()

    # Son eklenen dosyanın id'sini almak için SCOPE_IDENTITY() kullan
    cursor.execute("SELECT SCOPE_IDENTITY()")
    file_id = cursor.fetchone()[0]  # Son eklenen ID
    connection.close()

    return file_id

def insert_metrics(file_id, metrics):
    connection = connect_db()
    cursor = connection.cursor()

    # Metrikleri Metrics tablosuna ekle
    cursor.execute("""
        INSERT INTO Metrics (file_id, difficulty, effort, volume, complexity, maintainability, 
                             loc, lloc, sloc, comments, blank, multiline_comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        file_id, metrics['Halstead Zorluk'], metrics['Halstead Çaba'], metrics['Halstead Hacim'],
        metrics['Çevrimsel Karmaşıklık'], metrics['Sürdürülebilirlik İndeksi'], metrics['LOC'],
        metrics['LLOC'], metrics['SLOC'], metrics['Yorumlar'], metrics['Boş Satırlar'],
        metrics['Çoklu Satırlar']
    ))
    connection.commit()
    connection.close()

def analiz_et(dosya_adi, kod):
    print(f"\n{dosya_adi} için analiz sonuçları:")

    halstead = h_visit(kod)
    print(f"Halstead Zorluk: {halstead[0].difficulty:.2f}")
    print(f"Halstead Çaba: {halstead[0].effort:.2f}")
    print(f"Halstead Hacim: {halstead[0].volume:.2f}")

    maintainability = mi_visit(kod, multi=False)
    print(f"Sürdürülebilirlik İndeksi: {maintainability:.2f}")

    complexity = cc_visit(kod)
    for c in complexity:
        print(f"Fonksiyon: {c.name}, Karmaşıklık: {c.complexity}")

    raw_metrics = analyze(kod)
    print(f"LOC (Line of Code): {raw_metrics.loc}")
    print(f"LLOC (Logical Lines of Code): {raw_metrics.lloc}")
    print(f"SLOC (Source Lines of Code): {raw_metrics.sloc}")
    print(f"Yorumlar: {raw_metrics.comments}")
    print(f"Boş Satırlar: {raw_metrics.blank}")

    # Çoklu Satırları Elle Kontrol Etme
    multiline_comments = kod.count('"""') + kod.count("'''")
    print(f"Çoklu Satırlar: {multiline_comments}")

    # Code Smell Kontrolleri
    print("\nCode Smell Tespit Edildi:")
    if halstead[0].difficulty > 10:
        print(f"  - {dosya_adi} dosyasında Yüksek Halstead Zorluğu (Önerilen: <= 10).")
    if sum(c.complexity for c in complexity) > 15:
        print(f"  - {dosya_adi} dosyasında Yüksek Çevrimsel Karmaşıklık (Önerilen: <= 15).")
    if maintainability < 20:
        print(f"  - {dosya_adi} dosyasında Düşük Sürdürülebilirlik (Önerilen: >= 20).")

def analiz_et_tablo(dosya_adi, kod):

    halstead = h_visit(kod)
    maintainability = mi_visit(kod, multi=False)
    complexity = cc_visit(kod)
    raw_metrics = analyze(kod)

    siklomatik_karmaşıklık = sum(c.complexity for c in complexity)

    multiline_comments = kod.count('"""') + kod.count("'''")

    metrics = {
        "Dosya": dosya_adi,
        "Halstead Zorluk": halstead[0].difficulty,
        "Halstead Çaba": halstead[0].effort,
        "Halstead Hacim": halstead[0].volume,
        "Çevrimsel Karmaşıklık": siklomatik_karmaşıklık,
        "Sürdürülebilirlik İndeksi": maintainability,
        "LOC": raw_metrics.loc,
        "LLOC": raw_metrics.lloc,
        "SLOC": raw_metrics.sloc,
        "Yorumlar": raw_metrics.comments,
        "Boş Satırlar": raw_metrics.blank,
        "Çoklu Satırlar": multiline_comments
    }

    file_id = insert_file(dosya_adi)  # Dosya adı veritabanına kaydedilir
    insert_metrics(file_id, metrics)  # Elde edilen metrikler veritabanına kaydedilir

    return metrics

if __name__ == "__main__":
    cov = coverage.Coverage()
    cov.start()

    suite = unittest.TestLoader().loadTestsFromModule(test_faktöriyel)
    unittest.TextTestRunner().run(suite)

    cov.stop()
    cov.report()
    cov.xml_report()
    cov.html_report(directory="htmlcov")

    with open("faktöriyel.py", "r", encoding="utf-8") as f:
        faktoriyel_code = f.read()

    with open("test_faktöriyel.py", "r", encoding="utf-8") as f:
        test_code = f.read()

    # Analizleri çalıştırma
    analiz_et("faktöriyel.py", faktoriyel_code)
    analiz_et("test_faktöriyel.py", test_code)

    faktoriyel_results = analiz_et_tablo("faktöriyel.py", faktoriyel_code)
    test_results = analiz_et_tablo("test_faktöriyel.py", test_code)

    df = pd.DataFrame([faktoriyel_results, test_results])
    df = df.rename(columns={
        "Dosya": "Dosya Adı",
        "Halstead Zorluk": "Zorluk",
        "Halstead Çaba": "Çaba",
        "Halstead Hacim": "Hacim",
        "Çevrimsel Karmaşıklık": "Karmaşıklık",
        "Sürdürülebilirlik İndeksi": "Sürdürülebilirlik",
        "LOC": "LOC",
        "LLOC": "LLOC",
        "SLOC": "SLOC",
        "Yorumlar": "Yorumlar",
        "Boş Satırlar": "Boş Satırlar",
        "Çoklu Satırlar": "Çoklu Satırlar"
    })
    print(df)