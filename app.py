import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import pytz
import json
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

# --- Google Sheets API setup ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from secrets
service_account_info = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Get sheet key from secrets
sheet_key = st.secrets["sheets"]["sheet_key"]

# Load worksheets
orders_sheet = client.open_by_key(sheet_key).worksheet("Orders")
results_sheet = client.open_by_key(sheet_key).worksheet("PullResults")

# Read orders into DataFrame
data = orders_sheet.get_all_records()
df = pd.DataFrame(data)

# ✅ Filter only for 'Gacha with Irene'
df = df[df["Item"] == "Gacha with Irene"]

# Set timezone ke Asia/Jakarta
tz = pytz.timezone("Asia/Jakarta")
today = datetime.now(tz).date()

# Parse kolom Date dan filter hanya yang tanggalnya adalah hari ini
df["DateParsed"] = pd.to_datetime(df["Date"], errors='coerce')  # handle format yang invalid
df = df[df["DateParsed"].dt.date == today]

st.title("🎲 Untuk Admin Lis Input Hasil Pull - Gacha")

# Select customer name
customer_names = df["Name"].unique().tolist()
selected_customer = st.selectbox("Pilih Nama Customer", customer_names)

# Get all orders for selected customer
cust_orders = df[df["Name"] == selected_customer]

# Show available dates for this customer
available_dates = cust_orders["Date"].unique().tolist()

if available_dates:
    selected_date = st.selectbox("Pilih Tanggal Transaksi", available_dates)
    match_row = cust_orders[cust_orders["Date"] == selected_date]

    if not match_row.empty:
        cust_row = match_row.iloc[0]

        # Clean quantity from Discount column (remove 'pcs' etc.)
        qty_str = str(cust_row["Discount"])
        qty_clean = ''.join(filter(str.isdigit, qty_str))
        qty = int(qty_clean) if qty_clean else 0

        whatsapp = cust_row.get("WhatsApp", "")
        address = cust_row.get("Alamat lengkap", "")

        st.info(f"{selected_customer} memesan **{qty} pcs** pada **{selected_date}**.")

        # ✅ Simplified single-choice options (no dice categories)
        product_options = [
            "pin",
            "tcg genshin",
            "2 pcs tcg pokemon",
            "Nendo bebas",
            "Nendo pilihan Lis",
            "Blokees",
            "boneka jamur",
            "price figure",
        ]

        selections = []

        st.markdown("### 🎁 Input Hadiah Berdasarkan Hasil Pull")
        for i in range(qty):
            st.markdown(f"#### Pull {i+1}")
            choice = st.selectbox(
                f"Hadiah {i+1}",
                product_options,
                key=f"product_{i}"
            )
            selections.append(f"- {choice}")

        if st.button("Submit Pull Results"):
            timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M")

            # Keep sheet structure: fill both text columns with the same selections
            product_text = "\n".join(selections)
            #pull_text = product_text

            results_sheet.append_row([
                timestamp,
                selected_customer,
                selected_date,
                qty,
                #pull_text,     # previously: dice category list → now same as product list
                product_text,  # product selections (single dropdown per pull)
                whatsapp,
                address,
            ])

            st.success("✅ Data hasil pull berhasil dicatat di sheet 'PullResults'.")

    else:
        st.warning("Tidak ditemukan data transaksi untuk tanggal tersebut.")
else:
    st.warning("Belum ada transaksi 'Gacha with Irene' hari ini yang terdeteksi. Jika ini tidak benar, refresh halaman ini")
