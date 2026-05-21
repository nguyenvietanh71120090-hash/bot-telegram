import json, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8791243948:AAF-IBPovuIqfh7NVSt8kvhLYstfhdhB0XI"
ADMIN_ID = 123456789 

def load_db():
    if not os.path.exists("db.json"):
        return {"users": {}, "data": [], "proxy": [], "orders": {}, "vouchers": {}, "config": {"note": True, "v_price": 50000, "locked": []}}
    with open("db.json", "r") as f: return json.load(f)

def save_db(db):
    with open("db.json", "w") as f: json.dump(db, f, indent=4)

# --- CÁC HÀM XỬ LÝ (LOGIC) ---
async def cmd_start(u: Update, c): await u.message.reply_text("🌸 Bot Đã Sẵn Sàng!")
async def cmd_naptien(u: Update, c): await u.message.reply_text("💰 Chuyển khoản STK: 12345 - Nội dung: NAP <ID>")
async def cmd_add(u: Update, c):
    db = load_db()
    sdt = c.args[0] if c.args else ""
    res = [d for d in db['data'] if sdt in d]
    await u.message.reply_text(f"Kết quả: {res[0]}" if res else "Không thấy!")

async def cmd_themdata(u: Update, c):
    db = load_db()
    if u.message.reply_to_message:
        for line in u.message.reply_to_message.text.split('\n'):
            if '|' in line: db['data'].append(line)
    save_db(db); await u.message.reply_text("✅ Đã thêm data.")

async def cmd_xoadata(u: Update, c):
    db = load_db()
    search = c.args[0] if c.args else ""
    db['data'] = [d for d in db['data'] if search not in d]
    save_db(db); await u.message.reply_text("🗑️ Đã xóa.")

# --- CÁC LỆNH ADMIN (PHẢI CÓ ĐIỀU KIỆN ADMIN_ID) ---
async def cmd_cong(u: Update, c):
    if u.effective_user.id != ADMIN_ID: return
    db = load_db()
    db['users'].setdefault(c.args[0], {"balance": 0})
    db['users'][c.args[0]]["balance"] += int(c.args[1])
    save_db(db); await u.message.reply_text("✅ Đã cộng.")

async def cmd_khoa(u: Update, c):
    if u.effective_user.id != ADMIN_ID: return
    db = load_db()
    db['config']['locked'].append(c.args[0])
    save_db(db); await u.message.reply_text("🔒 Đã khóa.")

# ... (Bạn có thể thêm các hàm /tru, /xacnhan, /themproxy tương tự ở đây)

# --- ĐĂNG KÝ LỆNH ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", cmd_start))
app.add_handler(CommandHandler("naptien", cmd_naptien))
app.add_handler(CommandHandler("add", cmd_add))
app.add_handler(CommandHandler("themdata", cmd_themdata))
app.add_handler(CommandHandler("xoadata", cmd_xoadata))
app.add_handler(CommandHandler("cong", cmd_cong))
app.add_handler(CommandHandler("khoa", cmd_khoa))

app.run_polling()
