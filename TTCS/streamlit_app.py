import streamlit as st
import whisper
from transformers import pipeline

# Load mô hình
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")
    grammar_corrector = pipeline("text2text-generation", model="vennify/t5-base-grammar-correction")
    return whisper_model, grammar_corrector

whisper_model, grammar_corrector = load_models()

st.title("🎤 Chatbot chỉnh ngữ pháp từ âm thanh hoặc văn bản")

# Chọn chế độ
option = st.selectbox("Bạn muốn làm gì?", ["🎧 Upload file âm thanh", "✍️ Nhập văn bản"])

if option == "🎧 Upload file âm thanh":
    uploaded_file = st.file_uploader("Tải lên file âm thanh (.wav hoặc .mp3)", type=["wav", "mp3"])
    if uploaded_file is not None:
        with open("temp.wav", "wb") as f:
            f.write(uploaded_file.read())
        with st.spinner("🔍 Đang nhận diện giọng nói..."):
            result = whisper_model.transcribe("temp.wav")
            transcribed_text = result["text"]
            st.text_area("📝 Văn bản nhận diện được:", transcribed_text, height=100)
        with st.spinner("🛠️ Đang chỉnh ngữ pháp..."):
            corrected = grammar_corrector("grammar: " + transcribed_text)[0]["generated_text"]
            st.text_area("✅ Văn bản sau khi chỉnh:", corrected, height=100)

elif option == "✍️ Nhập văn bản":
    user_input = st.text_area("Nhập câu bạn muốn chỉnh ngữ pháp:", height=100)
    if st.button("🛠️ Chỉnh ngữ pháp"):
        if user_input.strip() == "":
            st.warning("⚠️ Vui lòng nhập văn bản.")
        else:
            with st.spinner("🛠️ Đang chỉnh ngữ pháp..."):
                corrected = grammar_corrector("grammar: " + user_input)[0]["generated_text"]
                st.text_area("✅ Văn bản sau khi chỉnh:", corrected, height=100)
