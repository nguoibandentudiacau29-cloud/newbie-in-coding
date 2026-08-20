import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Trợ Lý AI", page_icon="⚡")
st.title("⚡ Trợ Lý AI (Siêu Tốc)")

# 1. Khởi tạo Client bằng API Key từ Secrets hoặc biến cố định
# Cách 1: Lấy từ Secrets của Streamlit (Khuyên dùng khi đưa lên Cloud)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Cách 2: Nếu chạy ở máy local hoặc chưa điền Secrets, điền trực tiếp key vào đây
    api_key = "AQ.Ab8RN6KB1BiiHRZVxfC71zpApni_aQEUU3tpRwLNMaZqwsvSQw"

@st.cache_resource
def get_client(key):
    # Truyền rõ tham số api_key=key để tránh lỗi 401 UNAUTHENTICATED
    return genai.Client(api_key=key)

client = get_client(api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Khung tải ảnh ở Sidebar
st.sidebar.header("📸 Tải ảnh lên")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh...", type=["jpg", "jpeg", "png"])

image_input = None
if uploaded_file is not None:
    # Nén nhỏ kích thước ảnh để gửi đi cực nhanh
    img = Image.open(uploaded_file)
    img.thumbnail((800, 800))
    image_input = img
    st.sidebar.image(image_input, caption="Ảnh đã chọn", use_container_width=True)

# 3. Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Ô nhập tin nhắn và xử lý phản hồi
if prompt := st.chat_input("Nhập câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    contents_to_send = []
    if image_input is not None:
        contents_to_send.append(image_input)
    contents_to_send.append(prompt)

    with st.chat_message("assistant"):
        def stream_generator():
            try:
                response = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=contents_to_send,
                    config={
                        "max_output_tokens": 300,
                        "system_instruction": "Trả lời cực kỳ ngắn gọn, tối đa 2-3 câu, đi thẳng vào đáp án."
                    }
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                yield f"Lỗi AI: {e}"

        full_response = st.write_stream(stream_generator())
        st.session_state.messages.append({"role": "assistant", "content": full_response})