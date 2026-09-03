# pages.py
def get_dashboard_html():
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>RVN Panel Pro</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
        <style>body { font-family: 'Vazirmatn', sans-serif; }</style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen p-6">
        <div class="max-w-6xl mx-auto">
            <header class="flex justify-between items-center mb-8 bg-slate-900 border border-slate-800 p-6 rounded-3xl">
                <div>
                    <h1 class="text-xl font-black text-white">RVN Panel Pro</h1>
                    <p class="text-xs text-slate-400 mt-1">سیستم پیشرفته مدیریت دستی کانفیگ‌ها</p>
                </div>
                <button onclick="logout()" class="px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-bold rounded-xl transition">خروج از حساب</button>
            </header>

            <!-- کادر ثابت نمودار مصرف شبکه -->
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-3xl mb-8">
                <h2 class="font-extrabold text-sm text-white mb-4">📊 نمودار مصرف شبکه</h2>
                <div style="height:220px; position:relative;">
                    <canvas id="usageChart"></canvas>
                </div>
            </div>

            <!-- فرم ساخت کانفیگ -->
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-3xl mb-8">
                <h2 class="text-sm font-bold text-violet-400 mb-4">ساخت کانفیگ جدید</h2>
                <form onsubmit="createConfig(event)" class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                    <div>
                        <label class="block text-slate-400 mb-1">نام کانفیگ</label>
                        <input type="text" id="cfgName" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white" value="pro-sample" required>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1">پروتکل</label>
                        <select id="cfgProto" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white">
                            <option>Vless WS</option>
                            <option>Vless gRPC</option>
                            <option>WireGuard</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1">حجم (GB)</label>
                        <input type="number" id="cfgVol" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white" value="25">
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1">مدت زمان (روز)</label>
                        <input type="number" id="cfgDays" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white" value="30">
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1">پورت</label>
                        <input type="number" id="cfgPort" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white" value="443">
                    </div>
                    <div class="flex items-end">
                        <button type="submit" class="w-full bg-violet-600 hover:bg-violet-700 text-white font-bold py-2 rounded-xl transition">ساخت کانفیگ</button>
                    </div>
                </form>
            </div>

            <!-- جدول مدیریت کانفیگ‌ها -->
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-3xl">
                <h2 class="text-sm font-bold text-white mb-4">مدیریت کانفیگ‌های ساخته شده</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-right border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-xs text-slate-400">
                                <th class="p-3">نام</th>
                                <th class="p-3">پروتکل</th>
                                <th class="p-3">حجم</th>
                                <th class="p-3">مدت</th>
                                <th class="p-3">پورت</th>
                                <th class="p-3">تنظیمات</th>
                                <th class="p-3">وضعیت</th>
                                <th class="p-3 text-center">عملیات</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- بارگذاری پویا -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
  
