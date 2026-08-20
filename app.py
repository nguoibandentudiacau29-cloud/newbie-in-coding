import streamlit as st
from google import genai
from PIL import Image

# Cấu hình giao diện trang web
st.set_page_config(page_title="Trợ Lý AI Dạng Web", page_icon="🤖")
st.title("🤖 Trợ Lý AI (Hỗ trợ Nhắn tin & Gửi ảnh)")

# =========================================================
# DÁN GEMINI API KEY CỦA BẠN VÀO ĐÂY:
GEMINI_API_KEY = "AQ.Ab8RN6Kaf-Z43lszppjS4Qxv6rAqMZWbZLVNh8L0mZfojNp8oA"
# =========================================================

# Khởi tạo Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Khởi tạo lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị thanh tải ảnh ở cột bên trái (Sidebar)
st.sidebar.header("📸 Tải ảnh lên")
uploaded_file = st.sidebar.file_uploader("Chọn 1 bức ảnh...", type=["jpg", "jpeg", "png"])

image_input = None
if uploaded_file is not None:
    image_input = Image.open(uploaded_file)
    st.sidebar.image(image_input, caption="Ảnh đã chọn", use_container_width=True)

# Hiển thị lại các tin nhắn cũ trong khung chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Ô nhập tin nhắn từ người dùng
if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu xử lý ảnh..."):
    # Lưu và hiển thị câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Chuẩn bị nội dung gửi cho AI (Ảnh + Chữ)
    contents_to_send = []
    if image_input is not None:
        contents_to_send.append(image_input)
    contents_to_send.append(prompt)

    # Gọi Gemini AI trả lời
    with st.chat_message("assistant"):
        with st.spinner("AI đang phân tích và suy nghĩ..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents_to_send
                )
                reply = response.text if response.text else "Không có phản hồi từ AI."
            except Exception as e:
                reply = f"Lỗi AI: {e}"
            
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})