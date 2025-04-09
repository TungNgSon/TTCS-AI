import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

st.set_page_config(page_title="Grammar Correction App", layout="centered")
st.title("📝 Grammar Correction App")

# Load mô hình
@st.cache_resource
def load_model():
    model = T5ForConditionalGeneration.from_pretrained("vennify/t5-base-grammar-correction")
    tokenizer = T5Tokenizer.from_pretrained("vennify/t5-base-grammar-correction")
    return model, tokenizer

model, tokenizer = load_model()

# Giao diện nhập liệu
input_text = st.text_area("✍️ Nhập đoạn văn tiếng Anh bạn muốn sửa ngữ pháp:", height=150)

if st.button("🔧 Sửa ngữ pháp"):
    if not input_text.strip():
        st.warning("Vui lòng nhập một đoạn văn bản trước khi nhấn sửa.")
    else:
        input_text = "grammar: " + input_text

        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
        corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        st.success("✅ Đoạn văn đã được sửa:")
        st.write(corrected_text)
