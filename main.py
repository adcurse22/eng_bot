import telebot
from decouple import config

TOKEN = config("TOKEN")
bot = telebot.TeleBot(TOKEN)

questions = [
    'Введите вашу фамилию и имя. Например "Алексеев Алексей"',
    'Где вы проживаете? \n Введите ваше местоположение: \n город (деревня), регион. страна. Например: "Новосибирск, Новосибирская облась, Россия"',
    'Для кого Вы выбираете этот курс? \n 1. Для себя \n 2. Для своего ребенка Выберите один вариант ответа и введите его номер \n Например "1"',
    'Введите свой возраст \n Например "35"',
    'Введите возраст ребёнка',
    'Какой бы Вы хотели изучать язык? \n 1.Английский \n 2.Французский \n 3.Испанский \n 4.Немецкий \n 5.Сербский \n 6.Турецкий \n Выберите один вариант ответа и введите его номер Например "1"',
    'Как вы оцениваете свой уровень знания языка. \n 1. Нулевой или ближе к нулю \n 2.Читаю, но не говорю \n 3.Понимаю, но не говорю \n 4.Базовый: могу объясниться в простых ситуациях \n 5.Средний уровень есть \n6.Свободно говорю Выберите один вариант ответа и введите его номер \n Например "1"',
    'Какой у вас опыт изучения языка \n 1. Не учил язык \n 2. Учил в школе \n 3. Школа и вуз \n 4. Курсы или индивидуальные занятия \n 5. Есть опыт проживания в стране изучаемого языка \n Выберите один вариант ответа и введите его номер Например "5"',
    'Пройдите тестирование по сылке \n Также Вы можете пропустить тестирование и ответить "Не прошёл" \n Ссылка: Например \n "B1"',
    'Для чего Вам нужен язык? \n 1. Общение \n 2. Путешествия \n 3.Срочная поездка \n 4.Релокация \n 5.Работа \n 6 Учёба \n 7.Хобби \n 8. Саморазвитие \n Выберите один или несколько вариантов ответа и введите их номера \n Например "1, 2, 5, 7"',
    'Какова цель Вашего обучения? \n 1.Сдать экзамен TOEFL, IELTS, FCE, CAE,  CPE, BEC, DELF, DALF, ОГЭ (английский), ЕГЭ (английский), ОГЭ (французский), ЕГЭ (французский), \n экзамен в вузе, экзамен по моей профессии, пока не решил \n 2.Пройти собеседование \n 3.Пройти тестирование \n 4.Повысить уровень Выберите один вариант ответа и введите его номер Например "1" Также Вы можете ввести свой вариант',
    'Введите срок, за который Вы предполагаете достичь своей цели \n Например "1 год 3 месяца"',
    'Сколько времени Вы можете уделять изучению языка? \n 1. 1 раз в неделю 2 часа 2. \n2 или 3 раза в неделю по часу \n 3. Только 2 раза в неделю \n 4. Обязательно 3 раза в неделю \n 5. Каждый день или почти каждый по 20-40 минут \n6. Каждый день по нескольку часов \n Например "2" \n Также Вы можете ввести свой вариант',
    'В какое время дня Вам удобнее заниматься? \n 1. Утро \n 2. День \n 3. Вечер Выберите один вариант ответа и введите его номер Например "3" Также Вы можете ввести свой вариант',
    'В какой день недели Вам удобнее заниматься? \n 1. Будние дни \n 2. Выходные \n 3. И будние и выходные дни Выберите один вариант ответа и введите его номер Например "2" \n Также Вы можете ввести свой вариант',
    'Готовы ли Вы заниматься постоянно в одно и то же время или у вас плавающий график? \n 1. Выбираю постоянные дни и время \n 2. Желательно договариваться накануне (за день до занятия)Выберите один вариант ответа и введите его номер \n Например "2" Или Вы можете сообщать свой расписание на определённй промежуток времени? Тогда в сообщении введите время, например "2 недели вперёд" или "месяц вперёд"',
    'Готовы ли Вы делать домашние задания? \n 1. Да, в полном объёме \n 2. Да, но не большие на 20-30 минут \n 3. Готов(а) минут 10 позаниматься \n 4. Желательно обойтись без домашних заданий Выберите один вариант ответа и введите его номер \n Например "4"',
]




user_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data[user_id] = {'index': 0, 'answers': []}
    bot.reply_to(message, "Привет! Пройдите опрос, и мы дадим вам персональные рекомендации по изучению языка :")
    bot.send_message(user_id, questions[0])


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return  # Пользователь начал вводить текст до команды /start

    user_data[user_id]['answers'].append(message.text)
    user_data[user_id]['index'] += 1

    if user_data[user_id]['index'] < len(questions):
        next_question = questions[user_data[user_id]['index']] 
        bot.send_message(user_id, next_question)
    else:
        bot.send_message(user_id, "Спасибо за ответы!")
        # Тут можно сохранить ответы в файл или базу данных
        with open(f"{user_id}_answers.txt", "w") as file:
            for q, a in zip(questions, user_data[user_id]['answers']):
                file.write(q + "\n" + a + "\n\n")
        del user_data[user_id]


if __name__ == '__main__':
    bot.polling(none_stop=True)