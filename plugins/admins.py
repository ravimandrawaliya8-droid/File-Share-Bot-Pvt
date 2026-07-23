from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import time

import psutil
import shutil

#===============================================================#

async def admins(client, query):
    if not (query.from_user.id==client.owner):
        return await query.answer('This can only be used by owner.')
    msg = f"""<blockquote>**Admin Settings:**</blockquote>
**Admin User IDs:** {", ".join(f"`{a}`" for a in client.admins)}

__Use the appropriate button below to add or remove an admin based on your needs!__
"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ᴀᴅᴅ ᴀᴅᴍɪɴ', 'add_admin'), InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ', 'rm_admin')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]
    )
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_message(filters.command("stats"))
async def usage_cmd(client: Client, message: Message):
    if not message.from_user.id in client.admins:
        return await message.reply("✗ ᴛʜɪs ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴀᴅᴍɪɴs!")
    
    reply = await message.reply("<blockquote>›› ᴇxᴛʀᴀᴄᴛɪɴɢ ᴜsᴀɢᴇ ᴅᴀᴛᴀ...</blockquote>")

    # Get total users from database
    try:
        total_users_list = await client.mongodb.full_userbase()
        total_users = len(total_users_list)
    except Exception as e:
        total_users = "ᴇʀʀᴏʀ"

    # Bot uptime calculation
    from datetime import datetime, timedelta
    uptime_duration = datetime.now() - getattr(client, 'uptime', datetime.now())
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    uptime_str = f"{days}ᴅ {hours}ʜ {minutes}ᴍ"

    # System stats
    total, used, free = shutil.disk_usage("/")
    total_gb = total / (1024**3)
    used_gb = used / (1024**3)
    free_gb = free / (1024**3)
    disk_percent = (used / total) * 100

    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024**3)
    used_ram = ram.used / (1024**3)
    free_ram = ram.available / (1024**3)
    ram_percent = ram.percent

    swap = psutil.swap_memory()
    total_swap = swap.total / (1024**3)
    used_swap = swap.used / (1024**3)
    free_swap = swap.free / (1024**3)
    swap_percent = swap.percent

    cpu_usage = psutil.cpu_percent(interval=1)

    # Network stats with error handling
    try:
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent / (1024**2)
        bytes_recv = net_io.bytes_recv / (1024**2)
        network_status = "✓ ᴀᴠᴀɪʟᴀʙʟᴇ"
        net_section = f"""<blockquote>›› **ᴜᴘʟᴏᴀᴅᴇᴅ:** `{bytes_sent:.2f} ᴍʙ`
›› **ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ:** `{bytes_recv:.2f} ᴍʙ`</blockquote>"""
    except PermissionError:
        network_status = "✗ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ"
        net_section = "<blockquote>›› **sᴛᴀᴛᴜs:** `ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴘʀᴏᴏᴛ`</blockquote>"

    # Bot process usage
    try:
        process = psutil.Process()
        bot_cpu_usage = process.cpu_percent(interval=1)
        bot_memory_usage = process.memory_info().rss / (1024**2)
        bot_status = "✓ ʀᴜɴɴɪɴɢ"
    except Exception:
        bot_cpu_usage = 0.0
        bot_memory_usage = 0.0
        bot_status = "✗ ᴇʀʀᴏʀ"

    # Status indicators based on usage levels
    disk_status = "✓ ɴᴏʀᴍᴀʟ" if disk_percent < 80 else "✗ ʜɪɢʜ" if disk_percent < 95 else "✗ ᴄʀɪᴛɪᴄᴀʟ"
    ram_status = "✓ ɴᴏʀᴍᴀʟ" if ram_percent < 80 else "✗ ʜɪɢʜ" if ram_percent < 95 else "✗ ᴄʀɪᴛɪᴄᴀʟ"
    cpu_status = "✓ ɴᴏʀᴍᴀʟ" if cpu_usage < 80 else "✗ ʜɪɢʜ" if cpu_usage < 95 else "✗ ᴄʀɪᴛɪᴄᴀʟ"

    # Final message construction with enhanced UI
    msg = f"""<blockquote>✦ sʏsᴛᴇᴍ ᴜsᴀɢᴇ sᴛᴀᴛs</blockquote>

<blockquote><u>**≡ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{total_users}`
›› **ʙᴏᴛ sᴛᴀᴛᴜs:** {bot_status}
›› **ᴜᴘᴛɪᴍᴇ:** `{uptime_str}`
›› **ᴀᴅᴍɪɴs:** `{len(client.admins)}`</blockquote>

<blockquote><u>**≡ ᴅɪsᴋ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ:** `{total_gb:.2f} ɢʙ`
›› **ᴜsᴇᴅ:** `{used_gb:.2f} ɢʙ` ({disk_percent:.1f}%)
›› **ꜰʀᴇᴇ:** `{free_gb:.2f} ɢʙ`
›› **sᴛᴀᴛᴜs:** {disk_status}</blockquote>

<blockquote><u>**≡ ʀᴀᴍ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ:** `{total_ram:.2f} ɢʙ`
›› **ᴜsᴇᴅ:** `{used_ram:.2f} ɢʙ` ({ram_percent:.1f}%)
›› **ꜰʀᴇᴇ:** `{free_ram:.2f} ɢʙ`
›› **sᴛᴀᴛᴜs:** {ram_status}</blockquote>

<blockquote><u>**≡ sᴡᴀᴘ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ:** `{total_swap:.2f} ɢʙ`
›› **ᴜsᴇᴅ:** `{used_swap:.2f} ɢʙ` ({swap_percent:.1f}%)
›› **ꜰʀᴇᴇ:** `{free_swap:.2f} ɢʙ`</blockquote>

<blockquote><u>**≡ ᴄᴘᴜ & ɴᴇᴛᴡᴏʀᴋ:**</u></blockquote>
<blockquote>›› **ᴄᴘᴜ ᴜsᴀɢᴇ:** `{cpu_usage:.2f}%` {cpu_status}
›› **ɴᴇᴛᴡᴏʀᴋ:** {network_status}</blockquote>
{net_section}

<blockquote><u>**≡ ʙᴏᴛ ʀᴇsᴏᴜʀᴄᴇ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴄᴘᴜ:** `{bot_cpu_usage:.2f}%`
›› **ᴍᴇᴍᴏʀʏ:** `{bot_memory_usage:.2f} ᴍʙ`</blockquote>

<blockquote>**• ᴜsᴇ ᴛʜɪs ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴛᴏ ᴍᴏɴɪᴛᴏʀ ʏᴏᴜʀ ʙᴏᴛ's ᴘᴇʀꜰᴏʀᴍᴀɴᴄᴇ!**</blockquote>"""

    await reply.edit_text(msg)
#===============================================================#

@Client.on_callback_query(filters.regex("^add_admin$"))
async def add_new_admins(client: Client, query: CallbackQuery):
    await query.answer()
    if not query.from_user.id in client.admins:
        return await client.send_message(query.from_user.id, client.reply_text)
    ids_msg = await client.ask(query.from_user.id, "Send user ids seperated by a space in the next 60 seconds!\nEg: `838278682 83622928 82789928`", filters=filters.text, timeout=60)
    ids = ids_msg.text.split()
    
    try:
        for identifier in ids:
            if int(identifier) not in client.admins:
                client.admins.append(int(identifier))
            
    except Exception as e:
        return await ids_msg.reply(f"Error: {e}")
    await admins(client, query)
    return await ids_msg.reply(f"__{len(ids)} admin {'id' if len(ids)==1 else 'ids'} have been promoted!!__")
    
#===============================================================#

@Client.on_callback_query(filters.regex("^rm_admin$"))
async def remove_admins(client: Client, query: CallbackQuery):
    await query.answer()
    if not query.from_user.id in client.admins:
        return await client.send_message(query.from_user.id, client.reply_text)
    ids_msg = await client.ask(query.from_user.id, "Send user ids seperated by a space in the next 60 seconds!\nEg: `838278682 83622928 82789928`", filters=filters.text, timeout=60)
    ids = ids_msg.text.split()
    
    try:
        for identifier in ids:
            if int(identifier) == client.owner:
                await client.send_message(query.from_user.id, "Nigga i can never remove the owner from the admin list!!")
                continue
            if int(identifier) in client.admins:
                client.admins.remove(int(identifier))
    except Exception as e:
        return await ids_msg.reply(f"Error: {e}")
    await admins(client, query)
    return await ids_msg.reply(f"__{len(ids)} admin {'id' if len(ids)==1 else 'ids'} have been removed!!__")

#===============================================================#
#                   FSUB BOTS COMMANDS ADDED HERE               #
#===============================================================#

@Client.on_message(filters.command("add_fsub_bot"))
async def add_fsub_bot_cmd(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply("✗ ᴛʜɪs ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴀᴅᴍɪɴs!")
    
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply("**Format:** `/add_fsub_bot @BotUsername https://t.me/BotUsername?start=fsub_code`")
    
    bot_username = args[1].replace("@", "")
    start_link = args[2]
    
    await client.mongodb.add_fsub_bot(bot_username, start_link)
    await message.reply(f"✅ **Bot `@{bot_username}` successfully added to FSUB!**\n\n🔗 **Link:** `{start_link}`")

#===============================================================#

@Client.on_message(filters.command("del_fsub_bot"))
async def del_fsub_bot_cmd(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply("✗ ᴛʜɪs ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴀᴅᴍɪɴs!")
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("**Format:** `/del_fsub_bot @BotUsername`")
    
    bot_username = args[1].replace("@", "")
    
    # Check if bot exists before deleting
    bots = await client.mongodb.get_fsub_bots()
    if bot_username not in bots:
        return await message.reply(f"⚠️ Bot `@{bot_username}` is not in the FSUB list.")

    await client.mongodb.remove_fsub_bot(bot_username)
    await message.reply(f"✅ **Bot `@{bot_username}` successfully removed from FSUB!**")

#===============================================================#

@Client.on_message(filters.command("fsub_bots"))
async def list_fsub_bots_cmd(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply("✗ ᴛʜɪs ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴀᴅᴍɪɴs!")
    
    bots = await client.mongodb.get_fsub_bots()
    
    if not bots:
        return await message.reply("⚠️ **No FSUB Bots found in the database.**")
    
    msg = "<blockquote>**🤖 Active FSUB Bots:**</blockquote>\n\n"
    for idx, (username, link) in enumerate(bots.items(), 1):
        msg += f"**{idx}.** `@{username}`\n🔗 {link}\n\n"
    
    await message.reply(msg, disable_web_page_preview=True)

