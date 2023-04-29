from fastapi import FastAPI
from Backend.CRUD_FUNCTIONS.router import user
import os

app = FastAPI()

app.include_router(user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


