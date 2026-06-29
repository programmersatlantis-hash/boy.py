import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import re
import json
import os
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, FloodWait

# ======================== تنظیمات ========================
TOKEN = "8938238778:AAGIgpPvXaC-_jXLfCvGniBIqt8mr65NCg8"
CHANNEL_LINK = "https://t.me/Sazandeye_Maskan_news"
CHANNEL_USERNAME = "@Sazandeye_Maskan_news"

API_ID = 33522742
API_HASH = "6336429ffba8810dcd0d03b2a05e567b"
ADMIN_ID = 8635643219

# ======================== دیتابیس JSON ========================
DB_FILE = "data.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# بارگذاری دیتا
db = load_data()
users_data = db.get('users_data', {})
user_settings = db.get('user_settings', {})
user_font = db.get('user_font', {})
user_custom_name = db.get('user_custom_name', {})

user_clients = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======================== فونت‌ها ========================
FONTS = {
    "𝕊𝕥𝕪𝕝𝕚𝕤𝕙": "𝕊𝕥𝕪𝕝𝕚𝕤𝕙",
    "𝓢𝓽𝔂𝓵𝓲𝓼𝓱": "𝓢𝓽𝔂𝓵𝓲𝓼𝓱",
    "𝘚𝘵𝘺𝘭𝘪𝘴𝘩": "𝘚𝘵𝘺𝘭𝘪𝘴𝘩",
    "🅂🅃🅈🄻🄸🅂🄷": "Bubble",
    "𝑺𝒕𝒚𝒍𝒊𝒔𝒉": "Cursive",
    "𝚂𝚝𝚢𝚕𝚒𝚜𝚑": "Monospace",
    "Sᴛʏʟɪsʜ": "Small Caps",
    "S͎t͎y͎l͎i͎s͎h͎": "Underline",
    "S⃟t⃟y⃟l⃟i⃟s⃟h⃟": "Dotted",
    "S̷t̷y̷l̷i̷s̷h̷": "Strike",
    "S̲t̲y̲l̲i̲s̲h̲": "Underline2"
}

def apply_font(text: str, font_name: str) -> str:
    fonts = {
        "𝕊𝕥𝕪𝕝𝕚𝕤𝕙": {
            'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼',
            'F': '𝔽', 'G': '𝔾', 'H': 'ℍ', 'I': '𝕀', 'J': '𝕁',
            'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ', 'O': '𝕆',
            'P': 'ℙ', 'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋',
            'U': '𝕌', 'V': '𝕍', 'W': '𝕎', 'X': '𝕏', 'Y': '𝕐', 'Z': 'ℤ',
            'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖',
            'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛',
            'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠',
            'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥',
            'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫',
            '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜',
            '5': '𝟝', '6': '𝟞', '7': '𝟟', '8': '𝟠', '9': '𝟡', ':': ':'
        },
        "𝓢𝓽𝔂𝓵𝓲𝓼𝓱": {
            'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔',
            'F': '𝓕', 'G': '𝓖', 'H': '𝓗', 'I': '𝓘', 'J': '𝓙',
            'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞',
            'P': '𝓟', 'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣',
            'U': '𝓤', 'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩',
            'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮',
            'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲', 'j': '𝓳',
            'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸',
            'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽',
            'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃',
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', ':': ':'
        },
        "𝘚𝘵𝘺𝘭𝘪𝘴𝘩": {
            'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌',
            'F': '𝘍', 'G': '𝘎', 'H': '𝘏', 'I': '𝘐', 'J': '𝘑',
            'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕', 'O': '𝘖',
            'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛',
            'U': '𝘜', 'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡',
            'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦',
            'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪', 'j': '𝘫',
            'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰',
            'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵',
            'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻',
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', ':': ':'
        },
        "S͎t͎y͎l͎i͎s͎h͎": {
            '0': '0͎', '1': '1͎', '2': '2͎', '3': '3͎', '4': '4͎',
            '5': '5͎', '6': '6͎', '7': '7͎', '8': '8͎', '9': '9͎', ':': ':͎'
        },
        "S̷t̷y̷l̷i̷s̷h̷": {
            '0': '0̷', '1': '1̷', '2': '2̷', '3': '3̷', '4': '4̷',
            '5': '5̷', '6': '6̷', '7': '7̷', '8': '8̷', '9': '9̷', ':': ':̷'
        },
        "S̲t̲y̲l̲i̲s̲h̲": {
            '0': '0̲', '1': '1̲', '2': '2̲', '3': '3̲', '4': '4̲',
            '5': '5̲', '6': '6̲', '7': '7̲', '8': '8̲', '9': '9̲', ':': ':̲'
        }
    }
    
    font_map = fonts.get(font_name, {})
    if not font_map:
        return text
    
    result = ""
    for char in text:
        if char in font_map:
            result += font_map[char]
        else:
            result += char
    return result

def convert_time_to_font(time_str: str, font_name: str) -> str:
    return apply_font(time_str, font_name)

def save_all_data():
    db = {
        'users_data': users_data,
        'user_settings': user_settings,
        'user_font': user_font,
        'user_custom_name': user_custom_name
    }
    save_data(db)
    logger.info("✅ دیتا ذخیره شد")

# ======================== توابع اصلی ========================
async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

async def set_username_with_time(user_id: int):
    data = users_data.get(str(user_id))
    if not data:
        return False
    
    try:
        session_name = data.get('session_name', f'session_{user_id}')
        
        client = Client(
            session_name,
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=data['phone']
        )
        
        await client.connect()
        
        try:
            me = await client.get_me()
        except Exception:
            await client.disconnect()
            return False
        
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        
        font_name = user_font.get(str(user_id), "𝕊𝕥𝕪𝕝𝕚𝕤𝕙")
        styled_time = convert_time_to_font(time_str, font_name)
        
        custom_name = user_custom_name.get(str(user_id), "مسکن")
        new_name = f"{custom_name} | {styled_time}"
        
        await client.update_profile(first_name=new_name)
        await client.disconnect()
        
        logger.info(f"✅ نام کاربر {user_id} به '{new_name}' تغییر یافت")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطا در تغییر نام: {e}")
        return False

async def update_time_for_user(user_id: int):
    if not user_settings.get(str(user_id), False):
        return
    await set_username_with_time(user_id)

async def schedule_updates():
    while True:
        now = datetime.now()
        wait_seconds = 60 - now.second
        await asyncio.sleep(wait_seconds)
        
        for user_id in list(user_settings.keys()):
            if user_settings.get(user_id, False):
                await update_time_for_user(int(user_id))

# ======================== هندلرهای ربات ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    if not await check_membership(user.id, context):
        keyboard = [[InlineKeyboardButton("📢 عضویت در کانال", url=CHANNEL_LINK)]]
        await update.message.reply_text(
            f"🚫 {user.first_name} عزیز، ابتدا در کانال عضو شوید!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📝 ثبت‌نام", callback_data='register')],
        [InlineKeyboardButton("🎨 سلف تایم (فونت)", callback_data='font_menu')],
        [InlineKeyboardButton("ℹ️ وضعیت", callback_data='status')],
        [InlineKeyboardButton("🔧 تنظیمات", callback_data='settings')],
        [InlineKeyboardButton("📖 راهنما", callback_data='help')]
    ]
    
    if await is_admin(user.id):
        keyboard.append([InlineKeyboardButton("👑 پنل مدیریت", callback_data='admin_panel')])
    
    font_name = user_font.get(user_id, "𝕊𝕥𝕪𝕝𝕚𝕤𝕙")
    custom_name = user_custom_name.get(user_id, "مسکن")
    
    await update.message.reply_text(
        f"🎉 **به ربات مسکن خوش آمدید {user.first_name}!**\n\n"
        "🏠 تنظیم خودکار ساعت روی نام کاربری\n"
        "⏰ به‌روزرسانی هر دقیقه\n"
        f"📛 اسم انتخابی: {custom_name}\n"
        f"🎨 فونت فعلی: {font_name}\n\n"
        "🎨 **سلف تایم (فونت) رایگان!**\n\n"
        "📌 از منوی زیر انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    if not await check_membership(int(user_id), context):
        await query.edit_message_text("❌ ابتدا در کانال عضو شوید!")
        return
    
    await query.edit_message_text(
        "📱 **مرحله 1 از 3: وارد کردن شماره تلفن**\n\n"
        "لطفاً شماره تلفن خود را با کد کشور وارد کنید:\n"
        "مثال: +989123456789"
    )
    context.user_data['step'] = 'phone'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    step = context.user_data.get('step')
    
    if not await check_membership(int(user_id), context):
        await update.message.reply_text("❌ ابتدا در کانال عضو شوید!")
        return
    
    # ===== مرحله 1: دریافت شماره =====
    if step == 'phone':
        if re.match(r'^\+?\d{10,15}$', text):
            phone = text
            
            users_data[user_id] = {
                'phone': phone,
                'session_name': f'session_{user_id}'
            }
            save_all_data()
            
            try:
                client = Client(
                    f'session_{user_id}',
                    api_id=API_ID,
                    api_hash=API_HASH
                )
                await client.connect()
                
                sent_code = await client.send_code(phone)
                
                user_clients[user_id] = {
                    'client': client,
                    'phone_code_hash': sent_code.phone_code_hash,
                    'phone': phone
                }
                
                context.user_data['step'] = 'code'
                
                await update.message.reply_text(
                    "✅ **مرحله 2 از 3: تایید کد**\n\n"
                    "📨 کد ۵ رقمی به شماره شما ارسال شد.\n"
                    "⏳ لطفاً کد را وارد کنید:"
                )
                
            except PhoneNumberInvalid:
                await update.message.reply_text(
                    "❌ شماره تلفن نامعتبر!\nمثال: +989123456789"
                )
                context.user_data['step'] = 'phone'
            except Exception as e:
                await update.message.reply_text(f"❌ خطا: {str(e)}")
                context.user_data['step'] = None
        else:
            await update.message.reply_text(
                "❌ شماره نامعتبر!\nمثال: +989123456789"
            )
    
    # ===== مرحله 2: دریافت کد =====
    elif step == 'code':
        code = text.strip()
        
        if user_id not in user_clients:
            await update.message.reply_text("❌ جلسه منقضی! لطفاً /start کنید.")
            return
        
        try:
            client_data = user_clients[user_id]
            client = client_data['client']
            
            await client.sign_in(
                phone_number=client_data['phone'],
                phone_code=code,
                phone_code_hash=client_data['phone_code_hash']
            )
            
            context.user_data['step'] = 'custom_name'
            
            await client.disconnect()
            del user_clients[user_id]
            
            await update.message.reply_text(
                "✅ **مرحله 3 از 3: انتخاب اسم دلخواه**\n\n"
                "لطفاً اسمی که می‌خواهید روی اکانتتان نمایش داده شود را وارد کنید:\n"
                "مثال: مسکن, خانه من, سلف ساز, ..."
            )
            
        except PhoneCodeExpired:
            await update.message.reply_text("❌ کد منقضی شد! لطفاً /start کنید.")
            context.user_data['step'] = None
            if user_id in user_clients:
                await user_clients[user_id]['client'].disconnect()
                del user_clients[user_id]
                
        except PhoneCodeInvalid:
            await update.message.reply_text("❌ کد نامعتبر! دوباره وارد کنید:")
            
        except SessionPasswordNeeded:
            await update.message.reply_text("🔐 اکانت دو مرحله‌ای! رمز را وارد کنید:")
            context.user_data['step'] = 'password'
            
        except Exception as e:
            await update.message.reply_text(f"❌ خطا: {str(e)}\nلطفاً /start کنید.")
            context.user_data['step'] = None
    
    # ===== مرحله 3: دریافت اسم دلخواه =====
    elif step == 'custom_name':
        custom_name = text.strip()
        
        if len(custom_name) < 2 or len(custom_name) > 30:
            await update.message.reply_text(
                "❌ اسم باید بین ۲ تا ۳۰ کاراکتر باشد!\n"
                "دوباره وارد کنید:"
            )
            return
        
        user_custom_name[user_id] = custom_name
        user_settings[user_id] = True
        context.user_data['step'] = None
        save_all_data()
        
        await update.message.reply_text("⏳ در حال تنظیم ساعت...")
        
        success = await set_username_with_time(int(user_id))
        
        keyboard = [
            [InlineKeyboardButton("⏸ خاموش", callback_data='toggle')],
            [InlineKeyboardButton("🎨 سلف تایم (فونت)", callback_data='font_menu')],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ]
        
        if success:
            now = datetime.now()
            font_name = user_font.get(user_id, "𝕊𝕥𝕪𝕝𝕚𝕤𝕙")
            styled_time = convert_time_to_font(now.strftime("%H:%M"), font_name)
            await update.message.reply_text(
                f"✅ **ثبت‌نام موفق!**\n\n"
                f"📛 اسم شما: {custom_name}\n"
                f"⏰ ساعت: {custom_name} | {styled_time}\n\n"
                "هر دقیقه به‌روزرسانی می‌شود.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                "⚠️ ثبت‌نام موفق بود اما تغییر نام انجام نشد!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    # ===== رمز دو مرحله‌ای =====
    elif step == 'password':
        password = text
        
        if user_id not in user_clients:
            await update.message.reply_text("❌ جلسه منقضی! لطفاً /start کنید.")
            return
        
        try:
            client = user_clients[user_id]['client']
            
            await client.check_password(password)
            await client.sign_in(password=password)
            
            context.user_data['step'] = 'custom_name'
            
            await client.disconnect()
            del user_clients[user_id]
            
            await update.message.reply_text(
                "✅ **مرحله 3 از 3: انتخاب اسم دلخواه**\n\n"
                "لطفاً اسمی که می‌خواهید روی اکانتتان نمایش داده شود را وارد کنید:"
            )
            
        except Exception as e:
            await update.message.reply_text("❌ رمز اشتباه! دوباره وارد کنید:")

# ======================== منوی فونت ========================
async def font_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    row = []
    for i, (font_name, font_desc) in enumerate(FONTS.items()):
        row.append(InlineKeyboardButton(font_name, callback_data=f'font_{font_desc}'))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')])
    
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    preview = convert_time_to_font(time_str, list(FONTS.keys())[0])
    
    await query.edit_message_text(
        f"🎨 **انتخاب فونت سلف تایم**\n\n"
        f"⏰ پیش‌نمایش: {preview}\n\n"
        "👇 یکی از فونت‌های زیر را انتخاب کنید **(رایگان)**:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def select_font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    font_desc = query.data.replace('font_', '')
    
    selected_font = None
    for font_name, font_desc_value in FONTS.items():
        if font_desc_value == font_desc:
            selected_font = font_name
            break
    
    if not selected_font:
        await query.edit_message_text("❌ فونت نامعتبر!")
        return
    
    user_font[user_id] = selected_font
    save_all_data()
    await set_username_with_time(int(user_id))
    
    now = datetime.now()
    custom_name = user_custom_name.get(user_id, "مسکن")
    time_str = now.strftime("%H:%M")
    preview = convert_time_to_font(time_str, selected_font)
    
    await query.edit_message_text(
        f"✅ **فونت با موفقیت انتخاب شد!**\n\n"
        f"🎨 فونت: {selected_font}\n"
        f"⏰ پیش‌نمایش: {preview}\n\n"
        f"🔰 نام جدید شما: {custom_name} | {preview}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 تغییر فونت", callback_data='font_menu')],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ])
    )

# ======================== دکمه‌های مدیریتی ========================
async def toggle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    current = user_settings.get(user_id, True)
    user_settings[user_id] = not current
    save_all_data()
    
    status = "🟢 روشن" if user_settings[user_id] else "🔴 خاموش"
    button_text = "⏸ خاموش" if user_settings[user_id] else "▶️ روشن"
    
    await query.edit_message_text(
        f"⚙️ وضعیت: {status}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(button_text, callback_data='toggle')],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ])
    )

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    if user_id not in users_data:
        await query.edit_message_text(
            "❌ ثبت‌نام نکرده‌اید!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 ثبت‌نام", callback_data='register')],
                [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
            ])
        )
        return
    
    data = users_data[user_id]
    status = "🟢 روشن" if user_settings.get(user_id, False) else "🔴 خاموش"
    now = datetime.now()
    font_name = user_font.get(user_id, "𝕊𝕥𝕪𝕝𝕚𝕤𝕙")
    styled_time = convert_time_to_font(now.strftime("%H:%M"), font_name)
    custom_name = user_custom_name.get(user_id, "مسکن")
    
    await query.edit_message_text(
        f"📊 **وضعیت اکانت**\n\n"
        f"📱 شماره: {data['phone']}\n"
        f"📛 اسم: {custom_name}\n"
        f"⏰ زمان: {styled_time}\n"
        f"🎨 فونت: {font_name}\n"
        f"⚙️ ساعت: {status}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 به‌روزرسانی", callback_data='status')],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ])
    )

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    keyboard = [
        [InlineKeyboardButton("🎨 سلف تایم (فونت)", callback_data='font_menu')],
        [InlineKeyboardButton("⏸ خاموش/روشن", callback_data='toggle')],
        [InlineKeyboardButton("🔄 تغییر اسم", callback_data='change_name')],
        [InlineKeyboardButton("🗑 حذف اطلاعات", callback_data='delete_data')],
        [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
    ]
    
    if await is_admin(int(user_id)):
        keyboard.append([InlineKeyboardButton("👑 پنل مدیریت", callback_data='admin_panel')])
    
    await query.edit_message_text(
        "🔧 **تنظیمات**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def change_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔄 **تغییر اسم دلخواه**\n\n"
        "اسم جدید خود را وارد کنید:"
    )
    context.user_data['step'] = 'change_name'

async def change_name_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    
    if context.user_data.get('step') != 'change_name':
        return
    
    if len(text) < 2 or len(text) > 30:
        await update.message.reply_text(
            "❌ اسم باید بین ۲ تا ۳۰ کاراکتر باشد!\n"
            "دوباره وارد کنید:"
        )
        return
    
    user_custom_name[user_id] = text
    context.user_data['step'] = None
    save_all_data()
    
    await set_username_with_time(int(user_id))
    
    now = datetime.now()
    font_name = user_font.get(user_id, "𝕊𝕥𝕪𝕝𝕚𝕤𝕙")
    styled_time = convert_time_to_font(now.strftime("%H:%M"), font_name)
    
    await update.message.reply_text(
        f"✅ **اسم شما تغییر کرد!**\n\n"
        f"📛 اسم جدید: {text}\n"
        f"⏰ نام کامل: {text} | {styled_time}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ])
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📖 **راهنمای کامل ربات مسکن**\n\n"
        "1️⃣ **ثبت‌نام:**\n"
        "   • وارد کردن شماره تلفن\n"
        "   • وارد کردن کد تایید\n"
        "   • انتخاب اسم دلخواه\n\n"
        "2️⃣ **سلف تایم (فونت):**\n"
        "   • ۱۱ فونت مختلف **(رایگان)**\n"
        "   • نمایش ساعت با فونت خاص\n"
        "   • تغییر خودکار هر دقیقه\n\n"
        "3️⃣ **دستورات:**\n"
        "   • /start - شروع مجدد",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ])
    )

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    keyboard = [
        [InlineKeyboardButton("📝 ثبت‌نام", callback_data='register')],
        [InlineKeyboardButton("🎨 سلف تایم (فونت)", callback_data='font_menu')],
        [InlineKeyboardButton("ℹ️ وضعیت", callback_data='status')],
        [InlineKeyboardButton("🔧 تنظیمات", callback_data='settings')],
        [InlineKeyboardButton("📖 راهنما", callback_data='help')]
    ]
    
    if await is_admin(int(user_id)):
        keyboard.append([InlineKeyboardButton("👑 پنل مدیریت", callback_data='admin_panel')])
    
    await query.edit_message_text(
        "🏠 **منوی اصلی**\n\n"
        "لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def delete_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    if user_id in users_data:
        del users_data[user_id]
    if user_id in user_settings:
        del user_settings[user_id]
    if user_id in user_clients:
        await user_clients[user_id]['client'].disconnect()
        del user_clients[user_id]
    if user_id in user_font:
        del user_font[user_id]
    if user_id in user_custom_name:
        del user_custom_name[user_id]
    
    save_all_data()
    
    await query.edit_message_text(
        "🗑 اطلاعات حذف شد!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data='main_menu')]
        ])
    )

# ======================== پنل مدیریت ========================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if not await is_admin(user_id):
        await query.edit_message_text("❌ شما دسترسی به این بخش ندارید!")
        return
    
    total_users = len(users_data)
    active_users = sum(1 for v in user_settings.values() if v)
    
    keyboard = [
        [InlineKeyboardButton("📊 آمار کاربران", callback_data='admin_stats')],
        [InlineKeyboardButton("📨 پیام همگانی", callback_data='admin_broadcast')],
        [InlineKeyboardButton("👥 لیست کاربران", callback_data='admin_users')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='main_menu')]
    ]
    
    await query.edit_message_text(
        f"👑 **پنل مدیریت**\n\n"
        f"📊 آمار کلی:\n"
        f"👥 کل کاربران: {total_users}\n"
        f"🟢 کاربران فعال: {active_users}\n"
        f"🔴 غیرفعال: {total_users - active_users}\n\n"
        "از دکمه‌های زیر استفاده کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if not await is_admin(user_id):
        return
    
    total = len(users_data)
    active = sum(1 for v in user_settings.values() if v)
    
    await query.edit_message_text(
        f"📊 **آمار دقیق کاربران**\n\n"
        f"👥 کل کاربران: {total}\n"
        f"🟢 فعال: {active}\n"
        f"🔴 غیرفعال: {total - active}\n\n"
        f"📅 تاریخ: {datetime.now().strftime('%Y/%m/%d %H:%M')}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت به پنل", callback_data='admin_panel')]
        ])
    )

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if not await is_admin(user_id):
        return
    
    if not users_data:
        await query.edit_message_text(
            "❌ هیچ کاربری ثبت‌نام نکرده است!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]
            ])
        )
        return
    
    users_list = ""
    count = 0
    for uid, data in list(users_data.items())[:10]:
        count += 1
        custom_name = user_custom_name.get(uid, "نامشخص")
        status = "🟢" if user_settings.get(uid, False) else "🔴"
        users_list += f"{count}. {custom_name} | {status}\n"
    
    if len(users_data) > 10:
        users_list += f"\n... و {len(users_data) - 10} کاربر دیگر"
    
    await query.edit_message_text(
        f"👥 **لیست کاربران**\n\n"
        f"{users_list}\n\n"
        f"📌 کل: {len(users_data)} کاربر",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]
        ])
    )

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if not await is_admin(user_id):
        return
    
    await query.edit_message_text(
        "📨 **ارسال پیام همگانی**\n\n"
        "لطفاً پیام خود را وارد کنید.\n"
        "این پیام برای **همه کاربران** ارسال خواهد شد.\n\n"
        "⚠️ برای لغو، /cancel را بزنید."
    )
    context.user_data['step'] = 'broadcast'

async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        return
    
    message = update.message.text
    total = len(users_data)
    success = 0
    fail = 0
    
    await update.message.reply_text(f"⏳ در حال ارسال پیام به {total} کاربر...")
    
    for uid in list(users_data.keys()):
        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"📨 **پیام همگانی**\n\n{message}"
            )
            success += 1
            await asyncio.sleep(0.1)
        except:
            fail += 1
    
    context.user_data['step'] = None
    
    await update.message.reply_text(
        f"✅ **ارسال پیام تکمیل شد!**\n\n"
        f"✅ موفق: {success}\n"
        f"❌ ناموفق: {fail}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت به پنل", callback_data='admin_panel')]
        ])
    )

async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        return
    
    if context.user_data.get('step') == 'broadcast':
        context.user_data['step'] = None
        await update.message.reply_text(
            "❌ ارسال پیام لغو شد.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت به پنل", callback_data='admin_panel')]
            ])
        )

# ======================== اجرا ========================
async def main():
    app = Application.builder().token(TOKEN).build()
    
    # هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel_broadcast))
    
    # کال‌بک‌ها
    app.add_handler(CallbackQueryHandler(register, pattern='^register$'))
    app.add_handler(CallbackQueryHandler(font_menu, pattern='^font_menu$'))
    app.add_handler(CallbackQueryHandler(select_font, pattern='^font_'))
    app.add_handler(CallbackQueryHandler(toggle_handler, pattern='^toggle$'))
    app.add_handler(CallbackQueryHandler(status_handler, pattern='^status$'))
    app.add_handler(CallbackQueryHandler(settings_handler, pattern='^settings$'))
    app.add_handler(CallbackQueryHandler(change_name_handler, pattern='^change_name$'))
    app.add_handler(CallbackQueryHandler(help_handler, pattern='^help$'))
    app.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^main_menu$'))
    app.add_handler(CallbackQueryHandler(delete_data_handler, pattern='^delete_data$'))
    
    # پنل مدیریت
    app.add_handler(CallbackQueryHandler(admin_panel, pattern='^admin_panel$'))
    app.add_handler(CallbackQueryHandler(admin_stats, pattern='^admin_stats$'))
    app.add_handler(CallbackQueryHandler(admin_users, pattern='^admin_users$'))
    app.add_handler(CallbackQueryHandler(admin_broadcast, pattern='^admin_broadcast$'))
    
    # پیام‌ها
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_process))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_broadcast))
    
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_updates())
    
    print("🤖 ربات مسکن نسخه نهایی روشن شد...")
    print("=" * 50)
    print(f"📢 کانال: {CHANNEL_LINK}")
    print(f"👑 ادمین: {ADMIN_ID}")
    print(f"📁 دیتابیس: {DB_FILE}")
    print("👥 منتظر کاربران...")
    print("=" * 50)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 توقف...")
        save_all_data()
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
