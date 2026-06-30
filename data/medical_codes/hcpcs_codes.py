"""HCPCS DME & Services Codes database (30+ codes with cost estimates and risk weights)"""

HCPCS_CODES = {
    # Durable Medical Equipment (DME)
    "E0601": {"description": "Continuous positive airway pressure (CPAP) device", "cost_estimate": 800, "risk_weight": 40, "category": "respiratory_equipment"},
    "E0424": {"description": "Stationary compressed gaseous oxygen system, rental", "cost_estimate": 1200, "risk_weight": 60, "category": "respiratory_equipment"},
    "E0431": {"description": "Portable gaseous oxygen system, rental", "cost_estimate": 800, "risk_weight": 55, "category": "respiratory_equipment"},
    "E1390": {"description": "Oxygen concentrator, single delivery port", "cost_estimate": 1500, "risk_weight": 60, "category": "respiratory_equipment"},
    
    "E0250": {"description": "Hospital bed, fixed height, with mattress", "cost_estimate": 500, "risk_weight": 30, "category": "bed_equipment"},
    "E0260": {"description": "Hospital bed, semi-electric, with mattress", "cost_estimate": 950, "risk_weight": 35, "category": "bed_equipment"},
    "E0290": {"description": "Hospital bed, total electric, without mattress", "cost_estimate": 1200, "risk_weight": 40, "category": "bed_equipment"},

    "E1130": {"description": "Standard wheelchair, fixed full length arms", "cost_estimate": 450, "risk_weight": 25, "category": "mobility_equipment"},
    "E1236": {"description": "Wheelchair, pediatric size, folding, adjustable", "cost_estimate": 850, "risk_weight": 25, "category": "mobility_equipment"},
    "E0985": {"description": "Wheelchair accessory, seat lift mechanism", "cost_estimate": 350, "risk_weight": 15, "category": "mobility_equipment"},
    "E0143": {"description": "Walker, folding, wheeled, without seat", "cost_estimate": 120, "risk_weight": 10, "category": "mobility_equipment"},
    "E0114": {"description": "Crutches, underarm, aluminum, pair", "cost_estimate": 60, "risk_weight": 5, "category": "mobility_equipment"},

    # Emergency Transport (Ambulance)
    "A0425": {"description": "Ground mileage, per statute mile", "cost_estimate": 15, "risk_weight": 5, "category": "transport"},
    "A0427": {"description": "Ambulance service, Advanced Life Support, emergency (ALS1)", "cost_estimate": 950, "risk_weight": 40, "category": "transport"},
    "A0428": {"description": "Ambulance service, Basic Life Support, non-emergency (BLS)", "cost_estimate": 400, "risk_weight": 15, "category": "transport"},
    "A0429": {"description": "Ambulance service, Basic Life Support, emergency (BLS-Emergency)", "cost_estimate": 650, "risk_weight": 25, "category": "transport"},
    "A0433": {"description": "Advanced Life Support, level 2 (ALS2)", "cost_estimate": 1400, "risk_weight": 50, "category": "transport"},
    "A0434": {"description": "Specialty care transport (SCT)", "cost_estimate": 1800, "risk_weight": 55, "category": "transport"},
    "A0430": {"description": "Ambulance service, conventional air service, fixed wing", "cost_estimate": 6500, "risk_weight": 70, "category": "transport"},
    "A0431": {"description": "Ambulance service, conventional air service, rotary wing", "cost_estimate": 8500, "risk_weight": 75, "category": "transport"},

    # Medical Supplies & Orthotic Devices
    "A4253": {"description": "Blood glucose test or reagent strips, 50 strips", "cost_estimate": 45, "risk_weight": 5, "category": "supplies"},
    "A4259": {"description": "Lancets, per box of 100", "cost_estimate": 15, "risk_weight": 2, "category": "supplies"},
    "A4550": {"description": "Surgical trays, sterile, list", "cost_estimate": 35, "risk_weight": 2, "category": "supplies"},
    "L1810": {"description": "Knee orthosis, elastic with joints, prefabricated", "cost_estimate": 150, "risk_weight": 10, "category": "orthotics"},
    "L1830": {"description": "Knee orthosis, immobilizer, canvas, prefabricated", "cost_estimate": 120, "risk_weight": 10, "category": "orthotics"},
    "L3908": {"description": "Wrist hand orthosis, wrist extension control, prefabricated", "cost_estimate": 80, "risk_weight": 5, "category": "orthotics"},

    # Procedures & Drugs Administered
    "J1745": {"description": "Injection, infliximab, 10mg", "cost_estimate": 950, "risk_weight": 65, "category": "drugs_injected"},
    "J7030": {"description": "Infusion, normal saline solution, 1000cc", "cost_estimate": 80, "risk_weight": 5, "category": "drugs_injected"},
    "J3301": {"description": "Injection, triamcinolone acetonide, not otherwise specified, 10mg", "cost_estimate": 45, "risk_weight": 10, "category": "drugs_injected"},
    "J0696": {"description": "Injection, ceftriaxone sodium, 250mg", "cost_estimate": 35, "risk_weight": 8, "category": "drugs_injected"},
    "J1885": {"description": "Injection, ketorolac tromethamine, 15mg", "cost_estimate": 25, "risk_weight": 5, "category": "drugs_injected"},
    "J1100": {"description": "Injection, dexamethasone sodium phosphate, 1mg", "cost_estimate": 15, "risk_weight": 5, "category": "drugs_injected"},
    "J2270": {"description": "Injection, morphine sulfate, up to 10mg", "cost_estimate": 45, "risk_weight": 25, "category": "drugs_injected"},
    "J3010": {"description": "Injection, fentanyl citrate, up to 2mL", "cost_estimate": 35, "risk_weight": 20, "category": "drugs_injected"}
}
