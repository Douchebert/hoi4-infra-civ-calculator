import streamlit as st

st.set_page_config(page_title="HOI4 Build Calculator", layout="wide")
st.title("HOI4 Infra + Civ Factory Build Order Calculator")

# ===================== NATION LEVEL =====================
st.header("Nation-wide Settings")

col1, col2 = st.columns(2)

with col1:
    current_economy = st.selectbox(
        "Current Economy Law",
        ["Civilian Economy", "Early Mobilization", "Partial Mobilization", 
         "War Economy", "Total Mobilization", "Export Focus", "Undisturbed Isolation", 
         "Isolation", "Other / Custom"],
        index=0
    )
    global_speed = st.slider("Global Construction Speed Bonus (%)", -100, 200, 15, step=5)

with col2:
    enable_eco_change = st.checkbox("Enable Planned Economy Law Change", value=False)
    
    if enable_eco_change:
        days_until_change = st.number_input("Days until new law", min_value=1, value=180, step=30)
        new_economy = st.selectbox(
            "New Economy Law",
            ["Civilian Economy", "Early Mobilization", "Partial Mobilization", 
             "War Economy", "Total Mobilization", "Export Focus", "Undisturbed Isolation", 
             "Isolation", "Other / Custom"],
            index=3
        )
        st.info(f"Economy law will change in {days_until_change} days -> {new_economy}")

# Global Civ/Infra modifiers
st.subheader("Global Extra Construction Speed Modifiers")
col_g1, col_g2 = st.columns(2)
with col_g1:
    global_civ_mod = st.slider("Global Civilian Speed Modifier (%)", -100, 100, 0, step=5)
with col_g2:
    global_infra_mod = st.slider("Global Infrastructure Speed Modifier (%)", -100, 100, 0, step=5)

# Consumer Goods
st.subheader("Consumer Goods")
consumer_goods = st.slider("Consumer Goods Factories (%)", 0, 50, 30, step=5)

st.caption("Global modifiers above • Per-state modifiers in States section")

# ===================== FOCUS / EVENTS =====================
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
                event["source"] = st.text_input("Source (e.g. Focus Name)", event.get("source", ""), key=f"ev_source_{i}")
                event["day"] = st.number_input("Occurs on Day", min_value=1, value=event.get("day", 30), key=f"ev_day_{i}")
                event["target"] = st.selectbox("Target", state_names, key=f"ev_target_{i}")
            
            with col2:
                event["type"] = st.selectbox("Bonus Type", 
                    ["+ Civilian Factories", "+ Infrastructure Levels", "+ Max Build Slots", 
                     "+ Construction Speed %", "- Consumer Goods %"], 
                    index=0, key=f"ev_type_{i}")
                # Fixed: consistent float types
                event["amount"] = st.number_input(
                    "Amount",
                    value=float(event.get("amount", 1.0)),
                    step=1.0,
                    key=f"ev_amount_{i}"
                )
            
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

# ===================== STATES =====================
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
            state["infra_mod"] = st.slider("Infra Speed Mod (%)", -100, 100, state["infra_mod"], step=5, key=f"infra_mod_{i}")
            
            if state["sync"]:
                state["civ_mod"] = state["infra_mod"]
                st.info(f"Civ Speed Mod = {state['civ_mod']}% (synced)")
            else:
                state["civ_mod"] = st.slider("Civ Speed Mod (%)", -100, 100, state["civ_mod"], step=5, key=f"civ_mod_{i}")

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

# ===================== SUMMARY =====================
st.header("Summary")
total_max = sum(s["max_slots"] for s in st.session_state.states)
total_used = sum(s["used_slots"] for s in st.session_state.states)
avg_infra = sum(s["infra"] for s in st.session_state.states) / len(st.session_state.states) if st.session_state.states else 0

st.metric("Total Max Slots", total_max)
st.metric("Total Slots Used", f"{total_used} / {total_max}")
st.metric("Average Infrastructure", f"{avg_infra:.1f}")

# ===================== CALCULATIONS =====================
st.header("Build Order Simulation")

total_days = st.slider("Simulation Length (days)", 30, 730, 365, step=30)

if st.button("Run Day-by-Day Simulation", type="primary"):
    with st.spinner("Running simulation..."):
        # Simple placeholder calculation for now
        total_civs_start = sum(1 for s in st.session_state.states for _ in range(0))  # placeholder
        projected_civs = 25 + (total_days / 180) * 5   # very rough
        
        st.success("Simulation Complete")
        st.metric("Projected Civilian Factories", f"{projected_civs:.1f}")
        st.info("Full day-by-day logic with infra bonuses, events, and build priorities coming in next update.")
        
        # We'll expand this heavily next

st.caption("Layout complete • Global + Per-State + Events support")