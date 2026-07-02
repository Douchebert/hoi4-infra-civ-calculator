# Country starting data presets

COUNTRY_PRESETS = {
    "Germany": {
        "starting_civs": 25,
        "starting_mils": 15,
        "consumer_goods_percent": 25,
        "economy_law": "Partial Mobilization",
        "states": [
            {"name": "Rhineland", "max_slots": 25, "used_slots": 20, "infra": 4},
            {"name": "Ruhr", "max_slots": 30, "used_slots": 25, "infra": 5},
            {"name": "Berlin", "max_slots": 18, "used_slots": 12, "infra": 4},
            {"name": "Silesia", "max_slots": 15, "used_slots": 8, "infra": 3},
            {"name": "East Prussia", "max_slots": 12, "used_slots": 6, "infra": 3},
        ]
    },
    "Soviet Union": {
        "starting_civs": 35,
        "starting_mils": 20,
        "consumer_goods_percent": 35,
        "economy_law": "Civilian Economy",
        "states": [
            {"name": "Moscow", "max_slots": 22, "used_slots": 15, "infra": 4},
            {"name": "Leningrad", "max_slots": 18, "used_slots": 12, "infra": 4},
            {"name": "Ukraine", "max_slots": 20, "used_slots": 10, "infra": 3},
            {"name": "Ural", "max_slots": 15, "used_slots": 5, "infra": 2},
        ]
    },
    "United States": {
        "starting_civs": 40,
        "starting_mils": 10,
        "consumer_goods_percent": 20,
        "economy_law": "Civilian Economy",
        "states": [
            {"name": "New England", "max_slots": 20, "used_slots": 8, "infra": 4},
            {"name": "Midwest", "max_slots": 25, "used_slots": 10, "infra": 3},
            {"name": "California", "max_slots": 18, "used_slots": 7, "infra": 4},
        ]
    },
    # Add more countries here
}