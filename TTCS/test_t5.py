from happytransformer import HappyTextToText, TTSettings

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)
result = happy_tt.generate_text("grammar: How about play inside", args=args)
print("Generated text:", result.text)
