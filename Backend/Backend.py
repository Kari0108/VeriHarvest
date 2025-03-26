from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.models.transactions import Payment
from xrpl.models.requests import AccountTx
from xrpl.models.amounts import IssuedCurrencyAmount

# Initialize FastAPI App
app = FastAPI()

# XRPL Configuration
XRPL_RPC_URL = "https://s.altnet.rippletest.net:51234"  # Testnet RPC
ISSUER_WALLET = Wallet(seed="YOUR_ISSUER_SEED", sequence=0)
DESTINATION_WALLET = Wallet(seed="YOUR_DEST_SEED", sequence=0)
client = JsonRpcClient(XRPL_RPC_URL)

# Define Models
class FoodBatch(BaseModel):
    batch_id: int
    product_name: str
    supplier: str
    freshness_score: int
    blockchain_verified: bool
    status: str

# API Endpoints
@app.post("/add_batch/")
def add_batch(batch: FoodBatch):
    try:
        payment = Payment(
            account=ISSUER_WALLET.classic_address,
            destination=DESTINATION_WALLET.classic_address,
            amount=IssuedCurrencyAmount(
                currency="FRESH",
                issuer=ISSUER_WALLET.classic_address,
                value=str(batch.freshness_score),
            ),
            memos=[
                {"Memo": {"MemoData": batch.product_name}},
                {"Memo": {"MemoData": batch.supplier}},
                {"Memo": {"MemoData": batch.status}},
            ],
        )
        signed_tx = safe_sign_and_autofill_transaction(payment, ISSUER_WALLET, client)
        response = send_reliable_submission(signed_tx, client)
        return {"message": "Batch added to XRPL", "tx_hash": response.result["hash"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_batch/{account}")
def get_batch(account: str):
    try:
        response = client.request(AccountTx(account=account))
        return response.result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
