# 🎲 Pull Result - Dice with Irene

**⚠️ INTERNAL USE ONLY**
Aplikasi ini dibuat khusus untuk tim internal Lichtschein Hobby Store dalam mencatat hasil pull dari event *"Dice with Irene"* secara otomatis ke Google Sheets.

## 🧩 Fitur Utama

* **Filter otomatis** untuk pesanan dengan item “dice with irene”.
* **Dropdown dinamis** berdasarkan jumlah unit yang dipesan.
* **Pemilihan hasil pull & hadiah** dengan dependensi antar pilihan.
* **Pilihan nama dan tanggal transaksi** langsung dari data pesanan.
* **Auto-submit** ke sheet `PullResults`, dilengkapi:

  * Nama
  * Tanggal
  * Jumlah unit
  * Rangkuman hasil pull
  * Rangkuman hadiah
  * Nomor WhatsApp
  * Alamat lengkap

## 📁 Output di Google Sheets (`PullResults`)

| Timestamp        | Name    | Date       | Qty | Pull Results | Product Results | WhatsApp | Alamat Lengkap   |
| ---------------- | ------- | ---------- | --- | ------------ | --------------- | -------- | ---------------- |
| 2025-07-19 12:45 | john doe | 2025-07-18 | 3   | - 2 sama ... | - Booster ...   | 081xxxxx | Jl. ABC, Jakarta |

## 🛠️ Dependensi

* `streamlit`
* `gspread`
* `oauth2client`
* `pandas`
* `pytz`

---

💡 *Aplikasi ini tidak diperuntukkan bagi publik. Hanya digunakan oleh staff Lichtschein dalam operasional backend event pull reward.*
