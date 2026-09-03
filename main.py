# main.py
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from pages import get_dashboard_html

app = FastAPI()

db_configs = [
    {
        "name": "pro-sample", 
        "protocol": "VLESS WebSocket", 
        "volume": 25, 
        "unit": "GB",
        "days": 30,
        "ip_limit": 0,
        "conn_limit": 0,
        "speed": 0,
        "fp": "chrome",
        "frag": "خاموش",
        "port": 443,
        "alpn": "http/1.1",
        "note": "تست اول",
        "link": "vless://pro-sample@rvn.railway.app:443?type=ws&fp=chrome&alpn=http/1.1#pro-sample"
    }
]

class AdvancedConfigRequest(BaseModel):
    name: str
    protocol: str
    volume: Optional[float] = 0
    unit: str = "GB"
    days: Optional[int] = 0
    ip_limit: Optional[int] = 0
    conn_limit: Optional[int] = 0
    speed: Optional[int] = 0
    fp: str = "chrome"
    frag: str = "خاموش"
    port: int = 443
    alpn: str = "http/1.1"
    note: Optional[str] = ""

@app.get("/", response_class=HTMLResponse)
def read_dashboard():
    return get_dashboard_html()

@app.get("/api/get-configs")
def get_configs():
    return db_configs

@app.post("/api/create-config")
def create_config(req: AdvancedConfigRequest):
    wg_file = None
    if req.protocol == "WireGuard":
        wg_file = f"[Interface]\nPrivateKey = PRIV_KEY\nAddress = 10.0.0.2/32\n\n[Peer]\nPublicKey = PUB_KEY\nEndpoint = rvn.railway.app:{req.port}\nAllowedIPs = 0.0.0.0/0"
        link = f"wireguard://{req.name}@rvn.railway.app:{req.port}"
    else:
        proto_prefix = req.protocol.split()[0].lower()
        link = f"{proto_prefix}://{req.name}@rvn.railway.app:{req.port}?fp={req.fp}&alpn={req.alpn}#{req.name}"

    item = req.dict()
    item["link"] = link
    item["wireguard_file"] = wg_file

    db_configs.insert(0, item)
    return {"status": "ok", "config": item}

@app.delete("/api/delete-config")
def delete_config(name: str):
    global db_configs
    db_configs = [c for c in db_configs if c["name"] != name]
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
  
