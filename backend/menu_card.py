from fastapi import FastAPI
from fastapi import APIRouter
from schemas.seller_side import menu_request
from fastapi.encoders import jsonable_encoder
import os
from pathlib import Path
from fastapi.responses import JSONResponse
import json
from fastapi import FastAPI, Body, Depends
from auth import UserSchema, UserLoginSchema,JWTBearer,signJWT


menu_card=APIRouter()

current_directory= Path(__file__).parents[0]
response_file="menu.json"
menu_response_file = current_directory / 'responses' / response_file

category_response_file = "category.json"
category_file_name = current_directory / 'responses' / category_response_file

# menu_response_file="C:/Users/manju/OneDrive/Desktop/pro/Food_inventory/backend/responses/menu.json"
menu_data={}

@menu_card.post("/menu-card/",dependencies=[Depends(JWTBearer())],tags=['Menu Card'])
async def create_menu(menu:menu_request):
    menu_card  = {}
    if os.path.exists(category_file_name) and os.path.getsize(category_file_name) >0:
        with open(category_file_name,'r') as f:
            res = json.load(f)
        res_key= list(res.keys())  # check from category.json not from menu.json for existing category u have to post 
        
        if (menu.category_name) not in res_key:
            detail={
                    "message": f"Sorry we dont serve {menu.category_name}",
                    "reason": "Invalid value",
                    "referenceError": None,
                    "code": "invalid"
                    }
            return JSONResponse(content = detail, status_code=409)
        
        

        else:
            with open(menu_response_file,'r') as file:
                data=json.load(file)
            if menu.category_name in data:
                detail={
                    "message": f"{menu.category_name}  is already present, please use /update-menu-list to update the menu",
                    "reason": "duplicate attribute",
                    "referenceError": None,
                    "code": "notFound"
                    }
                return JSONResponse(content = detail, status_code=404)
            
            else:
                 # menu_data={}
                menu_data[menu.category_name]=jsonable_encoder(menu)
                menu_card.update(menu_data)
                with open(menu_response_file,'w') as f:
                    json.dump(menu_card,f,indent = 4)
                return JSONResponse(content = menu_data,status_code = 201)
            
    else:
        detail={
                "message": f"Sorry we dont serve {menu.category_name}",
                "reason": "Invalid value",
                "referenceError": None,
                "code": "invalid"
                }
        return JSONResponse(content = detail, status_code=409)
        # with open(menu_response_file,'w') as file:
        #     menu_data={}
        #     menu_data[menu.category_name] = jsonable_encoder(menu)
        #     json.dump(menu_data,file,indent=4)
            
        # return JSONResponse(content=menu_data,status_code = 201) 
    
    
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
     