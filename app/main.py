from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.services.brain import think
from app.db.database import init_db, save_message

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/chat")
def chat_with_ai(data: dict):
    user_text = data.get("text")
    print(f"--- Отримано повідомлення: {user_text} ---")
    
    ai_response = think(user_text)
    save_message(user_text, ai_response)
    
    return {"reply": ai_response}

if __name__ == "__main__":
    # ДЛЯ РЕНДЕРА: використовуємо 0.0.0.0 та динамічний порт
    # Це дозволяє серверу приймати запити з будь-якого місця (з інтернету)
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)