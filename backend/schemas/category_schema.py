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
    
    

