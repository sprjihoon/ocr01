from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models  # noqa
from .routes import auth, users, stores, images, price_history, logs, categories, products


def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()

app = FastAPI(title="Costco Price OCR Tracker")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                # 또는 ['https://<vercel-domain>']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(stores.router)
app.include_router(images.router)
app.include_router(price_history.router)
app.include_router(logs.router)
app.include_router(categories.router)
app.include_router(products.router) 