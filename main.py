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
    salida = 'Pais no soportado'
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
            cursor.execute(f"SELECT timezone_id FROM {tableName} WHERE timezone_id='"+zona+"'")
            zona_in_table = cursor.fetchall()
            if len(zona_in_table) > 0:
                for x in zona_in_table:
                    pais = paises.get_pais(x[0])
                    aux = pytz.timezone(x[0])
                    hora = str(datetime.datetime.now(aux).strftime('%H:%M'))
                    salida = pais + '\t\t' + hora + '\n'
            else:
                salida = 'Pais no añadido'
    
    bot.reply_to(message, salida)

def get_hora(str_hora:str):
    hm = []
    if 'am' in str_hora:
        str_hora = str_hora.removesuffix('am')
        str_hora = str_hora.split(':')
        if str_hora[0] == 12:
            hm.append(0)
        else:
            hm.append(int(str_hora[0]))
        if len(str_hora) > 1:
            hm.append(int(str_hora[1]))
        else:
            hm.append(0)
    elif 'pm' in str_hora:
        str_hora = str_hora.removesuffix('pm')
        str_hora = str_hora.split(':')
        if str_hora[0] == 12:
            hm.append(int(str_hora[0]))
        else:
            hm.append(int(str_hora[0])+12)
        if len(str_hora) > 1:
            hm.append(int(str_hora[1]))
        else:
            hm.append(0)
    else:
        str_hora = str_hora.split(':')
        for i in str_hora:
            hm.append(int(i))
        if len(hm) < 2: hm.append(0)
    if hm[0] > 23:
        return -1
    return hm

# /timeat [hora] [pais]
# /timeat 6pm Puerto Rico
# /timeat 6pm mexico
# /timeat 06:07pm mx
# /timeat 18 mex
# /timeat 18:04 mx
@bot.message_handler(commands=['timeat'])
def timeat(message):
    entrada = message.text.lower().split()
    salida = 'output'
    chat_id = message.chat.id
    tableName = get_tableName(chat_id)
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
    if len(entrada) == 3 or len(entrada) == 4:
        entrada.remove('/timeat')
        if len(entrada) == 3:
            in_pais = entrada[1] + ' ' + entrada[2]
        else:
            in_pais = entrada[1]
        zona = paises.get_timezone(in_pais)
        in_hora = get_hora(entrada[0])
        if zona != '' and in_hora != -1:
            salida = ''
            cursor.execute(f"SELECT timezone_id FROM {tableName} WHERE timezone_id='"+zona+"'")
            zona_in_table = cursor.fetchall()
            if len(zona_in_table) > 0:
                for x in zona_in_table:
                    tz = pytz.timezone(x[0])
                    time_base = datetime.datetime.now(tz)
                cursor.execute(f"SELECT * FROM {tableName}")
                all_zones = cursor.fetchall()
                for y in all_zones:
                    tz = pytz.timezone(y[0])
                    time_destino = datetime.datetime.now(tz)
                    hora_delta = time_destino.hour - time_base.hour
                    minuto_delta = time_destino.minute - time_base.minute
                    time_ouput = [in_hora[0]+hora_delta, in_hora[1]+minuto_delta]
                    pais_ouput = paises.get_pais(y[0])
                    hora_menos = 0
                    if time_ouput[1] < 0:
                        time_ouput[1]+=60
                        hora_menos = -1
                    if time_ouput[0] < 0:
                        time_ouput[0]+=24
                    time_ouput[0]+=hora_menos
                    salida += pais_ouput + ' ' + str(time_ouput[0]).zfill(2) + ':' + str(time_ouput[1]).zfill(2) + '\n'
            else:
                salida = 'Pais no enlistado'
        else:
            salida = 'Pais no enlistado o error en la hora'
    else:
        salida = 'error en comando, mostrar help'
    
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