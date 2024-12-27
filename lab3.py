#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Импорт необходимых модулей
from math import cos, sin, pi
from gimpfu import *

# Функция билинейной интерполяции для вычисления цвета пикселя
def bilinear_interpolation(drawable, x, y):
    # Округляем координаты до целых чисел
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, drawable.width - 1), min(y1 + 1, drawable.height - 1)

    # Вычисляем разницу между координатами
    dx, dy = x - x1, y - y1

    # Получаем цвета соседних пикселей
    status, Q11 = pdb.gimp_drawable_get_pixel(drawable, x1, y1)
    status, Q21 = pdb.gimp_drawable_get_pixel(drawable, x2, y1)
    status, Q12 = pdb.gimp_drawable_get_pixel(drawable, x1, y2)
    status, Q22 = pdb.gimp_drawable_get_pixel(drawable, x2, y2)

    # Выполняем билинейную интерполяцию для вычисления итогового цвета
    interpolated_color = [
        int(
            (1 - dx) * (1 - dy) * Q11[i] +
            dx * (1 - dy) * Q21[i] +
            (1 - dx) * dy * Q12[i] +
            dx * dy * Q22[i]
        )
        for i in range(3)
    ]

    return interpolated_color

# Функция для поворота слоя
def rotate(image, drawable, angle, center_x, center_y):
    # Начинаем процесс отмены операций
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)

    # Создаем новый слой для результата поворота
    new_layer = gimp.Layer(
        image,
        "Rotated Layer",
        drawable.width,
        drawable.height,
        drawable.type,
        100,
        NORMAL_MODE,
    )

    # Добавляем новый слой в изображение
    image.add_layer(new_layer, 0)

    width, height = new_layer.width, new_layer.height
    angle_rad = angle * pi / 180.0  # Преобразуем угол в радианы

    pixels = []  # Список для хранения пикселей нового слоя

    pdb.gimp_message("Начинаем обработку")

    # Проходим по каждому пикселю нового слоя
    for y_t in range(height):
        for x_t in range(width):
            # Преобразуем координаты с учетом угла поворота
            x_s = (x_t - center_x) * cos(angle_rad) + (y_t - center_y) * sin(angle_rad) + center_x
            y_s = -(x_t - center_x) * sin(angle_rad) + (y_t - center_y) * cos(angle_rad) + center_y

            # Проверяем, что полученные координаты находятся в пределах изображения
            if 0 <= x_s < width and 0 <= y_s < height:
                # Получаем цвет пикселя с использованием билинейной интерполяции
                color = bilinear_interpolation(drawable, x_s, y_s)
                # Добавляем пиксель в список
                pixels.append((x_t, y_t, color[0:3]))

    # Записываем новые пиксели в слой
    for x_t, y_t, color in pixels:
        pdb.gimp_drawable_set_pixel(new_layer, x_t, y_t, 3, color)

    pdb.gimp_message("Обработка завершена")

    # Обновляем отображение
    pdb.gimp_displays_flush()
    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_context_pop()

# Регистрация плагина
register(
    "python-fu-Rotate-operator",  # Имя плагина
    "Rotate",  # Описание плагина
    "Rotate with new layer, custom center, and angle",  # Подробное описание
    "Batyr",  # Автор плагина
    "Allamyradov",  # Авторский коллектив
    "2024",  # Год
    "ROTATE",  # Название команды
    "*",  # Тип изображения
    [
        (PF_IMAGE, "image", "Image", None),  # Изображение
        (PF_DRAWABLE, "drawable", "Drawable", None),  # Слой
        (PF_INT, "angle", "Angle (in degrees)", 180),  # Угол поворота
        (PF_INT, "center_x", "Center X", 0),  # Координата X центра
        (PF_INT, "center_y", "Center Y", 0),  # Координата Y центра
    ],
    [],  # Нет дополнительных параметров
    rotate,  # Основная функция
    menu="<Image>/TEST1"  # Путь меню
)

# Запуск плагина
main()
