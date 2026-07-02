# Country starting data presets

COUNTRY_PRESETS = {
    "Sweden": {
        "starting_civs": 9,
        "starting_mils": 3,
        "consumer_goods_percent": 0,
        "global_construction_bonus":0,
        "economy_law": "Civilian Economy",
        "states": [
            {"name": "Skåne", "max_slots": 6, "used_slots": 2, "infra": 3},
            {"name": "Småland", "max_slots": 2, "used_slots": 1, "infra": 3},
            {"name": "Västergötland", "max_slots": 4, "used_slots": 3, "infra": 3},
            {"name": "Bohuslän", "max_slots": 2, "used_slots": 0, "infra": 3},
            {"name": "Gotland", "max_slots": 1, "used_slots": 0, "infra": 3},
            {"name": "Södermanland", "max_slots": 6, "used_slots": 6, "infra": 4},
            {"name": "Värmland", "max_slots": 2, "used_slots": 0, "infra": 2},
            {"name": "Dalarna", "max_slots": 2, "used_slots": 0, "infra": 3},
            {"name": "Gävleborg", "max_slots": 4, "used_slots": 1, "infra": 2, "infra_mod": 15, "civ_mod": 15},
            {"name": "Jämtland", "max_slots": 2, "used_slots": 0, "infra": 2},
            {"name": "Västerbotten", "max_slots": 2, "used_slots": 0, "infra": 2},
            {"name": "Norrbotten", "max_slots": 2, "used_slots": 1, "infra": 2},
        ]
    },
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