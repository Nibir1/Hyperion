"""
Unit Tests for Calculation Engine
---------------------------------
Verifies the physics simulation and financial math.
"""
from app import calculations

# Mock Engine Specs (Wärtsilä 31SG)
MOCK_SPECS = {
    "nominal_power_mw": 10.0, # Simplified for easy math
    "electrical_efficiency": 0.50,
    "heat_rate_kj_kwh": 7000,
    "capex_per_kw": 800,
    "opex_per_mwh": 5.0
}

def test_simulation_shape():
    """
    Test that the simulation returns 24 hours of data.
    """
    result = calculations.calculate_hybrid_performance(
        num_engines=4,
        solar_mw=20,
        battery_mwh=10,
        engine_specs=MOCK_SPECS
    )
    
    charts = result["charts"]
    assert len(charts) == 24
    assert charts[0]["hour"] == 0
    assert charts[23]["hour"] == 23

def test_pure_engine_logic():
    """
    Test a scenario with ONLY engines (No Solar, No Battery).
    Engines should run at Baseload (50MW) or Max Capacity.
    """
    # Case: Capacity (40MW) < Load (50MW) -> Should Max Out
    result = calculations.calculate_hybrid_performance(
        num_engines=4, # 4 * 10MW = 40MW Max
        solar_mw=0,
        battery_mwh=0,
        engine_specs=MOCK_SPECS
    )
    
    # Check Hour 12 (Noon)
    noon = result["charts"][12]
    assert noon["solar_mw"] == 0
    assert noon["battery_mw"] == 0
    assert noon["engine_mw"] == 40.0 # Capped at max capacity

def test_solar_impact():
    """
    Test that Solar generation reduces Engine output at noon.
    """
    result = calculations.calculate_hybrid_performance(
        num_engines=10, # 100MW Capacity (Plenty)
        solar_mw=20,
        battery_mwh=0,
        engine_specs=MOCK_SPECS
    )
    
    noon = result["charts"][12]
    
    # Solar should be peaking ~20MW
    assert noon["solar_mw"] > 19.0 
    
    # Load is 50. Engine should be 50 - Solar
    expected_engine = 50.0 - noon["solar_mw"]
    assert abs(noon["engine_mw"] - expected_engine) < 0.01

def test_financials():
    """
    Test CAPEX calculation.
    """
    # 1 Engine (10MW * $800/kW) = $8,000,000
    # 0 Solar
    # 0 Battery
    result = calculations.calculate_hybrid_performance(
        num_engines=1,
        solar_mw=0,
        battery_mwh=0,
        engine_specs=MOCK_SPECS
    )
    
    # 10 MW * 1000 kW/MW * $800 = 8,000,000
    expected_capex = 10 * 1000 * 800
    assert result["kpis"]["total_capex_usd"] == expected_capex