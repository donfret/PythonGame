import sys

# ==============================================================================
# 1. глобальные коллекции данных (кортежи и словари)
# ==============================================================================
LEVEL_CONFIGS = (
    (1, "Главный холл участка R.P.D.", (10, 25), "Низкий"),
    (2, "Западный коридор и Офис S.T.A.R.S.", (14, 30), "Средний"),
    (3, "Подземная парковка и Канализация", (5, 5), "Высокий"),
    (4, "Секретная лаборатория NEST", (0, 0), "Критический")
)

ITEMS_DB = {
    "пистолет": "Табельный пистолет Матильда. Эффективен против обычных зомби.",
    "патроны": "Коробка патронов 9мм для пистолета.",
    "зеленая трава": "Лечебная трава из R.P.D. Восстанавливает 35 HP.",
    "красная трава": "Усиливает лечебный эффект зеленой травы при смешивании.",
    "аптечка": "Смесь трав. Полностью восстанавливает здоровье (100 HP).",
    "медаль льва": "Золотая медаль с профилем льва для статуи Богини.",
    "медаль девы": "Старинная бронзовая медаль с рельефом девы.",
    "медаль единорога": "Медаль с изображением мифического единорога.",
    "зажигалка": "Бензиновая зажигалка с гербом полиции Раккун-Сити.",
    "дробовик": "Помповое ружье W-870. Смертельно для Лизунов.",
    "болтрез": "Тяжелый инструмент для перекусывания стальных цепей.",
    "вентиль": "Чугунный шестигранный вентиль для паровых труб.",
    "синяя колба": "Стеклянная капсула с базовым химическим реагентом.",
    "красная колба": "Капсула с термоактивным реагентом.",
    "фиолетовая колба": "Синтезированный реагент для допуска к фуникулеру.",
    "вакцина": "Экспериментальный антивирус против G-вируса.",
    "ракетница": "Противотанковая ракетница с одним зарядом. Убивает Тирана."
}

SECURITY_CODES = {"сейф": "2236", "шкафчик": "CAP"}
CRAFT_RECIPES = {
    ("зеленая трава", "красная трава"): "аптечка",
    ("красная колба", "синяя колба"): "фиолетовая колба"
}

# ==============================================================================
# 2. состояние игрока и мира (словарь, списки, множества)
# ==============================================================================
player = {"name": "", "hp": 100, "max_hp": 100, "level": 1, "infected": False}
inventory = ["пистолет", "зеленая трава"]

unlocked_doors = set()
solved_puzzles = set()
defeated_enemies = set()

level_items = {
    1: ["патроны", "медаль льва", "красная трава"],
    2: ["зеленая трава", "патроны"],
    3: ["синяя колба", "зеленая трава"],
    4: ["аптечка", "ракетница"]
}

required_medals = {"медаль льва", "медаль девы", "медаль единорога"}
inserted_medals = set()
enemies_lvl2 = ["зомби-полицейский", "лизун"]
correct_torches = ["северный", "южный", "восточный"]
valves_lvl3 = {"труба 1": True, "труба 2": False, "труба 3": True}

quiz_lvl4 = {
    "Какой вирус вызвал зомби-эпидемию в городе? (т-вирус / лас-плагас)": "т-вирус",
    "Название корпорации, создавшей био-оружие? (амбрелла / трайселл)": "амбрелла",
    "Что получается при смешивании зеленой и красной травы? (аптечка / спрей)": "аптечка"
}
tyrant_alive = True

# ==============================================================================
# 3. старт игры и ввод имени
# ==============================================================================
print("\n" + "=" * 68)
print("   RESIDENT EVIL: RACCOON CITY ESCAPE (ТЕКСТОВАЯ НОВЕЛЛА)   ")
print("=" * 68)

while player["name"] == "":
    entered_name = input("Введите имя вашего героя: ").strip()
    if entered_name != "":
        player["name"] = entered_name
    else:
        print(">> Ошибка: имя не может быть пустым! Пожалуйста, введите имя.")

print(f"\nДобро пожаловать в кошмар Раккун-Сити, {player['name']}!")
print("Подсказка: в любой момент вводите 'действия' (или 'д') для списка команд.")

# ==============================================================================
# 4. главный игровой цикл
# ==============================================================================
game_active = True
level_announced = 0

while game_active and player["hp"] > 0:
    current_lvl = player["level"]
    room_items = level_items[current_lvl]

    if level_announced != current_lvl:
        cfg = LEVEL_CONFIGS[current_lvl - 1]
        print("\n" + "=" * 68)
        print(f"УРОВЕНЬ {cfg[0]}: {cfg[1]} | Сектор: {cfg[2]} | Угроза: {cfg[3]}")
        print("=" * 68)

        match current_lvl:
            case 1:
                print("СЮЖЕТ: Вы заперты в холле R.P.D. Соберите 3 медали в статую Богини.")
            case 2:
                print("СЮЖЕТ: В коридоре монстры. Зачистите путь и зажгите 3 факела.")
            case 3:
                print("СЮЖЕТ: Проход забит паром. Перекройте трубы вентилем и сделайте колбу.")
            case 4:
                player["infected"] = True
                print("СЮЖЕТ: Вы заражены G-вирусом! Создайте вакцину и убейте Тирана Т-103.")
        level_announced = current_lvl

    cmd = input(f"\n[Уровень {current_lvl}] Введите команду: ").strip().lower()
    parts = cmd.split(" ", 1)
    verb = parts[0]
    arg = parts[1].strip() if len(parts) > 1 else ""

    # --------------------------------------------------------------------------
    # блок общих команд
    # --------------------------------------------------------------------------
    command_handled = True
    match verb:
        case "помощь":
            print("\n--- ОБЩИЕ КОМАНДЫ ---")
            print("  осмотреть, действия (д), взять <предмет>, инфо <предмет>")
            print("  лечиться, смешать, статус, выход")
        case "статус":
            cfg = LEVEL_CONFIGS[current_lvl - 1]
            inf = "ЗАРАЖЕН" if player["infected"] else "Здоров"
            inv = ", ".join(inventory) if inventory else "Пусто"
            print(f"\nЛОКАЦИЯ: {cfg[1]} | HP: {player['hp']} | Статус: {inf} | Инвентарь: {inv}")
        case "действия" | "д":
            print(f"\n--- ДЕЙСТВИЯ НА УРОВНЕ {current_lvl} ---")
            print("Общие: осмотреть, взять <предмет>, инфо <предмет>, лечиться, смешать, статус")
            if current_lvl == 1:
                print("Сюжет: читать памятку, обыскать стол, открыть сейф, вставить медали" + (
                    " | идти дальше" if "проход_1" in unlocked_doors else ""))
            elif current_lvl == 2:
                print("Сюжет: читать дневник, открыть шкафчик, атаковать, зажечь факелы" + (
                    " | идти дальше" if "проход_2" in unlocked_doors else ""))
            elif current_lvl == 3:
                print("Сюжет: читать записку, срезать цепь, перекрыть пар, сканировать" + (
                    " | идти дальше" if "проход_3" in unlocked_doors else ""))
            elif current_lvl == 4:
                print("Финал: терминал, бой с тираном, эвакуация")
        case "лечиться":
            if "аптечка" in inventory:
                inventory.remove("аптечка")
                player["hp"] = player["max_hp"]
                print(">> Здоровье полностью восстановлено (100 HP)!")
            elif "зеленая трава" in inventory:
                inventory.remove("зеленая трава")
                player["hp"] = min(player["max_hp"], player["hp"] + 35)
                print(f">> Здоровье: {player['hp']} HP.")
            else:
                print(">> Нет лечебных средств.")
        case "смешать":
            print("Инвентарь:", ", ".join(inventory))
            i1 = input("Первый предмет: ").strip().lower()
            i2 = input("Второй предмет: ").strip().lower()
            if i1 not in inventory or i2 not in inventory or i1 == i2:
                print(">> Ошибка: нужны два разных предмета из инвентаря.")
            else:
                key = tuple(sorted([i1, i2]))
                if key in CRAFT_RECIPES:
                    res = CRAFT_RECIPES[key]
                    inventory.remove(i1)
                    inventory.remove(i2)
                    inventory.append(res)
                    print(f">> Успех! Получено: '{res}'.")
                else:
                    print(">> Эти предметы нельзя объединить.")
        case "инфо":
            print(f">> [{arg.upper()}]: {ITEMS_DB[arg]}" if arg in ITEMS_DB else ">> Предмет не найден.")
        case "взять":
            if arg == "ракетница" and current_lvl == 4 and player["infected"]:
                print(">> Ошибка: сначала вылечитесь в терминале от заражения!")
            elif arg in room_items:
                room_items.remove(arg)
                inventory.append(arg)
                print(f">> '{arg}' добавлен в инвентарь.")
            else:
                print(f">> Предмета '{arg}' здесь нет.")
        case "выход":
            print(">> Выход из игры...")
            game_active = False
        case _:
            command_handled = False

    # --------------------------------------------------------------------------
    # блок сюжетных команд уровней
    # --------------------------------------------------------------------------
    if not command_handled and game_active:
        match current_lvl:
            case 1:
                if cmd == "осмотреть":
                    print(f"\nПредметы: {', '.join(room_items) if room_items else 'пусто'}")
                    print("Объекты: памятка офицера, стол, сейф, статуя Богини.")
                elif cmd == "читать памятку":
                    print(">> Код сейфа: 2236.")
                elif cmd == "обыскать стол":
                    if "стол" not in solved_puzzles:
                        print(">> Найдена 'медаль девы'. Возьмите ее.")
                        room_items.append("медаль девы")
                        solved_puzzles.add("стол")
                    else:
                        print(">> Стол пуст.")
                elif cmd == "открыть сейф":
                    if "сейф" in solved_puzzles:
                        print(">> Сейф уже открыт.")
                    elif input("Код: ").strip() == SECURITY_CODES["сейф"]:
                        print(">> Получены 'медаль единорога' и 'зажигалка'.")
                        inventory.extend(["медаль единорога", "зажигалка"])
                        solved_puzzles.add("сейф")
                    else:
                        player["hp"] -= 15
                        print(f">> Неверно! Удар током (-15 HP). Осталось: {player['hp']}.")
                elif cmd == "вставить медали":
                    found = set(inventory).intersection(required_medals)
                    if not found:
                        print(">> Нет медалей в инвентаре.")
                    else:
                        for m in found:
                            inventory.remove(m)
                            inserted_medals.add(m)
                            print(f">> Вставлена '{m}'.")
                        if required_medals.issubset(inserted_medals):
                            print(">> Проход открыт! Введите 'идти дальше'.")
                            unlocked_doors.add("проход_1")
                elif cmd == "идти дальше":
                    if "проход_1" in unlocked_doors:
                        player["level"] = 2
                    else:
                        print(">> Проход закрыт.")
                else:
                    print(">> Неизвестная команда.")

            case 2:
                if cmd == "осмотреть":
                    print(f"\nПредметы: {', '.join(room_items) if room_items else 'пусто'}")
                    print(f"Враги: {', '.join(enemies_lvl2) if enemies_lvl2 else 'нет'}")
                elif cmd == "читать дневник":
                    print(">> Код шкафчика: CAP. Факелы: северный -> южный -> восточный.")
                elif cmd == "открыть шкафчик":
                    if "шкафчик" in solved_puzzles:
                        print(">> Шкафчик пуст.")
                    elif input("Код: ").strip().upper() == SECURITY_CODES["шкафчик"]:
                        print(">> Получены 'дробовик' и 'болтрез'.")
                        inventory.extend(["дробовик", "болтрез"])
                        solved_puzzles.add("шкафчик")
                    else:
                        print(">> Неверный код.")
                elif cmd == "атаковать":
                    if not enemies_lvl2:
                        print(">> Никого нет.")
                    elif enemies_lvl2.pop(0) == "зомби-полицейский":
                        if "пистолет" in inventory and "патроны" in inventory:
                            inventory.remove("патроны")
                            print(">> Зомби застрелен из пистолета.")
                        else:
                            player["hp"] -= 30
                            print(">> Без патронов укус зомби (-30 HP).")
                    else:
                        if "дробовик" in inventory:
                            print(">> Лизун убит из дробовика!")
                        else:
                            player["hp"] -= 55
                            print(">> Без дробовика ранение от Лизуна (-55 HP).")
                elif cmd == "зажечь факелы":
                    if enemies_lvl2:
                        print(">> Сначала убейте врагов!")
                    elif "зажигалка" not in inventory:
                        print(">> Нет зажигалки!")
                    elif [input("Факел 1: ").lower(), input("Факел 2: ").lower(),
                          input("Факел 3: ").lower()] == correct_torches:
                        print(">> Решетка поднята! Введите 'идти дальше'.")
                        unlocked_doors.add("проход_2")
                    else:
                        player["hp"] -= 15
                        print(">> Ожог ловушки (-15 HP).")
                elif cmd == "идти дальше":
                    if "проход_2" in unlocked_doors:
                        player["level"] = 3
                    else:
                        print(">> Решетка закрыта.")
                else:
                    print(">> Неизвестная команда.")

            case 3:
                if cmd == "осмотреть":
                    print(f"\nПредметы: {', '.join(room_items) if room_items else 'пусто'}")
                elif cmd == "читать записку":
                    print(">> Отключите трубу 1 и 3 вентилем. Смешайте синюю и красную колбы.")
                elif cmd == "срезать цепь":
                    if "цепь" in solved_puzzles:
                        print(">> Цепь уже срезана.")
                    elif "болтрез" in inventory:
                        print(">> Получены 'вентиль' и 'красная колба'.")
                        inventory.extend(["вентиль", "красная колба"])
                        solved_puzzles.add("цепь")
                    else:
                        print(">> Нужен болтрез.")
                elif cmd == "перекрыть пар":
                    if "вентиль" not in inventory:
                        print(">> Нет вентиля.")
                    else:
                        for p, on in valves_lvl3.items(): print(f"  * {p}: {'ПАР' : <5} if on else 'ВЫКЛ'")
                        tp = input("Труба: ").strip().lower()
                        if tp in valves_lvl3:
                            valves_lvl3[tp] = not valves_lvl3[tp]
                            print(f">> Труба '{tp}' переключена.")
                            if not any(valves_lvl3.values()):
                                print(">> Пар перекрыт!")
                                solved_puzzles.add("пар")
                        else:
                            print(">> Нет такой трубы.")
                elif cmd == "сканировать":
                    if "пар" not in solved_puzzles:
                        player["hp"] -= 25
                        print(">> Ожог паром (-25 HP)!")
                    elif "фиолетовая колба" in inventory:
                        print(">> Двери фуникулера открыты! Введите 'идти дальше'.")
                        unlocked_doors.add("проход_3")
                    else:
                        print(">> Требуется фиолетовая колба.")
                elif cmd == "идти дальше":
                    if "проход_3" in unlocked_doors:
                        player["level"] = 4
                    else:
                        print(">> Двери закрыты.")
                else:
                    print(">> Неизвестная команда.")

            case 4:
                if cmd == "осмотреть":
                    print(f"\nПредметы: {', '.join(room_items) if room_items else 'пусто'}")
                elif cmd == "терминал":
                    if not player["infected"]:
                        print(">> Вы уже здоровы.")
                    elif all(input(f"Q: {q}\nA: ").strip().lower() == a for q, a in quiz_lvl4.items()):
                        player["infected"] = False
                        inventory.append("вакцина")
                        solved_puzzles.add("вакцина")
                        print(">> Вакцина принята! Заражение снято.")
                    else:
                        player["hp"] -= 20
                        print(">> Ошибка! G-вирус отнимает 20 HP.")
                elif cmd == "бой с тираном":
                    if not tyrant_alive:
                        print(">> Тиран уже мертв.")
                    elif "ракетница" in inventory:
                        inventory.remove("ракетница")
                        tyrant_alive = False
                        defeated_enemies.add("тиран т-103")
                        print(">> Ракетница уничтожает Тирана!")
                    else:
                        player["hp"] -= 50
                        print(">> Обычное оружие бесполезно! Удар (-50 HP).")
                elif cmd == "эвакуация":
                    if tyrant_alive:
                        print(">> Тиран жив!")
                    elif player["infected"]:
                        print(">> Вы заражены! Сделайте вакцину.")
                    else:
                        print(f"\nПОБЕДА! {player['name']} спасся из Раккун-Сити! HP: {player['hp']}")
                        game_active = False
                else:
                    print(">> Неизвестная команда.")

# ==============================================================================
# 5. проверка поражения
# ==============================================================================
if player["hp"] <= 0:
    print("\n" + "=" * 68)
    print("ВЫ ПОГИБЛИ... ИГРА ОКОНЧЕНА.")
    print("=" * 68)
    sys.exit()