"""
Calculation Engine (Pandas/NumPy)
---------------------------------
Performs physics-based simulation of hybrid power plants.
Includes Geospatial Solar Irradiance modeling.
"""
import pandas as pd
import numpy as np

# Constants
BASE_LOAD_MW = 50.0 
CO2_GRID_INTENSITY = 0.5 
CO2_GAS_INTENSITY = 0.2 

def calculate_solar_geometry(latitude: float, day_of_year: int = 172):
    """
    Calculates the theoretical solar irradiance profile (0.0 to 1.0)
    based on Earth-Sun geometry for a specific Latitude.
    
    day_of_year=172 is approx June 21st (Summer Solstice).
    """
    # 1. Convert Latitude to Radians
    phi = np.radians(latitude)
    
    # 2. Solar Declination (delta) - Approx formula
    # The tilt of the earth towards the sun on this specific day
    delta = np.radians(23.45 * np.sin(2 * np.pi * (284 + day_of_year) / 365))
    
    # 3. Create Hour Range (0 to 23)
    hours = np.arange(24)
    
    # 4. Solar Hour Angle (omega)
    # 12:00 is Solar Noon (0 degrees). Earth rotates 15 degrees per hour.
    omega = np.radians(15 * (hours - 12))
    
    # 5. Calculate Solar Elevation (alpha)
    # Formula: sin(alpha) = sin(phi)*sin(delta) + cos(phi)*cos(delta)*cos(omega)
    sin_alpha = np.sin(phi) * np.sin(delta) + np.cos(phi) * np.cos(delta) * np.cos(omega)
    
    # Clip values: If sun is below horizon (sin_alpha < 0), irradiance is 0
    solar_profile = np.maximum(sin_alpha, 0)
    
    return solar_profile

def calculate_hybrid_performance(
    num_engines: int, 
    solar_mw: float, 
    battery_mwh: float,
    engine_specs: dict,
    latitude: float = 0.0 # Default to Equator if not provided
) -> dict:
    """
    Simulates a 24-hour dispatch cycle using Geospatial inputs.
    """
    
    # 1. Create Time Index
    hours = np.arange(24)
    df = pd.DataFrame(index=hours)
    df['hour'] = hours

    # 2. GEOSPATIAL SOLAR CALCULATION
    # Get the normalized curve (0.0 to ~1.0) based on location
    # Using Day 172 (June) to show best-case scenario
    irradiance_curve = calculate_solar_geometry(latitude, day_of_year=172)
    
    # Apply capacity
    df['solar_mw'] = solar_mw * irradiance_curve
    
    # 3. Battery Logic (Peak Shifting)
    discharge_power = 0
    if battery_mwh > 0:
        discharge_power = battery_mwh / 4.0 

    df['battery_mw'] = 0.0
    mask_evening = (df['hour'] >= 18) & (df['hour'] <= 21)
    df.loc[mask_evening, 'battery_mw'] = discharge_power

    # 4. Engine Dispatch
    nominal_mw = engine_specs.get("nominal_power_mw", 0)
    total_engine_capacity = num_engines * nominal_mw
    
    df['load_mw'] = BASE_LOAD_MW
    df['net_load'] = df['load_mw'] - (df['solar_mw'] + df['battery_mw'])
    df['engine_mw'] = df['net_load'].clip(lower=0, upper=total_engine_capacity)
    df['total_mw'] = df['solar_mw'] + df['engine_mw'] + df['battery_mw']

    # 5. Financials (LCOE / Capex)
    total_solar_mwh = df['solar_mw'].sum()
    total_engine_mwh = df['engine_mw'].sum()
    total_battery_mwh = df['battery_mw'].sum()
    total_gen_mwh = total_solar_mwh + total_engine_mwh + total_battery_mwh

    cost_per_kw = engine_specs.get("capex_per_kw", 800)
    capex_engine = num_engines * (nominal_mw * 1000) * cost_per_kw
    capex_solar = solar_mw * 1000 * 700       
    capex_battery = battery_mwh * 1000 * 350  
    total_capex = capex_engine + capex_solar + capex_battery

    baseline_co2 = (BASE_LOAD_MW * 24) * CO2_GRID_INTENSITY
    actual_co2 = total_engine_mwh * CO2_GAS_INTENSITY
    co2_savings = (baseline_co2 - actual_co2) * 365 

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