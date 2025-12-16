import React from 'react';
import {
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Paper, Typography, Box } from '@mui/material';
import { SimulationFrame } from '../services/api';

interface Props {
  data: SimulationFrame[];
}

const EnergyChart: React.FC<Props> = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <Paper elevation={3} sx={{ p: 3, height: '400px', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h6" gutterBottom color="primary">
        24-Hour Power Generation Profile
      </Typography>
      <Box sx={{ flexGrow: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
            <XAxis dataKey="hour" label={{ value: 'Hour of Day', position: 'insideBottom', offset: -5 }} />
            <YAxis label={{ value: 'MW', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#333' }}
              formatter={(value: number) => value.toFixed(1)}
            />
            <Legend verticalAlign="top" height={36}/>
            
            {/* Generation Sources (Stacked) */}
            <Area type="monotone" dataKey="solar_mw" stackId="1" stroke="#fbc02d" fill="#fbc02d" name="Solar PV" />
            <Area type="monotone" dataKey="battery_mw" stackId="1" stroke="#4caf50" fill="#4caf50" name="Battery Disch." />
            <Area type="monotone" dataKey="engine_mw" stackId="1" stroke="#9e9e9e" fill="#757575" name="Gas Engine" />
            
            {/* Load Line */}
            <Line type="monotone" dataKey="load_mw" stroke="#ff5252" strokeWidth={2} dot={false} name="Load Demand" />
          </ComposedChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
};

export default EnergyChart;