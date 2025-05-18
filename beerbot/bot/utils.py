# САМАЯ ВАЖНАЯ Функция для склонения слова "стол" в зависимости от количества
def declension_tables(count):
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} стол"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return f"{count} стола"
    else:
        return f"{count} столов"