import whisper

# Tải model Whisper
model = whisper.load_model("base")  # Hoặc chọn "small", "medium", "large" tùy vào tài nguyên máy

# Chạy transcribe
result = model.transcribe("test2.mp3")
print(result["text"])


