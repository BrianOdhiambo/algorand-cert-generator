from pydantic import BaseModel


class receiver(BaseModel):
    address: str
    asset_id: str


class Table(BaseModel):
    db_name: str
    schema_name: str


class Data(BaseModel):

    trainee: str
    email: str
    asset: str
    status: str
    hashed:str
class Insert(BaseModel):

    db_name: str
    tb_data: Data
    table_name: str
    
class Update(BaseModel):

    asset: str
    status: str
    email: str
    hashed:str

class OptinUpdate(BaseModel):

    status: str
    remark: str
    asset: str