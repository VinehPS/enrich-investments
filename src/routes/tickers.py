from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Depends, HTTPException

from src.db.mongodb import get_database
from src.models.schemas import TickerCache

router = APIRouter()

BRAPI_URL = "https://brapi.dev/api/quote/list"


async def fetch_tickers_from_brapi():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BRAPI_URL)
            response.raise_for_status()
            data = response.json()
            stocks = []
            fiis = []

            for item in data.get("stocks", []):
                ticker = item.get("stock")
                if not ticker:
                    continue
                name = item.get("name", "")

                # FIIs na B3 geralmente terminam em 11 e possuem 4 letras iniciais
                # (brapi.dev retorna type="fund" as vezes, mas analisaremos o ticker via heuristica simple)
                is_fii = len(ticker) >= 5 and ticker.endswith("11")

                asset = {"ticker": ticker, "name": name}
                if is_fii:
                    fiis.append(asset)
                else:
                    stocks.append(asset)

            return stocks, fiis
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Failed to fetch data from brapi: {str(e)}")


@router.get("/available")
async def get_available_tickers(db=Depends(get_database)):
    # 1. Check if cache exists and is fresh (< 7 days)
    collection = db["tickers"]
    cached_data = await collection.find_one()

    now = datetime.utcnow()
    needs_update = True

    if cached_data:
        last_updated = cached_data.get("last_updated")
        if last_updated and (now - last_updated) < timedelta(days=7):
            needs_update = False

    # 2. Return cached data if valid
    if not needs_update:
        return {
            "stocks": cached_data.get("stock_tickers", []),
            "fiis": cached_data.get("fund_tickers", []),
            "last_updated": cached_data.get("last_updated"),
            "cached": True,
        }

    # 3. Fetch new data from brapi
    stocks, fiis = await fetch_tickers_from_brapi()

    # 4. Save to DB
    new_cache = TickerCache(stock_tickers=stocks, fund_tickers=fiis, last_updated=now)

    if cached_data:
        # Update existing
        await collection.update_one(
            {"_id": cached_data["_id"]}, {"$set": {"stock_tickers": stocks, "fund_tickers": fiis, "last_updated": now}}
        )
    else:
        # Insert new
        await collection.insert_one(new_cache.model_dump(by_alias=True, exclude={"id"}))

    return {"stocks": stocks, "fiis": fiis, "last_updated": now, "cached": False}
