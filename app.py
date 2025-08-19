import streamlit as st
import qrcode
import uuid
from io import BytesIO

# ------------------------
# Generate QR Code
# ------------------------
def generate_qr(unique_id):
    base_url = "https://walk-in.streamlit.app"  # ✅ Your deployed Streamlit app URL
    url = url = f"{base_url}/?page=upload&uid={unique_id}"

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), url

# ------------------------
# Streamlit App
# ------------------------
st.set_page_config(page_title="Interview Portal", layout="centered")
st.title("Interview Portal")

query_params = st.query_params
page = query_params.get("page", ["home"])[0]

if page == "home":
    st.header("Choose Interview Type")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Walk-in Interview"):
            unique_id = str(uuid.uuid4())
            qr_image, qr_url = generate_qr(unique_id)
            st.image(qr_image, caption="Scan this QR to fill the form")
            st.markdown(f"Or click here to fill the form", unsafe_allow_html=True)
            st.download_button(
                label="Download QR Code",
                data=qr_image,
                file_name="upload_qr.png",
                mime="image/png"
            )

    with col2:
        if st.button("Pre-Planned Interview"):
            st.info("Pre-planned interview booking system coming soon!")

elif page == "upload":
    st.header("Candidate Information Form")
    uid = query_params.get("uid", [""])[0]

    with st.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not name or not email or not phone or not resume:
            st.warning("Please fill in all fields and upload your resume.")
        else:
            st.success("✅ Thank you for submitting your details!")
            st.write("We have received your information.")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Phone:** {phone}")

