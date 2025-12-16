import React from 'react';
import { Paper, Typography, Slider, Box, Button, CircularProgress } from '@mui/material';
import { Inputs } from '../services/api';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import PublicIcon from '@mui/icons-material/Public'; // Globe icon for geospatial

interface Props {
  inputs: Inputs;
  setInputs: React.Dispatch<React.SetStateAction<Inputs>>;
  onGenerateProposal: () => void;
  loadingAI: boolean;
}

const ConfiguratorForm: React.FC<Props> = ({ inputs, setInputs, onGenerateProposal, loadingAI }) => {
  
  const handleChange = (name: keyof Inputs) => (event: Event, value: number | number[]) => {
    setInputs(prev => ({ ...prev, [name]: value as number }));
  };

  return (
    <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
      <Typography variant="h6" gutterBottom color="primary">
        Plant Configuration
      </Typography>
      
      {/* 1. Geospatial Input (New Feature) */}
      <Box sx={{ my: 4 }}>
        <Typography gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <PublicIcon fontSize="small" color="action" /> 
          Site Latitude ({inputs.latitude}°)
        </Typography>
        <Slider
          value={inputs.latitude}
          onChange={handleChange('latitude')}
          step={5} 
          min={-60} 
          max={60}
          valueLabelDisplay="auto"
          sx={{ color: '#2196f3' }} 
        />
        <Typography variant="caption" color="text.secondary">
          -60° (South) to 60° (North). Affects solar physics.
        </Typography>
      </Box>

      {/* 2. Engines */}
      <Box sx={{ my: 4 }}>
        <Typography gutterBottom>Industrial Gas Engine Units</Typography>
        <Slider
          value={inputs.num_engines}
          onChange={handleChange('num_engines')}
          step={1} min={0} max={10}
          valueLabelDisplay="on"
          marks
        />
      </Box>

      {/* 3. Solar */}
      <Box sx={{ my: 4 }}>
        <Typography gutterBottom>Solar Capacity (MW)</Typography>
        <Slider
          value={inputs.solar_mw}
          onChange={handleChange('solar_mw')}
          step={5} min={0} max={100}
          valueLabelDisplay="auto"
          color="secondary"
        />
      </Box>

      {/* 4. Battery */}
      <Box sx={{ my: 4 }}>
        <Typography gutterBottom>Battery Storage (MWh)</Typography>
        <Slider
          value={inputs.battery_mwh}
          onChange={handleChange('battery_mwh')}
          step={5} min={0} max={100}
          valueLabelDisplay="auto"
          sx={{ color: '#4caf50' }}
        />
      </Box>

      <Button 
        variant="contained" 
        fullWidth 
        size="large"
        startIcon={loadingAI ? <CircularProgress size={20} color="inherit"/> : <AutoAwesomeIcon />}
        onClick={onGenerateProposal}
        disabled={loadingAI}
        sx={{ mt: 2, background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)' }}
      >
        {loadingAI ? "Drafting Proposal..." : "Generate AI Proposal"}
      </Button>
    </Paper>
  );
};

export default ConfiguratorForm;