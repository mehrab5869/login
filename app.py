# -*- coding: utf-8 -*-

import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive
keep_alive()
# تنظیمات
TOKEN = "7427429689:AAEbiE5uk6Et6p2V2ZKMU57WHFt6dGXhyt0"  # توکن ربات تلگرام را جایگزین کنید

# دیکشنری‌های ذخیره وضعیت و داده‌های کاربر
user_states = {}  # وضعیت‌های کاربران؛ کلید: user_id، مقدار: یکی از عبارات زیaر:
# "awaiting_account_count"  => در انتظار دریافت تعداد اکانت‌ها
# "awaiting_credentials"    => در انتظار دریافت اطلاعات اکانت (شماره، API_ID، API_HASH)
# "awaiting_code"           => در انتظار دریافت کد ورود (در صورت نیاز)
# "awaiting_send_message"   => در انتظار دستور نهایی برای شروع ارسال پیام‌ها

user_data = {}  # ذخیره داده‌های مربوط به هر کاربر

# --------------------------
# Handler مربوط به دستور /start
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # تنظیم اولیه وضعیت و داده‌های کاربر
    user_states[user_id] = "awaiting_account_count"
    user_data[user_id] = {
        'num_accounts': None,      # تعداد اکانت‌های مورد نظر
        'credentials': [],         # لیست اطلاعات اکانت‌ها (هر کدام به صورت (api_id, api_hash, phone))
        'clients': [],             # لیست کلاینت‌های وارد شده
        'current_account': 0,      # شماره اکانتی که در حال ورود هستیم
        'pending': None            # برای ذخیره موقت (client, phone) در صورتی که ورود نیاز به کد داشته باشد
    }
    await update.message.reply_text("🤖 خوش آمدید!\n\nلطفاً تعداد اکانت‌های تلگرامی را وارد کنید:")

# --------------------------
# Handler مربوط به دستور /restart
# --------------------------
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # ریست کردن وضعیت و داده‌های کاربر
    user_states[user_id] = "awaiting_account_count"
    user_data[user_id] = {
        'num_accounts': None,
        'credentials': [],
        'clients': [],
        'current_account': 0,
        'pending': None
    }
    await update.message.reply_text("🔄 عملیات ریست شد.\n\nلطفاً تعداد اکانت‌های تلگرامی را وارد کنید:")

# --------------------------
# Handler عمومی برای دریافت پیام‌های متنی (با توجه به وضعیت کاربر)
# --------------------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # اگر وضعیت کاربر تنظیم نشده باشد، از کاربر بخواهید ابتدا /start را ارسال کند
    if user_id not in user_states:
        await update.message.reply_text("❗ ابتدا دستور /start را ارسال کنید.")
        return

    state = user_states[user_id]

    # مرحله 1: دریافت تعداد اکانت‌ها
    if state == "awaiting_account_count":
        try:
            num = int(update.message.text)
            user_data[user_id]['num_accounts'] = num
            user_states[user_id] = "awaiting_credentials"
            await update.message.reply_text(
                "لطفاً اطلاعات اکانت‌ها را به صورت زیر وارد کنید:\n\n+98********* API_ID API_HASH"
            )
        except ValueError:
            await update.message.reply_text("⚠️ لطفاً یک عدد معتبر وارد کنید!")
        return

    # مرحله 2: دریافت اطلاعات اکانت (credentials)
    elif state == "awaiting_credentials":
        try:
            parts = update.message.text.split()
            if len(parts) != 3:
                raise Exception("فرمت ورودی صحیح نیست")
            phone, api_id, api_hash = parts
            api_id = int(api_id)
            user_data[user_id]['credentials'].append((api_id, api_hash, phone))
        except Exception as e:
            await update.message.reply_text(f"⚠️ خطا: {str(e)}")
            return

        if len(user_data[user_id]['credentials']) < user_data[user_id]['num_accounts']:
            await update.message.reply_text(
                f"✅ اطلاعات اکانت {len(user_data[user_id]['credentials'])} ثبت شد.\nلطفاً اطلاعات اکانت بعدی را وارد کنید."
            )
        else:
            await update.message.reply_text("🎉 تمامی اطلاعات دریافت شد. در حال ورود به اکانت‌ها...")
            await login_next_account(update, context, user_id)
        return

    # مرحله 3: دریافت کد ورود (در صورتی که لازم باشد)
    elif state == "awaiting_code":
        code = update.message.text.strip()
        pending = user_data[user_id].get('pending')
        if not pending:
            await update.message.reply_text("⚠️ هیچ اکانتی در انتظار کد نیست!")
            return
        client, phone = pending
        try:
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            await update.message.reply_text(f"⚠️ خطا در ورود: {e}\nلطفاً دوباره کد را وارد کنید:")
            return
        user_data[user_id]['clients'].append(client)
        user_data[user_id]['pending'] = None
        user_data[user_id]['current_account'] += 1
        await update.message.reply_text(f"✅ ورود موفق برای {phone}!")
        await login_next_account(update, context, user_id)
        return

    # مرحله 4: شروع ارسال پیام (زمانی که همه اکانت‌ها وارد شده‌اند)
    elif state == "awaiting_send_message":
        if update.message.text.strip() != "1":
            await update.message.reply_text("⚠️ لطفاً عدد 1 را وارد کنید تا ارسال پیام آغاز شود.")
            return
        await update.message.reply_text("🚀 در حال شروع عملیات ارسال پیام‌ها...")
        await send_messages(update, context, user_id)
        await update.message.reply_text("✅ تمامی پیام‌ها ارسال شدند.")
        # در صورت نیاز می‌توانید وضعیت کاربر را ریست کنید یا نگه دارید
        return

# --------------------------
# تابع ورود به اکانت‌های تلگرام به صورت مرحله‌ای
# --------------------------
async def login_next_account(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    data = user_data[user_id]
    # اگر همه اکانت‌ها وارد شده باشند، وضعیت را به مرحله ارسال پیام تغییر می‌دهیم
    if data['current_account'] >= data['num_accounts']:
        user_states[user_id] = "awaiting_send_message"
        await update.message.reply_text("✅ تمامی اکانت‌ها وارد شدند.\nبرای شروع ارسال پیام عدد 1 را وارد کنید:")
        return

    # ورود به اکانت بعدی
    api_id, api_hash, phone = data['credentials'][data['current_account']]
    session_name = f"session_{phone.replace('+', '')}.session"
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()

    if await client.is_user_authorized():
        data['clients'].append(client)
        await update.message.reply_text(f"✅ اکانت {phone} وارد شد.")
        data['current_account'] += 1
        await login_next_account(update, context, user_id)
    else:
        try:
            await client.send_code_request(phone)
            # ذخیره موقت جهت دریافت کد
            data['pending'] = (client, phone)
            user_states[user_id] = "awaiting_code"
            await update.message.reply_text(f"🔑 لطفاً کد ارسال شده به {phone} را وارد کنید:")
        except Exception as e:
            await update.message.reply_text(f"⚠️ خطا در ارسال کد به {phone}: {e}")
            data['current_account'] += 1
            await login_next_account(update, context, user_id)

# --------------------------
# تابع ارسال پیام به اعضای گروه‌ها با استفاده از Telethon
# --------------------------
async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    data = user_data[user_id]
    clients = data['clients']
    message_text = (
        "👋سلام، شما دعوت شدید!\n\n"
        "برای شرکت در گروه، لطفاً به لینک زیر بپیوندید:\n"
        "https://t.me/+y-3kH__4DKY0M2Rk"
    )
    total_success = 0
    total_failed = 0
    sent_users = set()

    for client in clients:
        async with client:
            dialogs = await client.get_dialogs()
            for dialog in dialogs:
                if dialog.is_group:
                    await update.message.reply_text(f"🔍 بررسی گروه: {dialog.title}")
                    messages = await client.get_messages(dialog, limit=3000)
                    for msg in messages[:30]:
                        if msg.sender_id:
                            try:
                                user_entity = await client.get_entity(msg.sender_id)
                                if (hasattr(user_entity, 'username') and user_entity.username and
                                        user_entity.username not in sent_users):
                                    await client(SendMessageRequest(peer=user_entity.id, message=message_text))
                                    sent_users.add(user_entity.username)
                                    total_success += 1
                                    await update.message.reply_text(f"✅ پیام ارسال شد به {user_entity.username}")
                                    await asyncio.sleep(2)  # وقفه کوتاه برای جلوگیری از بلاک شدن
                            except Exception as e:
                                total_failed += 1
                                uname = getattr(user_entity, 'username', 'نامشخص')
                                await update.message.reply_text(f"⚠️ خطا در ارسال به {uname}: {e}")
    await update.message.reply_text(f"✅ ارسال به {total_success} نفر موفق و به {total_failed} نفر ناموفق بود.")

# --------------------------
# تابع اصلی جهت راه‌اندازی ربات
# --------------------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
