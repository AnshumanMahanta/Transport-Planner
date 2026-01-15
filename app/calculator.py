EMISSION_FACTORS = {
    "suv": 0.213,
    "hatchback": 0.111,
    "motorcycle": 0.032,
    "electric bus": 0.012,
    "cng bus": 0.053,
    "metro": 0.011,
    "walking": 0.0,
    "cycling": 0.0
}

def calculate_emissions(mode: str, distance_km: float) -> float:
    mode = mode.lower()
    if mode not in EMISSION_FACTORS:
        raise ValueError("Unknown transport mode")
    return EMISSION_FACTORS[mode] * distance_km