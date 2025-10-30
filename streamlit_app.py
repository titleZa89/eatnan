import streamlit as st
import pandas as pd
from PIL import Image
import os
import glob
import re
import pdfplumber

# =====================================
# 🔹 ฟังก์ชันโหลดข้อมูลจาก CSV หรือ PDF
# =====================================
def load_data(data_dir="data"):
    """โหลดข้อมูลจาก CSV หรือ PDF ภายในโฟลเดอร์ data/
    คืนค่าเป็น DataFrame ที่มีคอลัมน์: name, province, ingredients, description, image_path
    """
    if not os.path.exists(data_dir):
        return pd.DataFrame(columns=["name", "province", "ingredients", "description", "image_path"])

    # ✅ 1. ถ้าเจอไฟล์ CSV
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if csv_files:
        try:
            return pd.read_csv(csv_files[0])
        except Exception:
            pass

    # ✅ 2. ถ้าเจอไฟล์ PDF
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    if pdf_files:
        pdf_path = pdf_files[0]
        records = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                    for line in text.split("\n"):
                        # 🔸 ปรับรูปแบบนี้ให้ตรงกับไฟล์ PDF ของคุณ
                        # ตัวอย่าง: "ต้มยำกุ้ง - กรุงเทพฯ - กุ้ง ตะไคร้ ใบมะกรูด - อาหารไทยรสจัดจ้าน"
                        parts = [p.strip() for p in line.split(" - ")]
                        if len(parts) >= 4:
                            records.append({
                                "name": parts[0],
                                "province": parts[1],
                                "ingredients": parts[2],
                                "description": parts[3],
                                "image_path": ""
                            })
            if records:
                return pd.DataFrame(records)
        except Exception as e:
            st.error(f"ไม่สามารถอ่าน PDF ได้: {e}")

    # ✅ 3. ถ้าเจอ index.txt
    index_path = os.path.join(data_dir, "index.txt")
    if os.path.exists(index_path):
        records = []
        with open(index_path, "r", encoding="utf-8") as f:
            for line in f:
                path = line.strip()
                if not path:
                    continue
                filename = os.path.basename(path)
                name_no_ext = os.path.splitext(filename)[0]
                parts = name_no_ext.split("_")
                if len(parts) >= 3 and re.match(r"^\d+", parts[0]):
                    if re.match(r"^\d{8,}$", parts[-1]):
                        name_parts = parts[1:-1]
                    else:
                        name_parts = parts[1:]
                else:
                    name_parts = parts
                name = " ".join(name_parts).replace("-", " ")
                records.append({
                    "name": name,
                    "province": "Unknown",
                    "ingredients": "",
                    "description": "",
                    "image_path": "",
                })
        return pd.DataFrame(records)

    # ✅ 4. ถ้าไม่พบอะไรเลย
    return pd.DataFrame(columns=["name", "province", "ingredients", "description", "image_path"])


# =====================================
# 🔹 เริ่มต้นแอป Streamlit
# =====================================
st.set_page_config(page_title="อาหารพื้นถิ่นไทย", page_icon="🍲", layout="wide")
st.title("อาหารพื้นถิ่นไทย 🍲")

data = load_data("data")

if data.empty:
    st.warning("⚠️ ไม่พบข้อมูล กรุณาเพิ่มไฟล์ CSV หรือ PDF ในโฟลเดอร์ `data/`")
    st.stop()

# ตรวจสอบว่ามีคอลัมน์ province ไหม
if "province" not in data.columns:
    data["province"] = "Unknown"

# =====================================
# 🔹 ส่วนเลือกจังหวัด
# =====================================
province = st.selectbox(
    "เลือกจังหวัด",
    ["ทั้งหมด"] + sorted(data["province"].dropna().unique())
)

# =====================================
# 🔹 กรองข้อมูล
# =====================================
if province != "ทั้งหมด":
    filtered_data = data[data["province"] == province]
else:
    filtered_data = data

# =====================================
# 🔹 แสดงผลข้อมูล
# =====================================
if filtered_data.empty:
    st.info("ไม่พบข้อมูลในจังหวัดที่เลือก")
else:
    for _, row in filtered_data.iterrows():
        with st.container():
            st.subheader(row.get("name", "ชื่อไม่ระบุ"))
            st.write(f"📍 จังหวัด: {row.get('province', 'ไม่ระบุ')}")
            if row.get("ingredients"):
                st.write(f"🥗 ส่วนผสม: {row.get('ingredients', '')}")
            if row.get("description"):
                st.write(f"📝 {row.get('description', '')}")

            # แสดงรูปภาพถ้ามี
            img_path = row.get("image_path", "")
            if isinstance(img_path, str) and os.path.exists(img_path):

                try:
                    image = Image.open(img_path)
                    st.image(image, use_column_width=True)
                except Exception:
                    st.write("ไม่สามารถแสดงรูปภาพได้ ❌")

            st.markdown("---")
