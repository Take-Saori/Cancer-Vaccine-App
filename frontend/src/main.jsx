import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import React from 'react'
import ReactDOM from 'react-dom/client'
import ResearcherPage from './Components/ResearcherPage/index.jsx'
// refer here for bootstrap theme: https://bootswatch.com/zephyr/
import './bootstrap.min.css';


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ResearcherPage />
  </React.StrictMode>,
)

