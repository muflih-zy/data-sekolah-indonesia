from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Baca file Excel dengan daftar NPSN
df = pd.read_excel('npsn.xlsx')  # Ganti 'npsn.xlsx' dengan nama file Anda

# Inisialisasi driver browser
driver = webdriver.Chrome()  # Ganti dengan driver browser yang Anda unduh

# Membuat list kosong untuk menyimpan hasil pencairan
hasil_pencairan = []

# Loop melalui setiap NPSN dan lakukan pencarian
for npsn in df['npsn']:
    url = f"https://referensi.data.kemdikbud.go.id/tabs.php?npsn={npsn}"
    driver.get(url)
    
    # Mengambil konten halaman web
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Mengekstrak data dari tabel
    table = soup.find('table')
    rows = table.find_all('tr')
    
    school_data = {}
    
    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 4:
            label = columns[1].text.strip()
            value = columns[3].text.strip()
            school_data[label] = value
    
    # Simpan hasil pencairan ke dalam list
    data = {
        'npsn': npsn,
        'Nama': school_data.get('Nama', ''),
        'Status Sekolah': school_data.get('Status Sekolah', ''),
        'Bentuk Pendidikan': school_data.get('Bentuk Pendidikan', ''),
        'Alamat': school_data.get('Alamat', ''),
        'Propinsi/Luar Negeri (LN)': school_data.get('Propinsi/Luar Negeri (LN)', ''),
        'Kab.-Kota/Negara (LN)': school_data.get('Kab.-Kota/Negara (LN)', ''),
        'Kecamatan/Kota (LN)': school_data.get('Kecamatan/Kota (LN)', ''),
        'Desa/Kelurahan': school_data.get('Desa/Kelurahan', ''),            
    }
    
    hasil_pencairan.append(data)

# Tutup browser setelah selesai
driver.quit()

# Buat DataFrame dari list hasil pencairan
hasil_df = pd.DataFrame(hasil_pencairan)

# Simpan hasil pencairan ke file Excel baru
hasil_df.to_excel('hasil_pencairan.xlsx', index=False)
