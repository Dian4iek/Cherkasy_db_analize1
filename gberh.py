import streamlit as st
import pandas as pd

language = st.radio("🌐 Language / Мова:", ["Українська", "English"])


t = {
    "Українська": {
        "title": "Noise Robot 🤖",
        "desc": "Визначаю рівень шуму, кількість людей та рекомендований час перебування",
        "time_label": "🕒 Яка година вас цікавить?",
        "place_label": "📍 Яке місце вас цікавить?",
        "safe": "✅ Рівень безпечний, можна перебувати довго (до {time}).",
        "warn": "⚠️ Систематичний вплив понад 80 дБ може пошкодити слух. Рекомендується не перевищувати {time} на день та використовувати захист.",
        "danger": "🚫 Рівень шуму перевищує 100 дБ — навіть кілька хвилин можуть бути небезпечними. Перемістіться у тихіше місце або використовуйте навушники із захистом.",
        "nodata": "Для цього часу або місця поки немає даних.",
        "graph": "📊 Динаміка середнього рівня шуму протягом дня",
        "caption": "На графіку видно, як змінюється рівень шуму з 8:00 до 19:00. Найвищий рівень у ТРЦ Любава, середній — біля дороги, а найнижчий — у парку. Це показує, що відстань від джерел шуму суттєво впливає на комфорт людини.",
        "people": "Кількість людей поруч",
        "avg": "Середній рівень шуму",
        "at": "У {place} о {time}: {min}-{max} дБ",
    },
    "English": {
        "title": "Noise Robot 🤖",
        "desc": "I measure the noise level, number of people, and recommend safe exposure time",
        "time_label": "🕒 What time are you interested in?",
        "place_label": "📍 Which place are you interested in?",
        "safe": "✅ Safe level — you can stay for a long time (up to {time}).",
        "warn": "⚠️ Continuous exposure above 80 dB can damage hearing. Recommended limit: {time} per day with protection.",
        "danger": "🚫 Noise exceeds 100 dB — even a few minutes may be dangerous. Move to a quieter area or use hearing protection.",
        "nodata": "No data for this time or place yet.",
        "graph": "📊 Noise level dynamics throughout the day",
        "caption": "This chart shows how the average noise level changes from 8:00 to 19:00. The highest levels are in the mall, medium near the road, and the lowest in the park — showing how distance from noise sources affects comfort.",
        "people": "Number of nearby people",
        "avg": "Average noise level",
        "at": "In the {place} at {time}: {min}-{max} dB",
    }
}

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background-color: #E7D3BB; }
        [data-testid="stHeader"] { background-color: #E7D3BB; }
        [data-testid="stSidebar"] { background-color: #E7D3BB; }
        html, body { background-color: #E7D3BB; }
    </style>
""", unsafe_allow_html=True)

st.title(t[language]["title"])
st.write(t[language]["desc"])


data = {
    ("8:00", "Парк"): (46, 60, 1, 54),
    ("8:00", "Дорога"): (61, 83, 2, 72),
    ("9:00", "Парк"): (44, 81, 3, 64),
    ("9:00", "Дорога"): (50, 62, 2, 55),
    ("9:00", "ТРЦ Любава"): (55, 70, 3, 63),
    ("10:00", "Парк"): (48, 63, 3, 56),
    ("10:00", "Дорога"): (45, 50, 0, 47),
    ("10:00", "ТРЦ Любава"): (65, 84, 32, 75),
    ("11:00", "Парк"): (48, 74, 5, 80),
    ("11:00", "Дорога"): (49, 69, 4, 59),
    ("11:00", "ТРЦ Любава"): (58, 78, 43, 68),
    ("12:00", "Парк"): (45, 58, 9, 50),
    ("12:00", "Дорога"): (47, 77, 2, 61),
    ("12:00", "ТРЦ Любава"): (60, 84, 47, 68),
    ("13:00", "Парк"): (50, 82, 15, 66),
    ("13:00", "Дорога"): (47, 83, 4, 67),
    ("13:00", "ТРЦ Любава"): (64, 69, 85, 66),
    ("14:00", "Парк"): (52, 73, 7, 59),
    ("14:00", "Дорога"): (52, 63, 9, 56),
    ("14:00", "ТРЦ Любава"): (71, 89, 86, 84),
    ("15:00", "Парк"): (47, 59, 4, 50),
    ("15:00", "Дорога"): (52, 77, 5, 63),
    ("15:00", "ТРЦ Любава"): (70, 89, 56, 80),
    ("16:00", "Парк"): (46, 53, 7, 49),
    ("16:00", "Дорога"): (47, 70, 11, 50),
    ("16:00", "ТРЦ Любава"): (47, 70, 41, 79),
    ("17:00", "Дорога"): (54, 77, 15, 66),
    ("17:00", "Парк"): (45, 72, 12, 60),
    ("17:00", "ТРЦ Любава"): (73, 94, 58, 83),
    ("18:00", "Дорога"): (57, 76, 5, 65),
    ("18:00", "Парк"): (44, 53, 3, 47),
    ("18:00", "ТРЦ Любава"): (69, 88, 54, 82),
    ("19:00", "Дорога"): (57, 87, 0, 66),
    ("19:00", "Парк"): (47, 58, 3, 51),
    ("19:00", "ТРЦ Любава"): (65, 75, 54, 69),
}

safe_time_table = {
    80: (5, 30),
    85: (1, 45),
    90: (0, 30),
    95: (0, 10),
    100: (0, 5),
}


time = st.selectbox(t[language]["time_label"], [
    "8:00", "9:00", "10:00", "11:00", "12:00", "13:00",
    "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"
])
location = st.selectbox(t[language]["place_label"], ["Парк", "Дорога", "ТРЦ Любава"])


if (time, location) in data:
    dB_min, dB_max, people, avg_db = data[(time, location)]

    st.subheader(t[language]["at"].format(place=location.lower(), time=time, min=dB_min, max=dB_max))
    st.write(f"**{t[language]['people']}:** {people}")
    st.write(f"**{t[language]['avg']}:** {avg_db} dB")

    recommended = None
    for level, (hours, mins) in sorted(safe_time_table.items()):
        if avg_db <= level:
            recommended = (hours, mins)
            break

    if recommended:
        h, m = recommended
        pretty = f"{h} год {m} хв" if language == "Українська" else f"{h} h {m} min"
        if avg_db >= 80:
            st.warning(t[language]["warn"].format(time=pretty))
        else:
            st.success(t[language]["safe"].format(time=pretty))
    else:
        st.error(t[language]["danger"])
else:
    st.warning(t[language]["nodata"])

# --- chart ---
df = pd.DataFrame([
    {"time": t, "location": l, "avg_db": v[3]} for (t, l), v in data.items()
])
time_order = ["8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00"]
df["time"] = pd.Categorical(df["time"], categories=time_order, ordered=True)
df = df.sort_values("time")

st.subheader(t[language]["graph"])
st.line_chart(df.pivot(index="time", columns="location", values="avg_db"))
st.caption(t[language]["caption"])

#gallery#

st.subheader("📸 Noise Robot Gallery")

col1, col2 = st.columns(2)

with col1:
    st.image(r"C:/Users/Diana/Desktop/Genius/lubava.jpg", caption="ТРЦ Любава / Lybava Mall", use_container_width=True)
    st.image(r"C:/Users/Diana/Desktop/Genius/park.jpg", caption="Парк / Park", use_container_width=True)
    st.image(r"C:\Users\Diana\Desktop\Genius\road.png", caption="Дорога / Road", use_container_width=True)


with col2:
    st.image(r"C:/Users/Diana/Desktop/Genius/night_park.jpg", caption="Парк вночі/Night Park", use_container_width=True)

    st.image("https://vycherpno.ck.ua/wp-content/uploads/2021/10/245618473_3083612635253536_7618553771366827715_n-e1634931799161.jpg", caption="Дитяча площадка / Playground", use_container_width=True)

#streamlit run "C:\Users\Diana\Desktop\gberh.py"    