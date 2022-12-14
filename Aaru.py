import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
   f"__**https://telegra.ph/file/c70635cc28eec97a43f40.jpg",
    "__**š'š¦ ššš šš„š„ ššØš­**, š¢ ššš§ ššš§š­š¢šØš§ šš„š„ ššš¦ššš«š¬ šš§ šš«šØš®š© šš« šš”šš§š§šš„ š»\nšš„š¢šš¤ **/help** ššØš« ššØš«š šš§ššØš«š¦šš­š¢šØš§__\n\n ššØš„š„šØš° [ā-šš'ššššš š¬ šššš-š±š Ā°](https://t.me/botatiiii) š¢š» ššš„ššš«šš¦",
    link_preview=False,
    buttons=(
      [
        Button.url('āØ ššāāšāš', 'https://t.me/botatiiii'),
        Button.url('š ššāš¼ā_šš»', 'https://t.me/hms_01')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of TagAllBot**\n\nCommand: /all\n__You can use this command with text what you want to mention others.__\nExample: `/all Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nUse /cancel To Stop Tagging in group\n\nFollow [ā-šš'ššššš š¬ šššš-š±š Ā°](https://t.me/botatiiii) š¢š” š§ššššš„šš "
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('āØ ššāāšāš', 'https://t.me/botatiiii'),
        Button.url('š ššāš¼ā_šš»', 'https://t.me/hms_01')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def all(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command Can Be Use In Groups And Channels @botatiiii !__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only Admins Can Mention All\n\nFor More Go On @botatiiii !__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I Can't Mention Members For Older Messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply To a Message Or Give Me Some Text To Mention Others\n\nMade bY @botatiiii !__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}\n\nMade bY ā-šš'ššššš š¬ šššš-š±š Ā° āļøš„"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There Is No Proccess On Going @botatiiii...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> AARU TAGALL STARTED @botatiiii<<")
client.run_until_disconnected()
