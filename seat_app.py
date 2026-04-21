import streamlit as st
import random
import json
import os

password = st.text_input("パスワードを入力", type="password")

if password != "classA":
    st.stop()

st.title("席替えアプリ")
st.write("ボタンを押して席替え！")

st.markdown("""
<style>
td {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

students = list(range(1,27))

boys = students[:13].copy()
girls = students[13:].copy()

saved_seats=None
if os.path.exists("seats.json") and os.path.getsize("seats.json") > 0:
    with open("seats.json", "r") as f:
        try:
            saved_seats = json.load(f)
            st.write("前回の座席")
            st.table(saved_seats)
        except json.JSONDecodeError:
            saved_seats = None

if "current_result" not in st.session_state:
    st.session_state.current_result = None

            
if st.button("席替えする"):

    for _ in range(100):
        random.shuffle(boys)
        random.shuffle(girls)

        seats = [
            ["男", "女", "男", "女","男","女"],
            ["男", "女", "男", "女","男","女"],
            ["女", "男", "女", "男","女","男"],
            ["女", "男", "女", "男","女","男"],
            [ "",  "男", "女", "", "", ""],
        ]

        boy_i = 0
        girl_i = 0
        result = []

        for col in seats:
            row_result = []
            for s in col:
                if s == "男":
                    row_result.append(boys[boy_i])
                    boy_i += 1
                elif s=="女":
                    row_result.append(girls[girl_i])
                    girl_i += 1
                else:
                    row_result.append("")
            result.append(row_result)

        if saved_seats is None:
            break

        same_count = 0
        total = 0

        for i in range(len(result)):
            for j in range(len(result[i])):
                total += 1
                if result[i][j] == saved_seats[i][j]:
                    same_count += 1

        if same_count < 5:
            break

    
    st.session_state.current_result = result

if st.session_state.current_result:
    st.write("現在の席")
    st.table(st.session_state.current_result)

if st.button("この席を保存"):
    if st.session_state.current_result:
        with open("seats.json", "w") as f:
            json.dump(st.session_state.current_result, f)
        st.success("保存しました！")
