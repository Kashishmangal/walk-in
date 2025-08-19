import streamlit as st
import qrcode
import uuid
import os
from io import BytesIO
import base64
import re
from PyPDF2 import PdfReader
import docx

# ------------------------
# Function to extract text from PDF
# ------------------------
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# ------------------------
# Function to extract text from DOCX
# ------------------------
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# ------------------------
# Function to auto extract details
# ------------------------
def extract_details(text):
    details = {"Name": "Not Found", "Email": "Not Found", "Phone": "Not Found"}
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"
    phone_pattern = r"\+?\d[\d\s-]{8,15}"

    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)

    if email:
        details["Email"] = email.group()
    if phone:
        details["Phone"] = phone.group()

    first_line = text.split("\n")[0]
    name_guess = " ".join(first_line.split()[:2])
    details["Name"] = name_guess

    return details

# ------------------------
# Generate QR Code
# ------------------------
def generate_qr(unique_id):
    qr = qrcode.QRCode(box_size=10, border=4)
    url = f"http://localhost:8501/?page=upload&uid={unique_id}"
  # fixed &amp;
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im, url

# ------------------------
# Streamlit App
# ------------------------
st.title("Interview Portal")

# ✅ Updated to use st.query_params
query_params = st.query_params
page = query_params.get("page", ["home"])[0]

if page == "home":
    st.header("Choose Interview Type")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Walk-in Interview"):
            unique_id = str(uuid.uuid4())
            qr_image, qr_url = generate_qr(unique_id)
            st.image(qr_image, caption="Scan this QR to upload CV")
            st.write(f"Or click here: Upload CV Page")

    with col2:
        if st.button("Pre-Planned Interview"):
            st.success("Pre-planned interview booking system coming soon!")

elif page == "upload":
    st.header("Upload Your CV")
    uid = query_params.get("uid", [""])[0]
    uploaded_file = st.file_uploader("Upload CV (PDF/DOCX)", type=["pdf", "docx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

        details = extract_details(text)

        st.subheader("Extracted Details")
        st.write(f"**Name:** {details['Name']}")
        st.write(f"**Email:** {details['Email']}")
        st.write(f"**Phone:** {details['Phone']}")
