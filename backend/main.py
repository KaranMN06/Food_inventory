from fastapi import FastAPI
from category import category_app
from menu_card import menu_card
from auth import auth_seller

app=FastAPI(title="Restaraunt Management System")

app.include_router(category_app)
app.include_router(menu_card)
app.include_router(auth_seller)
