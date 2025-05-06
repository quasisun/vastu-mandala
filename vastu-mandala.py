{\rtf1\ansi\ansicpg1251\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import matplotlib.pyplot as plt\
import numpy as np\
import requests\
\
# \uc0\u1062 \u1074 \u1077 \u1090 \u1072  \u1087 \u1086  \u1087 \u1083 \u1072 \u1085 \u1077 \u1090 \u1072 \u1084  (\u1074 \u1072 \u1096 \u1072  \u1087 \u1072 \u1083 \u1080 \u1090 \u1088 \u1072 )\
color_map = \{\
    1: '#E52B50', 2: '#87CEEB', 3: '#F4C430', 4: '#86261c',\
    5: '#009B77', 6: '#FADADD', 7: '#b2beb5', 8: '#0047AB', 9: '#ff4040'\
\}\
\
# \uc0\u1042 \u1072 \u1089 \u1090 \u1091  \u1079 \u1086 \u1085 \u1099 \
zone_coords = \{\
    1: [(4,4), (5,4), (6,4), (4,5), (5,5), (6,5), (4,6), (5,6), (6,6),\
        (2,1), (2,2), (1,2), (8,1), (8,2), (9,2), (1,8), (2,8), (2,9), (8,8), (8,9), (9,8)],\
    2: [(5,1), (4,2), (5,2), (6,2), (4,3), (5,3), (6,3),\
        (2,4), (3,4), (1,5), (2,5), (3,5), (2,6), (3,6),\
        (4,7), (5,7), (6,7), (4,8), (5,8), (6,8), (5,9),\
        (7,4), (7,5), (7,6), (8,4), (8,5), (8,6), (9,5)],\
    3: [(1,6), (3,3), (7,3), (1,4), (9,6), (3,7), (7,7), (4,9)],\
    4: [(1,1), (3,1), (9,1), (9,3), (1,7), (1,9), (7,9), (9,9)]\
\}\
\
# \uc0\u1054 \u1076 \u1085 \u1086 \u1079 \u1085 \u1072 \u1095 \u1085 \u1086 \u1077  \u1095 \u1080 \u1089 \u1083 \u1086  \u1080 \u1079  \u1089 \u1091 \u1084 \u1084 \u1099  \u1094 \u1080 \u1092 \u1088 \
def reduce_to_digit(value):\
    total = sum(int(d) for d in str(value) if d.isdigit())\
    while total > 9:\
        total = sum(int(d) for d in str(total))\
    return total\
\
# \uc0\u1043 \u1077 \u1086 \u1082 \u1086 \u1076 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1077  \u1095 \u1077 \u1088 \u1077 \u1079  OpenStreetMap\
def get_coordinates_from_address(address):\
    url = 'https://nominatim.openstreetmap.org/search'\
    params = \{'q': address, 'format': 'json', 'limit': 1\}\
    headers = \{'User-Agent': 'VastuApp/1.0'\}\
    response = requests.get(url, params=params, headers=headers)\
    data = response.json()\
    if data:\
        return float(data[0]['lat']), float(data[0]['lon'])\
    else:\
        return None, None\
\
# \uc0\u1056 \u1080 \u1089 \u1091 \u1077 \u1084  \u1084 \u1072 \u1085 \u1076 \u1072 \u1083 \u1091 \
def draw_grid(colors):\
    zone_map = np.zeros((9, 9), dtype=int)\
    for zone, coords in zone_coords.items():\
        for x, y in coords:\
            zone_map[y - 1, x - 1] = zone\
    fig, ax = plt.subplots(figsize=(6, 6))\
    for y in range(9):\
        for x in range(9):\
            zone = zone_map[y, x]\
            color = color_map[colors[zone]] if zone in colors else 'white'\
            rect = plt.Rectangle([x, 8 - y], 1, 1, facecolor=color, edgecolor='black')\
            ax.add_patch(rect)\
    ax.set_xlim(0, 9)\
    ax.set_ylim(0, 9)\
    ax.set_xticks(np.arange(9) + 0.5)\
    ax.set_yticks(np.arange(9) + 0.5)\
    ax.set_xticklabels(range(1, 10))\
    ax.set_yticklabels(range(1, 10))\
    ax.set_aspect('equal')\
    plt.grid(True)\
    st.pyplot(fig)\
\
# Streamlit \uc0\u1080 \u1085 \u1090 \u1077 \u1088 \u1092 \u1077 \u1081 \u1089 \
st.title("\uc0\u55358 \u56813  \u1048 \u1085 \u1076 \u1080 \u1074 \u1080 \u1076 \u1091 \u1072 \u1083 \u1100 \u1085 \u1072 \u1103  \u1042 \u1072 \u1089 \u1090 \u1091  \u1052 \u1072 \u1085 \u1076 \u1072 \u1083 \u1072  \u1087 \u1086  \u1072 \u1076 \u1088 \u1077 \u1089 \u1091 ")\
\
address = st.text_input("\uc0\u1042 \u1074 \u1077 \u1076 \u1080 \u1090 \u1077  \u1072 \u1076 \u1088 \u1077 \u1089  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 : \u1056 \u1086 \u1089 \u1089 \u1080 \u1103 , \u1063 \u1077 \u1083 \u1103 \u1073 \u1080 \u1085 \u1089 \u1082 , \u1091 \u1083 \u1080 \u1094 \u1072  \u1043 \u1072 \u1073 \u1076 \u1091 \u1083 \u1083 \u1099  \u1058 \u1091 \u1082 \u1072 \u1103 , 20)", "")\
\
if st.button("\uc0\u1056 \u1072 \u1089 \u1089 \u1095 \u1080 \u1090 \u1072 \u1090 \u1100  \u1080  \u1087 \u1086 \u1089 \u1090 \u1088 \u1086 \u1080 \u1090 \u1100  \u1084 \u1072 \u1085 \u1076 \u1072 \u1083 \u1091 "):\
    if address:\
        lat, lon = get_coordinates_from_address(address)\
        if lat is None:\
            st.error("\uc0\u1050 \u1086 \u1086 \u1088 \u1076 \u1080 \u1085 \u1072 \u1090 \u1099  \u1085 \u1077  \u1085 \u1072 \u1081 \u1076 \u1077 \u1085 \u1099 . \u1055 \u1088 \u1086 \u1074 \u1077 \u1088 \u1100 \u1090 \u1077  \u1072 \u1076 \u1088 \u1077 \u1089 .")\
        else:\
            st.success(f"\uc0\u1050 \u1086 \u1086 \u1088 \u1076 \u1080 \u1085 \u1072 \u1090 \u1099 : \u1096 \u1080 \u1088 \u1086 \u1090 \u1072  \{lat\}, \u1076 \u1086 \u1083 \u1075 \u1086 \u1090 \u1072  \{lon\}")\
            lat_deg = int(lat)\
            lat_min = int(abs(lat - lat_deg) * 10000)\
            lon_deg = int(lon)\
            lon_min = int(abs(lon - lon_deg) * 10000)\
\
            z1 = reduce_to_digit(lat_deg)\
            z2 = reduce_to_digit(lon_deg)\
            z3 = reduce_to_digit(lat_min)\
            z4 = reduce_to_digit(lon_min)\
\
            st.write(f"\uc0\u1063 \u1080 \u1089 \u1083 \u1072  \u1087 \u1086  \u1082 \u1086 \u1086 \u1088 \u1076 \u1080 \u1085 \u1072 \u1090 \u1072 \u1084 : \u55356 \u57118  \{z1\}, \u55356 \u57101  \{z2\}, \u9201  \{z3\}, \u55358 \u56813  \{z4\}")\
            draw_grid(\{1: z1, 2: z2, 3: z3, 4: z4\})\
    else:\
        st.warning("\uc0\u1042 \u1074 \u1077 \u1076 \u1080 \u1090 \u1077  \u1072 \u1076 \u1088 \u1077 \u1089  \u1076 \u1083 \u1103  \u1085 \u1072 \u1095 \u1072 \u1083 \u1072  \u1088 \u1072 \u1089 \u1095 \u1105 \u1090 \u1072 .")\
}