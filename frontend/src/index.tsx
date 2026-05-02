import React from 'react';
import ReactDOM from 'react-dom/client';

// 1. IBM Plex font (loaded first so all subsequent styles inherit it)
import '@ibm/plex/css/ibm-plex.css';

// 2. Carbon Design System defaults
import '@carbon/styles/css/styles.css';

// 3. ProcessDoctor design tokens (override Carbon where needed)
import './styles/global.css';

import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
