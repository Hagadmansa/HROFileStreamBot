import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

START_TEXT = """
👋 Hello {},

🤖 My Name is Hagadmansa Mega Bot, I can stream Telegram Files over HTTP

🧐 Don't know how to do? No worries, just press the help button.

👨‍💻 My Creator is <a href=https://t.me/hagadmansa>Hagadmansa</a>."""

HELP_TEXT = """<b>ℹ️ HELP</b> >

Here are the list of my commands.

<b>🔞 Warning:</b>

• 18+ content and pornography are strictly prohibited. Don't send me any pornographic/violent videos. You will get an instant ban if we see any kind of content like this."""

INSTRUCTIONS_TEXT = """<b>ℹ️ Help</b> > Instructions

<b>👤 Instructions for an individual:</b>

1. Don't send photos to the bot, send them as a file.
2. Don't send multiple files at a time, send them one by one.

<b>👤 Instructions for groups/channels:</b>

1. Don't send too many files to your groups/channels.
2. Bot takes time to generate and edit links, keep patience.

<b>🔞 Warning:</b>

• 18+ content and pornography are strictly prohibited. Don't send me any pornographic/violent videos. You will get an instant ban if we see any kind of content like this."""

TUTORIALS_TEXT = """<b>ℹ️ Help</b> > Instructions

All tutorials related to Bots, Website, Movies and etc, will be updated here. Till then you can visit my movie website <b>www.hagadmansa.com</b> to watch movies."""

HOWTOUSEME_TEXT = """<b>ℹ️ Help</b> > How To Use Me

<b>👤 For an individual:</b>

My name is Hagdmansa Mega Bot, I am a member of Hagdmansa family. I can provide you direct download link of any telegram file/media. If you send me any file/media I will give an external download link, you can use that link to download any file outside telegram. My link is supported in any browser.

• Send me any file/media from Telegram.
• I Will provide an external download link for you.
• All links will be permanent and have the fastest speed.

<b>👥 For groups/channels:</b>

I also work in Public/Private groups/Channels. If you have multiple files in your group/channel then just add me to your group/channel, I will add an external download link on each file which will be added after I joined the group/channel.

• I must be an admin in your Channel/Group.
• Don't forget to give all permissions otherwise I will not work.

<b>🔞 Warning:</b>

• 18+ content and pornography are strictly prohibited. Don't send me any pornographic/violent videos. You will get an instant ban if we see any kind of content like this."""

ABOUT_TEXT = """<b>✯ My Name:</b> Hagadmansa Mega Bot
<b>✯ Creator:</b> <a href='https://t.me/hagadmansa'>Hagadmansa</a>
<b>✯ Library:</b> <a href='https://pyrogram.org'>Pyrogram</a>
<b>✯ Language:</b> <a href='https://Python.org'>Python</a>
<b>✯ Database:</b> <a href='https://mongodb.com'>MongoDB</a>
<b>✯ Server:</b> <a href='https://heroku.com'>Heroku</a>
<b>✯ Channel:</b> <a href='https://t.me/hagadmansa'>Hagadmansa</a>
<b>✯ Group:</b> <a href='https://t.me/hagadmansachat'>Hagadmansa Support</a>
<b>✯ Brothers:</b> <a href='https://t.me/hagadmansabot'>Hagadmansa Bot</a>, <a href='https://t.me/hagadmansarobot'>Hagadmansa Robot</a>"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🌐 Website', url='https://hagadmansa.com'),
            InlineKeyboardButton('📣 Updates', url='https://t.me/hagadmansa')
            ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('😊 About', callback_data='about')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('⚙️ Instructions', callback_data='instructions'),
            InlineKeyboardButton('🕹 Tutorials', callback_data='tutorials')
            ],[
            InlineKeyboardButton('🔙 Back', callback_data='home'),
            InlineKeyboardButton('❓ How to use me', url='https://t.me/hagadmansa')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup( [[InlineKeyboardButton('🏠 Home', callback_data='home'),InlineKeyboardButton('🔐 Close', callback_data='close')]] )
INSTRUCTIONS_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🔙 Back', callback_data='help'),
            InlineKeyboardButton('🏠 Home', callback_data='home')
            ]]
    )
TUTORIALS_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🔙 Back', callback_data='help'),
            InlineKeyboardButton('🏠 Home', callback_data='home')
            ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "instructions":
        await update.message.edit_text(
            text=INSTRUCTIONS_TEXT,
            disable_web_page_preview=True,
            reply_markup=INSTRUCTIONS_BUTTONS
        )
    elif update.data == "tutorials":
        await update.message.edit_text(
            text=TUTORIALS_TEXT,
            disable_web_page_preview=True,
            reply_markup=TUTORIALS_BUTTONS
        )
    else:
        await update.message.delete()

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**New User Joined** \n\n**My New Friend** [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started your bot"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry you are banned to use me, contact support @hagadmansachat.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>🔐 Join my updates channel to use me.</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("📡 Join Now", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went wrong contact support @hagadmansachat.",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text=START_TEXT.format(m.from_user.mention),
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
              )                                                                         
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry you are banned to use me, contact support @hagadmansachat.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="😒 You need to join my updates channel to use me. Due to overload only channel subscribers can use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton("📡 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")],
                         [InlineKeyboardButton("🔄 Refresh / Try Again", url=f"https://t.me/{(await b.get_me()).username}?start={usr_cmd}")
                        
                        ]]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went wrong contact support @hagadmansachat.",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.message_id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id,
                                     file_name)

        msg_text ="""
<b><u>Here is your link.</u></b>\n
<b>📂 File Name:</b> <code><i>{}</i></code>\n
<b>📦 File Size:</b> <i>{}</i>\n
<b>📥 Download:</b> <i>{}</i>\n
<b>🚸 Note:</b> This is a permant link.\n
<b>🔞 Warning:</b> 18+ Content will permanently ban you."""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download Now", url=stream_link)]])
        )



@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined \n\nName: [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started your bot!"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Sorry you are banned to use me, contact support @hagadmansachat.",
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="😒 You need to join my updates channel to use me. Due to overload only channel subscribers can use me.",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("📡 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Something went wrong contact support @hagadmansachat.",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
        )

