import streamlit as st

st.set_page_config(page_title="HOI4 Build Calculator", layout="wide")
st.title("HOI4 Infra + Civ Factory Build Order Calculator")

# ===================== NATION LEVEL =====================
st.header("Nation-wide Settings")

col1, col2 = st.columns(2)

with col1:
    starting_civs = st.number_input("Starting Civilian Factories", min_value=0, value=6, step=1)
    current_economy = st.selectbox(
        "Current Economy Law",
        ["Civilian Economy", "Early Mobilization", "Partial Mobilization", 
         "War Economy", "Total Mobilization", "Export Focus", "Undisturbed Isolation", 
         "Isolation", "Other / Custom"],
        index=0
    )
    global_speed = st.slider("Global Construction Speed Bonus (%)", -100, 200, 15, step=5)

with col2:
    starting_mils = st.number_input("Starting Military Factories", min_value=0, value=2, step=1)
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
                    ["+ Civilian Factories", "+ Military Factories", "+ Infrastructure Levels", 
                     "+ Max Build Slots", "+ Construction Speed %", "- Consumer Goods %"], 
                    index=0, key=f"ev_type_{i}")
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
        {"name": f"State {i+1}", "max_slots": 6, "used_slots": 0, "infra": 3, 
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

# ===================== CALCULATION ENGINE =====================
st.header("Optimal Build Order Simulation")

total_days = st.slider("Simulation Length (days)", 30, 730, 365, step=30)
show_debug = st.checkbox("Show Debug Info", value=True)

if st.button("Calculate Optimal Build Order", type="primary"):
    with st.spinner("Running simulation..."):
        
        best_result = {"score": -1.0, "order": []}
        
        def get_infra_multiplier(infra_level):
            return 1.0 + (infra_level * 0.2)
        
        def simulate(current_civs, sim_states, actions_left, current_order):
            if actions_left <= 0:
                if current_civs > best_result["score"]:
                    best_result["score"] = current_civs
                    best_result["order"] = current_order[:]
                return
            
            for idx, state in enumerate(sim_states):
                open_slots = state["max_slots"] - state["used_slots"]
                if open_slots <= 0:
                    continue
                
                infra_mult = get_infra_multiplier(state["infra"])
                
                # Calculate scores
                infra_score = open_slots * 3 - (state["infra"] * 5)
                civ_score = open_slots * 2.5 + (state["infra"] * 4) + (infra_mult * 10)
                
                if show_debug:
                    st.write(f"Debug | State: {state['name']} | Infra score: {infra_score:.1f} | Civ score: {civ_score:.1f} | Infra mult: {infra_mult:.1f}x")
                
                # Choose best action for this state
                if infra_score > civ_score and state["infra"] < 5:
                    new_states = [s.copy() for s in sim_states]
                    new_states[idx]["infra"] += 1
                    new_order = current_order + [f"Infrastructure in {state['name']} (infra {state['infra']} → {state['infra']+1})"]
                    simulate(current_civs, new_states, actions_left-1, new_order)
                else:
                    new_states = [s.copy() for s in sim_states]
                    new_states[idx]["used_slots"] += 1
                    new_order = current_order + [f"Civilian Factory in {state['name']} (infra {state['infra']}, speed {infra_mult:.1f}x)"]
                    simulate(current_civs + 0.3, new_states, actions_left-1, new_order)
        
        # Run
        sim_states = [s.copy() for s in st.session_state.states]
        simulate(float(starting_civs), sim_states, 8, [])
        
        st.success("Best build order found")
        
        st.subheader("Recommended Build Order")
        for idx, action in enumerate(best_result["order"], 1):
            st.write(f"{idx}. {action}")
        
        st.metric("Projected Civilian Factories", int(best_result["score"]))

st.caption("Layout complete • Global + Per-State + Events support")