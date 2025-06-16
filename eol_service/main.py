from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
import httpx
from functools import lru_cache

CACHE_DIR = Path(__file__).with_name('cache')
API_URL = 'https://endoflife.date/api/{}.json'

app = FastAPI(title="EOL Checker")


class EOLInfo(BaseModel):
    name: str
    version: str
    eol: str
    supported: bool


@lru_cache()
def get_software_data(name: str):
    name = name.lower()
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{name}.json"
    if cache_file.exists():
        with cache_file.open() as f:
            return json.load(f)
    try:
        resp = httpx.get(API_URL.format(name), timeout=10.0)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Failed to fetch data: {exc}")
    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Software not found")
    data = resp.json()
    with cache_file.open("w") as f:
        json.dump(data, f)
    return data

@app.get('/eol', response_model=EOLInfo)
def check_eol(name: str, version: str):
    data = get_software_data(name)
    entry = next((i for i in data if i.get('cycle') == version), None)
    if not entry:
        raise HTTPException(status_code=404, detail='Version not found')
    eol_val = entry.get('eol')
    if not eol_val:
        raise HTTPException(status_code=404, detail='EOL date not available')
    eol_date = date.fromisoformat(eol_val)
    return EOLInfo(
        name=name,
        version=version,
        eol=eol_date.isoformat(),
        supported=date.today() <= eol_date
    )
