import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { SimulationKPIs } from '../services/api';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import Co2Icon from '@mui/icons-material/Co2';
import FlashOnIcon from '@mui/icons-material/FlashOn';

interface Props {
  kpis: SimulationKPIs | null;
}

const KPIGrid: React.FC<Props> = ({ kpis }) => {
  if (!kpis) return null;

  const items = [
    { 
      label: 'Total CAPEX', 
      value: `$${(kpis.total_capex_usd / 1000000).toFixed(1)} M`, 
      icon: <AttachMoneyIcon fontSize="large" color="success" /> 
    },
    { 
      label: 'LCOE', 
      value: `${kpis.lcoe_cents_kwh} ¢/kWh`, 
      icon: <FlashOnIcon fontSize="large" color="warning" /> 
    },
    { 
      label: 'CO2 Reduction', 
      value: `${kpis.annual_co2_savings_tons.toLocaleString()} Tons`, 
      icon: <Co2Icon fontSize="large" color="info" /> 
    },
  ];

  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      {items.map((item, index) => (
        <Grid item xs={12} md={4} key={index}>
          <Paper elevation={3} sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box>{item.icon}</Box>
            <Box>
              <Typography variant="body2" color="text.secondary">{item.label}</Typography>
              <Typography variant="h5" fontWeight="bold">{item.value}</Typography>
            </Box>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
};

export default KPIGrid;