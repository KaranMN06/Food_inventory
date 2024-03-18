from fastapi import FastAPI
from category import category_app


app=FastAPI(title="Restaraunt Management System")

app.include_router(category_app)
