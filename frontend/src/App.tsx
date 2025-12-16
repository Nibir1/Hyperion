import { useEffect, useState, useCallback } from 'react';
import { Container, Grid, Typography, Box, Alert, Fade } from '@mui/material';
import ConfiguratorForm from './components/ConfiguratorForm';
import EnergyChart from './components/EnergyChart';
import KPIGrid from './components/KPIGrid';
import { Inputs, SimulationKPIs, SimulationFrame, fetchCalculation, fetchProposal } from './services/api';

function App() {
  // --- State ---
  const [inputs, setInputs] = useState<Inputs>({
    num_engines: 4,
    solar_mw: 20,
    battery_mwh: 10
  });

  const [charts, setCharts] = useState<SimulationFrame[]>([]);
  const [kpis, setKpis] = useState<SimulationKPIs | null>(null);
  const [proposal, setProposal] = useState<string>("");
  const [loadingAI, setLoadingAI] = useState(false);

  // --- Logic ---
  
  // 1. Auto-Calculate whenever inputs change (Debounced slightly in real apps, direct here)
  const runSimulation = useCallback(async () => {
    try {
      const data = await fetchCalculation(inputs);
      setCharts(data.charts);
      setKpis(data.kpis);
    } catch (error) {
      console.error("Simulation failed:", error);
    }
  }, [inputs]);

  // Run simulation on mount and when inputs change
  useEffect(() => {
    const timer = setTimeout(() => {
      runSimulation();
    }, 300); // 300ms debounce to prevent API spam while sliding
    return () => clearTimeout(timer);
  }, [inputs, runSimulation]);

  // 2. AI Proposal Generation
  const handleGenerateProposal = async () => {
    setLoadingAI(true);
    setProposal("");
    try {
      const text = await fetchProposal(inputs);
      setProposal(text);
    } catch (error) {
      console.error("AI generation failed:", error);
    } finally {
      setLoadingAI(false);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
        <img src="/logo.svg" alt="logo" style={{ width: 50, backgroundColor: "#000000ff", filter: "invert(1)", }} />
        <Typography variant="h4" component="h1" fontWeight="bold" sx={{ letterSpacing: 1 }}>
          HYPERION <span style={{ color: '#ff9800', fontSize: '0.6em' }}>CONFIGURATOR</span>
        </Typography>
      </Box>

      <Grid container spacing={3}>
        
        {/* Left Column: Configurator */}
        <Grid item xs={12} md={3}>
          <ConfiguratorForm 
            inputs={inputs} 
            setInputs={setInputs} 
            onGenerateProposal={handleGenerateProposal}
            loadingAI={loadingAI}
          />
        </Grid>

        {/* Right Column: Visuals & Data */}
        <Grid item xs={12} md={9}>
          {/* KPIs */}
          <KPIGrid kpis={kpis} />

          {/* Chart */}
          <EnergyChart data={charts} />

          {/* AI Proposal Result */}
          {proposal && (
            <Fade in={true}>
              <Alert 
                severity="info" 
                icon={<AutoAwesomeIcon />}
                sx={{ mt: 3, '& .MuiAlert-message': { width: '100%' } }}
              >
                <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                  AI Generated Proposal
                </Typography>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                  {proposal}
                </Typography>
              </Alert>
            </Fade>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

// Icon for the Alert (needed since we used it in JSX)
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

export default App;