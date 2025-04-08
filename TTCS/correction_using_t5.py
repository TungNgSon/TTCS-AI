import pyaudio
import wave
import whisper
import numpy as np
from happytransformer import HappyTextToText, TTSettings
# Cấu hình thu âm
FORMAT = pyaudio.paInt16  # Định dạng âm thanh 16-bit
CHANNELS = 1              # Số kênh (1 = mono, 2 = stereo)
RATE = 44100              # Tần số lấy mẫu (Hz)
CHUNK = 1024              # Kích thước mỗi buffer
RECORD_SECONDS = 5        # Thời gian thu âm
OUTPUT_FILENAME = ".venv/recorded_audio.wav"

# Khởi tạo PyAudio
audio = pyaudio.PyAudio()

# Mở luồng thu âm
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Đang thu âm...")

frames = []

# Thu âm trong RECORD_SECONDS giây
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Dừng thu âm.")

# Dừng và đóng luồng thu âm
stream.stop_stream()
stream.close()
audio.terminate()

# Lưu file WAV
wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Load mô hình Whisper
model = whisper.load_model("base")  # Thay "base" bằng model bạn có

# Nhận diện giọng nói
# result = model.transcribe(OUTPUT_FILENAME)
print("Nhận diện giọng nói từ âm thanh...")
result = model.transcribe(OUTPUT_FILENAME)
print("Kết quả nhận diện: ", result["text"])

# Khởi tạo mô hình T5 để sửa ngữ pháp
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

# Sửa ngữ pháp của văn bản đã nhận diện
corrected_text = happy_tt.generate_text(f"grammar: {result['text']}", args=args)

print("Văn bản sau khi sửa ngữ pháp: ")
print(corrected_text.text)
