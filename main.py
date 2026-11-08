import json
import os
import random
import time

import vk_api
from requests.exceptions import ConnectionError as RequestsConnectionError

from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

load_dotenv()

TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = 242961901

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, GROUP_ID)
print("Бот запущен!")

DIRECTIONS = {
    "development": {
        "label": "Разработка программного обеспечения",
        "summary": "Создание продукта, программной логики и приложений.",
        "advice": (
            "Общий старт: изучите основы алгоритмов, Git и один язык "
            "(JavaScript/TypeScript или Python). Сделайте небольшой проект и "
            "опубликуйте код на GitHub.\n"
            "• Frontend-разработка: начните с HTML, CSS, JavaScript и TypeScript, "
            "затем соберите интерфейс на React.\n"
            "• Backend-разработка: изучите Python или JavaScript, API и SQL; "
            "создайте серверную часть приложения.\n"
            "• Full-stack: после основ frontend и backend свяжите их в одном "
            "небольшом веб-проекте.\n"
            "• Разработка игр и спец. софта: попробуйте C# и Unity либо "
            "C++ и Unreal Engine, соберите простой прототип."
        ),
    },
    "qa": {
        "label": "QA и тестирование",
        "summary": "Проверка продукта, сценариев и качества перед выпуском.",
        "advice": (
            "Общий старт: научитесь составлять чек-листы, тест-кейсы и понятные "
            "баг-репорты. Практикуйтесь на учебных приложениях, изучите HTTP и "
            "основы SQL.\n"
            "• Ручное тестирование: проверяйте пользовательские сценарии, "
            "граничные случаи и корректность интерфейса.\n"
            "• Автоматизированное тестирование: освойте основы программирования, "
            "Postman и один инструмент автотестов, например Selenium или Playwright.\n"
            "• Нагрузочное тестирование: изучите метрики производительности и "
            "проведите безопасный тест на учебном приложении или собственном стенде."
        ),
    },
    "design": {
        "label": "Дизайн (UX/UI)",
        "summary": "Проектирование удобного пользовательского опыта и интерфейсов.",
        "advice": (
            "Общий старт: освойте Figma, композицию, типографику и создание "
            "интерактивных прототипов. Разберите знакомый сервис и оформите "
            "результат в портфолио.\n"
            "• UX-исследования: научитесь проводить интервью, анализировать "
            "поведение пользователей и строить User Journey; проверьте гипотезы "
            "на небольшой группе.\n"
            "• UI-дизайн: тренируйтесь создавать макеты, компоненты и дизайн-системы; "
            "соберите несколько экранов и проверьте их на разных размерах."
        ),
    },
    "analytics": {
        "label": "Аналитика и работа с данными (Data Science & Analytics)",
        "summary": "Поиск закономерностей и превращение данных и требований в решения.",
        "advice": (
            "Общий старт: Excel или Google Sheets, SQL (SELECT, JOIN, GROUP BY), "
            "описательная статистика и визуализация. Сделайте небольшой проект "
            "на открытых данных и объясните выводы простым языком.\n"
            "• Системный / бизнес-аналитик: тренируйте интервью и сбор требований, "
            "user stories, BPMN/UML, описание API и проверку требований с заказчиком.\n"
            "• Продуктовый аналитик: изучите события, воронки, конверсию, удержание, "
            "когорты, юнит-экономику и основы A/B-тестов; соберите дашборд и "
            "предложите решение по метрикам.\n"
            "• Data Science / ML-инженер: добавьте Python, pandas, вероятность и "
            "статистику, затем scikit-learn. Обучите простую модель, сравните её "
            "с базовым прогнозом и проверьте качество; позже изучайте API, Docker "
            "и мониторинг моделей."
        ),
    },
    "infrastructure": {
        "label": "Инфраструктура и кибербезопасность",
        "summary": "Надёжность, автоматизация развёртывания и защита систем.",
        "advice": (
            "Общий старт: изучите Linux, командную строку, сети (TCP/IP, DNS, "
            "HTTP), Git и основы Bash или Python.\n"
            "• DevOps / SRE: соберите учебное приложение в Docker, настройте "
            "CI/CD и попробуйте развернуть его в облачной учебной среде. Затем "
            "изучайте мониторинг и надёжность сервисов.\n"
            "• Кибербезопасность: начните с основ защиты сетей и систем, разбора "
            "логов и безопасной настройки. Практикуйтесь только на собственном "
            "стенде и в легальных учебных лабораториях."
        ),
    },
    "management": {
        "label": "Управление проектами и продуктом",
        "summary": "Координация команды, сроков, приоритетов и развития продукта.",
        "advice": (
            "Общий старт: изучите Scrum/Kanban, постановку целей, приоритизацию "
            "и основы работы с метриками. На учебном проекте опишите проблему, "
            "составьте план и подведите итоги.\n"
            "• Product Manager / Product Owner: исследуйте потребности пользователей, "
            "сформулируйте видение продукта, приоритеты и измеримые цели (OKR).\n"
            "• Project Manager / Scrum Master: потренируйтесь планировать сроки и "
            "ресурсы, организовывать командную работу и отслеживать риски.\n"
            "• Team Lead: развивайте технические навыки и практикуйте постановку "
            "задач, обратную связь и поддержку команды; обычно полезен опыт разработки."
        ),
    },
    "docs_support": {
        "label": "Техническая документация и поддержка",
        "summary": "Понятные инструкции и помощь пользователям и командам.",
        "advice": (
            "Общий старт: учитесь ясно описывать технические процессы, освойте "
            "Markdown и основы HTTP. Напишите инструкцию и попросите новичка "
            "выполнить её без подсказок.\n"
            "• Технический писатель: создавайте пошаговые руководства, FAQ и "
            "API-документацию; изучите структуру документации и инструменты "
            "совместной работы, например Confluence.\n"
            "• Специалист техподдержки: тренируйтесь уточнять симптомы и "
            "воспроизводить проблему, искать ответы в логах и базе знаний; "
            "изучите основы SQL и правила эскалации сложных обращений."
        ),
    },
}

QUESTION_BLOCKS = [
    ("Личные качества", [
        ("Вам дали сложную задачу, решение которой неочевидно. Что вы сделаете в первую очередь?", [
            ("Буду разбираться сам(а), пока не найду решение, даже если это займёт много времени", "development"),
            ("Разберу задачу на мелкие части и проверю, на каком шаге что-то идёт не так", "qa"),
            ("Соберу всю доступную информацию и цифры, чтобы понять причины", "analytics"),
            ("Обсужу задачу с коллегами, распределю роли и составлю план", "management"),
        ]),
        ("Как вы относитесь к деталям и порядку?", [
            ("Замечаю мелкие несоответствия и ошибки, которые другие пропускают", "qa"),
            ("Мне важно, чтобы всё выглядело гармонично и аккуратно", "design"),
            ("Люблю, когда всё описано чётко и по пунктам, чтобы любой разобрался", "docs_support"),
            ("Люблю, чтобы всё работало стабильно и без сбоев", "infrastructure"),
        ]),
        ("Что в общении с людьми у вас получается лучше всего?", [
            ("Объяснять сложное простыми словами", "docs_support"),
            ("Слушать человека и понимать, что ему на самом деле нужно", "design"),
            ("Договариваться, мотивировать и держать всех в курсе", "management"),
            ("Мало общаюсь, лучше работаю в одиночку над одной задачей", "development"),
        ]),
        ("Как вы ведёте себя в стрессовой ситуации (горят сроки, что-то сломалось)?", [
            ("Сохраняю спокойствие и действую по чёткому алгоритму", "infrastructure"),
            ("Быстро ищу причину и чиню", "development"),
            ("Беру на себя координацию: кто что делает и к какому сроку", "management"),
            ("Поддерживаю тех, кому трудно, и помогаю им разобраться", "docs_support"),
        ]),
        ("Что вас больше всего мотивирует в работе?", [
            ("Видеть, как придуманная мной вещь заработала", "development"),
            ("Находить закономерности и неожиданные выводы в данных", "analytics"),
            ("Создавать красивые и удобные вещи, которыми приятно пользоваться", "design"),
            ("Найти критическую ошибку раньше, чем её увидят пользователи", "qa"),
        ]),
    ]),
    ("Опыт в IT и в жизни", [
        ("Что из этого вы уже пробовали делать?", [
            ("Писать код (сайт, бот, программу, игру)", "development"),
            ("Рисовать макеты, делать графику или оформлять презентации", "design"),
            ("Настраивать компьютер, ставить Linux, разбираться в сетях и защите", "infrastructure"),
            ("Работать с таблицами: считать, строить графики, сравнивать данные", "analytics"),
        ]),
        ("Какой опыт из жизни вам ближе всего?", [
            ("Организовывал(а) мероприятия, проекты, командные дела", "management"),
            ("Писал(а) тексты, конспекты, инструкции, помогал(а) другим разобраться", "docs_support"),
            ("Часто находил(а) ошибки в играх, приложениях или чужих работах", "qa"),
            ("Любил(а) головоломки, логические игры, олимпиады", "analytics"),
        ]),
        ("Как вы обычно осваиваете новое?", [
            ("Сразу пробую на практике и смотрю, что получится", "development"),
            ("Читаю документацию и разбираюсь, как всё устроено внутри", "infrastructure"),
            ("Изучаю удачные примеры и подмечаю, как это сделано у лучших", "design"),
            ("Учусь через общение: спрашиваю опытных людей и обсуждаю в команде", "management"),
        ]),
        ("Вспомните учебный или личный проект, который вам удался. В чём была ваша сильная сторона?", [
            ("Придумал(а) идею и довёл(а) её до готового результата", "management"),
            ("Тщательно всё проверил(а) и довёл(а) до безупречного состояния", "qa"),
            ("Разобрался(лась) в фактах и данных и сделал(а) из них выводы", "analytics"),
            ("Объяснил(а) всё так, что другие смогли повторить", "docs_support"),
        ]),
    ]),
    ("Интересы", [
        ("Какой контент вам интереснее смотреть или читать?", [
            ("Как работают взломы, защита, сети и вирусы", "infrastructure"),
            ("Как создаются игры и приложения, разборы кода", "development"),
            ("Дизайн интерфейсов, анимация, фирменный стиль", "design"),
            ("Истории стартапов, продуктов и команд", "management"),
        ]),
        ("Какая из этих задач кажется вам самой интересной?", [
            ("Выяснить, почему упала активность пользователей, и предложить гипотезы", "analytics"),
            ("Придумать, как «сломать» новую функцию и где она может не сработать", "qa"),
            ("Настроить сервер так, чтобы сервис обновлялся и запускался автоматически", "infrastructure"),
            ("Написать понятную инструкцию к новому сервису", "docs_support"),
        ]),
        ("Что вам ближе по духу?", [
            ("Погрузиться в задачу на несколько часов и работать «в потоке»", "development"),
            ("Исследовать, почему люди ведут себя в приложениях именно так", "design"),
            ("Вести людей к общей цели и отвечать за результат", "management"),
            ("Искать слабые места в системе и думать, как это сделал бы злоумышленник", "infrastructure"),
        ]),
    ]),
    ("Рабочие ситуации и ценности", [
        ("Какой рабочий день вам комфортнее?", [
            ("Чёткие задачи, проверка и фиксация результатов, поиск расхождений", "qa"),
            ("Работа с цифрами, отчётами и вопросом «почему так происходит?»", "analytics"),
            ("Мониторинг систем, автоматизация, быстрое решение сбоев", "infrastructure"),
            ("Общение с пользователями и командой, объяснения и помощь", "docs_support"),
        ]),
        ("Какую роль в команде вы бы выбрали?", [
            ("«Последний рубеж», который не пропустит ошибку к пользователю", "qa"),
            ("«Голос пользователя», который отстаивает удобство продукта", "design"),
            ("«Капитан», отвечающий за сроки и итоговый результат", "management"),
            ("«Переводчик» между сложной техникой и обычными людьми", "docs_support"),
        ]),
        ("Что для вас важнее всего в будущей профессии?", [
            ("Создавать продукт своими руками (код, архитектура)", "development"),
            ("Глубоко разбираться в данных и влиять на решения бизнеса", "analytics"),
            ("Быть экспертом по надёжности и защите систем", "infrastructure"),
            ("Быть уверенным(ой) в качестве всего, что выходит к людям", "qa"),
        ]),
    ]),
]

QUESTIONS = [
    {
        "block": block,
        "text": question,
        "options": [
            {"text": answer, "direction": direction}
            for answer, direction in answers
        ],
    }
    for block, block_questions in QUESTION_BLOCKS
    for question, answers in block_questions
]


def default_scores():
    return {key: 0 for key in DIRECTIONS}


def build_start_keyboard():
    return json.dumps(
        {
            "one_time": True,
            "buttons": [
                [
                    {
                        "action": {"type": "text", "label": "Начать"},
                        "color": "primary",
                    }
                ]
            ],
        },
        ensure_ascii=False,
    )


def build_intro_keyboard():
    return json.dumps(
        {
            "one_time": False,
            "buttons": [
                [
                    {
                        "action": {"type": "text", "label": "Приступить к тесту"},
                        "color": "primary",
                    }
                ],
                [
                    {
                        "action": {"type": "text", "label": "Перезапустить бота"},
                        "color": "secondary",
                    }
                ],
            ],
        },
        ensure_ascii=False,
    )


def build_question_keyboard(question, question_index):
    buttons = []
    for index in range(len(question["options"])):
        buttons.append([
            {
                "action": {
                    "type": "text",
                    "label": f"{question_index + 1}{'абвг'[index]}",
                },
                "color": "primary",
            }
        ])
    if question_index > 0:
        buttons.append([
            {
                "action": {"type": "text", "label": "⬆️ Вернуться"},
                "color": "secondary",
            }
        ])
    buttons.append([
        {
            "action": {"type": "text", "label": "Перезапустить бота"},
            "color": "secondary",
        }
    ])
    return json.dumps({"one_time": True, "buttons": buttons}, ensure_ascii=False)


def build_question_message(question_index):
    question = QUESTIONS[question_index]
    block_number = get_question_block_number(question_index)
    options = [
        f"{question_index + 1}{'абвг'[index]}) {option['text']}"
        for index, option in enumerate(question["options"])
    ]
    return (
        f"🧭 Блок {block_number} · {question['block']}\n"
        f"📍 Вопрос {question_index + 1} из {len(QUESTIONS)}\n"
        "──────────────\n\n"
        f"❓ {question['text']}\n\n"
        + "\n".join(options)
    )


def find_chosen_option(question_index, text):
    question = QUESTIONS[question_index]
    for index, option in enumerate(question["options"]):
        button_key = f"{question_index + 1}{'абвг'[index]}"
        if text in {button_key, option["text"].casefold()}:
            return option
    return None


def is_stale_answer_button(question_index, text):
    for previous_question_index in range(question_index):
        question = QUESTIONS[previous_question_index]
        for index in range(len(question["options"])):
            button_key = f"{previous_question_index + 1}{'абвг'[index]}"
            if text == button_key:
                return True
    return False


def undo_last_answer(state):
    state["step"] -= 1
    direction = state["answers"].pop()
    state["scores"][direction] -= 1


def get_question_block_number(question_index):
    blocks = list(dict.fromkeys(item["block"] for item in QUESTIONS))
    return blocks.index(QUESTIONS[question_index]["block"]) + 1


def build_vk_format_data(message, bold_segments):
    items = []
    for segment in bold_segments:
        start = message.index(segment)
        offset = len(message[:start].encode("utf-16-le")) // 2
        length = len(segment.encode("utf-16-le")) // 2
        items.append({"type": "bold", "offset": offset, "length": length})
    return json.dumps({"version": 1, "items": items}, ensure_ascii=False)


def get_question_bold_segments(question_index):
    question = QUESTIONS[question_index]
    return [
        f"🧭 Блок {get_question_block_number(question_index)} · {question['block']}",
        f"📍 Вопрос {question_index + 1} из {len(QUESTIONS)}",
        f"❓ {question['text']}",
    ]


def format_points(points):
    last_two_digits = points % 100
    last_digit = points % 10
    if 11 <= last_two_digits <= 14:
        word = "баллов"
    elif last_digit == 1:
        word = "балл"
    elif 2 <= last_digit <= 4:
        word = "балла"
    else:
        word = "баллов"
    return f"{points} {word}"


def build_result_messages(scores):
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top = [(direction, points) for direction, points in ranked if points > 0][:3]

    if not top:
        message = (
            "📊 РЕЗУЛЬТАТЫ ТЕСТА\n\n"
            "Пока не удалось определить выраженные предпочтения. "
            "Попробуйте пройти тест ещё раз и выбирайте варианты, "
            "которые действительно вам интересны 🙂"
        )
        return [
            (
                message,
                build_vk_format_data(message, ["📊 РЕЗУЛЬТАТЫ ТЕСТА"]),
            )
        ]

    summary_paragraphs = [
        "📊 РЕЗУЛЬТАТЫ ТЕСТА",
        "По вашим ответам вам могут подойти:",
    ]
    for direction, points in top:
        summary_paragraphs.append(
            f"🔹 {DIRECTIONS[direction]['label']} — {format_points(points)}"
        )

    summary_message = (
        summary_paragraphs[0]
        + "\n\n"
        + "\n".join(summary_paragraphs[1:])
    )
    messages = [
        (
            summary_message,
            build_vk_format_data(
                summary_message,
                [
                    "📊 РЕЗУЛЬТАТЫ ТЕСТА",
                    "По вашим ответам вам могут подойти:",
                    *[DIRECTIONS[key]["label"] for key, _ in top],
                ],
            ),
        ),
        (
            "💡 Ниже представлены практические советы и рекомендации по первым шагам ⬇️",
            None,
        ),
    ]

    for direction, points in top:
        item = DIRECTIONS[direction]
        heading = f"🎯 {item['label']}"
        message = "\n\n".join(
            [
                f"{heading}\n━━━━━━━━━━━━━━━━━━━━\n{item['summary']}",
                item["advice"].replace("\n", "\n\n"),
            ]
        )
        messages.append(
            (message, build_vk_format_data(message, [heading]))
        )

    conclusion = (
        "❗ ВАЖНО\n\n"
        "Баллы показывают интересы, а не уровень навыков.\n"
        "Если результаты близки, попробуйте по одному небольшому проекту "
        "из нескольких направлений 🙂\n\n"
        "Если захотите пройти тест ещё раз, нажмите «Начать» 🔄"
    )
    messages.append(
        (conclusion, build_vk_format_data(conclusion, ["❗ ВАЖНО"]))
    )

    return messages


state_by_peer = {}


def listen_with_reconnect():
    global longpoll

    retry_delay = 5
    while True:
        try:
            for event in longpoll.listen():
                retry_delay = 5
                yield event
        except RequestsConnectionError as error:
            print(
                f"Потеряно соединение с VK Long Poll: {error}. "
                f"Повторное подключение через {retry_delay} сек."
            )
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)

            try:
                longpoll = VkBotLongPoll(vk_session, GROUP_ID)
            except RequestsConnectionError as reconnect_error:
                print(f"Не удалось переподключиться к VK Long Poll: {reconnect_error}")


for event in listen_with_reconnect():
    if event.type != VkBotEventType.MESSAGE_NEW:
        continue

    message = event.obj.message
    text = message.get("text", "").strip().casefold()
    peer_id = message["peer_id"]
    additional_messages = []

    if text == "начать":
        state_by_peer.pop(peer_id, None)
        answer = (
            "🤖 Привет! Помогу разобраться, какое направление в IT может подойти именно вам. "
            "Готовы начать?"
        )
        keyboard = build_intro_keyboard()
        format_data = None
    elif text == "приступить к тесту":
        state_by_peer[peer_id] = {
            "step": 0,
            "scores": default_scores(),
            "answers": [],
        }
        answer = (
            "✨ НОВОЕ ПРОХОЖДЕНИЕ ТЕСТА ✨\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "В тесте 15 вопросов, разбитых на 4 блока. "
            "Выбирайте вариант, который больше всего подходит вам\n"
            "— правильных ответов нет 🙂"
        )
        format_data = build_vk_format_data(
            answer,
            ["✨ НОВОЕ ПРОХОЖДЕНИЕ ТЕСТА ✨"],
        )
        current_question = QUESTIONS[0]
        keyboard = build_question_keyboard(current_question, 0)
        first_question_message = build_question_message(0)
        additional_messages = [
            (
                first_question_message,
                build_vk_format_data(
                    first_question_message,
                    get_question_bold_segments(0),
                ),
            )
        ]
    elif text == "перезапустить бота":
        state_by_peer.pop(peer_id, None)
        answer = (
            "🔄 Прогресс теста сброшен, история переписки сохранена.\n"
            "Нажмите «Начать», чтобы пройти сценарий заново."
        )
        keyboard = build_start_keyboard()
        format_data = None
    elif peer_id in state_by_peer:
        current_state = state_by_peer[peer_id]
        if text == "⬆️ вернуться" and current_state["step"] > 0:
            undo_last_answer(current_state)
            answer = (
                "↩️ Предыдущий ответ отменён. Выберите другой вариант:\n\n"
                + build_question_message(current_state["step"])
            )
            format_data = build_vk_format_data(
                answer,
                get_question_bold_segments(current_state["step"]),
            )
            keyboard = build_question_keyboard(
                QUESTIONS[current_state["step"]],
                current_state["step"],
            )
        else:
            current_question = QUESTIONS[current_state["step"]]
            chosen_option = find_chosen_option(current_state["step"], text)

            if chosen_option is None:
                if is_stale_answer_button(current_state["step"], text):
                    answer = (
                        "ℹ️ Ответ на предыдущий вопрос уже учтён. Повторно показываю "
                        "текущий вопрос:\n\n"
                        + build_question_message(current_state["step"])
                    )
                else:
                    answer = (
                        "⚠️ Пожалуйста, выберите один из вариантов кнопками ниже.\n\n"
                        + build_question_message(current_state["step"])
                    )
                format_data = build_vk_format_data(
                    answer,
                    get_question_bold_segments(current_state["step"]),
                )
                keyboard = build_question_keyboard(current_question, current_state["step"])
            else:
                current_state["scores"][chosen_option["direction"]] += 1
                current_state["answers"].append(chosen_option["direction"])
                current_state["step"] += 1

                if current_state["step"] >= len(QUESTIONS):
                    result_messages = build_result_messages(current_state["scores"])
                    state_by_peer.pop(peer_id, None)
                    answer, format_data = result_messages[0]
                    additional_messages = result_messages[1:]
                    keyboard = build_start_keyboard()
                else:
                    next_question = QUESTIONS[current_state["step"]]
                    answer = build_question_message(current_state["step"])
                    format_data = build_vk_format_data(
                        answer,
                        get_question_bold_segments(current_state["step"]),
                    )
                    keyboard = build_question_keyboard(next_question, current_state["step"])
    else:
        answer = (
            "🤖 Привет! Я помогу найти направление в IT, которое может вам подойти.\n\n"
            "Чтобы начать, нажмите кнопку «Начать» 👇"
        )
        keyboard = build_start_keyboard()
        format_data = None

    outgoing_messages = [(answer, format_data), *additional_messages]
    for index, (message_text, message_format_data) in enumerate(outgoing_messages):
        if index > 0:
            time.sleep(2)

        send_params = {
            "peer_id": peer_id,
            "message": message_text,
            "random_id": random.randint(1, 2_147_483_647) if len(outgoing_messages) > 1 else 0,
        }
        if index == len(outgoing_messages) - 1:
            send_params["keyboard"] = keyboard
        if message_format_data is not None:
            send_params["format_data"] = message_format_data

        vk.messages.send(**send_params)