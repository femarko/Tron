from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tronpy import Tron

app = FastAPI()

# Настройка базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///tron_wallets.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance = Column(Integer)

Base.metadata.create_all(bind=engine)

# Настройка Tron API
tron = Tron()
tron.get_bandwidth()


class WalletRequest(BaseModel):
    address: str

@app.post("/wallet")
async def get_wallet_info(wallet_request: WalletRequest):
    address = wallet_request.address
    try:
        wallet_info = tron.get_account_info(address)
        bandwidth = wallet_info["bandwidth"]
        energy = wallet_info["energy"]
        balance = wallet_info["balance"]
        wallet = Wallet(address=address, bandwidth=bandwidth, energy=energy, balance=balance)
        db = SessionLocal()
        db.add(wallet)
        db.commit()
        return JSONResponse(
            content={
                "address": address, "bandwidth": bandwidth, "energy": energy, "balance": balance
            },
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Wallet not found: {e}")

@app.get("/wallets")
async def get_wallets(limit: int = 10, offset: int = 0):
    db = SessionLocal()
    wallets = db.query(Wallet).limit(limit).offset(offset).all()
    return JSONResponse(
        content=[
        {
            "address": wallet.address,
            "bandwidth": wallet.bandwidth,
            "energy": wallet.energy,
            "balance": wallet.balance
        } for wallet in wallets
    ],
        media_type="application/json"
    )