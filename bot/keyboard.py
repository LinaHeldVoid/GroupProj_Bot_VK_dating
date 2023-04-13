def keyboard_1_generate():
    keyboard_1 = VkKeyboard()
    keyboard_1.add_button("Вперёд!", VkKeyboardColor.POSITIVE)
    return keyboard_1


def keyboard_2_generate():
    keyboard_2 = VkKeyboard()
    keyboard_2.add_button("Парня", VkKeyboardColor.PRIMARY)
    keyboard_2.add_line()
    keyboard_2.add_button("Девушку", VkKeyboardColor.PRIMARY)
    keyboard_2.add_line()
    keyboard_2.add_button("Пол не важен", VkKeyboardColor.PRIMARY)
    return keyboard_2


def keyboard_3_generate():
    keyboard_3 = VkKeyboard()
    keyboard_3.add_button("Да! Добавь в Избранное", VkKeyboardColor.POSITIVE)
    keyboard_3.add_line()
    keyboard_3.add_button("Давай посмотрим ещё", VkKeyboardColor.PRIMARY)
    keyboard_3.add_line()
    keyboard_3.add_button("Нет. Больше не показывай", VkKeyboardColor.SECONDARY)
    keyboard_3.add_line()
    keyboard_3.add_button("Стоп", VkKeyboardColor.NEGATIVE)
    keyboard_3.add_line()
    return keyboard_3


def keyboard_4_generate():
    keyboard_4 = VkKeyboard()
    keyboard_4.add_button("Страна не имеет значения", VkKeyboardColor.PRIMARY)
    return keyboard_4


def keyboard_5_generate():
    keyboard_5 = VkKeyboard()
    keyboard_5.add_button("Город не имеет значения", VkKeyboardColor.PRIMARY)
    return keyboard_5


def keyboard_6_generate():
    keyboard_6 = VkKeyboard()
    keyboard_6.add_button("Поищем ещё!", VkKeyboardColor.POSITIVE)
    keyboard_6.add_line()
    keyboard_6.add_button("Заканчивай", VkKeyboardColor.POSITIVE)
    keyboard_6.add_line()
    return keyboard_6