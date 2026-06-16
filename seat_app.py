import streamlit as st
import random
import json
import os

ROWS = 5
COLS = 6
TOTAL = 26

def render_table(table_data):

    html = "<table style='border-collapse: collapse; margin:auto;'>"

    for row in table_data:
        html += "<tr>"

        for cell in row:

            if cell == 0:
                bg = "#f0f0f0"
                text = ""
            elif 1 <= cell <= 13:
                bg = "#d0e8ff"
                text = str(cell)
            else:
                bg = "#ffd6e7"
                text = str(cell)

            html += f"<td style='border:1px solid #999; width:60px; height:60px; text-align:center; vertical-align:middle; font-size:18px; background-color:{bg};'>{text}</td>"

        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
def load_data():
    if os.path.exists("seats.json"):
        try:
            with open("seats.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    return None

def save_data(data):
    with open("seats.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


saved_seats = load_data()

st.title("席替えアプリ")

password=st.text_input(" パスワードを入力",type="password")
if password !="classA":
    st.stop()


mode = st.radio(
    "モード",
    ["前回の席を使う", "席を編集する"]
)

seat_layout = None


if mode == "前回の席を使う":
    if saved_seats:
        st.write("前回の席")
        render_table(saved_seats)
        seat_layout = saved_seats
    else:
        st.warning("データがありません")


else:
    st.write("0=空席 / 1-13=男 / 14-26=女")

    default = saved_seats if saved_seats else [[0]*COLS for _ in range(ROWS)]

    seat_layout = []

    for i in range(ROWS):
        row = []
        for j in range(COLS):

            value = st.number_input(
                f"{i+1}-{j+1}",
                min_value=0,
                max_value=26,
                value=int(default[i][j]),
                step=1,
                key=f"cell_{i}_{j}"
            )

            row.append(int(value))

        seat_layout.append(row)

    st.write("現在の席")
    render_table(seat_layout)
    
fixed_positions = st.multiselect(
    "固定したい席（行-列）",
    [(i, j) for i in range(ROWS) for j in range(COLS)]
)
fixed_positions = set(fixed_positions)


if seat_layout:

    boys = list(range(1, 14))
    girls = list(range(14, 27))

    random.shuffle(boys)
    random.shuffle(girls)

    if st.button("席替えする"):

        boys = list(range(1, 14))
        girls = list(range(14, 27))

        previous = saved_seats if saved_seats else []

        fixed_values = {
        seat_layout[i][j]
        for (i, j) in fixed_positions
        if seat_layout[i][j] != 0
    }
        boys = [b for b in boys if b not in fixed_values]
        girls = [g for g in girls if g not in fixed_values]

        random.shuffle(boys)
        random.shuffle(girls)

        boy_i = 0
        girl_i = 0

        result = []

        for i, row in enumerate(seat_layout):
            new_row = []

            for j, cell in enumerate(row):

                if (i,j) in fixed_positions:
                    new_row.append(cell)
                    continue


                if 1 <= cell <= 13:

                    choices = [
                        b for b in boys
                        if not previous 
                        or previous[i][j] != b
                    ]

                    if not choices:
                        choices = boys

                    value = random.choice(choices)
                    boys.remove(value)

                    new_row.append(value)


                elif 14 <= cell <= 26:

                    choices = [
                        g for g in girls
                        if not previous
                        or previous[i][j] != g
                    ]

                    if not choices:
                        choices = girls


                    value = random.choice(choices)
                    girls.remove(value)

                    new_row.append(value)


                else:
                    new_row.append(0)

            result.append(new_row)

        st.session_state.current_result = result

if "current_result" in st.session_state:
    st.write("現在の席（結果）")
    render_table(st.session_state.current_result)


if st.button("保存"):
    if "current_result" in st.session_state:
        save_data(st.session_state.current_result)
        st.success("席替え結果を保存した")
    elif seat_layout:
        save_data(seat_layout)
        st.success("編集した席を保存した")

if st.button("リセット"):
    if os.path.exists("seats.json"):
        os.remove("seats.json")
    st.session_state.current_result = None
    st.success("リセットした")

