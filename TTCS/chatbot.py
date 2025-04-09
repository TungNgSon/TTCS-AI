import streamlit as st
import pyaudio
import wave
import whisper
from happytransformer import HappyTextToText, TTSettings


# ---------------------------
# Cấu hình
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILENAME = "recorded_audio.wav"

# Load mô hình
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")  # hoặc "tiny" nếu muốn nhẹ
    happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
    return whisper_model, happy_tt

whisper_model, happy_tt = load_models()
t5_args = TTSettings(num_beams=5, min_length=1)

# Ghi âm
def record_audio(filename):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Nhận diện giọng nói
def transcribe_audio(filename):
    result = whisper_model.transcribe(filename)
    return result["text"]

# Sửa ngữ pháp
def correct_grammar(text):
    result = happy_tt.generate_text("grammar: " + text, args=t5_args)
    return result.text

# ---------------------------
# Giao diện Streamlit
st.title("🎤 Chatbot chỉnh ngữ pháp từ giọng nói")

if st.button("🎙️ Ghi âm và xử lý"):
    with st.spinner("Đang ghi âm..."):
        record_audio(OUTPUT_FILENAME)
        st.success("Đã ghi âm xong!")

    with st.spinner("Đang chuyển giọng nói thành văn bản..."):
        raw_text = transcribe_audio(OUTPUT_FILENAME)
        st.text_area("📝 Văn bản nhận diện:", raw_text, height=100)

    with st.spinner("Đang chỉnh ngữ pháp..."):
        corrected_text = correct_grammar(raw_text)
        st.text_area("✅ Văn bản đã chỉnh:", corrected_text, height=100)

# Danh sách lưu đoạn hội thoại (giữa các lần ghi âm)
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if st.button("🗣️ Bắt đầu hội thoại"):
    with st.spinner("Đang ghi âm..."):
        record_audio(OUTPUT_FILENAME)
        st.success("Đã ghi âm xong!")

    with st.spinner("Đang chuyển giọng nói thành văn bản..."):
        raw_text = transcribe_audio(OUTPUT_FILENAME)

    with st.spinner("Đang chỉnh ngữ pháp..."):
        corrected_text = correct_grammar(raw_text)

    # Lưu vào session_state để hiển thị đoạn hội thoại
    st.session_state.conversation.append({
        "raw": raw_text,
        "corrected": corrected_text
    })

# Hiển thị toàn bộ hội thoại đã chỉnh
if st.session_state.conversation:
    st.markdown("### 💬 Lịch sử hội thoại:")
    for i, turn in enumerate(st.session_state.conversation, 1):
        st.markdown(f"**Lần {i}:**")
        st.text_area("📝 Nhận dạng:", turn["raw"], height=80, key=f"raw_{i}")
        st.text_area("✅ Đã chỉnh:", turn["corrected"], height=80, key=f"corrected_{i}")
st.markdown("---")
st.subheader("✍️ Nhập văn bản để chỉnh ngữ pháp")

# Text input + button
input_text = st.text_area("Nhập văn bản cần chỉnh:", "", height=100)

if st.button("🛠️ Chỉnh ngữ pháp văn bản đã nhập"):
    if input_text.strip() == "":
        st.warning("Vui lòng nhập văn bản trước khi chỉnh!")
    else:
        with st.spinner("Đang chỉnh ngữ pháp..."):
            corrected_text = correct_grammar(input_text)
            st.success("✅ Đã chỉnh xong!")
            st.text_area("Văn bản sau khi chỉnh:", corrected_text, height=100)


