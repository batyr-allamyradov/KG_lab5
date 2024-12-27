#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импорт библиотеки GIMP-Python
from gimpfu import *

def laplacian(image, drawable):
    # Сохранение текущего состояния контекста GIMP
    pdb.gimp_context_push()
    # Начало группы действий для возможности отмены одним шагом
    pdb.gimp_image_undo_group_start(image)

    # Проверка, является ли изображение RGB, и конвертация в оттенки серого
    if pdb.gimp_drawable_is_rgb(drawable):
        pdb.gimp_image_convert_grayscale(image)

    # Получение ширины и высоты изображения
    width = drawable.width
    height = drawable.height

    # Матрица ядра оператора Лапласа
    kernel_matrix = [
        [0,  1,  0],
        [1, -4,  1],
        [0,  1,  0]
    ]

    # Инициализация массива для новых значений пикселей
    new_pixels = [[0] * width for _ in range(height)]

    # Сообщение о начале обработки
    pdb.gimp_message("Начинаем обработку")

    # Применение оператора Лапласа к каждому пикселю изображения
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            sum = 0
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    # Получение значения яркости соседнего пикселя
                    pix = pdb.gimp_drawable_get_pixel(drawable, x + kx, y + ky)[1][0]
                    # Применение коэффициента из матрицы ядра
                    sum += pix * kernel_matrix[ky + 1][kx + 1]
            # Ограничение значения яркости в диапазоне 0-255
            new_pixels[y][x] = max(0, min(255, int(sum)))

    # Обновление пикселей изображения новыми значениями
    for y in range(height):
        for x in range(width):
            pdb.gimp_drawable_set_pixel(drawable, x, y, 1, [new_pixels[y][x]])

    # Сообщение о завершении обработки
    pdb.gimp_message("Обработка завершена")

    # Обновление дисплеев GIMP
    pdb.gimp_displays_flush()
    # Завершение группы действий
    pdb.gimp_image_undo_group_end(image)
    # Восстановление состояния контекста
    pdb.gimp_context_pop()

# Регистрация плагина в GIMP
register(
    "python-fu-Laplas-operator",  # Уникальное имя плагина
    "Laplas",                      # Краткое описание
    "Laplas",                      # Подробное описание
    "Batyr",                       # Автор
    "Allamyradov",                 # Авторские права
    "2024",                        # Год
    "LAPLAS",                      # Имя в меню GIMP
    "*",                           # Типы изображений (все)
    [
        (PF_IMAGE, "image", "Image", None),
        (PF_DRAWABLE, "drawable", "Drawable", None)
    ],
    [],
    laplacian, menu="<Image>/TEST2/"
)

# Главная функция
main()