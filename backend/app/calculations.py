"""
Calculation Engine (Pandas/NumPy)
---------------------------------
Performs physics-based simulation of hybrid power plants.
"""
import pandas as pd
import numpy as np

# Constants for Simulation
BASE_LOAD_MW = 50.0 
CO2_GRID_INTENSITY = 0.5 
CO2_GAS_INTENSITY = 0.2 

def calculate_hybrid_performance(
    num_engines: int, 
    solar_mw: float, 
    battery_mwh: float,
    engine_specs: dict
) -> dict:
    """
    Simulates a 24-hour dispatch cycle.
    """
    
    # 1. Create Time Index
    hours = np.arange(24)
    df = pd.DataFrame(index=hours)
    df['hour'] = hours

    # 2. Solar Profile
    df['solar_mw'] = solar_mw * np.exp( - (hours - 12)**2 / (2 * 2.5**2) )
    df['solar_mw'] = df['solar_mw'].clip(lower=0) 

    # 3. Battery Profile
    discharge_power = 0
    if battery_mwh > 0:
        discharge_power = battery_mwh / 4.0 

    df['battery_mw'] = 0.0
    mask_evening = (df['hour'] >= 18) & (df['hour'] <= 21)
    df.loc[mask_evening, 'battery_mw'] = discharge_power

    # 4. Engine Dispatch
    # Use dynamic capacity from specs, not hardcoded!
    nominal_mw = engine_specs.get("nominal_power_mw", 0)
    total_engine_capacity = num_engines * nominal_mw
    
    df['load_mw'] = BASE_LOAD_MW
    df['net_load'] = df['load_mw'] - (df['solar_mw'] + df['battery_mw'])
    df['engine_mw'] = df['net_load'].clip(lower=0, upper=total_engine_capacity)
    df['total_mw'] = df['solar_mw'] + df['engine_mw'] + df['battery_mw']

    # ---------------------------------------------------------
    # Financial & Environmental Calculations
    # ---------------------------------------------------------
    
    total_solar_mwh = df['solar_mw'].sum()
    total_engine_mwh = df['engine_mw'].sum()
    total_battery_mwh = df['battery_mw'].sum()
    total_gen_mwh = total_solar_mwh + total_engine_mwh + total_battery_mwh

    # CAPEX Calculation
    # FIX: Use dynamic nominal power from specs (MW -> kW conversion)
    # If specs don't have cost, fallback to default 800
    cost_per_kw = engine_specs.get("capex_per_kw", 800)
    
    capex_engine = num_engines * (nominal_mw * 1000) * cost_per_kw
    capex_solar = solar_mw * 1000 * 700       
    capex_battery = battery_mwh * 1000 * 350  
    total_capex = capex_engine + capex_solar + capex_battery

    # CO2 Calculation
    baseline_co2 = (BASE_LOAD_MW * 24) * CO2_GRID_INTENSITY
    actual_co2 = total_engine_mwh * CO2_GAS_INTENSITY
    co2_savings = (baseline_co2 - actual_co2) * 365 

    # LCOE Calculation
    annual_generation = total_gen_mwh * 365
    amortized_capex = total_capex / 20 
    annual_fuel_cost = total_engine_mwh * 365 * 50 
    
    lcoe = 0
    if annual_generation > 0:
        lcoe = ((amortized_capex + annual_fuel_cost) / annual_generation) * 100 

    return {
        "kpis": {
            "total_capex_usd": round(total_capex, 2),
            "annual_co2_savings_tons": round(co2_savings, 1),
            "lcoe_cents_kwh": round(lcoe, 2)
        },
        "charts": df.to_dict(orient='records')
    }