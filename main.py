import os, telebot, sqlite3, pytz, datetime
import paises

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

def get_tableName(chat_id: int):
    tableName = ''
    if chat_id > 0:
        tableName = 'chatp' + str(abs(chat_id))
    else:
        tableName = 'chatg' + str(abs(chat_id))
    return tableName

# /add [pais] - Añade un pais
@bot.message_handler(commands=['add'])
def add(message):
    entrada = message.text.lower()
    salida = 'output'
    chat_id = message.chat.id
    tableName = get_tableName(chat_id)
    if len(entrada.removeprefix('/add')) > 1:
        entrada = entrada.removeprefix('/add ')
        conn = sqlite3.connect('./database.db')
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
        zona = paises.get_timezone(entrada)
        if zona != '':
            cursor.execute(f"INSERT OR IGNORE INTO {tableName} VALUES('" + zona + "')")
        conn.commit()
        conn.close()
        salida = 'Pais añadido'
    else:
        salida = 'No se pudo agregar el pais'

    bot.reply_to(message, salida)

# /timenow - Muestra todos los horarios actuales de los paises añadidos, o muestra UTC
# /timenow [pais] - Muestra el horario actual del pais indicado, o muestra mensaje de error si no se encuentra
@bot.message_handler(commands=['timenow'])
def timenow(message):
    entrada = message.text.lower()
    salida = 'output'
    chat_id = message.chat.id
    tableName = get_tableName(chat_id)
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
    if entrada == '/timenow':
        cursor.execute(f"SELECT * FROM {tableName}")
        zones = cursor.fetchall()
        if len(zones) > 0:
            salida = ''
            for zone in zones:
                pais = paises.get_pais(zone[0])
                aux = pytz.timezone(zone[0])
                hora = str(datetime.datetime.now(aux).strftime('%H:%M'))
                salida += pais + '\t\t' + hora + '\n'
        else:
            aux = pytz.timezone('UTC')
            hora = str(datetime.datetime.now(aux).strftime('%H:%M'))
            salida = 'UTC' + hora + '\n'
    else:
        entrada = entrada.removeprefix('/timenow ')
        zona = paises.get_timezone(entrada)
        if zona != '':
            cursor.execute(f"SELECT 1 OR IGNORE FROM {tableName} WHERE timezone_id='"+zona+"'")
            zona_in_table = str(cursor.fetchone())
            pais = paises.get_pais(zona_in_table)
            if zona_in_table != '' and pais != '':
                aux = pytz.timezone(zona_in_table)
                hora = str(datetime.datetime.now(aux).strftime('%H:%M'))
                salida = pais + '\t\t' + hora + '\n'
            else:
                salida = 'Pais no encontrado'
    
    bot.reply_to(message, salida)

# @bot.message_handler(commands=['list'])
# def list(message):
#     conn = sqlite3.connect('./database.db')
#     cursor = conn.cursor()
#     chat_id = message.chat.id
#     tableName = get_tableName(chat_id)

#     cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
#     cursor.execute(f"SELECT * FROM {tableName}")
#     rows = cursor.fetchall()
#     if len(rows) > 0:
#         items = ''
#         for row in rows:
#             items += row[0] + '\n'
#     else:
#         items = 'No hay elementos agregados'
#     bot.reply_to(message, items)


bot.polling()