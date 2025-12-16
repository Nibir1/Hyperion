import { useEffect, useState } from 'react';
import { Container, Typography, Box, Paper, Chip } from '@mui/material';
import axios from 'axios';

// Interface for API Health Response
interface HealthStatus {
  status: string;
  modules: {
    pandas: string;
    sqlalchemy: string;
  }
}

function App() {
  const [backendStatus, setBackendStatus] = useState<string>('Connecting...');
  const [pandasVer, setPandasVer] = useState<string>('-');

  useEffect(() => {
    // Attempt to handshake with the backend
    const checkHealth = async () => {
      try {
        const response = await axios.get<HealthStatus>('http://localhost:8000/health');
        setBackendStatus(response.data.status);
        setPandasVer(response.data.modules.pandas);
      } catch (error) {
        setBackendStatus('Offline');
        console.error("Backend connection failed", error);
      }
    };

    checkHealth();
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          HYPERION
        </Typography>
        <Typography variant="h5" color="text.secondary" gutterBottom>
          Hybrid Energy Configurator
        </Typography>
        
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', gap: 2 }}>
          <Chip 
            label={`Backend: ${backendStatus.toUpperCase()}`} 
            color={backendStatus === 'healthy' ? 'success' : 'error'} 
          />
          <Chip 
            label={`Pandas Engine: v${pandasVer}`} 
            variant="outlined" 
          />
        </Box>
      </Paper>
    </Container>
  );
}

export default App;