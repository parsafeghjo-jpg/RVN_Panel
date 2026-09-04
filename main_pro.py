# main_pro.py
import os
import uvicorn
from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# دیتابیس موقت برای نگهداری کانفیگ‌ها
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
            <title>ورود | RVN Panel Pro</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
            <style>body { font-family: 'Vazirmatn', sans-serif; }</style>
        </head>
        <body class="bg-[#090d16] text-white flex items-center justify-center h-screen m-0">
            <div class="bg-slate-900/80 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl shadow-2xl w-96 relative overflow-hidden">
                <div class="absolute -top-24 -right-24 w-48 h-48 bg-violet-600/20 rounded-full blur-3xl"></div>
                <h2 class="text-2xl font-black mb-2 text-center text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-cyan-400">RVN Panel Pro</h2>
                <p class="text-xs text-slate-400 text-center mb-6">پنل مدیریت هوشمند و پیشرفته</p>
                <form onsubmit="handleLogin(event)" class="space-y-4">
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">نام کاربری</label>
                        <input type="text" id="username" class="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-violet-500 transition" required>
                    </div>
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">رمز عبور</label>
                        <input type="password" id="password" class="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-violet-500 transition" required>
                    </div>
                    <button type="submit" class="w-full bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 font-bold py-3 rounded-xl transition shadow-lg shadow-violet-600/30 text-sm">ورود به پنل</button>
                    <div id="error" class="text-red-400 text-xs text-center hidden">نام کاربری یا رمز عبور اشتباه است</div>
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
        <title>RVN Panel Pro - Ultimate Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;900&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Vazirmatn', sans-serif; background-color: #050811; color: #f8fafc; }
            .glass { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.07); }
            .glow-violet { box-shadow: 0 0 40px -10px rgba(139, 92, 246, 0.15); }
        </style>
    </head>
    <body class="min-h-screen p-4 md:p-8">
        <div class="max-w-7xl mx-auto space-y-8">
            
            <!-- هدر مدرن -->
            <header class="glass p-6 rounded-3xl flex flex-col md:flex-row justify-between items-center gap-4 glow-violet">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center font-black text-xl shadow-lg shadow-violet-500/30">RVN</div>
                    <div>
                        <h1 class="text-xl font-black text-white">RVN Panel Pro <span class="text-xs px-2 py-0.5 bg-violet-500/20 text-violet-400 rounded-full border border-violet-500/30 mr-2">نسخه نهایی</span></h1>
                        <p class="text-xs text-slate-400">سیستم فوق‌پیشرفته مدیریت پروکسی و ترافیک شبکه</p>
                    </div>
                </div>
                <button onclick="logout()" class="px-5 py-2.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-bold rounded-xl transition border border-red-500/20">خروج از حساب</button>
            </header>

            <!-- بخش نمودارهای خفن -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="glass p-6 rounded-3xl lg:col-span-2 flex flex-col justify-between">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="font-extrabold text-sm text-white flex items-center gap-2">📈 نمودار مصرف لحظه‌ای ترافیک کل</h2>
                        <span class="text-[10px] text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">● زنده و فعال</span>
                    </div>
                    <div style="height: 240px;"><canvas id="mainTrafficChart"></canvas></div>
                </div>
                <div class="glass p-6 rounded-3xl flex flex-col justify-between">
                    <h2 class="font-extrabold text-sm text-white mb-4">⚡ وضعیت پروتکل‌ها</h2>
                    <div style="height: 200px;"><canvas id="protocolPieChart"></canvas></div>
                </div>
            </div>

            <!-- فرم ساخت کانفیگ خفن -->
            <div class="glass p-8 rounded-3xl relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-violet-500 via-cyan-500 to-emerald-500"></div>
                <h2 class="text-base font-black text-violet-400 mb-6 flex items-center gap-2">🛠️ ساخت کانفیگ فوق‌پیشرفته با هاست زنده</h2>
                <form onsubmit="createConfig(event)" class="grid grid-cols-1 md:grid-cols-4 gap-5 text-xs">
                    <div>
                        <label class="block text-slate-400 mb-2 font-semibold">نام کانفیگ</label>
                        <input type="text" id="cfgName" class="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-white focus:border-violet-500 focus:outline-none transition" value="rvn-vip-01" required>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-2 font-semibold">پروتکل</label>
                        <select id="cfgProto" class="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-white focus:border-violet-500 focus:outline-none transition">
                            <option value="Vless WS">Vless + WebSocket</option>
                            <option value="Vless gRPC">Vless + gRPC</option>
                            <option value="WireGuard">WireGuard VPN</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-2 font-semibold">حجم واقعی (GB)</label>
                        <input type="number" id="cfgVol" class="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-white focus:border-violet-500 focus:outline-none transition" value="50" required>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-2 font-semibold">زمان واقعی (روز)</label>
                        <input type="number" id="cfgDays" class="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-white focus:border-violet-500 focus:outline-none transition" value="30" required>
                    </div>
                    <input type="hidden" id="cfgPort" value="443">
                    <div class="md:col-span-4 pt-2">
                        <button type="submit" class="w-full bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-600 hover:opacity-90 text-white font-extrabold py-3.5 rounded-2xl transition shadow-xl shadow-violet-600/25 text-sm tracking-wide">🚀 ساخت و تولید نهایی کانفیگ</button>
                    </div>
                </form>
            </div>

            <!-- جدول مدیریت کانفیگ‌ها -->
            <div class="glass p-6 rounded-3xl">
                <h2 class="text-sm font-black text-white mb-6 flex items-center gap-2">📋 لیست کانفیگ‌های فعال (مدیریت کامل)</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-right border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800/80 text-xs text-slate-400">
                                <th class="p-4">نام کانفیگ</th>
                                <th class="p-4">پروتکل</th>
                                <th class="p-4">حجم مصرفی / کل</th>
                                <th class="p-4">زمان باقی‌مانده</th>
                                <th class="p-4">وضعیت</th>
                                <th class="p-4 text-center">عملیات (کپی، قطع، حذف)</th>
                            </tr>
                        </thead>
                        <tbody id="configTableBody">
                            <!-- به صورت پویا پر می‌شود -->
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

        <script>
            // راه‌اندازی نمودارها
            document.addEventListener('DOMContentLoaded', () => {
                const ctx1 = document.getElementById('mainTrafficChart').getContext('2d');
                new Chart(ctx1, {
                    type: 'line',
                    data: {
                        labels: ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'امروز'],
                        datasets: [{
                            label: 'مصرف کل شبکه (GB)',
                            data: [35, 59, 80, 81, 56, 95, 120],
                            borderColor: '#8b5cf6',
                            backgroundColor: 'rgba(139, 92, 246, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#64748b' } }, y: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#64748b' } } } }
                });

                const ctx2 = document.getElementById('protocolPieChart').getContext('2d');
                new Chart(ctx2, {
                    type: 'doughnut',
                    data: {
                        labels: ['Vless WS', 'Vless gRPC', 'WireGuard'],
                        datasets: [{ data: [60, 25, 15], backgroundColor: ['#8b5cf6', '#06b6d4', '#10b981'], borderWidth: 0 }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', boxWidth: 12 } } } }
                });

                loadConfigs();
            });

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
                    loadConfigs();
                    alert('کانفیگ با موفقیت ساخته شد و به لیست اضافه شد!');
                }
            }

            async function loadConfigs() {
                const res = await fetch('/api/list');
                const configs = await res.json();
                const tbody = document.getElementById('configTableBody');
                let html = '';

                if(configs.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-slate-500 text-xs">هنوز هیچ کانفیگی ساخته نشده است.</td></tr>`;
                    return;
                }

                configs.forEach((c, index) => {
                    let statusBadge = c.active 
                        ? '<span class="px-3 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">فعال</span>' 
                        : '<span class="px-3 py-1 rounded-full text-[10px] font-bold bg-red-500/10 text-red-400 border border-red-500/20">قطع شده</span>';
                    
                    html += `
                        <tr class="border-b border-slate-800/40 hover:bg-slate-800/20 transition text-xs">
                            <td class="p-4 font-bold text-white">${c.name}</td>
                            <td class="p-4"><span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300">${c.protocol}</span></td>
                            <td class="p-4 font-mono text-cyan-400">0 GB / ${c.volume} GB</td>
                            <td class="p-4 font-mono text-violet-400">${c.days} روز باقی‌مانده</td>
                            <td class="p-4">${statusBadge}</td>
                            <td class="p-4 flex justify-center gap-2">
                                <button onclick="copyText('${c.link}')" class="px-3 py-1.5 bg-violet-600 hover:bg-violet-700 text-white rounded-xl font-bold transition shadow-md shadow-violet-600/20">📋 کپی</button>
                                <button onclick="toggleStatus('${c.name}')" class="px-3 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 rounded-xl font-bold transition">⚡ ${c.active ? 'قطع' : 'وصل'}</button>
                                <button onclick="deleteConfig('${c.name}')" class="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl font-bold transition">🗑️ حذف</button>
                            </td>
                        </tr>
                    `;
                });
                tbody.innerHTML = html;
            }

            function copyText(txt) {
                navigator.clipboard.writeText(txt).then(() => alert('لینک کانفیگ با موفقیت کپی شد!'));
            }

            async function toggleStatus(name) {
                await fetch('/api/toggle?name=' + encodeURIComponent(name), { method: 'POST' });
                loadConfigs();
            }

            async function deleteConfig(name) {
                if(confirm('آیا از حذف این کانفیگ مطمئن هستید؟')) {
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
        proto = "vless"
        link = f"{proto}://{req.name}@{current_host}:{req.port}?encryption=none&security=tls&type={net_type}&fp={req.fp}&alpn={req.alpn}#{req.name}"

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
  
