from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn  # Додаємо імпорт uvicorn
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
    # Додаємо вивід в консоль, щоб бачити, чи прийшло повідомлення
    print(f"--- Отримано повідомлення: {user_text} ---")
    
    ai_response = think(user_text)
    save_message(user_text, ai_response)
    
    return {"reply": ai_response}

# ОЦЕ ВАЖЛИВА ЧАСТИНА:
if __name__ == "__main__":
    # host="0.0.0.0" означає "слухай всі пристрої в мережі"
    # Замініть рядок у main.py на цей:
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)