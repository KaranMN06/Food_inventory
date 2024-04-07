from fastapi import FastAPI
from pydantic import BaseModel,Field
from enum import Enum

'''CATEGORY SCHEMA '''

class State(str,Enum):
    state_a = "available"
    state_b = "not available"
    
class Category(BaseModel):
    category_name:str    
    status:State 
    

class list_of_items(BaseModel):
    item_name:str
    no_of_items:int
    price:int
class menu_request(BaseModel):
    category_name:str 
    item_list:list[list_of_items]

# "south_indian":{
#     "category_name":"south_indian",
#     "item_list":[{
#         "item_name":"rice",
#         "no_of_items":10,
#         "price":40
#     }]
# }
    

