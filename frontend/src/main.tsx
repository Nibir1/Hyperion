import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

// ----------------------------------------------------------------------------
// Theme Configuration
// Energy Industry Style (Clean, Industrial, Orange Accents)
// ----------------------------------------------------------------------------
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff9800', // Industrial Orange
    },
    secondary: {
      main: '#2196f3', // Blue for Solar/Wind
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)