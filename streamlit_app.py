import streamlit as st
import pandas as pd
from PIL import Image

# โหลดข้อมูล
data = pd.read_csv("data/local_food.csv")

st.title("อาหารพื้นถิ่นไทย 🍲")

# สร้าง selectbox ให้เลือกจังหวัด
province = st.selectbox("เลือกจังหวัด", ["ทั้งหมด"] + sorted(data["province"].unique()))

# กรองข้อมูล
if province != "ทั้งหมด":
    filtered_data = data[data["province"] == province]
else:
    filtered_data = data

# แสดงข้อมูลอาหาร
for _, row in filtered_data.iterrows():
    st.header(row["name"])
    st.write(f"จังหวัด: {row['province']}")
    st.write(f"ส่วนผสม: {row['ingredients']}")
    st.write(row["description"])
    
    # แสดงรูป
    try:
        image = Image.open(row["image_path"])
        st.image(image, use_column_width=True)
    except:
        st.write("ไม่พบรูปภาพ")
