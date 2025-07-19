import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import pytz
import json

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

# Filter only for 'dice with irene'
df = df[df["Item"] == "dice with irene"]

st.title("🎲 Input Hasil Pull - Dice with Irene")

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

        st.info(f"{selected_customer} memesan **{qty} pcs** pada **{selected_date}**.")

        # Define dropdown choices
        pull_choices = {
            "beda semua": ["Keychain Genshin/HSR", "Nendoroid More Parts/Face", "Blokees Starlight/Defender"],
            "2 sama": ["Badge", "Booster Genshin", "2 pcs Booster Pokemon"],
            "3 sama": ["mousepad"],
            "straight": ["2 pcs Keychain Genshin/HSR", "2pcs Nendoroid More Parts/Face", "2pcs Blokees Starlight/Defender"],
            "2 x 2 sama": ["Teyvat Zoo", "Teyvat Paradasie", "Coin Pouch Collei"],
            "4 sama": ["nendo"]
        }

        pull_results = []
        product_results = []

        st.markdown("### 🎁 Input Hadiah Berdasarkan Hasil Pull")

        for i in range(qty):
            st.markdown(f"#### Pull {i+1}")
            col1, col2 = st.columns(2)

            with col1:
                pull = st.selectbox(f"Hasil Pull {i+1}", list(pull_choices.keys()), key=f"pull_{i}")
            with col2:
                product = st.selectbox(f"Hadiah {i+1}", pull_choices[pull], key=f"product_{i}")

            pull_results.append(f"- {pull}")
            product_results.append(f"- {product}")

        if st.button("Submit Pull Results"):
            tz = pytz.timezone("Asia/Jakarta")
            timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M")

            pull_text = "\n".join(pull_results)
            product_text = "\n".join(product_results)

            results_sheet.append_row([
                timestamp,
                selected_customer,
                selected_date,
                qty,
                pull_text,
                product_text
            ])

            st.success("✅ Data hasil pull berhasil dicatat di sheet 'PullResults'.")

    else:
        st.warning("Tidak ditemukan data transaksi untuk tanggal tersebut.")
else:
    st.warning("Customer ini belum punya transaksi 'dice with irene'.")
