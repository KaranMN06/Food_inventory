from fastapi import FastAPI
from fastapi import APIRouter
from schemas.seller_side import menu_request
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
        res_key= list(res.keys())  # check from category.json not from menu.json for existing category u have to post 
        
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
    
    
@menu_card.post("/update-menu-list/",tags=['Menu Card'])
async def create_menu(menu:menu_request):
    if os.path.exists(menu_response_file) and os.path.getsize(menu_response_file) >0:
        with open(menu_response_file,'r') as f:
            res = json.load(f)
        res_key= list(res.keys())
        
        
    if (menu.category_name)  not  in res_key:
            detail={
                    "message": f"There is no {menu.category_name}.",
                    "reason": "no  attribute",
                    "referenceError": None,
                    "code": "notFound"
                    }
            return JSONResponse(content = detail, status_code=404)
        
    file_items=res[str(menu.category_name)]['item_list']
    file_lst=[]
    for i in file_items:
        file_lst.append(i['item_name'])
        
    
    request_items = jsonable_encoder(menu)
    request_items=request_items['item_list']
    request_lst=[]
    count=0
    for i in request_items:
        request_lst.append(i['item_name'])
        if i['item_name'] in file_lst:
            count=count+1
    

    if count > 0:
            detail={
                    "message": f"{request_lst}  is already present",
                    "reason": "duplicate attribute",
                    "referenceError": None,
                    "code": "notFound"
                    }
            return JSONResponse(content = detail, status_code=404)
    else:
        
        with open(menu_response_file,'r') as f:
            res = json.load(f)
        
        request_body = jsonable_encoder(menu)
        request_item = request_body['item_list']
        
        for i in  request_item:
            res[str(menu.category_name)]['item_list'].append(i)
            
        
        
        
        with open(menu_response_file,'w') as f:
                json.dump(res,f,indent = 4)
                
        with open(menu_response_file,'r') as f:
                data = json.load(f)
        return JSONResponse(content=data[str(menu.category_name)],status_code=201)
     