# server.py
import os
import uvicorn
from fastapi import FastAPI, Response, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from pages import get_dashboard_html
from auth import is_authenticated, login_user, logout_user, get_login_html

app = FastAPI()

db_configs = []

class LoginRequest(BaseModel):
    username: str
    password: str

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
def read_dashboard(request: Request):
    if not is_authenticated(request):
        return get_login_html()
    return get_dashboard_html()

@app.post("/api/login")
def login(data: LoginRequest, response: Response):
    if login_user(data.username, data.password, response):
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/api/logout")
def logout(response: Response):
    logout_user(response)
    return {"status": "ok"}

@app.get("/api/get-configs")
def get_configs(request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db_configs

@app.post("/api/create-config")
def create_config(req: AdvancedConfigRequest, request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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
def delete_config(name: str, request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    global db_configs
    db_configs = [c for c in db_configs if c["name"] != name]
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
      
