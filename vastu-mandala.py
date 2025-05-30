import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Цвета планет в индийской астрологии
color_map = {
    1: '#E52B50', 2: '#87CEEB', 3: '#F4C430', 4: '#86261c',
    5: '#009B77', 6: '#FADADD', 7: '#b2beb5', 8: '#0047AB', 9: '#ff4040'
}

# Расположение зон в мандале
zone_coords = {
    1: [(4,4), (5,4), (6,4), (4,5), (5,5), (6,5), (4,6), (5,6), (6,6),
        (2,1), (2,2), (1,2), (8,1), (8,2), (9,2), (1,8), (2,8), (2,9), (8,8), (8,9), (9,8)],
    2: [(5,1), (4,2), (5,2), (6,2), (4,3), (5,3), (6,3),
        (2,4), (3,4), (1,5), (2,5), (3,5), (2,6), (3,6),
        (4,7), (5,7), (6,7), (4,8), (5,8), (6,8), (5,9),
        (7,4), (7,5), (7,6), (8,4), (8,5), (8,6), (9,5)],
    3: [(6,1), (3,3), (7,3), (1,4), (9,6), (3,7), (7,7), (4,9)],
    4: [(1,1), (3,1), (9,1), (9,3), (1,7), (1,9), (7,9), (9,9)]
}

# Планетарные значения
planet_info = {
    1: ("Солнце", "рубиновый", "лидерство, авторитет, ясность"),
    2: ("Луна", "светло-голубой", "эмоциональность, мягкость, интуиция"),
    3: ("Юпитер", "шафрановый", "мудрость, наставничество, рост"),
    4: ("Раху", "чайный", "иллюзии, нестабильность, неожиданности"),
    5: ("Меркурий", "изумрудный", "ум, коммуникация, адаптация"),
    6: ("Венера", "розовый", "гармония, любовь, эстетика"),
    7: ("Кету", "дымчатый", "уединение, отрешённость, интуиция"),
    8: ("Сатурн", "синий", "карма, дисциплина, ограничения"),
    9: ("Марс", "алый", "энергия, воля, действия")
}

def reduce_to_digit(value):
    total = sum(int(d) for d in str(value) if d.isdigit())
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def draw_grid(colors):
    zone_map = np.zeros((9, 9), dtype=int)
    for zone, coords in zone_coords.items():
        for x, y in coords:
            zone_map[y - 1, x - 1] = zone
    fig, ax = plt.subplots(figsize=(6, 6))
    for y in range(9):
        for x in range(9):
            zone = zone_map[y, x]
            color = color_map[colors[zone]] if zone in colors else 'white'
            rect = plt.Rectangle([x, 8 - y], 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(9) + 0.5)
    ax.set_yticks(np.arange(9) + 0.5)
    ax.set_xticklabels(range(1, 10))
    ax.set_yticklabels(range(1, 10))
    ax.set_aspect('equal')
    plt.grid(True)
    st.pyplot(fig)

# Интерфейс
st.title("Васту Янтра по координатам")

st.markdown("""
Введите координаты места — это может быть ваш дом, участок, квартира или место работы.  
Координаты можно узнать, введя адрес на [этой странице](https://snipp.ru/tools/address-coord).  
Скопируйте значения широты и долготы в поля ниже.

На основе координат строится индивидуальная Васту-янтра, в которой:

- каждая зона окрашена в цвет, соответствующий планете,
- планета определяется суммой градусов и минут географической долготы и широты.
- отображаются краткие характеристики и рекомендации по интерьеру.
""")

lat_input = st.text_input("Северная широта", "65.026802")
lon_input = st.text_input("Восточная долгота", "35.709128")

if st.button("Построить мандалу"):
    try:
        lat = float(lat_input)
        lon = float(lon_input)

        lat_deg = int(lat)
        lat_min = int(round((lat - lat_deg) * 60))
        lon_deg = int(lon)
        lon_min = int(round((lon - lon_deg) * 60))

        z1 = reduce_to_digit(lat_deg)
        z2 = reduce_to_digit(lon_deg)
        z3 = reduce_to_digit(lat_min)
        z4 = reduce_to_digit(lon_min)

        st.markdown(f"**Результаты по координатам:**")
        st.markdown(f"Зона 1 (градусы широты): {z1} — {planet_info[z1][0]} ({planet_info[z1][1]}, {planet_info[z1][2]})")
        st.markdown(f"Зона 2 (градусы долготы): {z2} — {planet_info[z2][0]} ({planet_info[z2][1]}, {planet_info[z2][2]})")
        st.markdown(f"Зона 3 (минуты широты): {z3} — {planet_info[z3][0]} ({planet_info[z3][1]}, {planet_info[z3][2]})")
        st.markdown(f"Зона 4 (минуты долготы): {z4} — {planet_info[z4][0]} ({planet_info[z4][1]}, {planet_info[z4][2]})")

        draw_grid({1: z1, 2: z2, 3: z3, 4: z4})

        if any(z in [4, 7, 8, 9] for z in [z1, z2, z3, z4]):
            st.warning("Обнаружены зоны, управляемые Раху, Кету, Сатурном или Марсом. Возможны нестабильность, напряжение или изоляция.")
            st.markdown("**Рекомендуется коррекция через свет, чистоту, мантры и янтры, символы благотворных планет: Юпитер, Луна и Солнце, живой огонь, благовония и звуки. Не злоупотребляйте цветами Раху, Кету, Сатурна или Марса в интерьере, сбалансируйте их нейтральным песочным цветом и натуральными материалами: дерево, камень, лён.**")

        st.markdown("""
---

**Как работает расчёт**

Мы переводим координаты в градусы и минуты:
- целое число — это градусы,
- дробная часть переводится в минуты (1° = 60′),
- затем сумма цифр сводится к числу от 1 до 9.

Основа расчёта — **свастическая Васту-мандала Южной Индии**, в которой 9×9 зон согласуются с планетами и пространством.

---

### 📌 Как использовать янтру:
- Распечатайте или сохраните как изображение
- Разместите в доме или на рабочем месте (ориентируясь по сторонам света — север вверху)
- Украсьте сектора соответствующими планетам цветами, символами, лампами, благовониями или мантрами.
""")

    except ValueError:
        st.error("Пожалуйста, введите корректные координаты.")

st.markdown("""
---

🔍 **Для полной интерпретации и коррекций вы можете обратиться за Васту-консультацией по [этой ссылке](https://goroskop1008.ru/uslugi/#consult#!/tproduct/842449103-1607970659374)**

🛠️ Программа разработана **С. А. Кройцер**  
Все права защищены.
""")
