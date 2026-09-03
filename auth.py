# auth.py
from fastapi import Response, Request

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def is_authenticated(request: Request) -> bool:
    return request.cookies.get("session") == "authenticated_admin"

def login_user(username: str, password: str, response: Response) -> bool:
    if username == ADMIN_USER and password == ADMIN_PASS:
        response.set_cookie(key="session", value="authenticated_admin", httponly=True)
        return True
    return False

def logout_user(response: Response):
    response.delete_cookie(key="session")

def get_login_html():
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>ورود به پنل مدیریت RVN</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
        <style>body { font-family: 'Vazirmatn', sans-serif; }</style>
    </head>
    <body class="bg-slate-950 text-white flex items-center justify-center h-screen m-0">
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-2xl w-96">
            <h2 class="text-xl font-black mb-6 text-center text-violet-400">RVN Panel Pro</h2>
            <form onsubmit="handleLogin(event)" class="space-y-4">
                <div>
                    <label class="block text-xs text-slate-400 mb-1">نام کاربری</label>
                    <input type="text" id="username" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-violet-500" required>
                </div>
                <div>
                    <label class="block text-xs text-slate-400 mb-1">رمز عبور</label>
                    <input type="password" id="password" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-violet-500" required>
                </div>
                <button type="submit" class="w-full bg-violet-600 hover:bg-violet-700 font-bold py-3 rounded-xl transition text-sm">ورود به پنل</button>
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
                if(data.status === 'ok') {
                    window.location.reload();
                } else {
                    document.getElementById('error').classList.remove('hidden');
                }
            }
        </script>
    </body>
    </html>
    """
  
