from fastapi import FastAPI
from Backend.CRUD_FUNCTIONS.router import user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()


"""Orins, the variable containing all the IP allowed to use the backend userlication in this case the only IP allowed is the ASCEPUPR Domain name"""
origins = [
    "https://www.examdev.net/"
]

"""Add the allowed origins IP's to the fastapi userlication variable """
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
