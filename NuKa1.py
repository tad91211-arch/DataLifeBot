from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from dataclasses import dataclass
from typing import List
from aiogram.types import LabeledPrice
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import LabeledPrice
import sqlite3

from dataclasses import dataclass
from typing import List

def create_db():
    conn=sqlite3.connect('users123.db')
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_bot(
    user_id INTEGER,
    name TEXT,
    phone TEXT,
    age INTEGER,
    school TEXT)
    """)
    conn.commit()
    conn.close()
def add_user(user_id,name,phone,age,school):
    conn=sqlite3.connect('users123.db')
    cursor=conn.cursor()
    cursor.execute("INSERT INTO user_bot(user_id,name,phone,age,school) VALUES(?,?,?,?,?)",(user_id,name,phone,age,school))
    conn.commit()
    conn.close()
st=MemoryStorage()
PAY_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"
bot=Bot(token='8786342742:AAEigHYtYajtqAEyhDIgV_I1uoTKHgILNvs')
dp=Dispatcher(bot,storage=st)

create_db()

@dataclass
class Product:
    """
    https://core.telegram.org/bots/api#sendinvoice
    """
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False
    provider_token: str = PAY_TOKEN

    def generate_invoice(self):   #
        return self.__dict__

class UserForm(StatesGroup):
    name=State()
    phone=State()
    age=State()
    school=State()

@dp.message_handler(commands="start")
async def s(message:types.Message):
    await message.answer(f"Assalawma Aleykum {message.from_user.full_name}, \natinizdi kiritin':")

    await UserForm.name.set()

@dp.message_handler(state=UserForm.name)
async def gn(message:types.Message,state=FSMContext):
    await state.update_data(name=message.text)

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="nomer jiberiw",request_contact=True))

    await message.answer("🔢telefon nomerinizdi jiberin':",reply_markup=markup)
    await UserForm.phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT,state=UserForm.phone)
async def gnm(message:types.Message, state:FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("👶Jasiniz neshede:",reply_markup=types.ReplyKeyboardRemove())
    await UserForm.age.set()
@dp.message_handler(state=UserForm.age)
async def gnm(message:types.Message, state:FSMContext):
    await state.update_data(age=message.text)
    await message.answer("🎒Qayerde oqiysiz:")
    await UserForm.school.set()
@dp.message_handler(state=UserForm.school)
async def ga(message:types.Message, state:FSMContext):
    await state.update_data(school=message.text)
    data=await state.get_data()
    add_user(message.from_user.id,data["name"],data["phone"],data["age"],data["school"])
    await message.answer("Mag'liwmatler saqlandi, Raxmet🤗. DataLife haqqinda informaciya bilew ushin /menu basin'🧵")
    await bot.send_message(chat_id=5195118856,text=f"bazag'a taza paydalaniwshi qosildi {data['name']}"
)
    await state.finish()

dl=InlineKeyboardMarkup(row_width=2)
dl.add(
    InlineKeyboardButton("Kurslar🏫", callback_data="k"),
    InlineKeyboardButton("Location📍", callback_data="l"),
    InlineKeyboardButton("About🆎", callback_data="a"),
    InlineKeyboardButton("IT💻 \nne?", callback_data="i"),
    InlineKeyboardButton("Call📱", callback_data="c"),
    InlineKeyboardButton("result❕", callback_data="r"),
    InlineKeyboardButton("Back🔙",callback_data="ba")
)
kurs=InlineKeyboardMarkup(row_width=2)
kurs.add(
    InlineKeyboardButton("Python🐍", callback_data="Py"),
    InlineKeyboardButton("Java🍵", callback_data="Ja"),
    InlineKeyboardButton("C++🎮", callback_data="C"),
    InlineKeyboardButton("dataBase📃", callback_data="d"),
    InlineKeyboardButton("graffik dizayn🎆",callback_data="gd"),
    InlineKeyboardButton("Robototexnika🦾",callback_data="ro"),
    InlineKeyboardButton("Back🔙",callback_data="bac")
)
onOff = InlineKeyboardMarkup(row_width=2)
onOff.add(
    InlineKeyboardButton("Online🧑‍💻",callback_data="on"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="off")
)
dlPY=InlineKeyboardMarkup(row_width=2)
dlPY.add(
InlineKeyboardButton("Online🧑‍💻",callback_data="onp"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="offp")
)
dlJa=InlineKeyboardMarkup(row_width=2)
dlJa.add(
InlineKeyboardButton("Online🧑‍💻",callback_data="onj"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="offj")
)
dlC=InlineKeyboardMarkup(row_width=2)
dlC.add(
InlineKeyboardButton("Online🧑‍💻",callback_data="onc"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="offc")
)
dlDB=InlineKeyboardMarkup(row_width=2)
dlDB.add(
InlineKeyboardButton("Online🧑‍💻",callback_data="ondb"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="offdb"))
dlGD=InlineKeyboardMarkup(row_width=2)
dlGD.add(
    InlineKeyboardButton("Online🧑‍💻",callback_data="ongd"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="offgd"))
dlR=InlineKeyboardMarkup(row_width=2)
dlR.add(
    InlineKeyboardButton("Online🧑‍💻",callback_data="onr"),
    InlineKeyboardButton("Offline🚵‍♂️",callback_data="offr"))
@dp.message_handler(commands="menu")
async def m(message:types.Message):
    await message.answer("Menu:", reply_markup=dl)

@dp.callback_query_handler(text="k")
async def k(message1:types.CallbackQuery):
    await message1.message.answer("qanday kursti saylaysiz❓❓❓:", reply_markup=kurs)


@dp.callback_query_handler(text="l")
async def loc(call: types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer("Menu:", reply_markup=dl)
@dp.callback_query_handler(text="a")
async def aa(msg:types.CallbackQuery):
    await msg.message.answer_photo(photo="AgACAgIAAxkBAAIBuGnRYZlR1scsrylrMSV6NQLHi_x-AAIKFGsbHRmQSk6juTq_nFcgAQADAgADeAADOwQ",caption="✨DataLife — больше, чем учебный центр✨.\nЗдесь каждая идея💡 рождается в жизнь🌱,\nКаждый клик мышки🖱️ — шаг к будущему🚀.\nКод превращается в магию🪄, цифры — в возможности📊,\nА знания📚 — в крылья🕊️, чтобы лететь дальше🏆.")


@dp.callback_query_handler(text="i")
async def it(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBu2nRYc-bCPrC3kWGcy0z2U81hF1rAAILFGsbHRmQSlKhoCm-MJumAQADAgADbQADOwQ",caption="IT-bul texnologiyadan paydalanıp, maǵlıwmatlardı jaratıw, qayta islew hám uzatıwǵa járdem beretuǵın barlıq zatlar.\n"
                                                                                                                                        "🔧 IT ne? \n🧑‍💻 Programmalastırıw — veb-saytlar, qosımshalar, oyınlar jaratıw \n"
                                                                                                                                        "🌐 Internet hám tarmaqlar — internet qanday isleyd \n"
                                                                                                                                        " 💾 Maǵlıwmatlar bazası — maǵlıwmatlardı saqlaw  \n"
                                                                                                                                        "🤖 Jasalma Intellekt — sanalı programmalar \n"
                                                                                                                                        "🎨 Dizayn — interfeysler, veb-saytlar, qosımshalar \n"
                                                                                                                                        "💡 Turmıstan mısal \n"
                                                                                                                                        "nstagram, Telegram, YouTube → bulardıń barlıǵı IT \n"
                                                                                                                                        "Oyınlar 🎮 → da IT \n"
                                                                                                                                        "Bank qosımshaları 💳 → IT \n"
                                                                                                                                        " Hátte botdaǵı tuyme, oǵan basqanıńız → da IT \n"
                                                                                                                                        "🚀 IT ne ushın kerek? \n"
                                                                                                                                        " veb-saytlar hám qosımshalar jaratıw \n"
                                                                                                                                        " Pul islep tabıw 💰 \n"
                                                                                                                                        " Jumıstı avtomatlastırıw \n"
                                                                                                                                        "Keleshek texnologiyaların jaratıw")

@dp.callback_query_handler(text="c")
async def c(call: types.CallbackQuery):
    await call.message.answer("baylanisiniz ushin nomerimiz:+998 (99) 208-11-77,\n "
                              "https://www.instagram.com/data_life_centre?igsh=ZTFsNWM1ejVzZnA1 instagram akkauntimiz,\n "
                              "https://t.me/datalifecentre telegam akkuntimiz\n "
                              "ha'mde https://datalife.uz/ websaytimiz")

@dp.callback_query_handler(text="r")
async def r(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBvmnRYh6IyYCNr05yXVc4TR8HZ_2FAAINFGsbHRmQSk0DrTfYX35-AQADAgADbQADOwQ",caption="Baxiyatdinov Sanjar \nMarttin' en' bilimli oqiwshisi")
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBvmnRYh6IyYCNr05yXVc4TR8HZ_2FAAINFGsbHRmQSk0DrTfYX35-AQADAgADbQADOwQ",caption="Azatov Sherzodbek \nHa'zir ol Tashkentte website jaratiw boynsha\n jumis islep atir")
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBvmnRYh6IyYCNr05yXVc4TR8HZ_2FAAINFGsbHRmQSk0DrTfYX35-AQADAgADbQADOwQ",caption="Saginbaeva Nargiz \nTelegram bot boynsha master")

@dp.callback_query_handler(text="Py")
async def p(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBQGnRArUf2wersp3MmJz4BW-a6iuSAAK8E2sbHRmISr1MYyQTJK6eAQADAgADeQADOwQ",caption="🐍🐍🐍python kursi en' jaqsi ha'm keleshekte en' daramat ko'p towatin' prommalastriw tili \n 🐍🐍🐍kurs waqti 6 ay \n 🐍🐍🐍kurstin' aynia to'lemi 600.000 swm")
    await call.message.answer(text="Siz python kursini sayladin'iz, siz online oqiysizba yamasa offline ❓",reply_markup=dlPY)

@dp.callback_query_handler(text="offp")
async def off(call:types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer(text="Bul DataLife oqiw orayinin' ma'nzili,\nsizge bizlerdin' adminlerimiz baylanisadi")

@dp.callback_query_handler(text="Ja")
async def j(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBR2nRAzuSDnKOcI4g0ncpoUXOP8ylAAK_E2sbHRmISo5vVgNBXjK3AQADAgADbQADOwQ",caption="🍵🍵🍵Java kursi en' jaqsilardan biri bolip esap lanadi \n 🍵🍵🍵kurs waqti 3 ay \n 🍵🍵🍵kurstin' aynia to'lemi 300.000 swm")
    await call.message.answer(text="Siz Java kursini sayladin'iz, siz online oqiysizba yamasa offline ❓",
                              reply_markup=dlJa)

@dp.callback_query_handler(text="offj")
async def off(call: types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer(text="Bul DataLife oqiw orayinin' ma'nzili,\nsizge bizlerdin' adminlerimiz baylanisadi")

@dp.callback_query_handler(text="onj")
async def on(call: types.CallbackQuery):
    await call.message.answer_video(video="BAACAgIAAxkBAAICtGnTlI9EMhorlQ1dVC7V00cFzl_1AAIqmwACQV2ZSl_kwe7i6gFQOwQ",
                                        caption="1️⃣bul sizdin' birinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAICt2nTlJggvZeuG1YO9C_wzgFho-PAAAIsmwACQV2ZSsrye4Mu5Po9OwQ",
                                        caption="2️⃣bul sizdin' ekinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAICumnTlKGLjmbAfRh4OPvapRE9C3WAAAItmwACQV2ZSi-RckESFb23OwQ",
                                        caption="3️⃣bul sizdin' ushinshi video sabagin'iz")

@dp.callback_query_handler(text="C")
async def c(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBRGnRAxdIW8Sz9qlyUf2ZhdJyR-vRAAK9E2sbHRmISlY-mGngaDYaAQADAgADbQADOwQ",caption="🎮🎮🎮c++ en' jaqsi oyn istew ushin programma \n 🎮🎮🎮kurstin' waqti 4 ay \n 🎮🎮🎮kurstin' ayna to'lemi 300.000 swm ")
    await call.message.answer(text="Siz c++ kursini sayladin'iz, siz online oqiysizba yamasa offline ❓",
                              reply_markup=dlC)


@dp.callback_query_handler(text="offc")
async def off(call: types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer(text="Bul DataLife oqiw orayinin' ma'nzili,\nsizge bizlerdin' adminlerimiz baylanisadi")
@dp.callback_query_handler(text="onc")
async def on(call:types.CallbackQuery):
    await call.message.answer_video(video="BAACAgIAAxkBAAICvWnTlLI9Go0OdebuoYf_km8DIgUkAAIvmwACQV2ZSuovLzQJG6fyOwQ",caption="1️⃣bul sizdin' birinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAICwGnTlLjFFsMhicwuulKZM7xowiUGAAIwmwACQV2ZSmnXNDOlv14COwQ",caption="2️⃣bul sizdin' ekinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAICw2nTlL9O9OpJQaa_zHuooJ3eLv8iAAIxmwACQV2ZSq_dGImKkRw_OwQ",caption="3️⃣bul sizdin' ushinshi video sabagin'iz")
@dp.callback_query_handler(text="d")
async def d(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBTWnRA9GS0r9mF456OIIw14sKDi4VAALCE2sbHRmISqAfPPONuc7PAQADAgADbQADOwQ",caption="Data Base bul buxgalter ushin en' jaqsi kurs bolip esaplanadi \n kurstin' waqti 3 ay \n kurstin' ayna tolemi 300.000 swm")
    await call.message.answer(text="Siz Data Base kursini sayladin'iz, siz online oqiysizba yamasa offline ❓",
                              reply_markup=dlDB)
@dp.callback_query_handler(text="offdb")
async def off(call: types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer(text="Bul DataLife oqiw orayinin' ma'nzili,\nsizge bizlerdin' adminlerimiz baylanisadi")
@dp.callback_query_handler(text="ondb")
async def on(call:types.CallbackQuery):
    await call.message.answer_video(video="BAACAgIAAxkBAAICxmnTlMZ2ihlzVZ_noxcR--_o4PAAAzObAAJBXZlKBmB_-Up5fnQ7BA",caption="1️⃣bul sizdin' birinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAICyWnTlM1rh08TqNexdLhW9Ws3CtZwAAI1mwACQV2ZSkfmm1032ga2OwQ",caption="2️⃣bul sizdin' ekinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAICzGnTlNTeT1Uch4G--4COK37d86EKAAI3mwACQV2ZSouCFgzrB9DLOwQ",caption="3️⃣bul sizdin' ushinshi video sabagin'iz")



@dp.callback_query_handler(text="gd")
async def gd(call:types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBSmnRA7FoEHwiGxxqHzMzWfxX-yKqAALAE2sbHRmISnz2xPfNe2WyAQADAgADeQADOwQ",caption="graffik dizyan kursi bul adamlar ushin en' qolayli kurslardan biri bolip esap lanadi sebebi usi kursta 1 ay oqip siz zakazlar aliwniz mumkin \n kurstin' baxasi 250.000 swm")
    await call.message.answer(text="Siz graffic design kursini sayladin'iz, siz online oqiysizba yamasa offline ❓",
                              reply_markup=dlGD)


@dp.callback_query_handler(text="offgd")
async def off(call: types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer(text="Bul DataLife oqiw orayinin' ma'nzili,\nsizge bizlerdin' adminlerimiz baylanisadi")

@dp.callback_query_handler(text="ongd")
async def on(call: types.CallbackQuery):
    await call.message.answer_video(video="BAACAgIAAxkBAAICz2nTlNwGRW-FxDaDCvxAi3m1olxKAAI7mwACQV2ZSrYhWOVVqZd_OwQ",caption="1️⃣bul sizdin' birinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAIC0mnTlOKzqhu2jkuuknncizFwM1U0AAI8mwACQV2ZSphImob_ZSISOwQ",caption="2️⃣bul sizdin' ekinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAIC1WnTlOnb4uaDPey8FdNXUy-rk3ALAAI-mwACQV2ZSr5L0zXgagFkOwQ",caption="3️⃣bul sizdin' ushinshi video sabagin'iz")




@dp.callback_query_handler(text="ro")
async def ro(call: types.CallbackQuery):
    await call.message.answer_photo(photo="AgACAgIAAxkBAAIBUGnRBDxJAnfDJnj37-MOlCLUdFSfAALEE2sbHRmISi6C-WM7F6kDAQADAgADbQADOwQ",caption="robotatexnika en' jaqsi \n kurstin' waqti 2 ay \n kurstin' baxasi 250.000 swm")
    await call.message.answer(text="Siz robatotexnika kursini sayladin'iz, siz online oqiysizba yamasa offline ❓",
                              reply_markup=dlR)


@dp.callback_query_handler(text="offr")
async def off(call: types.CallbackQuery):
    await bot.send_location(chat_id=call.message.chat.id, latitude=42.45254266978752, longitude=59.62350100019317)
    await call.message.answer(text="Bul DataLife oqiw orayinin' ma'nzili,\nsizge bizlerdin' adminlerimiz baylanisadi")

@dp.callback_query_handler(text="onr")
async def on(call:types.CallbackQuery):
    await call.message.answer_video(video="BAACAgIAAxkBAAIC2GnTlPWPMu-oqezsJEMu6xQqIW4nAAI_mwACQV2ZSn9Pq8SYvEiNOwQ",caption="1️⃣bul sizdin' birinshi video sabagin'iz")
    await call.message.answer_video(video="BAACAgIAAxkBAAIC22nTlP7NZDaux-lYgpIZ2R72WkGLAAJBmwACQV2ZSr6GAxb12GcEOwQ",caption="2️⃣bul sizdin' ekinshi video sabagin'iz")



@dp.callback_query_handler(text="bac")
async def bac(call:types.CallbackQuery):
    await call.message.answer("Menu:", reply_markup=dl)
    await call.answer()
@dp.callback_query_handler(text="ba")
async def back(call: types.CallbackQuery):
    await call.message.answer("Menu:", reply_markup=dl)
    await call.answer()

@dp.message_handler()
async def default_nadler(message:types.Message):
    await message.answer("Iltimas /start basin'")




#########################Button############################
def build_keyboard(product):
    keys = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Satip aliw", callback_data=f"product:{product}")
        ],  # product:book korinisinde callback qaytadi
    ])
    return keys

python_lessons = Product(
    title="Python kurs",   # tema
    description="Kursti satip aliw ushin tomendegi tuymeni basin: ",   # podtema
    currency="UZS",   #valiyuta
    prices=[
        LabeledPrice(
            label="Kurs",
            amount=60000000,
        )

    ],
    start_parameter="create_invoice_python_kurs",   # STARTI
    photo_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRw1VvHQ7ZzfHWdBODYTF64oFMKI_fIVQ-sJg&s',
    photo_width=851,
    photo_height=1280,

    need_email=True,
    need_name=True,
    need_phone_number=True,
)

#########################FILTER###############################

#
@dp.callback_query_handler(text="onp")
async def show_lessons(call: types.CallbackQuery):
    caption = "Python Kurs.\n\n ✔️ Python Basic \n Cenasi: 600000 so'm"
    await call.message.reply(text=caption, reply_markup=build_keyboard("python_kurs"))

@dp.callback_query_handler(text="product:python_kurs")
async def lessons_invoice(call: types.CallbackQuery):
    await bot.send_invoice(chat_id=call.from_user.id,
                           **python_lessons.generate_invoice(),
                           payload="Python Kurs")   # imenno ne zat satilip atirgani qalese index qoysa boladi
    await call.answer()

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(a: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=a.id,
                                        ok=True)
    await bot.send_message(chat_id=a.from_user.id,
                           text="Tolew ushin raxmet!")

    await bot.send_video(chat_id=a.from_user.id,video="BAACAgIAAxkBAAIClGnTkNn1uI956azfbgvXmsFG1FAVAAIYmwACQV2ZShPQKlrCuFiYOwQ",
                                    caption="1️⃣bul sizdin' birinshi video sabagin'iz")
    await bot.send_video(chat_id=a.from_user.id,video="BAACAgIAAxkBAAICl2nTkOVihqnGXK8y6v-6ndJabTmeAAIbmwACQV2ZSu7mHW8xolaYOwQ",
                                    caption="2️⃣bul sizdin' ekinshi video sabagin'iz")
    await bot.send_video(chat_id=a.from_user.id,video="BAACAgIAAxkBAAICmmnTkP8XHCdNlwdV3xQUuZonCvXGAAIdmwACQV2ZSklkO-stGdgdOwQ",
                                    caption="3️⃣bul sizdin' ushinshi video sabagin'iz")

    await bot.send_message(chat_id=5195118856,
                           text=f"Tomendegi zat satildi: {a.invoice_payload}\n"
                                f"ID: {a.id}\n"
                                f"Telegram user: {a.from_user.full_name}\n"
                                f"Klient: {a.order_info.name}, "  # order_info.name = Satip aliwga jazilg'an ati, from_user.name = paydalaniwshinin ati
                                f"tel: {a.order_info.phone_number}")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
