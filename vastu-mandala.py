import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests

# Цвета по планетам
color_map = {
    1: '#E52B50', 2: '#87CEEB', 3: '#F4C430', 4: '#86261c',
    5: '#009B77', 6: '#FADADD', 7: '#b2beb5', 8: '#0047AB', 9: '#ff4040'
}

# Координаты Васту-зон
zone_coords = {
    1: [(4,4), (5,4), (6,4), (4,5), (5,5), (6,5), (4,6), (5,6), (6,6),
        (2,1), (2,2), (1,2), (8,1), (8,2), (9,2), (1,8), (2,8), (2,9), (8,8), (8,9), (9,8)],
    2: [(5,1), (4,2), (5,2), (6,2), (4,3), (5,3), (6,3),
        (2,4), (3,4), (1,5), (2,5), (3,5), (2,6), (3,6),
        (4,7), (5,7), (6,7), (4,8), (5,8), (6,8), (5,9),
        (7,4), (7,5), (7,6), (8,4), (8,5), (8,6), (9,5)],
    3: [(1,6), (3,3), (7,3), (1,4), (9,6), (3,7), (7,7), (4,9)],
    4: [(1,1), (3,1), (9,1), (9,3), (1,7), (1,9), (7,9), (9,9)]
}

# Сумма цифр до однозначного числа
def reduce_to_digit(value):
    total = sum(int(d) for d in str(value) if d.isdigit())
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

# Получить координаты по адресу
def get_coordinates_from_address(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'VastuApp/1.0'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        return None, None

# Рисуем сетку
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

# Streamlit интерфейс
st.title("🧭 Индивидуальная Васту Мандала по адресу")

address = st.text_input("Введите адрес (например: Россия, Челябинск, улица Габдуллы Тукая, 20)", "")

if st.button("Рассчитать и построить мандалу"):
    if address:
        lat, lon = get_coordinates_from_address(address)
        if lat is None:
            st.error("Координаты не найдены. Проверьте адрес.")
        else:
            st.success(f"Координаты: широта {lat}, долгота {lon}")
            lat_deg = int(lat)
            lat_min = int(abs(lat - lat_deg) * 10000)
            lon_deg = int(lon)
            lon_min = int(abs(lon - lon_deg) * 10000)

            z1 = reduce_to_digit(lat_deg)
            z2 = reduce_to_digit(lon_deg)
            z3 = reduce_to_digit(lat_min)
            z4 = reduce_to_digit(lon_min)

            st.write(f"Числа по координатам: 🌞 {z1}, 🌍 {z2}, ⏱ {z3}, 🧭 {z4}")
            draw_grid({1: z1, 2: z2, 3: z3, 4: z4})
    else:
        st.warning("Введите адрес для начала расчёта.")
