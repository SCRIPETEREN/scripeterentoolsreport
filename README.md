# SCRIPETEREN TOOLS REPORT

Report ke 500+ layanan (sosmed, e-commerce, bank, pemerintah, internasional) dalam satu tools terminal interaktif.  
**Hanya untuk edukasi dan testing akun sendiri.**

## Perubahan Utama (Versi OAuth 2.0)
- **Tanpa App Password** – menggunakan Gmail API dengan autentikasi OAuth 2.0.
- **Login sekali** via browser, token disimpan untuk penggunaan selanjutnya.
- **Lebih aman** – tidak ada penyimpanan kata sandi di kode.

---

## 1. Persiapan Akun Google & Gmail API

### a. Buat Project di Google Cloud Console
1. Buka [Google Cloud Console](https://console.cloud.google.com).
2. Buat project baru atau pilih project yang sudah ada.
3. Pastikan Anda login dengan akun Gmail yang akan digunakan sebagai pengirim laporan.

### b. Aktifkan Gmail API
1. Di menu sebelah kiri, pilih **APIs & Services** > **Library**.
2. Cari "Gmail API", lalu klik dan aktifkan (Enable).

### c. Buat Kredensial OAuth 2.0
1. Masuk ke **APIs & Services** > **Credentials**.
2. Klik **+ CREATE CREDENTIALS** > pilih **OAuth client ID**.
3. Untuk **Application type**, pilih **Desktop app**.
4. Beri nama (misal: `report-tools`), lalu klik **Create**.
5. Setelah selesai, klik ikon download (↓) untuk mengunduh file JSON.
6. **Ganti nama file tersebut menjadi `credentials.json`** dan letakkan di folder yang sama dengan `main.py`.

### d. (Opsional) Tambahkan Test User
Jika tools hanya untuk penggunaan pribadi, Anda tidak perlu menambahkan pengguna uji. Saat pertama login, Google akan menampilkan peringatan "app tidak terverifikasi" – cukup klik **Advanced** > **Go to ... (unsafe)** untuk melanjutkan.

---

## 2. Instalasi & Dependensi

### a. Clone repositori (atau buat folder baru)
```bash
git clone https://github.com/SCRIPETERENTOOLS/report.git
cd scripteterentoolsreport

python -m venv venv
source venv/bin/activate   # Linux/Mac
# atau
venv\Scripts\activate      # Windows

pip install -r requirements.txt

python main.py

