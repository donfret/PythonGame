"""
Текстовая новелла: "Выбор проекта"
Описание: Два друга заходят в Макдоналдс и выбирают концепт для своей будущей игры.
"""

# =====================================================================
# 1. КОНСТАНТЫ И НЕИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ (КОРТЕЖИ)
# =====================================================================

# Кортеж: начальный бюджет друзей (Добрыня, Федя) в рублях
INITIAL_BUDGETS = (1200, 1500)

# Кортеж: доступные сеттинги для игры
WORLD_SETTINGS = (
    ("Викторианская эпоха", "Готика и старый город"),
    ("Постапокалипсис", "Пустоши и нехватка ресурсов"),
    ("Темное фэнтези", "Руины и магия"),
    ("Киберпанк", "Мегаполис и технологии"),
)

# Кортеж: базовые классы для RPG
RPG_ARCHETYPES = (
    ("Воин", 120, 20, "Тяжелая броня и щит"),
    ("Разбойник", 85, 45, "Кинжалы и скрытность"),
    ("Маг", 70, 60, "Боевые заклинания"),
)


# =====================================================================
# 2. БАЗЫ ДАННЫХ И КОНЦЕПТЫ (СЛОВАРИ)
# =====================================================================

# Меню Макдоналдс
MCDONALDS_MENU = {
    "1": {"name": "Биг Мак", "cost": 175, "category": "Бургеры", "portion": "двойной бифштекс"},
    "2": {"name": "Двойной Чизбургер", "cost": 145, "category": "Бургеры", "portion": "сыр и говядина"},
    "3": {"name": "Чикен Макнаггетс (9 шт.)", "cost": 169, "category": "Стартеры", "portion": "куриное филе"},
    "4": {"name": "Картофель фри (большой)", "cost": 105, "category": "Гарниры", "portion": "большая порция"},
    "5": {"name": "Сырный соус", "cost": 45, "category": "Соусы", "portion": "1 шт."},
    "6": {"name": "Кока-Кола 0.5 л", "cost": 95, "category": "Напитки", "portion": "500 мл"},
    "7": {"name": "Пирожок с вишней", "cost": 75, "category": "Десерты", "portion": "1 шт."},
}

# Варианты для Хоррора (Этап 2)
HORROR_DATA = {
    "locations": {
        "1": {"title": "Заброшенный НИИ", "danger": "Заражение"},
        "2": {"title": "Старый маяк", "danger": "Изоляция"},
        "3": {"title": "Заброшенная станция метро", "danger": "Темнота и замкнутое пространство"},
    },
    "antagonists": {
        "1": {"title": "Слепой монстр (ориентируется на звук)", "type": "Стелс"},
        "2": {"title": "Призрак", "type": "Мистика"},
        "3": {"title": "Сумасшедший сторож", "type": "Реализм"},
    },
    "mechanics": {
        "1": {"title": "Диктофон для поиска улик", "item": "Диктофон"},
        "2": {"title": "Камера ночного видения на батарейках", "item": "Камера"},
        "3": {"title": "Датчик движения", "item": "Датчик"},
    },
}

# Варианты для RPG (Этап 3)
RPG_DATA = {
    "combat_systems": {
        "1": {"title": "Пошаговые бои", "focus": "Тактика"},
        "2": {"title": "Бои в реальном времени", "focus": "Реакция"},
        "3": {"title": "Карточная боевая система", "focus": "Сборка колоды"},
    },
    "quest_systems": {
        "1": {"title": "Нелинейный сюжет с выбором", "impact": "Разные концовки"},
        "2": {"title": "Борьба фракций", "impact": "Репутация"},
        "3": {"title": "Линейный сюжет", "impact": "История одного героя"},
    },
}

# Варианты для Головоломки (Этап 4)
PUZZLE_DATA = {
    "core_mechanics": {
        "1": {"title": "Перемотка времени", "complexity": "Высокая"},
        "2": {"title": "Порталы и физика", "complexity": "Очень высокая"},
        "3": {"title": "Работа со светом и тенью", "complexity": "Средняя"},
    },
    "themes": {
        "1": {"title": "Часовая мастерская", "mood": "Спокойная атмосфера"},
        "2": {"title": "Научная лаборатория", "mood": "Фантастика"},
        "3": {"title": "Древние руины", "mood": "Приключения"},
    },
}


# =====================================================================
# 3. ДИНАМИЧЕСКИЕ ПЕРЕМЕННЫЕ ИГРОКА (СПИСКИ, МНОЖЕСТВА, СЛОВАРИ)
# =====================================================================

# Словарь бюджета
wallet = {
    "добрыня": INITIAL_BUDGETS[0],
    "федя": INITIAL_BUDGETS[1],
    "общий_счет": 0,
}

# Список заказанных блюд
mcdonalds_order_tray = []

# Множества выбранных параметров
game_tags = set()
approved_features = set()

# Словарь итогового проекта
game_pitch = {
    "genre": "Не определен",
    "setting": "Не выбран",
    "core_mechanic": "Не выбрана",
    "antagonist_or_goal": "Не задан",
    "selected_tags": set(),
}


# =====================================================================
# 4. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ВЫВОДА
# =====================================================================

def print_separator():
    print("=" * 70)


def print_sub_divider():
    print("-" * 70)


def show_wallet_status():
    """Выводит остаток денег и текущий заказ."""
    print_sub_divider()
    print(f"[БЮДЖЕТ] Добрыня: {wallet['добрыня']} руб. | Федя: {wallet['федя']} руб. | Сумма заказа: {wallet['общий_счет']} руб.")
    if mcdonalds_order_tray:
        print(f"[ЗАКАЗ]: {', '.join(mcdonalds_order_tray)}")
    print_sub_divider()


# =====================================================================
# 5. ЭТАП 1: МАКДОНАЛДС И ЗАКАЗ ЕДЫ
# =====================================================================

def stage_one_mcdonalds_ordering():
    """
    Этап 1: Покупка еды. Работа со словарем и списком.
    """
    print_separator()
    print("ЭТАП 1: ЗАКАЗ В МАКДОНАЛДС")
    print_separator()
    print("Добрыня и Федя зашли перекусить в Макдоналдс и заодно обсудить свой учебный проект.")
    print("Добрыня: 'Слушай, я с утра ничего не ел, голова вообще не варит. Давай сначала возьмем поесть, а потом уже решим с игрой.'")
    print("Федя: 'Давай, я тоже голодный. Смотри, сколько у нас там по деньгам выходит.'")

    ordering_active = True

    while ordering_active:
        show_wallet_status()
        print("Меню:")
        for key, item in MCDONALDS_MENU.items():
            print(f"{key}. {item['name']} ({item['category']}) — {item['cost']} руб. [{item['portion']}]")
        print("8. Завершить заказ и сесть за стол")

        choice = input("\nВыберите пункт (1-8): ").strip()

        if choice in MCDONALDS_MENU:
            item = MCDONALDS_MENU[choice]
            cost = item["cost"]

            # Платит тот, у кого сейчас больше денег
            payer = "федя" if wallet["федя"] >= wallet["добрыня"] else "добрыня"

            if wallet[payer] >= cost:
                wallet[payer] -= cost
                wallet["общий_счет"] += cost
                mcdonalds_order_tray.append(item["name"])
                print(f"\n[ОПЛАТА] {payer.capitalize()} добавил в заказ '{item['name']}' за {cost} руб.")
            else:
                print("\n[ОШИБКА] На это уже не хватает денег, давай выберем что-то другое.")

        elif choice == "8":
            if not mcdonalds_order_tray:
                print("\nФедя: 'Ну мы же поесть зашли, давай хоть картошку или напиток возьмем.'")
                continue
            print("\nПарни забрали заказ, нашли свободный столик в углу и сели обсуждать дела.")
            ordering_active = False
        else:
            print("\nНеверный номер. Выберите от 1 до 8.")

    return True


# =====================================================================
# 6. ЭТАП 2: ИДЕЯ ХОРРОРА ОТ ДОБРЫНИ
# =====================================================================

def stage_two_horror_pitch():
    """
    Этап 2: Добрыня предлагает сделать хоррор.
    Выбор локации, врага и механики.
    """
    print_separator()
    print("ЭТАП 2: ИДЕЯ ДОБРЫНИ — ХОРРОР")
    print_separator()
    print("Добрыня: 'Короче, у меня есть мысль. Давай сделаем хоррор. Там не нужно городить огромные миры,")
    print("достаточно одной мрачной локации и нормального звука. Вдвоем мы такое точно потянем.'")
    print("Федя: 'Ну не знаю, смотря про что он будет. Накидай примерно, как ты это видишь.'\n")

    # 1. Выбор локации
    print("--- Шаг 1: Выбор локации ---")
    for k, v in HORROR_DATA["locations"].items():
        print(f"{k}. {v['title']} ({v['danger']})")

    loc_choice = ""
    while loc_choice not in HORROR_DATA["locations"]:
        loc_choice = input("Выберите локацию (1-3): ").strip()
    selected_loc = HORROR_DATA["locations"][loc_choice]
    game_tags.add(selected_loc["title"])

    # 2. Выбор антагониста
    print("\n--- Шаг 2: Выбор противника ---")
    for k, v in HORROR_DATA["antagonists"].items():
        print(f"{k}. {v['title']} [{v['type']}]")

    ant_choice = ""
    while ant_choice not in HORROR_DATA["antagonists"]:
        ant_choice = input("Выберите противника (1-3): ").strip()
    selected_ant = HORROR_DATA["antagonists"][ant_choice]
    game_tags.add(selected_ant["title"])

    # 3. Выбор механики
    print("\n--- Шаг 3: Основной предмет игрока ---")
    for k, v in HORROR_DATA["mechanics"].items():
        print(f"{k}. {v['title']}")

    mech_choice = ""
    while mech_choice not in HORROR_DATA["mechanics"]:
        mech_choice = input("Выберите предмет (1-3): ").strip()
    selected_mech = HORROR_DATA["mechanics"][mech_choice]
    game_tags.add(selected_mech["item"])

    print_sub_divider()
    print("КОНЦЕПТ ДОБРЫНИ:")
    print(f"- Локация: {selected_loc['title']}")
    print(f"- Враг: {selected_ant['title']}")
    print(f"- Механика: {selected_mech['title']}")
    print_sub_divider()

    print("\nДобрыня: 'Вот, смотри. Атмосферно, понятно как кодить, и выглядит цельно.'")
    return True


# =====================================================================
# 7. ЭТАП 3: ИДЕЯ RPG ОТ ФЕДИ
# =====================================================================

def stage_three_rpg_rebellion():
    """
    Этап 3: Федя отказывается от хоррора и предлагает RPG.
    """
    print_separator()
    print("ЭТАП 3: ИДЕЯ ФЕДИ — РОЛЕВАЯ ИГРА (RPG)")
    print_separator()
    print("Федя: 'Слушай, ну хоррор — это совсем на один раз. Прошел за двадцать минут, испугался пару раз и забыл.")
    print("Мне вообще не особо хочется сидеть и настраивать темноту со скримерами. Давай лучше сделаем RPG.")
    print("Пусть небольшую, но с нормальной прокачкой, боевкой и сюжетом. Там хоть развернуться есть где.'\n")

    # 1. Выбор боевой системы
    print("--- Шаг 1: Боевая система ---")
    for k, v in RPG_DATA["combat_systems"].items():
        print(f"{k}. {v['title']} (Упор на: {v['focus']})")

    combat_choice = ""
    while combat_choice not in RPG_DATA["combat_systems"]:
        combat_choice = input("Выберите боевую систему (1-3): ").strip()
    selected_combat = RPG_DATA["combat_systems"][combat_choice]
    approved_features.add(selected_combat["title"])

    # 2. Выбор структуры квестов
    print("\n--- Шаг 2: Система квестов ---")
    for k, v in RPG_DATA["quest_systems"].items():
        print(f"{k}. {v['title']} ({v['impact']})")

    quest_choice = ""
    while quest_choice not in RPG_DATA["quest_systems"]:
        quest_choice = input("Выберите структуру сюжета (1-3): ").strip()
    selected_quest = RPG_DATA["quest_systems"][quest_choice]
    approved_features.add(selected_quest["title"])

    # 3. Выбор базового класса из кортежа
    print("\n--- Шаг 3: Основной класс персонажа ---")
    for idx, arch in enumerate(RPG_ARCHETYPES, start=1):
        print(f"{idx}. {arch[0]} (Здоровье: {arch[1]} | Урон: {arch[2]} | Описание: {arch[3]})")

    arch_choice = ""
    while arch_choice not in ("1", "2", "3"):
        arch_choice = input("Выберите класс (1-3): ").strip()
    selected_arch = RPG_ARCHETYPES[int(arch_choice) - 1]
    approved_features.add(selected_arch[0])

    print_sub_divider()
    print("КОНЦЕПТ ФЕДИ:")
    print(f"- Боевка: {selected_combat['title']}")
    print(f"- Сюжет: {selected_quest['title']}")
    print(f"- Класс: {selected_arch[0]} ({selected_arch[3]})")
    print_sub_divider()

    print("\nДобрыня: 'Федя, какая RPG? Мы только инвентарь и диалоги будем месяц писать, а нам сдавать скоро.'")
    print("Федя: 'Да не будем мы месяц писать, сделаем компактно! Зато в это реально интересно играть.'")
    return True


# =====================================================================
# 8. ЭТАП 4: ПРЕДЛОЖЕНИЕ РАБОТНИКА ЗАЛА — ГОЛОВОЛОМКА
# =====================================================================

def stage_four_worker_intervention():
    """
    Этап 4: Работник зала предлагает компромисс — головоломку.
    Выбор механик и финальное решение.
    """
    print_separator()
    print("ЭТАП 4: ТРЕТИЙ ВАРИАНТ — ГОЛОВОЛОМКА")
    print_separator()
    print("Пока парни спорили, соседний столик протирал сотрудник зала. Услышав знакомые темы, он улыбнулся и подошел ближе.")
    print("Работник: 'Парни, извините, что влезаю, случайно услышал ваш спор. Я просто сам на программиста учусь,")
    print("в прошлом году такой же проект сдавал. Мы тогда тоже между RPG и бродилкой выбирали, в итоге чуть не переругались.")
    print("Знаете, что нас спасло? Головоломка. Берете одну крутую фишку и строите вокруг нее пяток уровней. И кодить интересно, и по срокам успеете.'\n")
    print("Добрыня задумался: 'А ведь звучит здраво... Федь, что скажешь?'")
    print("Федя: 'Ну, как компромисс — вполне. Давай прикинем, что там можно сделать.'\n")

    # 1. Выбор механики головоломки
    print("--- Шаг 1: Основная механика головоломки ---")
    for k, v in PUZZLE_DATA["core_mechanics"].items():
        print(f"{k}. {v['title']} (Сложность реализации: {v['complexity']})")

    puz_choice = ""
    while puz_choice not in PUZZLE_DATA["core_mechanics"]:
        puz_choice = input("Выберите механику (1-3): ").strip()
    selected_puz = PUZZLE_DATA["core_mechanics"][puz_choice]

    # 2. Выбор сеттинга головоломки
    print("\n--- Шаг 2: Оформление уровней ---")
    for k, v in PUZZLE_DATA["themes"].items():
        print(f"{k}. {v['title']} ({v['mood']})")

    theme_choice = ""
    while theme_choice not in PUZZLE_DATA["themes"]:
        theme_choice = input("Выберите тему (1-3): ").strip()
    selected_theme = PUZZLE_DATA["themes"][theme_choice]

    # 3. Финальный выбор
    print("\n" + "=" * 70)
    print("ИТОГОВЫЙ ВЫБОР: НА ЧЕМ ОСТАНОВЯТСЯ ДРУЗЬЯ?")
    print("=" * 70)
    print("1. Хоррор (идея Добрыни)")
    print("2. RPG (идея Феди)")
    print("3. Головоломка (совет парня из зала)")
    print("4. Смешанный проект (объединить идеи всех троих)")

    final_choice = ""
    while final_choice not in ("1", "2", "3", "4"):
        final_choice = input("Выберите вариант (1-4): ").strip()

    if final_choice == "1":
        game_pitch["genre"] = "Хоррор на выживание"
        game_pitch["setting"] = list(game_tags)[0] if game_tags else "Закрытый объект"
        game_pitch["core_mechanic"] = "Скрытное перемещение и поиск предметов"
        game_pitch["antagonist_or_goal"] = "Выбраться из локации"
        game_pitch["selected_tags"] = game_tags

    elif final_choice == "2":
        game_pitch["genre"] = "Ролевая игра (RPG)"
        game_pitch["setting"] = WORLD_SETTINGS[2][0]
        game_pitch["core_mechanic"] = list(approved_features)[0] if approved_features else "Пошаговый бой"
        game_pitch["antagonist_or_goal"] = "Выполнение сюжетных квестов и прокачка"
        game_pitch["selected_tags"] = approved_features

    elif final_choice == "3":
        game_pitch["genre"] = "Логическая головоломка"
        game_pitch["setting"] = selected_theme["title"]
        game_pitch["core_mechanic"] = selected_puz["title"]
        game_pitch["antagonist_or_goal"] = "Прохождение цепочки тестовых комнат"
        game_pitch["selected_tags"] = {selected_puz["title"], selected_theme["title"]}

    elif final_choice == "4":
        game_pitch["genre"] = "Приключенческая игра с элементами RPG и головоломок"
        game_pitch["setting"] = selected_theme["title"]
        game_pitch["core_mechanic"] = f"{selected_puz['title']} + элементы прокачки"
        game_pitch["antagonist_or_goal"] = "Исследование мира и решение задач"
        game_pitch["selected_tags"] = game_tags | approved_features | {selected_puz["title"]}

    return True


# =====================================================================
# 9. ВЫВОД ИТОГОВОГО РЕЗУЛЬТАТА
# =====================================================================

def show_final_game_design_document():
    """
    Выводит итоговый концепт и данные из коллекций.
    """
    print_separator()
    print("ИТОГОВЫЙ ПЛАН ПРОЕКТА")
    print_separator()
    print(f"ЖАНР:              {game_pitch['genre']}")
    print(f"ЛОКАЦИЯ / СЕТТИНГ: {game_pitch['setting']}")
    print(f"ОСНОВНАЯ МЕХАНИКА: {game_pitch['core_mechanic']}")
    print(f"ЦЕЛЬ ИГРЫ:         {game_pitch['antagonist_or_goal']}")

    print("\nДАННЫЕ ИЗ КОЛЛЕКЦИЙ ПРОГРАММЫ:")
    print(f"1. Список покупок (list): {mcdonalds_order_tray}")
    print(f"2. Остаток бюджета (dict): {wallet}")
    print(f"3. Доступные миры из кортежа (tuple): {WORLD_SETTINGS[0][0]}, {WORLD_SETTINGS[1][0]}")
    print(f"4. Набор выбранных элементов (set): {game_pitch['selected_tags']}")
    print_separator()
    print("Работник зала: 'Отличный выбор, парни. Удачи со сдачей!'")
    print("Добрыня: 'Спасибо, реально выручил. Ну все, Федь, доедаем и по домам — пора садиться за код.'")
    print("Федя: 'Да, давай. Вечером созвонимся и поделим задачи.'")
    print_separator()


# =====================================================================
# 10. ЗАПУСК ПРОГРАММЫ
# =====================================================================

def main():
    print_separator()
    print("                ТЕКСТОВАЯ ИГРА: ВЫБОР КОНЦЕПТА ИГРЫ              ")
    print_separator()

    # Этап 1: Заказ еды
    stage_one_mcdonalds_ordering()

    # Этап 2: Вариант Добрыни (Хоррор)
    stage_two_horror_pitch()

    # Этап 3: Вариант Феди (RPG)
    stage_three_rpg_rebellion()

    # Этап 4: Вариант работника зала (Головоломка) и итог
    stage_four_worker_intervention()

    # Вывод результата
    show_final_game_design_document()


if __name__ == "__main__":
    main()