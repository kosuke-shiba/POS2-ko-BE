from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from pydantic import BaseModel, EmailStr
import os

# FastAPIアプリケーションのインスタンス作成
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/")
async def FastAPI():
    return { "message" : "Hello World" }

class SampleData(BaseModel):
    id:int
    name:str
    age:int

@app.get("/data")
def get_data():
    sample_data = {
        "id":1,
        "name":"John Doe",
        "age":30
    }
    return sample_data

 #MySQLデータベース接続設定
#DATABASE_URL = "mysql+pymysql://username:password@localhost/POS"  # 必要に応じて変更
DATABASE_URL = "mysql+pymysql://kosuke:Magmag33@127.0.0.1:3306/POS"  # 必要に応じて変更
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# 商品テーブルの定義
PrdMaster = Table(
    "PrdMaster", metadata,
    Column("PRD_ID", Integer, primary_key=True),
    Column("CODE", String(13), unique=True),
    Column("NAME", String(50)),
    Column("PRICE", Integer)
)

# 商品コードで商品名を検索するエンドポイント
@app.get("/product/{code}")
async def get_product_by_code(code: str):
    try:
        # データベース接続とクエリ実行
        with engine.connect() as connection:
            query = select(PrdMaster.c.NAME).where(PrdMaster.c.CODE == code)
            result = connection.execute(query).fetchone()
        
        # 結果が見つからない場合のエラーハンドリング
        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # 結果を返す
        return {"code": code, "name": result[0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/multiply/{id}")
def multipy(id: int):
    print("multiply")
    doubled_value = id * 2
    return {"doubled_value":doubled_value}

@app.get("/products/{user_id}")
def get_user(user_id:int):
    return {"user_id":user_id}

@app.get("/logout")
def logout():
    return RedirectResponse(url="/login")

@app.get("/login")
def login():
    return ("Login")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)