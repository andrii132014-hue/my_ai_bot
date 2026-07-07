import os
from groq import Groq

# Клієнт отримує ключ з налаштувань сервера (Environment Variables)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def think(user_text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_text}
            ],
            model="llama3-8b-8192", # Це швидка і потужна модель
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Сталася помилка API: {str(e)}"