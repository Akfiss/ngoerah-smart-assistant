import requests
from bs4 import BeautifulSoup
import os
import time

# ==========================================
# --- KONFIGURASI (WAJIB DIISI) ---
# ==========================================

# 1. Buka Chrome -> Buka Panduan SIMETRISS -> Tekan F12 (Inspect) -> Tab 'Network'
# 2. Refresh halaman. Klik satu request (biasanya yang paling atas/nama file html).
# 3. Di sebelah kanan, cari 'Request Headers'. Copy isi 'Cookie' dan 'User-Agent'.

COOKIES_DATA = "_ga=GA1.1.1230653024.1767767010; isDarkTheme=false; cf_clearance=e2AXFWn7KyToprH6NW1p_rCX7DAUmX92trGDzY_CzIo-1767767261-1.2.1.1-3aaNcJdp5y9fKY91VQSHdzet61286mdzS51cCVrEufLWSo345Zda19pbWB5Z_OGmt_kXtWhCaj0YvLuEAJTmQue6YWo.bTWPzDdwBiFtMyz4lIzLiymZeAt.k_z3EgJi7Emba3VFB79F3lrl8iaLRu2Jtk7Wx23DmXC.EKfDkK3Nk6mx4HP4Kw8T1vbD_qpQ2fU__jLMeUn6j.MNe6wRDegUa4rc2mIW8rSyPsLdbXA; _ga_3CVT71VNPZ=GS2.1.s1767785655$o2$g1$t1767786190$j59$l0$h0"

USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"

# URL halaman depan atau daftar isi
BASE_URL = "https://panduansimetriss.rsupsanglah.com" 

# Daftar URL spesifik yang mau diambil (Bisa ditambah manual)
# Tips: Ambil 3-5 URL dulu buat test
TARGET_URLS = [
    "https://panduansimetriss.rsupsanglah.com/simetriss/welcome-to-simetriss-docs",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/mengatur-jadwal-dokter",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/registrasi",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/registrasi-rawat-darurat",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/reservasi-registrasi-ranap",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/ubah-data-sosial-pasien",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/registrasi-keluar",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/registrasi-mutasi-kamar-rawat",
    "https://panduansimetriss.rsupsanglah.com/simetriss/petugas-rm/cara-mengubah-poliklinik"
    # Tambahkan link lain di sini...
]

# Folder tempat simpan hasil
OUTPUT_FOLDER = "D:\Magang Kemanker\chatbot-ngoerah\panduan-simetriss"

# ==========================================

def get_headers():
    return {
        'User-Agent': USER_AGENT,
        'Cookie': COOKIES_DATA
    }

def clean_text(text):
    """Membersihkan spasi berlebih dan enter kosong"""
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def scrape_page(url):
    print(f"sedang mengambil: {url} ...")
    
    try:
        response = requests.get(url, headers=get_headers())
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # --- BAGIAN PENTING: SELECTOR ---
            # Kita harus cari tag HTML mana yang berisi artikel.
            # Biasanya ada di <main>, <article>, atau div class="content"
            # Bestie coba menebak standar Docusaurus/Docs site:
            
            content = soup.find('main') or soup.find('article') or soup.find('div', class_='markdown')
            
            if content:
                # Ambil Judul
                title = soup.find('h1')
                title_text = title.text.strip() if title else "no_title"
                
                # Ambil Teks Bersih
                raw_text = content.get_text(separator='\n')
                clean_content = clean_text(raw_text)
                
                # Simpan ke File
                filename = title_text.replace(" ", "_").replace("/", "-").lower() + ".txt"
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Source: {url}\n\n")
                    f.write(clean_content)
                
                print(f"✅ Sukses! Disimpan di: {filepath}")
            else:
                print("⚠️  Gagal menemukan konten utama (Cek struktur HTML).")
        
        elif response.status_code == 403:
            print("⛔ Akses Ditolak (403). Cookie mungkin kadaluarsa atau salah copy.")
        else:
            print(f"❌ Error: Status Code {response.status_code}")
            
    except Exception as e:
        print(f"🔥 Error script: {e}")

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    for url in TARGET_URLS:
        scrape_page(url)
        # Jeda 2 detik biar server RS gak marah (Rate Limiting)
        time.sleep(2) 

if __name__ == "__main__":
    main()