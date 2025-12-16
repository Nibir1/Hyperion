import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// --- Types ---
export interface SimulationFrame {
  hour: number;
  solar_mw: number;
  engine_mw: number;
  battery_mw: number;
  load_mw: number;
  total_mw: number;
}

export interface SimulationKPIs {
  total_capex_usd: number;
  annual_co2_savings_tons: number;
  lcoe_cents_kwh: number;
}

export interface CalculationResponse {
  kpis: SimulationKPIs;
  charts: SimulationFrame[];
}

export interface Inputs {
  num_engines: number;
  solar_mw: number;
  battery_mwh: number;
}

// --- API Calls ---

export const fetchCalculation = async (inputs: Inputs): Promise<CalculationResponse> => {
  const response = await axios.post(`${API_URL}/calculate`, inputs);
  return response.data;
};

export const fetchProposal = async (inputs: Inputs): Promise<string> => {
  const response = await axios.post(`${API_URL}/generate-proposal`, inputs);
  return response.data.proposal_text;
};