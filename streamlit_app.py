
import streamlit as st
import random
import pandas as pd

class BatterCard:
    def __init__(self, name, p_H, p_BB, p_HR, p_K, p_GB, p_FB):
        self.name = name
        # raw inputs
        probs = [p_H, p_BB, p_HR, p_K, p_GB, p_FB]
        total = sum(probs)
        # normalize so they sum to 1
        self.p_H, self.p_BB, self.p_HR, self.p_K, self.p_GB, self.p_FB = [p/total for p in probs]

class PitcherCard:
    def __init__(self, name, p_H, p_BB, p_HR, p_K, p_GB, p_FB):
        self.name = name
        # raw inputs
        probs = [p_H, p_BB, p_HR, p_K, p_GB, p_FB]
        total = sum(probs)
        # normalize so they sum to 1
        self.p_H, self.p_BB, self.p_HR, self.p_K, self.p_GB, self.p_FB = [p/total for p in probs]

def simulate_plate_appearance(batter, pitcher):
    outcomes = ['H', 'BB', 'HR', 'K', 'GB', 'FB']
    # average probabilities
    probs = [
        (batter.p_H + pitcher.p_H) / 2,
        (batter.p_BB + pitcher.p_BB) / 2,
        (batter.p_HR + pitcher.p_HR) / 2,
        (batter.p_K + pitcher.p_K) / 2,
        (batter.p_GB + pitcher.p_GB) / 2,
        (batter.p_FB + pitcher.p_FB) / 2,
    ]
    total = sum(probs)
    normalized = [p / total for p in probs]
    return random.choices(outcomes, weights=normalized, k=1)[0]

# Streamlit UI
st.title("TCG Baseball Simulation MVP")

st.sidebar.header("Configure Batter Card")
with st.sidebar.form("batter_form"):
    b_name = st.text_input("Batter Name", "Power Hitter")
    b_H = st.number_input("p(H) - Hit", value=0.20, min_value=0.0, max_value=1.0, step=0.01)
    b_BB = st.number_input("p(BB) - Walk", value=0.10, min_value=0.0, max_value=1.0, step=0.01)
    b_HR = st.number_input("p(HR) - Home Run", value=0.05, min_value=0.0, max_value=1.0, step=0.01)
    b_K = st.number_input("p(K) - Strikeout", value=0.15, min_value=0.0, max_value=1.0, step=0.01)
    b_GB = st.number_input("p(GB) - Ground Ball", value=0.30, min_value=0.0, max_value=1.0, step=0.01)
    b_FB = st.number_input("p(FB) - Fly Ball", value=0.20, min_value=0.0, max_value=1.0, step=0.01)
    b_submit = st.form_submit_button("Set Batter")
if b_submit:
    batter = BatterCard(b_name, b_H, b_BB, b_HR, b_K, b_GB, b_FB)
else:
    batter = BatterCard("Power Hitter", 0.20, 0.10, 0.05, 0.15, 0.30, 0.20)

st.sidebar.header("Configure Pitcher Card")
with st.sidebar.form("pitcher_form"):
    p_name = st.text_input("Pitcher Name", "Ace Pitcher")
    p_H = st.number_input("p(H) - Hit", value=0.25, min_value=0.0, max_value=1.0, step=0.01)
    p_BB = st.number_input("p(BB) - Walk", value=0.08, min_value=0.0, max_value=1.0, step=0.01)
    p_HR = st.number_input("p(HR) - Home Run", value=0.10, min_value=0.0, max_value=1.0, step=0.01)
    p_K = st.number_input("p(K) - Strikeout", value=0.30, min_value=0.0, max_value=1.0, step=0.01)
    p_GB = st.number_input("p(GB) - Ground Ball", value=0.25, min_value=0.0, max_value=1.0, step=0.01)
    p_FB = st.number_input("p(FB) - Fly Ball", value=0.02, min_value=0.0, max_value=1.0, step=0.01)
    p_submit = st.form_submit_button("Set Pitcher")
if p_submit:
    pitcher = PitcherCard(p_name, p_H, p_BB, p_HR, p_K, p_GB, p_FB)
else:
    pitcher = PitcherCard("Ace Pitcher", 0.25, 0.08, 0.10, 0.30, 0.25, 0.02)

st.header("Simulation Control")
num_sims = st.number_input("Number of Plate Appearances to Simulate", value=1000, min_value=1, step=1)
if st.button("Run Simulation"):
    results = [simulate_plate_appearance(batter, pitcher) for _ in range(num_sims)]
    df = pd.DataFrame(results, columns=["Outcome"])
    counts = df["Outcome"].value_counts().reindex(['H','BB','HR','K','GB','FB'], fill_value=0)
    st.subheader("Simulation Results")
    st.table(counts)
    st.bar_chart(counts)
