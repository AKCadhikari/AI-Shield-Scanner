import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css'; // Make sure your Tailwind CSS is imported here
import App from './App'; // Or whatever you named your main component file

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);