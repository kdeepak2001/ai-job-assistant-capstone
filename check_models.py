import google.generativeai as genai

genai.configure(api_key="AIzaSyAaVfkxZiBiJLMkdbRBGFF64xp3je2X_DE")

print("Available models that support generateContent:\n")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)