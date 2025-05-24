# KPI Dashboard - Software Quality Metrics & Risk Management

A React-based dashboard for monitoring software quality Key Performance Indicators (KPIs) and managing project risks in high-assurance software environments.

## Overview

This application is designed for quality assurance teams in organizations that require rigorous software quality monitoring (like aerospace, automotive, or financial services). It provides two main functionalities:

1. **KPI Evaluation Dashboard** - Visualize and evaluate software quality metrics
2. **Risk Matrix Management** - Assess and track project risks using a likelihood/impact matrix

## Features

### KPI Dashboard
- **Interactive Charts** - Line charts showing KPI trends over sprints using Chart.js
- **Real-time Status Indicators** - Color-coded status (green/red) based on target achievement
- **Metric Selection** - Dropdown to switch between different KPIs
- **Evaluation System** - Allow users to categorize metrics as valuable or not valuable
- **Justification Capture** - Text area for users to explain their metric selections

### Risk Management
- **5x5 Risk Matrix** - Visual grid showing risks plotted by likelihood and impact
- **Color-coded Severity** - Automatic color coding based on risk score
- **Risk Submission** - Add new risks from a predefined library
- **Dynamic Updates** - Real-time matrix updates when risks are added

## Supported KPIs

| Metric | Description | Target Type |
|--------|-------------|-------------|
| `defect_density` | Defects per 1000 lines of code | Lower is better |
| `test_coverage` | Percentage of code tested by automated tests | Higher is better |
| `mttd` | Mean Time to Detect defects | Lower is better |
| `injection_rate` | Frequency of defect introduction during development | Lower is better |
| `detection_rate` | Effectiveness of developers detecting their own defects | Higher is better |
| `review_efficiency` | Effectiveness of peer reviews at catching issues | Higher is better |
| `checklist_adherence` | Extent developers follow process checklists | Higher is better |

## Technology Stack

- **Frontend**: React 18 with Hooks
- **Charts**: Chart.js for data visualization
- **Styling**: CSS classes (custom styling)
- **Build**: Modern ES6+ with JSX
- **State Management**: React useState for local state

## Project Structure

```
├── App.js              # Main React component
├── style.css           # Application styles
└── index.html          # Root HTML file
```

## Key React Concepts Used

### State Management
```javascript
const [kpiData, setKpiData] = useState({});           // KPI metrics data
const [selectedKPI, setSelectedKPI] = useState('defect_density'); // Current metric
const [riskData, setRiskData] = useState([]);         // Active risks
const [selectedValuable, setSelectedValuable] = useState([]); // User selections
```

### Effects & API Integration
```javascript
useEffect(() => {
  // Fetch data from Flask backend on component mount
  fetch('/api/kpi').then(res => res.json()).then(setKpiData);
  fetch('/api/risks').then(res => res.json()).then(setRiskData);
}, []);
```

### Chart Integration
```javascript
useEffect(() => {
  // Create/update Chart.js instance when data changes
  if (chartInstance.current) chartInstance.current.destroy();
  chartInstance.current = new Chart(chartRef.current.getContext('2d'), {
    type: 'line',
    data: { /* chart configuration */ }
  });
}, [kpiData, selectedKPI]);
```

## API Endpoints

The application expects a Flask backend with the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/kpi` | Retrieve KPI data |
| GET | `/api/kpi_targets` | Retrieve KPI target values |
| GET | `/api/risks` | Retrieve active risks |
| GET | `/api/predefined_risks` | Retrieve available risk templates |
| POST | `/api/risks` | Add new risk to matrix |
| POST | `/api/feedback-submission` | Submit user evaluations |

## Data Formats

### KPI Data Structure
```json
{
  "defect_density": [2.1, 1.8, 1.5, 1.2],
  "test_coverage": [85, 87, 90, 92],
  "mttd": [4.5, 4.2, 3.8, 3.5]
}
```

### Risk Data Structure
```json
{
  "id": "RISK-001",
  "description": "Database connection timeout during peak load",
  "likelihood": 3,
  "impact": 4
}
```

## Key Functions

### Status Evaluation
```javascript
function getStatus(value, target, isHigherBetter) {
  // Determines if KPI meets target (green) or not (red)
  if (isHigherBetter) return value >= target ? 'green' : 'red';
  return value <= target ? 'green' : 'red';
}
```

### Risk Matrix Rendering
```javascript
function renderMatrix() {
  // Creates 5x5 grid and plots risks based on likelihood/impact
  const matrix = Array.from({ length: 5 }, () => Array.from({ length: 5 }, () => []));
  riskData.forEach(r => {
    matrix[r.likelihood - 1][r.impact - 1].push(r);
  });
  // Returns JSX elements for matrix visualization
}
```

### Risk Color Coding
```javascript
function getColor(likelihood, impact) {
  const score = likelihood * impact;
  if (score <= 4) return 'green';      // Low risk
  if (score <= 9) return 'yellow';     // Medium-low risk
  if (score <= 16) return 'orange';    // Medium-high risk
  return 'red';                        // High risk
}
```

## User Interactions

### KPI Evaluation Workflow
1. User selects a KPI from dropdown
2. Chart updates to show selected metric trend
3. Status indicator shows current performance vs target
4. User categorizes metrics as valuable/not valuable
5. User provides justification for selections
6. Evaluation submitted via API

### Risk Management Workflow
1. User views current risks plotted on 5x5 matrix
2. User selects risk from predefined list
3. User assigns likelihood (1-5) and impact (1-5) values
4. Risk added to matrix with appropriate color coding
5. Matrix updates dynamically to show new risk

## Installation & Setup

```bash
# Install dependencies
npm install react react-dom chart.js

# Start development server
npm start
```

## Dependencies

```json
{
  "react": "^18.0.0",
  "react-dom": "^18.0.0",
  "chart.js": "^4.0.0"
}
```

## Usage Examples

### Selecting KPIs
The dashboard starts with `defect_density` selected. Users can switch metrics using the dropdown to analyze different aspects of software quality.

### Evaluating Metrics
Users are guided by evaluation questions:
- Does this metric influence actual quality or just track activity?
- Can this metric be gamed easily?
- Does this help identify risks early or improve team behavior?

### Adding Risks
Risks are selected from a predefined library and assigned likelihood/impact scores. The system automatically:
- Plots the risk on the appropriate matrix cell
- Applies color coding based on severity
- Removes the risk from the predefined list to prevent duplicates

## Educational Context

This application is designed as a learning tool for quality assurance professionals to:
- Understand different software quality metrics
- Practice risk assessment and visualization
- Learn to distinguish between actionable and vanity metrics
- Develop skills in quality-driven decision making

## Browser Compatibility

- Modern browsers supporting ES6+
- Canvas support required for Chart.js
- Fetch API support required for backend communication