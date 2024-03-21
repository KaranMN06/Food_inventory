from fastapi import FastAPI
from fastapi import APIRouter
from schemas.category_schema import Category
from fastapi.encoders import jsonable_encoder
import os
from fastapi.responses import JSONResponse
import json


category_app=APIRouter()

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
        
        if ((str(category_data['category_name'])).lower()) in res_key:
            detail={
                    "message": f"{category.category_name} is already present",
                    "reason": "duplicate attribute",
                    "referenceError": None,
                    "code": "notFound"
                    }
            return JSONResponse(content = detail, status_code=409)
        
        else:
            res[(str(category.category_name)).lower()] = (category_data['status']).lower()
            with open(category_path,'w') as f:
                json.dump(res,f,indent = 4)
            return JSONResponse(content = res,status_code = 201)
    else:
        with open(category_path,'w') as f:
            res_data={}
            res_data[(str(category.category_name)).lower()] = (category_data['status']).lower()
            json.dump(res_data,f,indent=4)
            
        return JSONResponse(content=res_data,status_code = 201)    


'''PATCH API for category management'''
@category_app.patch("/category-modify/",tags=['Category Management'])
async def modify_category(category:Category):
    
    category_data = jsonable_encoder(category)
    res_data={}
    res_data[(str(category.category_name)).lower()] = (category_data['status']).lower()
    with open(category_path,'r') as file:
        json_data=json.load(file)
    x=category.category_name
    for item in json_data.keys():
        if item==x:
            json_data[item]=res_data[x]
            with open(category_path,'w') as resp_file:
                json.dump(json_data,resp_file,indent=4)
            return JSONResponse(content=res_data,status_code = 201)
    else:
        return JSONResponse(content='category doesnt match',status_code = 422)        
    
    