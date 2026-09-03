@app.post("/api/create-config")
def create_config(req: AdvancedConfigRequest, request: Request):
    current_host = request.url.hostname or "rvn.railway.app"
    
    wg_file = None
    if req.protocol == "WireGuard":
        wg_file = f"[Interface]\nPrivateKey = PRIV_KEY\nAddress = 10.0.0.2/32\n\n[Peer]\nPublicKey = PUB_KEY\nEndpoint = {current_host}:{req.port}\nAllowedIPs = 0.0.0.0/0"
        link = f"wireguard://{req.name}@{current_host}:{req.port}"
    else:
        # تشخیص دقیق نوع پروتکل (ws یا grpc)
        net_type = "grpc" if "grpc" in req.protocol.lower() else "ws"
        proto_prefix = "vless" if "vless" in req.protocol.lower() else "vmess"
        
        link = f"{proto_prefix}://{req.name}@{current_host}:{req.port}?encryption=none&security=tls&type={net_type}&serviceName=grpc&fp={req.fp}&alpn={req.alpn}#{req.name}"

    item = req.dict()
    item["link"] = link
    item["wireguard_file"] = wg_file

    db_configs.insert(0, item)
    return {"status": "ok", "config": item}
  
