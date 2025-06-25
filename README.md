# 🩺 RSUD Konoha – Sistem Informasi Manajemen Rumah Sakit

Sistem informasi rumah sakit modern berbasis **Django** dan **DaisyUI/Tailwind CSS**.

---

## 🚀 Fitur Utama

- Login multi-peran: **Admin**, **Tenaga Medis**, **Pasien**
- Dashboard dinamis sesuai role
- Pendaftaran & manajemen pasien
- Reservasi Janji Temu
- Input & Rekam Medis
- Manajemen Inventaris (obat/alkes)
- Laporan PDF & export data
- Log Aktivitas Admin
- Pencarian & Filter Data
- Notifikasi Pop-up (Toast)
- Hamburger Sidebar Menu (Mobile & Desktop)
- AJAX validation: username unik, jadwal dokter, dll.
- Panduan Pengguna & Dokumentasi Admin

---

## 👤 **User Demo Siap Pakai**

| Peran        | Username  | Password     |
| ------------ | --------- | -----------  |
| Pasien       | pasien    | pasien123    |
| Tenaga Medis | staff     | staff123     |
| Admin        | admin     | admin123     |

> Semua user di atas sudah tersedia di database bawaan (`db.sqlite3`).

---

## ⚡️ **Cara Instalasi & Jalankan**

1. **Clone repo ini:**
    ```sh
    git clone https://github.com/awangsuryarmdhn/rsud-konoha.git
    cd rsud-konoha
    ```

2. **(Opsional) Aktifkan virtualenv:**
    ```sh
    python -m venv env
    # Untuk Mac/Linux:
    source env/bin/activate
    # Untuk Windows:
    env\Scripts\activate.bat
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Migrate DB & collectstatic:**
    ```sh
    python manage.py migrate
    python manage.py collectstatic
    ```

5. **Jalankan server:**
    ```sh
    python manage.py runserver
    ```

6. **Akses aplikasi:**
    - Aplikasi: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - Admin Django: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🖥️ Fitur Tampilan

- Sidebar Hamburger (klik tombol menu di pojok kiri navbar di semua device!)
- Dashboard otomatis sesuai peran user
- Notifikasi otomatis dengan Toastify
- Tampilan modern & responsive dengan DaisyUI + Tailwind CSS

---

## 📦 Catatan Teknis

- **Database:** SQLite (`db.sqlite3`) sudah termasuk untuk demo/testing
- **Staticfiles:** Sudah include agar tampilan langsung siap tanpa collect ulang
- **Export PDF:**  
  Fitur PDF butuh **wkhtmltopdf** di komputer  
  [Download di sini](https://wkhtmltopdf.org/downloads.html)
- **User Role:** Jika buat user baru lewat admin, pastikan field `peran` diisi!

---

MIT License © 2025 Awang Surya Ramadhan
