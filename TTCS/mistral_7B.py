from llama_cpp import Llama

# Đường dẫn đến file GGUF
model_path = "D:\mistral-7b-instruct-v0.2.Q2_K.gguf"

# Khởi tạo model
llm = Llama(model_path=model_path, n_ctx=2048)  # n_ctx là độ dài context tối đa

# Bắt đầu hỏi đáp
while True:
    user_input = input("Find grammar error in: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Tạm biệt!")
        break

    response = llm(user_input)
    print("Mistral:", response["choices"][0]["text"].strip())