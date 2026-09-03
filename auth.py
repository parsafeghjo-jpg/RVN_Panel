# auth.py
from fastapi import Request, Response

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def is_authenticated(request: Request):
    return request.cookies.get("session_auth") == "logged_in_true"

def login_user(username, password, response: Response):
    if username == ADMIN_USER and password == ADMIN_PASS:
        response.set_cookie(key="session_auth", value="logged_in_true", httponly=True)
        return True
    return False

def logout_user(response: Response):
    response.delete_cookie("session_auth")

def get_login_html():
    return """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ورود به RVN Panel</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    body { font-family: 'Vazirmatn', sans-serif; background: #07090e; color: #f1f5f9; }
    .glass { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
  </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">
  <div class="glass w-full max-w-md rounded-3xl p-8 border border-slate-700/50 text-center shadow-2xl">
    <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-violet-600 to-cyan-400 mx-auto flex items-center justify-center font-black text-white text-3xl mb-4">
      RVN
    </div>
    <h2 class="text-2xl font-black text-white mb-2">ورود به پنل مدیریت</h2>
    <p class="text-xs text-violet-400 mb-6">اطلاعات مدیر را وارد کنید</p>

    <form id="loginForm" class="space-y-4 text-right text-xs">
      <div>
        <label class="block text-gray-300 mb-1 font-bold">نام کاربری</label>
        <input type="text" id="username" required placeholder="admin" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-violet-500">
      </div>
      <div>
        <label class="block text-gray-300 mb-1 font-bold">رمز عبور</label>
        <input type="password" id="password" required placeholder="••••••••" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-violet-500">
      </div>
      
      <p id="errorMsg" class="text-red-400 text-xs hidden text-center font-bold">نام کاربری یا رمز عبور اشتباه است!</p>

      <button type="submit" class="w-full py-3.5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white font-bold rounded-2xl shadow-lg text-sm mt-2">
        ورود به داشبورد
      </button>
    </form>
  </div>

  <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
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
        document.getElementById('errorMsg').classList.remove('hidden');
      }
    });
  </script>
</body>
</html>
    """
  
