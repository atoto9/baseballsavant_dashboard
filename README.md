# Baseball Pitcher Visualization Dashboard

This project visualizes baseball data from the 2024 WBCQ, structured into several components:

## Project Overview

### 1. Data Scraping
Extracted baseball statistics from **Chinese Taipei VS South Africa (2/22/2025)** game data on Baseball Savant. Since the website only provides summary statistics without pitch-by-pitch logs, we focused on gathering statistical data. The extraction process combined Chrome Developer Tools and GPT to scrape data from the webpage and save it in CSV format.

*Note: For large-scale data extraction, Airflow DAGs and comprehensive scraping scripts would be necessary. This component is simplified for demonstration purposes.*

### 2. Data Storage
Designed a data warehouse and database architecture divided into ODS/DWS/ADS layers with a simplified ER model. Since Baseball Savant provides only statistical results, the ODS/DWS tables were created as simulations without actual data. However, DDL SQL statements were prepared, and the scraped CSV data was imported into the database.

### 3. Data Dashboard
Implemented data visualization using Python Dash. The core dashboard code was provided by GPT, with experience-based adjustments to components like database connection methods and logging content. While GPT provided sample data integration, we modified the implementation to connect directly to PostgreSQL queries.

### 4. Service Deployment
Utilized Docker and Docker Compose for service deployment, with Python package management through requirements.txt.

## Deployment Steps

```bash
git clone https://xxxx.git
cd baseballsavant_dashboard
docker-compose up -d --build
```

## Database ER Model
![Database ER Model](https://github.com/atoto9/baseballsavant_dashboard/blob/main/img/database.drawio.png)

## Dashboard Template
![Dashboard Template](https://github.com/atoto9/baseballsavant_dashboard/blob/main/img/dashboard.png)


## Technical Stack

- **Frontend**: Dash, Plotly
- **Backend**: Python, Flask (via Dash)
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: Chrome DevTools, GPT-assisted extraction

## Features

- Pitch type distribution analysis
- Velocity vs. hard-hit rate visualization
- Batting results analysis
- Detailed pitcher statistics table
- Team-based filtering
- Pitch count range selection

## Future Enhancements

- Implement comprehensive data scraping pipeline with Airflow
- Add pitch-by-pitch analysis when data becomes available
- Expand dashboard with additional visualization components
- Implement user authentication for data access control
- Add historical data comparison features
