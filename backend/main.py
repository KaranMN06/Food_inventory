from fastapi import FastAPI
from category import category_app
from menu_card import menu_card

app=FastAPI(title="Restaraunt Management System")

app.include_router(category_app)
app.include_router(menu_card)
