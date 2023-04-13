from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def keyboard_hello_generate():
    keyboard_hello = VkKeyboard()
    keyboard_hello.add_button("Вперёд!", VkKeyboardColor.POSITIVE)
    return keyboard_hello


def keyboard_gender_generate():
    keyboard_gender = VkKeyboard()
    keyboard_gender.add_button("Парня", VkKeyboardColor.PRIMARY)
    keyboard_gender.add_line()
    keyboard_gender.add_button("Девушку", VkKeyboardColor.PRIMARY)
    keyboard_gender.add_line()
    keyboard_gender.add_button("Пол не важен", VkKeyboardColor.PRIMARY)
    return keyboard_gender


def keyboard_stupid_generate():
    keyboard_stupid = VkKeyboard()
    keyboard_stupid.add_button("Введи число с клавиатуры", VkKeyboardColor.SECONDARY)
    return keyboard_stupid


def keyboard_discussion_generate():
    keyboard_discussion = VkKeyboard()
    keyboard_discussion.add_button("Да! Добавь в Избранное", VkKeyboardColor.POSITIVE)
    keyboard_discussion.add_line()
    keyboard_discussion.add_button("Давай посмотрим ещё", VkKeyboardColor.PRIMARY)
    keyboard_discussion.add_line()
    keyboard_discussion.add_button(
        "Нет. Больше не показывай", VkKeyboardColor.SECONDARY
    )
    keyboard_discussion.add_line()
    keyboard_discussion.add_button("Стоп", VkKeyboardColor.NEGATIVE)
    return keyboard_discussion


def keyboard_country_generate():
    keyboard_country = VkKeyboard()
    keyboard_country.add_button("Страна не имеет значения", VkKeyboardColor.PRIMARY)
    return keyboard_country


def keyboard_city_generate():
    keyboard_city = VkKeyboard()
    keyboard_city.add_button("Город не имеет значения", VkKeyboardColor.PRIMARY)
    return keyboard_city


def keyboard_final_generate():
    keyboard_final = VkKeyboard()
    keyboard_final.add_button("Поищем ещё!", VkKeyboardColor.POSITIVE)
    keyboard_final.add_line()
    keyboard_final.add_button("Заканчивай", VkKeyboardColor.POSITIVE)
    return keyboard_final
