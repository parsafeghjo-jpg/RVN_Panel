# pages.py

def get_dashboard_html():
    return """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RVN Panel Pro - Advanced Manual Builder</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;600;800&display=swap');
    body { font-family: 'Vazirmatn', sans-serif; background: #07090e; color: #f1f5f9; }
    .glass { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .glow-purple { box-shadow: 0 0 25px rgba(168, 85, 247, 0.15); }
    input, select { background: #0f172a !important; border-color: #334155 !important; }
    input:focus, select:focus { border-color: #8b5cf6 !important; outline: none; }
  </style>
</head>
<body class="p-4 md:p-8 min-h-screen flex flex-col justify-between">

  <div class="max-w-7xl mx-auto w-full">
    <!-- Header -->
    <header class="glass rounded-3xl p-5 mb-8 flex flex-col md:flex-row justify-between items-center gap-4 glow-purple">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-violet-600 to-cyan-400 flex items-center justify-center font-black text-white text-2xl">
          RVN
        </div>
        <div>
          <h1 class="font-extrabold text-2xl text-white">RVN Panel Pro</h1>
          <p class="text-xs text-violet-400 font-mono">● سیستم فرم پیشرفته ساخت دستی کانفیگ</p>
        </div>
      </div>
      
      <button onclick="openModal('manualModal')" class="bg-violet-600 hover:bg-violet-500 text-white text-xs font-bold px-5 py-3 rounded-2xl flex items-center gap-2 shadow-lg shadow-violet-600/30">
        <i class="fa-solid fa-sliders text-sm"></i> ساخت کانفیگ دستی
      </button>
    </header>

    <!-- Configs Table -->
    <div class="glass rounded-3xl p-6 overflow-hidden">
      <h2 class="font-extrabold text-lg text-white mb-6 flex items-center gap-2">
        <i class="fa-solid fa-list-check text-violet-400"></i> مدیریت کانفیگ‌های ساخته شده
      </h2>

      <div class="overflow-x-auto">
        <table class="w-full text-right text-xs">
          <thead>
            <tr class="text-gray-400 border-b border-slate-800/80 pb-3">
              <th class="pb-3 pr-2">نام</th>
              <th class="pb-3">پروتکل</th>
              <th class="pb-3">حجم</th>
              <th class="pb-3">مهلت (روز)</th>
              <th class="pb-3">پورت</th>
              <th class="pb-3">تنظیمات پیشرفته</th>
              <th class="pb-3">وضعیت</th>
              <th class="pb-3 text-center">عملیات</th>
            </tr>
          </thead>
          <tbody id="configTable" class="divide-y divide-slate-800/40">
            <!-- داده‌ها بارگذاری می‌شوند -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Advanced Manual Builder Modal -->
  <div id="manualModal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center z-50 p-4 overflow-y-auto">
    <div class="glass w-full max-w-2xl rounded-3xl p-6 border border-slate-700/50 glow-purple my-8">
      <div class="flex justify-between items-center mb-6 border-b border-slate-800 pb-3">
        <h3 class="font-extrabold text-white text-lg flex items-center gap-2">
          <i class="fa-solid fa-wand-magic-sparkles text-violet-400"></i> ساخت کانفیگ دستی
        </h3>
        <button onclick="closeModal('manualModal')" class="text-gray-400 hover:text-white"><i class="fa-solid fa-xmark text-xl"></i></button>
      </div>

      <form id="createForm" class="space-y-4 text-xs">
        
        <!-- Row 1: Name & Protocol -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-1 font-bold">نام کانفیگ</label>
            <input type="text" id="cfgName" required placeholder="pro-user" class="w-full rounded-xl p-2.5 text-white">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 font-bold">پروتکل</label>
            <select id="cfgProto" class="w-full rounded-xl p-2.5 text-white">
              <option value="VLESS WebSocket">VLESS WebSocket</option>
              <option value="VMess WebSocket">VMess WebSocket</option>
              <option value="Trojan gRPC">Trojan gRPC</option>
              <option value="WireGuard">WireGuard (.conf)</option>
              <option value="Hysteria2">Hysteria2</option>
            </select>
          </div>
        </div>

        <!-- Row 2: Volume & Volume Unit -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-1 font-bold">حجم (0 = نامحدود)</label>
            <input type="number" id="cfgVol" placeholder="0" class="w-full rounded-xl p-2.5 text-white">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 font-bold">واحد حجم</label>
            <select id="cfgUnit" class="w-full rounded-xl p-2.5 text-white">
              <option value="GB">GB</option>
              <option value="MB">MB</option>
            </select>
          </div>
        </div>

        <!-- Row 3: Days & IP Limit -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-1 font-bold">تعداد روز (0 = نامحدود)</label>
            <input type="number" id="cfgDays" placeholder="0" class="w-full rounded-xl p-2.5 text-white">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 font-bold">محدودیت IP (0 = نامحدود)</label>
            <input type="number" id="cfgIp" placeholder="0" class="w-full rounded-xl p-2.5 text-white">
          </div>
        </div>

        <!-- Row 4: Speed Limit & Connection Limit -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-1 font-bold">محدودیت اتصال (0 = نامحدود)</label>
            <input type="number" id="cfgConnLimit" placeholder="0" class="w-full rounded-xl p-2.5 text-white">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 font-bold">سرعت (Mbps - 0 = نامحدود)</label>
            <input type="number" id="cfgSpeed" placeholder="0" class="w-full rounded-xl p-2.5 text-white">
          </div>
        </div>

        <!-- Row 5: Fingerprint & Fragment -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-1 font-bold">Fingerprint</label>
            <select id="cfgFp" class="w-full rounded-xl p-2.5 text-white">
              <option value="chrome">Chrome</option>
              <option value="firefox">Firefox</option>
              <option value="safari">Safari</option>
              <option value="randomize">Randomize</option>
            </select>
          </div>
          <div>
            <label class="block text-gray-300 mb-1 font-bold">Fragment</label>
            <select id="cfgFrag" class="w-full rounded-xl p-2.5 text-white">
              <option value="خاموش">خاموش</option>
              <option value="10-20,10-20,tlshello">TLS Hello (10-20)</option>
              <option value="100-200,10-20,random">Random Fragment</option>
            </select>
          </div>
        </div>

        <!-- Row 6: Port & ALPN -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-1 font-bold">Port</label>
            <input type="number" id="cfgPort" value="443" class="w-full rounded-xl p-2.5 text-white">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 font-bold">ALPN</label>
            <select id="cfgAlpn" class="w-full rounded-xl p-2.5 text-white">
              <option value="http/1.1">http/1.1</option>
              <option value="h2">h2</option>
              <option value="h2,http/1.1">h2,http/1.1</option>
            </select>
          </div>
        </div>

        <!-- Row 7: Note -->
        <div>
          <label class="block text-gray-300 mb-1 font-bold">یادداشت</label>
          <input type="text" id="cfgNote" placeholder="توضیحات دلخواه..." class="w-full rounded-xl p-2.5 text-white">
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-4 border-t border-slate-800">
          <button type="button" onclick="closeModal('manualModal')" class="px-6 py-3 bg-slate-800 text-gray-300 rounded-2xl font-bold">انصراف</button>
          <button type="submit" class="px-8 py-3 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-bold rounded-2xl shadow-lg shadow-violet-600/30">ساخت کانفیگ</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    function openModal(id) { document.getElementById(id).classList.remove('hidden'); document.getElementById(id).classList.add('flex'); }
    function closeModal(id) { document.getElementById(id).classList.add('hidden'); document.getElementById(id).classList.remove('flex'); }

    async function loadConfigs() {
      const res = await fetch('/api/get-configs');
      const data = await res.json();
      const tbody = document.getElementById('configTable');
      tbody.innerHTML = '';

      data.forEach(item => {
        const volText = (!item.volume || item.volume == 0) ? '<span class="text-purple-400 font-bold">نامحدود ∞</span>' : `${item.volume} ${item.unit}`;
        const daysText = (!item.days || item.days == 0) ? '<span class="text-purple-400 font-bold">نامحدود ∞</span>' : `${item.days} روز`;
        
        tbody.innerHTML += `
          <tr class="hover:bg-slate-800/30 transition-all">
            <td class="py-4 pr-2 font-bold text-white">${item.name}</td>
            <td class="py-4"><span class="px-3 py-1 rounded-full text-[10px] font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">${item.protocol}</span></td>
            <td class="py-4 font-mono text-gray-300">${volText}</td>
            <td class="py-4 font-mono text-gray-300">${daysText}</td>
            <td class="py-4 font-mono text-gray-300">${item.port}</td>
            <td class="py-4 text-[10px] text-gray-400">FP: ${item.fp} | ALPN: ${item.alpn}</td>
            <td class="py-4"><span class="px-3 py-1 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">فعال</span></td>
            <td class="py-4 text-center">
              <button onclick="copyText('${item.link}')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded-xl mr-1 font-bold"><i class="fa-regular fa-copy"></i> کپی</button>
              <button onclick="deleteConfig('${item.name}')" class="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl"><i class="fa-solid fa-trash-can"></i></button>
            </td>
          </tr>
        `;
      });
    }

    document.getElementById('createForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const payload = {
        name: document.getElementById('cfgName').value,
        protocol: document.getElementById('cfgProto').value,
        volume: parseFloat(document.getElementById('cfgVol').value || 0),
        unit: document.getElementById('cfgUnit').value,
        days: parseInt(document.getElementById('cfgDays').value || 0),
        ip_limit: parseInt(document.getElementById('cfgIp').value || 0),
        conn_limit: parseInt(document.getElementById('cfgConnLimit').value || 0),
        speed: parseInt(document.getElementById('cfgSpeed').value || 0),
        fp: document.getElementById('cfgFp').value,
        frag: document.getElementById('cfgFrag').value,
        port: parseInt(document.getElementById('cfgPort').value || 443),
        alpn: document.getElementById('cfgAlpn').value,
        note: document.getElementById('cfgNote').value
      };

      const res = await fetch('/api/create-config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });

      const result = await res.json();
      if(result.status === 'ok') {
        if(payload.protocol === 'WireGuard' && result.config.wireguard_file) {
          downloadFile(`${payload.name}.conf`, result.config.wireguard_file);
        }
        closeModal('manualModal');
        loadConfigs();
      }
    });

    function downloadFile(filename, content) {
      const el = document.createElement('a');
      el.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
      el.setAttribute('download', filename);
      el.click();
    }

    function copyText(txt) {
      navigator.clipboard.writeText(txt);
      alert('لینک کانفیگ کپی شد!');
    }

    async function deleteConfig(name) {
      if(confirm('کانفیگ حذف شود؟')) {
        await fetch('/api/delete-config?name=' + name, { method: 'DELETE' });
        loadConfigs();
      }
    }

    loadConfigs();
  </script>
</body>
</html>
    """
  
