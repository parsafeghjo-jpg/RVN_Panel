# main_pro.py
import os
import uvicorn
from fastapi import FastAPI, Response, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

db_configs = []

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

class LoginRequest(BaseModel):
    username: str
    password: str

class ConfigRequest(BaseModel):
    name: str
    protocol: str
    volume: float
    days: int
    port: int
    fp: str = "chrome"
    alpn: str = "http/1.1"

def is_authenticated(request: Request) -> bool:
    return request.cookies.get("session") == "authenticated_admin"

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    if not is_authenticated(request):
        return """
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>System Authentication</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Vazirmatn:wght@400;500;700&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Vazirmatn', sans-serif; background: #0a0c10; color: #c9d1d9; }
                .mono { font-family: 'JetBrains Mono', monospace; }
            </style>
        </head>
        <body class="flex items-center justify-center h-screen m-0">
            <div class="w-full max-w-sm p-8 bg-[#121620] border border-[#21262d] rounded-2xl shadow-2xl">
                <div class="mb-6">
                    <span class="mono text-xs text-emerald-500 font-bold tracking-widest uppercase">[ ACCESS_GATEWAY ]</span>
                    <h2 class="text-lg font-bold text-white mt-1">احراز هویت سیستم</h2>
                </div>
                <form onsubmit="handleLogin(event)" class="space-y-4">
                    <div>
                        <label class="block text-xs text-slate-400 mb-1.5 mono">USER</label>
                        <input type="text" id="username" class="w-full bg-[#0a0c10] border border-[#30363d] rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition mono" required>
                    </div>
                    <div>
                        <label class="block text-xs text-slate-400 mb-1.5 mono">PASS</label>
                        <input type="password" id="password" class="w-full bg-[#0a0c10] border border-[#30363d] rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition mono" required>
                    </div>
                    <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-black font-bold py-2.5 rounded-xl transition text-xs mono tracking-wider mt-2">AUTHENTICATE</button>
                    <div id="error" class="text-red-400 text-xs text-center hidden mono mt-2">خطای دسترسی</div>
                </form>
            </div>
            <script>
                async function handleLogin(e) {
                    e.preventDefault();
                    const u = document.getElementById('username').value;
                    const p = document.getElementById('password').value;
                    const res = await fetch('/api/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username: u, password: p})
                    });
                    const data = await res.json();
                    if(data.status === 'ok') window.location.reload();
                    else document.getElementById('error').classList.remove('hidden');
                }
            </script>
        </body>
        </html>
        """
    
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>Node Control</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Vazirmatn:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Vazirmatn', sans-serif; background-color: #0d1117; color: #c9d1d9; }
            .mono { font-family: 'JetBrains Mono', monospace; }
            .panel { background: #161b22; border: 1px solid #30363d; }
            input, select { background: #0d1117 !important; border-color: #30363d !important; color: #fff !important; }
            input:focus, select:focus { border-color: #58a6ff !important; outline: none; }
        </style>
    </head>
    <body class="min-h-screen p-4 md:p-8">
        <div class="max-w-6xl mx-auto space-y-6">
            
            <header class="panel p-5 rounded-2xl flex flex-col sm:flex-row justify-between items-center gap-4">
                <div class="flex items-center gap-3">
                    <div class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
                    <div>
                        <span class="mono text-[10px] text-slate-400 block tracking-widest">NODE STATUS: ONLINE</span>
                        <h1 class="text-sm font-bold text-white mono">sys-core-node-01</h1>
                    </div>
                </div>
                <div class="flex items-center gap-2.5">
                    <button onclick="openModal()" class="px-4 py-2 bg-[#21262d] hover:bg-[#30363d] text-white text-xs font-medium rounded-xl transition mono border border-[#30363d]">+ New Tunnel</button>
                    <button onclick="logout()" class="px-3 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-medium rounded-xl transition mono border border-red-500/20">Logout</button>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="panel p-5 rounded-2xl">
                    <span class="text-xs text-slate-400 mono">ACTIVE TUNNELS</span>
                    <div id="statActive" class="text-2xl font-bold text-white mono mt-1">0</div>
                </div>
                <div class="panel p-5 rounded-2xl">
                    <span class="text-xs text-slate-400 mono">TOTAL ALLOCATED</span>
                    <div id="statVol" class="text-2xl font-bold text-emerald-400 mono mt-1">0 GB</div>
                </div>
                <div class="panel p-5 rounded-2xl">
                    <span class="text-xs text-slate-400 mono">INTERFACE PROTOCOL</span>
                    <div class="text-2xl font-bold text-blue-400 mono mt-1">VLESS/WS</div>
                </div>
            </div>

            <div class="panel rounded-2xl overflow-hidden">
                <div class="p-4 border-b border-[#30363d] flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-300 mono uppercase tracking-wider">Active Instances</span>
                    <span class="text-[10px] text-slate-500 mono">AUTOLOAD: ENABLED</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-right border-collapse text-xs">
                        <thead>
                            <tr class="border-b border-[#30363d] text-slate-400 mono">
                                <th class="p-4">IDENTIFIER</th>
                                <th class="p-4">PROTOCOL</th>
                                <th class="p-4">QUOTA</th>
                                <th class="p-4">EXPIRE</th>
                                <th class="p-4">STATUS</th>
                                <th class="p-4 text-center">ACTIONS</th>
                            </tr>
                        </thead>
                        <tbody id="configTableBody"></tbody>
                    </table>
                </div>
            </div>

        </div>

        <div id="configModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
            <div class="panel p-6 rounded-2xl w-full max-w-md relative">
                <div class="flex justify-between items-center mb-4 border-b border-[#30363d] pb-3">
                    <h2 class="text-xs font-bold text-white mono uppercase tracking-wider">Configure New Tunnel</h2>
                    <button onclick="closeModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
                </div>
                <form onsubmit="createConfig(event)" class="space-y-3.5 text-xs">
                    <div>
                        <label class="block text-slate-400 mb-1 mono">IDENTIFIER</label>
                        <input type="text" id="cfgName" class="w-full rounded-xl px-3.5 py-2.5 text-white mono" value="node-client-01" required>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 mono">PROTOCOL SPEC</label>
                        <select id="cfgProto" class="w-full rounded-xl px-3.5 py-2.5 text-white mono">
                            <option value="Vless WS">Vless + WebSocket</option>
                            <option value="Vless gRPC">Vless + gRPC</option>
                            <option value="WireGuard">WireGuard</option>
                        </select>
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-slate-400 mb-1 mono">QUOTA (GB)</label>
                            <input type="number" id="cfgVol" class="w-full rounded-xl px-3.5 py-2.5 text-white mono" value="50" required>
                        </div>
                        <div>
                            <label class="block text-slate-400 mb-1 mono">DAYS</label>
                            <input type="number" id="cfgDays" class="w-full rounded-xl px-3.5 py-2.5 text-white mono" value="30" required>
                        </div>
                    </div>
                    <input type="hidden" id="cfgPort" value="443">
                    <div class="pt-3">
                        <button type="submit" class="w-full bg-[#21262d] hover:bg-[#30363d] text-white font-bold py-2.5 rounded-xl transition mono border border-[#30363d]">DEPLOY INSTANCE</button>
                    </div>
                </form>
            </div>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', () => { loadConfigs(); });

            function openModal() { document.getElementById('configModal').classList.remove('hidden'); }
            function closeModal() { document.getElementById('configModal').classList.add('hidden'); }

            async function createConfig(e) {
                e.preventDefault();
                const data = {
                    name: document.getElementById('cfgName').value,
                    protocol: document.getElementById('cfgProto').value,
                    volume: parseFloat(document.getElementById('cfgVol').value),
                    days: parseInt(document.getElementById('cfgDays').value),
                    port: parseInt(document.getElementById('cfgPort').value)
                };

                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                if(res.ok) {
                    closeModal();
                    loadConfigs();
                }
            }

            async function loadConfigs() {
                const res = await fetch('/api/list');
                const configs = await res.json();
                const tbody = document.getElementById('configTableBody');
                
                document.getElementById('statActive').innerText = configs.length;
                let totalVol = configs.reduce((acc, curr) => acc + curr.volume, 0);
                document.getElementById('statVol').innerText = totalVol + ' GB';

                let html = '';
                if(configs.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-slate-500 mono text-xs">NO_ACTIVE_INSTANCES</td></tr>`;
                    return;
                }

                configs.forEach((c) => {
                    let statusBadge = c.active 
                        ? '<span class="text-emerald-400 mono text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">RUNNING</span>' 
                        : '<span class="text-red-400 mono text-[10px] px-2 py-0.5 rounded bg-red-500/10 border border-red-500/20">STOPPED</span>';
                    
                    html += `
                        <tr class="border-b border-[#30363d]/50 hover:bg-[#1f242c] transition">
                            <td class="p-4 font-bold text-white mono">${c.name}</td>
                            <td class="p-4 text-slate-300 mono text-[11px]">${c.protocol}</td>
                            <td class="p-4 font-mono text-cyan-400">${c.volume} GB</td>
                            <td class="p-4 font-mono text-slate-400">${c.days}D</td>
                            <td class="p-4">${statusBadge}</td>
                            <td class="p-4 flex justify-center gap-1.5">
                                <button onclick="copyText('${c.link}')" class="px-2.5 py-1 bg-[#21262d] hover:bg-[#30363d] text-slate-200 rounded-lg transition mono text-[11px] border border-[#30363d]">Copy</button>
                                <button onclick="toggleStatus('${c.name}')" class="px-2.5 py-1 bg-[#21262d] hover:bg-[#30363d] text-slate-200 rounded-lg transition mono text-[11px] border border-[#30363d]">${c.active ? 'Stop' : 'Start'}</button>
                                <button onclick="deleteConfig('${c.name}')" class="px-2.5 py-1 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition mono text-[11px] border border-red-500/20">Del</button>
                            </td>
                        </tr>
                    `;
                });
                tbody.innerHTML = html;
            }

            function copyText(txt) {
                navigator.clipboard.writeText(txt).then(() => alert('LINK_COPIED'));
            }

            async function toggleStatus(name) {
                await fetch('/api/toggle?name=' + encodeURIComponent(name), { method: 'POST' });
                loadConfigs();
            }

            async function deleteConfig(name) {
                if(confirm('CONFIRM_DELETE?')) {
                    await fetch('/api/delete?name=' + encodeURIComponent(name), { method: 'DELETE' });
                    loadConfigs();
                }
            }

            async function logout() {
                await fetch('/api/logout', { method: 'POST' });
                window.location.reload();
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/login")
def login(data: LoginRequest, response: Response):
    if data.username == ADMIN_USER and data.password == ADMIN_PASS:
        response.set_cookie(key="session", value="authenticated_admin", httponly=True)
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie(key="session")
    return {"status": "ok"}

@app.get("/api/list")
def list_configs():
    return db_configs

@app.post("/api/create")
def create(req: ConfigRequest, request: Request):
    current_host = request.url.hostname or "rvn.railway.app"
    
    if "WireGuard" in req.protocol:
        link = f"wireguard://{req.name}@{current_host}:{req.port}?vol={req.volume}GB#{req.name}"
    else:
        net_type = "grpc" if "grpc" in req.protocol.lower() else "ws"
        path = "vless-ws" if net_type == "ws" else "vless-grpc"
        link = f"vless://{req.name}@{current_host}:{req.port}?encryption=none&security=tls&type={net_type}&path=%2F{path}&fp={req.fp}&alpn={req.alpn}#{req.name}"

    item = {
        "name": req.name,
        "protocol": req.protocol,
        "volume": req.volume,
        "days": req.days,
        "link": link,
        "active": True
    }
    db_configs.insert(0, item)
    return {"status": "ok"}

@app.websocket("/vless-ws")
async def vless_websocket_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            await websocket.send_bytes(data)
    except WebSocketDisconnect:
        pass

@app.post("/api/toggle")
def toggle(name: str):
    for c in db_configs:
        if c["name"] == name:
            c["active"] = not c["active"]
    return {"status": "ok"}

@app.delete("/api/delete")
def delete(name: str):
    global db_configs
    db_configs = [c for c in db_configs if c["name"] != name]
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main_pro:app", host="0.0.0.0", port=port, reload=True)
