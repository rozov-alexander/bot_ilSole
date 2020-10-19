import telebot
from math import ceil
from telebot import types

factor = 0.0;
degree = 3.8;
hour_seamstr = 350;
t_seamstr = 0.0;
hour_cut = 400;
t_cut = 0.0;
#bot key
bot = telebot.TeleBot('1254708225:AAFpAZ6ktx1We_ftR2SjbnsOTgLzMKiDU2s')


@bot.message_handler(content_types=['text'])
def start_button(message): #делаем стартовую кнопку
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_calc = types.InlineKeyboardButton(text='Расчёт', callback_data='start')  # кнопка «Расчёт»
    keyboard.add(key_calc)  # добавляем кнопку в клавиатуру
    text1 = 'Для начала расчёта нажми на кнопку'
    bot.send_message(message.from_user.id, text=text1, reply_markup=keyboard)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Для начала нового расчёта нажми кнопку, или напиши "шить"')
    elif message.text.lower() == 'шить':
        bot.send_message(message.chat.id, 'Начнём')
        start_handler(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call): #Отрабатываем нажатие на кнопку
    if call.data == "start":
        bot.send_message(chat_id=call.message.chat.id, text=f"Значения для расчёта стоимости образца.\n"
                                                            f"Коэффициент партии = {degree}\n"
                                                            f"Час швеи = {hour_seamstr}.\n"
                                                            f"Час закройщика = {hour_cut}.")
        start_handler(call)


def start_handler(message): #запрашиваем значение
    try:
        chat_id = message.from_user.id
        msg = bot.send_message(chat_id, text=f"Введите 'Коэффициент сложности ткани:'")
        bot.register_next_step_handler(msg, factor_of_fabric)
    except Exception:
        bot.reply_to(message, "ooops")

def factor_of_fabric(message):
    global factor
    chat_id = message.chat.id
    factor1 = message.text
    try:
        factor = float(factor1)
        msg = bot.send_message(chat_id, f"Коэффициент сложности ткани = {factor}. \nВведите 'Время на пошив:")
        bot.register_next_step_handler(msg, t_seamstress) #вывод результата и переход в след.функцию
    except:
        msg = bot.send_message(chat_id, 'Значение должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, factor_of_fabric)
        return


def degree_of_difficulty(message):
    global degree
    chat_id = message.from_user.id
    degree = message.text
    if not degree.isdigit():
        msg = bot.send_message(chat_id, 'Значение должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, degree_of_difficulty)
        return
    msg = bot.send_message(chat_id, f"Коэффициент сложности изделия = {degree}.\nВведите 'Час швеи:'") #вывод результата и переход в след.функцию
    bot.register_next_step_handler(msg, hour_seamstress)


def hour_seamstress(message):
    global hour_seamstr
    chat_id = message.from_user.id
    hour_seamstr = message.text
    if not hour_seamstr.isdigit():
        msg = bot.send_message(chat_id, 'Значение должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, hour_seamstress) #возврат в начало функции
        return
    msg = bot.send_message(chat_id, f"Час швеи = {hour_seamstr}.\nВведите 'Время на пошив:'") #вывод результата и переход в след.функцию
    bot.register_next_step_handler(msg, t_seamstress)


def t_seamstress(message):
    global t_seamstr
    chat_id = message.from_user.id
    t_seamstr = message.text
    if not t_seamstr.isdigit():
        msg = bot.send_message(chat_id, 'Значение должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, t_seamstress) #возврат в начало функции
        return
    msg = bot.send_message(chat_id, f"Время на пошив = {t_seamstr}.\nВведите  'Время на закрой:'") #вывод результата и переход в след.функцию
    bot.register_next_step_handler(msg, t_cutter)


def hour_cutter(message):
    global hour_cut
    chat_id = message.from_user.id
    hour_cut = message.text
    if not hour_cut.isdigit():
        msg = bot.send_message(chat_id, 'Значение должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, hour_cutter) #возврат в начало функции
        return
    msg = bot.send_message(chat_id, f"Час закройщика = {hour_cut}.\nВведите  'Время на закрой:'") #вывод результата и переход в след.функцию
    bot.register_next_step_handler(msg, t_cutter)


def t_cutter(message):
    global t_cut
    chat_id = message.from_user.id
    t_cut = message.text
    if not t_cut.isdigit():
        msg = bot.send_message(chat_id, 'Значение должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, t_cutter) #возврат в начало функции
        return
    bot.send_message(chat_id, f"Коэффициент сложности ткани = {factor}. \n" #вывод констант
                              f"Коэффициент партии = {degree}. \n"
                              f"Час швеи = {hour_seamstr}.\n"
                              f"Время на пошив = {t_seamstr}.\n"
                              f"Час закройщика = {hour_cut}.\n"
                              f"Время на закрой = {t_cut}.\n"
                           )
    #расчёт требуемых значений
    total_sample = (hour_seamstr / 60 * float(t_seamstr) + hour_cut / 60 * float(t_cut)) * (1 + degree) * float(factor)
    total_10 = (hour_seamstr / 60 * float(t_seamstr) + (hour_cut - 50) / 60 * float(t_cut)) * (1 + degree - 0.6) * float(factor)
    total_30 = ((hour_seamstr - 50)/ 60 * float(t_seamstr) + (hour_cut - 50) / 60 * (float(t_cut)*0.9)) * (1 + degree - 1.1) * float(factor)
    total_50 = ((hour_seamstr - 100)/ 60 * float(t_seamstr) + (hour_cut - 90) / 60 * (float(t_cut)*0.9)) * (1 + degree - 1.6) * float(factor)
    total_99 = ((hour_seamstr - 100)/ 60 * float(t_seamstr) + (hour_cut - 90) / 60 * (float(t_cut)*0.9)) * (1 + degree - 2.2) * float(factor)
    total_300 = ((hour_seamstr - 100)/ 60 * float(t_seamstr) + (hour_cut - 90) / 60 * (float(t_cut)*0.9*0.9)) * (1 + degree - 2.6) * float(factor)
    total_301 = ((hour_seamstr - 100)/ 60 * float(t_seamstr) + (hour_cut - 90) / 60 * (float(t_cut)*0.9*0.9)) * (1 + degree - 2.8) * float(factor)

    bot.send_message(chat_id, f"Стоимость образца = {ceil(total_sample/10)*10}\n" #вывод расчётных значений
                              f"Стоимость партии от 2 до 10 единиц = {ceil(total_10/10)*10}\n"
                              f"Стоимость партии от 11 до 30 единиц = {ceil(total_30/10)*10}\n"
                              f"Стоимость партии от 31 до 50 единиц = {ceil(total_50/10)*10}\n"
                              f"Стоимость партии от 51 до 99 единиц = {ceil(total_99/10)*10}\n"
                              f"Стоимость партии от 100 до 300 единиц = {ceil(total_300/10)*10}\n"
                              f"Стоимость партии более 300 единиц = {ceil(total_301/10)*10}")

#if __name__ == '__main__':
#    bot.polling(none_stop=True)




bot.polling()
