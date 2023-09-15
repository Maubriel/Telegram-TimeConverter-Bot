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

def get_dia(in_dia):
    dia_a_nro = {
        'do':0,
        'lu':1,
        'ma':2,
        'mi':3,
        'ju':4,
        'vi':5,
        'sa':6,
    }
    nro_a_dia = ['Dom','Lun','Mar','Mie','Jue','Vie','Sab']
    if isinstance(in_dia, str):
        if len(in_dia) > 1:
            try:
                aux = in_dia[:2]
                return dia_a_nro[aux]
            except KeyError:
                return ''
    elif isinstance(in_dia, int):
        while in_dia < 0 or in_dia > 6:
            if in_dia < 0:
                in_dia += 7
            elif in_dia > 6:
                in_dia -= 7
        return nro_a_dia[in_dia]
    return ''


# /add [pais] - Añade un pais
@bot.message_handler(commands=['add'])
def add(message):
    entrada = message.text.lower().split()
    salida = 'output'
    chat_id = message.chat.id
    tableName = get_tableName(chat_id)
    if len(entrada) > 1:
        conn = sqlite3.connect('./database.db')
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
        entrada.pop(0)
        tz = ''
        for i in entrada:
            tz += i + ' '
        tz = tz.removesuffix(' ')
        zona = paises.get_timezone(tz)
        if zona != '':
            cursor.execute(f"INSERT OR IGNORE INTO {tableName} VALUES('" + zona + "')")
        conn.commit()
        conn.close()

# /timenow - Muestra todos los horarios actuales de los paises añadidos, o muestra UTC
# /timenow [pais] - Muestra el horario actual del pais indicado, o muestra mensaje de error si no se encuentra
@bot.message_handler(commands=['timenow'])
def timenow(message):
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
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
            pre_salida = []
            for zone in zones:
                tz = pytz.timezone(zone[0])
                fecha_hora = datetime.datetime.now(tz)
                pais_output = paises.get_pais(zone[0])
                dia_output = fecha_hora.weekday()
                hora_output = [fecha_hora.hour,fecha_hora.minute]
                pre_salida.append([pais_output,dia_output,hora_output])
            pre_salida_ordenada = sorted(pre_salida, key=lambda x: (x[1],x[2][0]))
            for sal in pre_salida_ordenada:
                    salida += sal[0] + ' - ' + get_dia(sal[1]) + ' ' + str(sal[2][0]).zfill(2) + ':' + str(sal[2][1]).zfill(2) + '\n'
        else:
            tz = pytz.timezone('UTC')
            fecha_hora = datetime.datetime.now(tz)
            dia = get_dia(fecha_hora.weekday())
            hora = str(fecha_hora.strftime('%H:%M'))
            salida = 'UTC 🕗 - ' + dia + ' ' + hora + '\n'
    else:
        entrada = entrada.split()
        entrada.pop(0)
        tz = ''
        for i in entrada:
            tz += i + ' '
        tz = tz.removesuffix(' ')
        zona = paises.get_timezone(tz)
        if zona != '':
            cursor.execute(f"SELECT timezone_id FROM {tableName} WHERE timezone_id='"+zona+"'")
            zona_in_table = cursor.fetchall()
            if len(zona_in_table) > 0:
                for x in zona_in_table:
                    tz = pytz.timezone(x[0])
                    fecha_hora = datetime.datetime.now(tz)
                    pais = paises.get_pais(x[0])
                    dia = get_dia(fecha_hora.weekday())
                    hora = str(datetime.datetime.now(tz).strftime('%H:%M'))
                    salida = pais + ' - ' + dia + ' ' + hora + '\n'
            else:
                salida = 'Pais no añadido'
    
    bot.reply_to(message, salida)


# /timeat [dia] [hora] [pais]
# /timeat sab 6pm Puerto Rico
# /timeat domingo 6pm mexico
# /timeat lu 06:07pm mx
# /timeat lun 18 mex
# /timeat MARTES 18:04 mx
@bot.message_handler(commands=['timeat'])
def timeat(message):
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
    entrada = message.text.lower().split()
    salida = 'output'
    chat_id = message.chat.id
    tableName = get_tableName(chat_id)
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
    if len(entrada) == 4 or len(entrada) == 5:
        entrada.pop(0)
        in_dia = get_dia(entrada.pop(0))
        in_hora = get_hora(entrada.pop(0))
        in_pais = ''
        for p in entrada:
            in_pais += p + ' '
        in_pais = in_pais.removesuffix(' ')
        zona = paises.get_timezone(in_pais)
        if zona != '' and in_dia != '' and in_hora != -1:
            salida = ''
            pre_salida = []
            cursor.execute(f"SELECT timezone_id FROM {tableName} WHERE timezone_id='"+zona+"'")
            zona_in_table = cursor.fetchall()
            if len(zona_in_table) > 0:
                tz = pytz.timezone(zona_in_table[0][0])
                hora_base = datetime.datetime.now(tz)
                cursor.execute(f"SELECT * FROM {tableName}")
                all_zones = cursor.fetchall()
                for az in all_zones:
                    tz = pytz.timezone(az[0])
                    hora_destino = datetime.datetime.now(tz)
                    hora_delta = hora_destino.hour - hora_base.hour
                    minuto_delta = hora_destino.minute - hora_base.minute
                    hora_output = [in_hora[0]+hora_delta, in_hora[1]+minuto_delta]
                    pais_output = paises.get_pais(az[0])
                    otra_hora = 0
                    if hora_output[1] < 0:
                        hora_output[1] += 60
                        otra_hora = -1
                    elif hora_output[1] > 59:
                        hora_output[1] -= 60
                        otra_hora = 1
                    hora_output[0] += otra_hora
                    otro_dia = 0
                    if hora_output[0] < 0:
                        hora_output[0] += 24
                        otro_dia = -1
                    elif hora_output[0] > 23:
                        hora_output[0] -= 24
                        otro_dia = 1
                    dia_output = in_dia + otro_dia
                    pre_salida.append([pais_output,dia_output,hora_output])
                pre_salida_ordenada = sorted(pre_salida, key=lambda x: (x[1],x[2][0]))
                for sal in pre_salida_ordenada:
                    salida += sal[0] + ' - ' + get_dia(sal[1]) + ' ' + str(sal[2][0]).zfill(2) + ':' + str(sal[2][1]).zfill(2) + '\n'
            else:
                salida = 'Pais no enlistado'
        else:
            salida = 'Pais no enlistado o error en la hora'
    else:
        salida = 'error en comando, mostrar help'
    
    bot.reply_to(message, salida)


@bot.message_handler(commands=['remove'])
def remove(message):
    entrada = message.text.lower().split()
    chat_id = message.chat.id
    if len(entrada) > 1:
        entrada.pop(0)
        tableName = get_tableName(chat_id)
        conn = sqlite3.connect('./database.db')
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(timezone_id TEXT PRIMARY KEY)")
        tz = ''
        for i in entrada:
            tz += i + ' '
        tz = tz.removesuffix(' ')
        zona = paises.get_timezone(tz)
        if zona != '':
            cursor.execute(f"DELETE FROM {tableName} WHERE timezone_id=('" + zona + "')")
        conn.commit()
        conn.close()
    pass


bot.polling()