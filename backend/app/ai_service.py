"""
AI Service (LangChain + OpenAI)
-------------------------------
Generates technical sales proposals using OpenAI GPT-4o-mini.
Now includes Geospatial awareness and Brand Neutrality.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Initialize LLM (GPT-4o mini is cost-effective and fast)
# It automatically looks for OPENAI_API_KEY in environment variables.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

async def generate_proposal_text(
    kpis: dict,
    num_engines: int,
    solar_mw: float,
    battery_mwh: float,
    latitude: float
) -> str:
    """
    Uses LLM to draft a sales proposal with geospatial context.
    """
    
    # Define the Persona and Instructions
    # Updated to include Latitude logic and strictly forbid brand names
    template = """
    You are a Senior Energy Sales Engineer. Write a persuasive Executive Summary for a Hybrid Power Plant proposal.

    TECHNICAL CONFIGURATION:
    - Location Latitude: {latitude}° (Consider the solar irradiance impact at this latitude)
    - Generation Source: {num_engines}x Industrial Gas Engines (Reciprocating Internal Combustion Engines)
    - Renewable Source: {solar_mw} MW Solar PV
    - Energy Storage: {battery_mwh} MWh Battery Energy Storage System (BESS)

    SIMULATION FINANCIALS & PHYSICS:
    - Total CAPEX: ${capex} Million
    - Levelized Cost of Electricity (LCOE): {lcoe} cents/kWh
    - Annual CO2 Savings: {co2} Tons (compared to coal baseline)

    INSTRUCTIONS:
    1. Write 1 professional paragraph (approx. 100-150 words).
    2. Highlight how the Hybrid solution ensures reliability despite solar intermittency.
    3. Specifically mention the location's Latitude ({latitude}°). If the latitude is high (e.g., >45°), mention seasonal solar variability. If low (near 0°), mention consistent high irradiance.
    4. BRAND NEUTRALITY: Do NOT use specific brand names like Wärtsilä, MAN, or Caterpillar. Refer to the engines strictly as "Industrial Gas Engines" or "Flexible Generation".
    5. Focus on the value: Fast-start capabilities of the engines balancing the solar curve.

    Draft the proposal text now:
    """

    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the chain: Prompt -> Model -> Text
    chain = prompt | llm | StrOutputParser()

    # Format numbers for readability before sending to AI
    capex_formatted = f"{kpis['total_capex_usd'] / 1_000_000:.1f}"
    co2_formatted = f"{kpis['annual_co2_savings_tons']:,.1f}"

    # Run the chain asynchronously
    result = await chain.ainvoke({
        "num_engines": num_engines,
        "solar_mw": solar_mw,
        "battery_mwh": battery_mwh,
        "latitude": latitude,
        "capex": capex_formatted,
        "co2": co2_formatted,
        "lcoe": kpis.get("lcoe_cents_kwh")
    })

    return result