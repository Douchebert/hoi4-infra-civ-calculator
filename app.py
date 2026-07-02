# HOI4 Infra + Civ Factory Build Order Calculator
# Clean foundation version

import streamlit as st
from data.countries import COUNTRY_PRESETS
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import copy

#===================== DATA STRUCTURES =====================

ECON_CIV = "Civilian Economy"
ECON_EARLY_MOB = "Early Mobilization"
ECON_PARTIAL_MOB = "Partial Mobilization"
ECON_WAR_ECON = "War Economy"
ECON_TOTAL_MOB = "Total Mobilization"
ECON_EXPORT_FOCUS = "Export Focus"
ECON_UNDISTURBED_ISOLATION = "Undisturbed Isolation"
ECON_ISOLATION = "Isolation"

ECON_TYPES = {
  ECON_CIV: {"eco_consume_mod":35, "eco_civ_mod":-30, "eco_mil_mod":-30},
  ECON_EARLY_MOB: {"eco_consume_mod":30, "eco_civ_mod":-10, "eco_mil_mod":-10},
  ECON_PARTIAL_MOB: {"eco_consume_mod":25, "eco_civ_mod":0, "eco_mil_mod":10},
  ECON_WAR_ECON: {"eco_consume_mod":20, "eco_civ_mod":0, "eco_mil_mod":20},
  ECON_TOTAL_MOB: {"eco_consume_mod":15, "eco_civ_mod":0, "eco_mil_mod":30},
  ECON_UNDISTURBED_ISOLATION: {"eco_consume_mod":20, "eco_civ_mod":-20, "eco_mil_mod":-20},
  ECON_ISOLATION: {"eco_consume_mod":10, "eco_civ_mod":-10, "eco_mil_mod":-10},
}



# ===================== COUNTRY SELECTION =====================

st.header("Country Selection")

country_list = list(COUNTRY_PRESETS.keys())

selected_country = st.selectbox(
    "Pick a Starting Country (searchable)",
    options=country_list,
    index=0
)

if selected_country:
    preset = COUNTRY_PRESETS[selected_country]
    
    # Auto-fill values
    starting_civs = preset["starting_civs"]
    starting_mils = preset["starting_mils"]
    consumer_goods = preset["consumer_goods_percent"]
    current_economy = preset["economy_law"]
    global_construction_bonus = preset["global_construction_bonus"]
    
    # Load states
    st.session_state.states = preset.get("states", []).copy()
    
    st.success(f"Loaded preset for **{selected_country}**")


# ===================== STREAMLIT UI =====================

st.set_page_config(page_title="HOI4 Build Calculator", layout="wide")
st.title("HOI4 Infra + Civ Factory Build Order Calculator")

# Nation Level
st.header("Nation-wide Settings")

col1, col2 = st.columns(2)

with col1:
    starting_civs = st.number_input("Starting Civilian Factories", min_value=0, value=starting_civs, step=1)
    current_economy = st.selectbox(
        "Current Economy Law",
        list(ECON_TYPES.keys()),
        index=0
    )
    global_speed = st.slider("Global Construction Speed Bonus (%)", -100, 200, global_construction_bonus, step=5)

with col2:
    starting_mils = st.number_input("Starting Military Factories", min_value=0, value=starting_mils, step=1)
    enable_eco_change = st.checkbox("Enable Planned Economy Law Change", value=False)
    
    if enable_eco_change:
        days_until_change = st.number_input("Days until new law", min_value=1, value=180, step=30)
        new_economy = st.selectbox(
            "New Economy Law",
            list(ECON_TYPES.keys()),
            index=3
        )
        st.info(f"Economy law will change in {days_until_change} days -> {new_economy}")

# Global modifiers
st.subheader("Global Extra Construction Speed Modifiers")
col_g1, col_g2 = st.columns(2)
with col_g1:
    global_civ_mod = st.slider("Global Civilian Speed Modifier (%)", -100, 100, 0, step=5)
with col_g2:
    global_infra_mod = st.slider("Global Infrastructure Speed Modifier (%)", -100, 100, 0, step=5)

# Consumer Goods
st.subheader("Consumer Goods")
consumer_goods = st.slider("Consumer Goods Factories (%)", 0, 100, consumer_goods, step=5)

# States section (simplified for cleanliness)
st.header("States")

if "states" not in st.session_state:
    st.session_state.states = [
        {"name": f"State {i+1}", "max_slots": 15, "used_slots": 0, "infra": 3, 
         "infra_mod": 0, "civ_mod": 0, "sync": True}
        for i in range(3)
    ]

for i, state in enumerate(st.session_state.states):
    with st.expander(f"{state['name']}", expanded=True):
        col_a, col_b, col_c = st.columns([3, 2, 3])
        with col_a:
            state["name"] = st.text_input("State Name", state["name"], key=f"name_{i}")
            state["max_slots"] = st.slider("Max Build Slots", 0, 25, state["max_slots"], step=1, key=f"max_{i}")
            state["used_slots"] = st.slider("Current Slots Used", 0, state["max_slots"], state["used_slots"], step=1, key=f"used_{i}")
        with col_b:
            state["infra"] = st.slider("Infrastructure Level", 0, 5, state["infra"], step=1, key=f"infra_{i}")
            state["sync"] = st.checkbox("Sync Civ & Infra modifiers", value=state.get("sync", True), key=f"sync_{i}")
        with col_c:
            state["infra_mod"] = st.slider("Infra Speed Mod (%)", -100, 100, state.get("infra_mod", 0), step=5, key=f"infra_mod_{i}")
            if state["sync"]:
                state["civ_mod"] = state["infra_mod"]
                st.info(f"Civ Speed Mod = {state['civ_mod']}% (synced)")
            else:
                state["civ_mod"] = st.slider("Civ Speed Mod (%)", -100, 100, state.get("civ_mod", 0), step=5, key=f"civ_mod_{i}")

        if st.button("Delete this state", key=f"del_{i}"):
            st.session_state.states.pop(i)
            st.rerun()

if st.button("Add New State"):
    st.session_state.states.append({
        "name": f"New State {len(st.session_state.states)+1}",
        "max_slots": 12,
        "used_slots": 0,
        "infra": 2,
        "infra_mod": 0,
        "civ_mod": 0,
        "sync": True
    })
    st.rerun()

# Events section (simplified)
st.header("Focuses, Events & National Spirits")

if "events" not in st.session_state:
    st.session_state.events = []

enable_events = st.checkbox("Enable Focuses / Events / Spirits", value=False)

if enable_events:
    state_names = ["Global"] + [s["name"] for s in st.session_state.states]
    
    for i, event in enumerate(st.session_state.events):
        with st.expander(f"Event {i+1}: {event.get('source', '')}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                event["source"] = st.text_input("Source", event.get("source", ""), key=f"ev_source_{i}")
                event["day"] = st.number_input("Day", min_value=1, value=event.get("day", 30), key=f"ev_day_{i}")
                event["target"] = st.selectbox("Target", state_names, key=f"ev_target_{i}")
            with col2:
                event["type"] = st.selectbox("Type", 
                    ["+ Civilian Factories", "+ Military Factories", "+ Infrastructure Levels", 
                     "+ Max Build Slots", "+ Construction Speed %", "- Consumer Goods %"], 
                    key=f"ev_type_{i}")
                event["amount"] = st.number_input("Amount", value=float(event.get("amount", 1.0)), step=1.0, key=f"ev_amount_{i}")
            
            if st.button("Delete Event", key=f"ev_del_{i}"):
                st.session_state.events.pop(i)
                st.rerun()

    if st.button("Add New Focus/Event"):
        st.session_state.events.append({
            "source": "New Focus",
            "day": 30,
            "target": "Global",
            "type": "+ Civilian Factories",
            "amount": 2.0
        })
        st.rerun()

# ===================== CALCULATION (Foundation) =====================
st.header("Simulation (Foundation)")


