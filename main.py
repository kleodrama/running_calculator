 
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import time

import json
import requests

from streamlit_lottie import st_lottie


url = requests.get("https://lottie.host/509a6dbb-4e38-4047-aa23-79434afe3b37/bbpn8q99Rg.json")
url_json = dict()

if url.status_code == 200:
    url_json = url.json()
else:
    print("Error in the URL")
st_lottie(url_json,
          reverse=True,
          height=100,
          width=100,
          speed=1,
          loop=True,
          quality='high',
          key='Car')

def pace_to_speed(p):
    s = 60 / p
    return s


def speed_to_pace(s):
    p = 60 / s
    return p


col1, col2 = st.columns(2)

with col1:
    "Επιλέξτε την απόσταση που θέλετε να τρέξετε:"

    distance = st.number_input("Απόσταση",
                               min_value=2.0,
                               value=42.195,
                               step=1.0,
                               format="%.3f"
                               )

    f'επιλεγμένη απόσταση: *{distance}* χιλιόμετρα'

with col2:
    "Επιλέξτε ρυθμό:"
    pace = st.number_input("Ρυθμός (σε λεπτά/χλμ)",
                           min_value=1.0,
                           value=6.0,
                           step=1.0
                           )
    # speed_value = pace_to_speed(pace)
    speed = st.number_input("Ταχύτητα (σε χλμ/ώρα)",
                           min_value=1.0,
                           value=pace_to_speed(pace),
                           step=1.0,
                           disabled=True
                           )

'---'
st.subheader('Χρόνος', divider="rainbow")

finish_time = pace * distance
finish_time = timedelta(minutes=round(finish_time, 1))

f'Τερματισμός {distance} χιλιομέτρων σε '
st.subheader(f'{finish_time}')

'---'

st.subheader('Περάσματα', divider="rainbow")
'''Παρακάτω μπορείτε να δείτε τους χρόνους σας ανα τμήμα.'''
'''Με διπλό κλικ στον ***Ρυθμό*** στον παρακάτω πίνακα, μπορείτε να επιλέξετε ρυθμό μόνο για το συγκεκριμένο τμήμα.'''

try:
    per_km = st.slider("Επιλέξτε ανά πόσα χιλιόμετρα.",
                       value=min(int(distance/2), 5),
                       min_value=1,
                       max_value=int(distance/2) + 1
                       )
except:
    pass

kms = range(per_km, int(distance) + 1, per_km)
kms = list(kms)
if distance - kms[-1] > 0:
    kms.append(distance)

kms_dif = list()
for i in range(len(kms)):
    if i == 0:
        kms_dif.append(kms[0])
    else:
        kms_dif.append(kms[i] - kms[i-1])
# print(kms_dif)


paces = list()
for i in kms:
    paces.append(pace)


df = pd.DataFrame(data={
    'Χιλιόμετρο': kms,
    'Ρυθμός': paces
})


# df["Χρόνος"] = df["Ρυθμός"] * df["Χιλιόμετρο"]

xronoi = list()
xronoi_tmima = list()
speeds = list()

# j = 0
for i in range(len(kms_dif)):
    # if j in st.session_state["data_key"]["edited_rows"]:
    try:
        rythmos = st.session_state["data_key"]["edited_rows"][i]["Ρυθμός"]
        xronos = rythmos * kms_dif[i]
        xronos = round(xronos, 1)
        speeds.append(pace_to_speed(rythmos))
    # else:
    except:
        # xronoi.append(timedelta(minutes=i))
        xronos = pace * kms_dif[i]
        xronos = round(xronos, 1)
        speeds.append(pace_to_speed(pace))
    if len(xronoi) == 0:
        xronoi.append(timedelta(minutes=xronos))
        xronoi_tmima.append(timedelta(minutes=xronos))
    else:
        xronoi_tmima.append(timedelta(minutes=xronos))
        x = xronoi[-1] + timedelta(minutes=xronos)
        xronoi.append(x)
    # j = j + 1


xronoi_str = list()
for i in xronoi:
    xronoi_str.append(str(i))

xronoi_tmima_str = list()
for i in xronoi_tmima:
    xronoi_tmima_str.append(str(i))


# df["Χρόνος περάσματος"] = xronoi
new_df = pd.DataFrame(data={
    'Ταχύτητα': speeds,
    'Χρόνος / τμήμα': xronoi_tmima_str,
    'Χρόνος': xronoi_str
})


col1, col2 = st.columns([5, 5], gap="small")

with col1:
    st.data_editor(
        df,
        key="data_key",
        column_order=("Χιλιόμετρο", "Ρυθμός", "Ταχύτητα", ),
        column_config={
            "Χιλιόμετρο": st.column_config.ProgressColumn(
                "Χιλιόμετρο",
                # help="The sales volume in USD",
                format="%f χλμ",
                min_value=0,
                max_value=distance,
            ),
            "Ρυθμός": st.column_config.NumberColumn(
                "Ρυθμός",
                # help="Επιλέξτε ρυθμό για το συγκεκριμένο τμήμα",
                min_value=0,
                max_value=1000,
                step=0.1,
                format="%0.1f λεπτά/χλμ",
            ),
        },
        hide_index=True,
        use_container_width=True,
        # on_change=pace_changed,
    )

with col2:
    st.dataframe(new_df,
                 column_config={
                     "Ταχύτητα": st.column_config.ProgressColumn(
                         "Ταχύτητα",
                         min_value=1,
                         max_value=25,
                         # step=1,
                         format="%d χλμ/ώρα",
                     ),
                 },
                 hide_index=True,
                 use_container_width=True)

# st.write(st.session_state["data_key"])

# for i in range(len(kms)):
#     st.write(i)
#     if i in st.session_state["data_key"]["edited_rows"]:
#         st.write("in")


st.subheader("Συνολική διάρκεια", divider="rainbow")
st.header(xronoi_str[-1])


new_new_df = pd.DataFrame(data={
    'Χιλιόμετρο': df["Χιλιόμετρο"],
    'Ταχύτητα': new_df["Ταχύτητα"]
})

st.bar_chart(new_new_df, x="Χιλιόμετρο", y="Ταχύτητα")





'---'

st.image('https://www.spotarace.gr/static/favicons/android-chrome-192x192.png',
         caption='Designed by Spot A Race', width=100)
st.link_button("spotarace.gr", "https://www.spotarace.gr")