from fastapi import FastAPI
from fastapi import APIRouter
from schemas.category_schema import menu_request
from fastapi.encoders import jsonable_encoder
import os
from pathlib import Path
from fastapi.responses import JSONResponse
import json


menu_card=APIRouter()
current_directory= Path(__file__).parents[0]
response_file="menu.json"
menu_response_file = current_directory / 'responses' / response_file

# menu_response_file="C:/Users/manju/OneDrive/Desktop/pro/Food_inventory/backend/responses/menu.json"
menu_data={}

@menu_card.post("/menu-card/",tags=['Menu Card'])
async def create_menu(menu:menu_request):
    # menu_data = jsonable_encoder(menu)
    if os.path.exists(menu_response_file) and os.path.getsize(menu_response_file) >0:
        with open(menu_response_file,'r') as f:
            res = json.load(f)
        res_key= list(res.keys())
        
        if (menu.category_name) in res_key:
            detail={
                    "message": f"{menu.category_name} is already present",
                    "reason": "duplicate attribute",
                    "referenceError": None,
                    "code": "notFound"
                    }
            return JSONResponse(content = detail, status_code=409)
        
        else:
            # menu_data={}
            menu_data[menu.category_name]=jsonable_encoder(menu)
            res.update(menu_data)
            with open(menu_response_file,'w') as f:
                json.dump(res,f,indent = 4)
            return JSONResponse(content = menu_data,status_code = 201)
            
    else:
        with open(menu_response_file,'w') as file:
            # menu_data={}
            menu_data[menu.category_name] = jsonable_encoder(menu)
            json.dump(menu_data,file,indent=4)
            
        return JSONResponse(content=menu_data,status_code = 201) 