# main_pro.py
import os
import uvicorn
from fastapi import FastAPI, Response, Request
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
    
    html = get_dashboard_html()
    
    # تزریق کامل Chart.js، نمودار، دکمه کپی، حذف و خروج
    full_ui_script = """
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
      // ۱. اضافه کردن بلوک نمودار به بالای جدول اگر وجود نداشته باشد
      document.addEventListener('DOMContentLoaded', () => {
        const header = document.querySelector('header');
        if (header && !document.getElementById('usageChartContainer')) {
          const chartDiv = document.createElement('div');
          chartDiv.id = 'usageChartContainer';
          chartDiv.className = 'glass rounded-3xl p-6 mb-8 glow-purple';
          chartDiv.innerHTML = '<h2 class="font-extrabold text-lg text-white mb-4 flex items-center gap-2"><i class="fa-solid fa-chart-line text-violet-400"></i> نمودار مصرف شبکه</h2><div style="height:250px;"><canvas id="usageChart"></canvas></div>';
          header.after(chartDiv);

          const ctx = document.getElementById('usageChart').getContext('2d');
          new Chart(ctx, {
            type: 'line',
            data: {
              labels: ['۶ روز پیش', '۵ روز پیش', '۴ روز پیش', '۳ روز پیش', '۲ روز پیش', 'دیروز', 'امروز'],
              datasets: [{
                label: 'مصرف ترافیک (GB)',
                data: [10, 25, 40, 35, 60, 50, 90],
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.15)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { labels: { color: '#fff' } } },
              scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
              }
            }
          });
        }
        refreshConfigs();
      });

      // ۲. کپی کردن لینک
      function copyText(txt) {
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(txt).then(() => alert('لینک کانفیگ کپی شد!'));
        } else {
          let t = document.createElement("textarea");
          t.value = txt;
          document.body.appendChild(t);
          t.select();
          document.execCommand('copy');
          document.body.removeChild(t);
          alert('لینک کانفیگ کپی شد!');
        }
      }

      // ۳. به‌روزرسانی جدول
      async function refreshConfigs() {
        const res = await fetch('/api/get-configs');
        const configs = await res.json();
        const tbody = document.getElementById('configTable') || document.querySelector('tbody');
        if (!tbody) return;

        let html = '';
        configs.forEach(c => {
          html += `
            <tr class="border-b border-slate-800/40 hover:bg-slate-800/30 transition text-center">
              <td class="py-4 pr-2 font-bold text-white text-right">${c.name}</td>
              <td class="py-4"><span class="px-3 py-1 rounded-full text-[10px] font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">${c.protocol}</span></td>
              <td class="py-4 font-mono text-gray-300">${c.volume} ${c.unit}</td>
              <td class="py-4 font-mono text-gray-300">${c.days} روز</td>
              <td class="py-4 font-mono text-gray-300">${c.port}</td>
              <td class="py-4 text-[10px] text-gray-400">FP: ${c.fp} | ALPN: ${c.alpn}</td>
              <td class="py-4"><span class="px-3 py-1 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">فعال</span></td>
              <td class="py-4 flex justify-center gap-2">
                <button onclick="copyText('${c.link}')" class="px-3 py-1.5 bg-violet-600 hover:bg-violet-700 text-white rounded-xl font-bold shadow-lg shadow-violet-600/20">📋 کپی</button>
                <button onclick="deleteConfig('${c.name}')" class="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl font-bold">🗑️</button>
              </td>
            </tr>
          `;
        });
        tbody.innerHTML = html;
      }

      // ۴. حذف کانفیگ
      async function deleteConfig(name) {
        if(confirm('کانفیگ حذف شود؟')) {
          await fetch('/api/delete-config?name=' + encodeURIComponent(name), { method: 'DELETE' });
          refreshConfigs();
        }
      }

      // ۵. خروج
      async function logout() {
        await fetch('/api/logout', { method: 'POST' });
        window.location.reload();
      }
    </script>
    """
    return html.replace("</body>", f"{full_ui_script}</body>")

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
    uvicorn.run("main_pro:app", host="0.0.0.0", port=port, reload=True)
          
