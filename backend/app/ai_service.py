"""
AI Service (LangChain + OpenAI)
-------------------------------
Generates text proposals based on simulation data.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM (GPT-4o mini is cost-effective and fast)
# It automatically looks for OPENAI_API_KEY in environment variables.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def generate_proposal_text(
    kpis: dict, 
    config: dict
) -> str:
    """
    Uses LLM to draft a sales proposal.
    """
    
    # Define the Persona and Instructions
    template = """
    You are Hyperion, a Senior Energy Sales Engineer at Wärtsilä.
    
    Your goal is to write a persuasive, technical executive summary for a client proposing a Hybrid Power Plant.
    
    CONFIGURATION:
    - Engines: {num_engines}x Wärtsilä 31SG
    - Solar Capacity: {solar_mw} MW
    - Battery Storage: {battery_mwh} MWh
    
    SIMULATION RESULTS (KPIs):
    - Total CAPEX: ${capex:,.2f}
    - Annual CO2 Savings: {co2:,.1f} Tons
    - LCOE (Levelized Cost): {lcoe} cents/kWh
    
    INSTRUCTIONS:
    1. Start with a hook about the environmental impact (CO2 savings).
    2. Explain the operational strategy: How the engines provide reliability while solar reduces fuel costs.
    3. Highlight the financial viability (LCOE).
    4. Tone: Professional, Confident, Data-Driven.
    5. Length: 1 paragraph (approx 100-150 words).
    """

    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the chain: Prompt -> Model -> Text
    chain = prompt | llm | StrOutputParser()

    # Run the chain
    result = chain.invoke({
        "num_engines": config.get("num_engines"),
        "solar_mw": config.get("solar_mw"),
        "battery_mwh": config.get("battery_mwh"),
        "capex": kpis.get("total_capex_usd"),
        "co2": kpis.get("annual_co2_savings_tons"),
        "lcoe": kpis.get("lcoe_cents_kwh")
    })

    return result