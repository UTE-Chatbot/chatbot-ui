import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyBNMDBIw8EgbJdVSR8_io747BJn-JssUiU"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name = "gemini-1.5-pro")
model
#response = model.generate_content("Hi")
#print(response.text)