import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="Ancient Tale", layout="wide")

# --- Utility to show full background image ---
def show_background(image_name):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('{image_name}') no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "character" not in st.session_state:
    st.session_state.character = None
if "hearts" not in st.session_state:
    st.session_state.hearts = 4
if "pearls_answered" not in st.session_state:
    st.session_state.pearls_answered = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# --- Page navigation ---
def next_page(page):
    st.session_state.page = page

# --- MENU PAGE ---
if st.session_state.page == "menu":
    show_background("menu.png")
    st.markdown("<h1 style='text-align:center; color:white; font-size:60px;'>Ancient Tales</h1>", unsafe_allow_html=True)
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign In", use_container_width=True):
            next_page("signin")
    with col2:
        if st.button("Enter as Guest", use_container_width=True):
            next_page("choose_character")

# --- SIGN IN PAGE ---
elif st.session_state.page == "signin":
    show_background("menu.png")
    st.markdown("<h2 style='text-align:center; color:white;'>Sign In</h2>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if email and password:
            next_page("choose_character")
        else:
            st.warning("Please enter your email and password")

# --- CHARACTER SELECTION PAGE ---
elif st.session_state.page == "choose_character":
    show_background("menu.png")
    st.markdown("<h2 style='text-align:center; color:white; font-size:40px;'>Choose Your Character</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Dhabia"):
            st.session_state.character = "girl"
            next_page("scene_dubai1")
    with col2:
        if st.button("Nahyan"):
            st.session_state.character = "boy"
            next_page("scene_dubai1")

# --- STORY SCENES ---
def show_scene(image_name, next_scene):
    show_background(image_name)
    if st.button("Next ➜", use_container_width=True):
        next_page(next_scene)

# Scene flow based on gender
c = st.session_state.character
if st.session_state.page == "scene_dubai1":
    show_scene(f"dubai_new{c}1.png", "scene_dubai2")

elif st.session_state.page == "scene_dubai2":
    show_scene(f"dubai_new{c}2.png", "scene_welcome1")

elif st.session_state.page == "scene_welcome1":
    show_scene(f"welcome{c}1.png", "scene_welcome2")

elif st.session_state.page == "scene_welcome2":
    show_scene(f"welcome{c}2.png", "scene_kids1")

elif st.session_state.page == "scene_kids1":
    show_scene(f"kids{c}1.png", "scene_kids2")

elif st.session_state.page == "scene_kids2":
    show_scene(f"kids{c}2.png", "scene_kids3")

elif st.session_state.page == "scene_kids3":
    show_scene(f"kids{c}3.png", "scene_kids4")

elif st.session_state.page == "scene_kids4":
    show_scene(f"kids{c}4.png", "scene_crew1")

# --- CREW SCENES (1–9) ---
for i in range(1, 10):
    if st.session_state.page == f"scene_crew{i}":
        next_scene = "pearl_game" if i == 9 else f"scene_crew{i+1}"
        show_scene(f"crew{c}{i}.png", next_scene)

# --- PEARL GAME ---
if st.session_state.page == "pearl_game":
    show_background(f"pearlgame{c}1.png")

    # Start timer
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # Timer heart logic
    elapsed = time.time() - st.session_state.start_time
    hearts_left = 4 - int(elapsed // 30)
    if hearts_left < st.session_state.hearts:
        st.session_state.hearts = hearts_left
    if hearts_left <= 0:
        st.warning("Time’s up!")
        next_page("ship")

    # Hearts display
    hearts = "❤️ " * st.session_state.hearts
    st.markdown(f"<h3 style='color:red;'>{hearts}</h3>", unsafe_allow_html=True)

    # Pearl buttons
    st.markdown("<h3 style='color:white;'>Click on a pearl to answer!</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    pearls = [
        ("pearl1.png", "What do pearl divers search for?", "Pearls"),
        ("pearl2.png", "Where did the divers usually go?", "The sea"),
        ("pearl3.png", "What tool did they use to dive?", "Nose clip"),
        ("pearl4.png", "Who leads the divers?", "Naukhada")
    ]

    for i, (img, q, a) in enumerate(pearls):
        with [col1, col2, col3, col4][i]:
            if st.button(f"Pearl {i+1}"):
                ans = st.text_input(q, key=f"q{i}")
                if ans:
                    st.success(f"Correct answer: {a}")
                    st.session_state.pearls_answered += 1

    if st.session_state.pearls_answered >= 4:
        st.balloons()
        next_page("ship")

# --- SHIP SCENE ---
if st.session_state.page == "ship":
    show_background(f"ship{c}1.png")
    st.markdown("<h3 style='color:white;'>Naukhada asks: What is the role of teamwork in pearl diving?</h3>", unsafe_allow_html=True)
    st.text_input("Answer here")
    if st.button("Finish Round"):
        next_page("congrats1")

# --- CONGRATS SCENES ---
if st.session_state.page == "congrats1":
    show_background(f"congrats{c}1.png")
    st.markdown("<h1 style='color:gold; text-align:center;'>Congratulations!</h1>", unsafe_allow_html=True)
    time.sleep(5)
    next_page("congrats2")

elif st.session_state.page == "congrats2":
    show_background(f"congrats{c}2.png")
    st.markdown("<h2 style='color:white; text-align:center;'>You completed the Ancient Tale!</h2>", unsafe_allow_html=True)
