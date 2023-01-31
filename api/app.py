import sys
import json
import requests
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from scripts.send_email import send
from scripts.sql_db import *
from .schemes import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/check")
def check():
    return "Your API is up!"

@app.post("/mint")
def create_upload_file():
    # Set file path
    file_path =  'crt.jpg'

    # POST method
    headers = {'pinata_api_key': API_KEY, 'pinata_secret_api_key': API_SECRET}
    endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as filedata:
            response = requests.post(endpoint, headers=headers, file={"file": filedata})

    print(response.text)

    # Store hash
    hash = response.json()['IpfsHash']
    return hash

    # You can see your image on the IPFS: https://ipfs.stibits.com/<your_hash>

@app.post("/mail")
def mail(rec: receiver):
    send(rec.asset_id, rec.address)

@app.post("/createDb")
def create_db(name: str):
    createDB(name)

@app.post("/createTable")
def create_table(table: Table):
    createTable(table.db_name, table.schema_name)

@app.post("/insert")
def insert(data: Insert):
    json_stream=(data.tb_data.json())
    insert_to_table(data.db_name, json_stream, data.table_name) 
    # return str(data.tb_data.json())

@app.post("/update")
def update(data: Update):
    json_stream=(data.json())

    update_table("trainee", json_stream, "trainee")

@app.post("/optinUpdate")
def update(data: OptinUpdate):
    json_stream=(data.json())

    optin_update("trainee", json_stream, "trainee")

@app.get("/getall")
def get_all():
    return db_get_values()

@app.get("/getTrainee")
def get_trainee(asset):
    return db_get_values_by_asset(asset)

@app.get("/getCertificates")
def get_trainee(addr):
    return db_get_values_by_addr(addr)