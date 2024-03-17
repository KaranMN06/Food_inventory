from fastapi import FastAPI
from fastapi import APIRouter
from schemas.category_schema import Category
from fastapi.encoders import jsonable_encoder
import os
from fastapi.responses import JSONResponse
import json


category_app=FastAPI()

category_data={}

category_path='C:/Users/kmysore/Desktop/project2/Food_inventory/backend/responses/category.json'

@category_app.post("/category-create/",tags=['Category Management'])
async def create_category(category:Category):
    category_data = jsonable_encoder(category)
    
    if os.path.exists(category_path) and os.path.getsize(category_path) >0:
        with open(category_path,'r') as f:
            res = json.load(f)
        print(res)
        res_key= list(res.keys())
        
        if category_data['category_name'] in res_key:
            return JSONResponse(content = f"{category.category_name} is already present", status_code=409)
        
        else:
            res[str(category.category_name)] = category_data['status']
            with open(category_path,'w') as f:
                json.dump(res,f,indent = 4)
            return JSONResponse(content = res,status_code = 201)
    else:
        with open(category_path,'w') as f:
            res_data={}
            res_data[str(category.category_name)] = category_data['status']
            json.dump(res_data,f,indent=4)
            
        return JSONResponse(content=res_data,status_code = 201)    
     
    
    