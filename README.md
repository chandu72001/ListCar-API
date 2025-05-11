
# Listcar-API

**Listcar-API** is a **FastAPI-based RESTful service** designed to extract, normalize, and serve insights from '**cars.com**'. The project provides powerful endpoints for analyzing vehicle trends, seller performance, damage impact, and supports frontend filtering with structured dropdown data. It is built with scalability, modularity, and analytical depth in mind.

## 📦 Features

-  **Listed Vehicle Details**
-  **Fuel efficiency**
-  **Seller performance statistics**
-  **Price impact from damage**
-  **Filtering metadata for UI dropdowns** (fuel types, drivetrain)
-  **Fully normalized PostgreSQL schema**
-  **Built with FastAPI** for speed and developer-friendliness


## 🧱 Architecture Overview

```bash
project/
├── main.py                           # FastAPI app entry point
├── data_scraping_pipeline.py         # Pipeline to execute data sracping and cleaning                                    
├── Scraper/                          # Webscraper
│   ├── listing_ids.py
│   └── scrape.py
├── data/
│   ├── Processed
│       └── vehicle_data_cleaned.csv  # Processed datasets ready for insertion
│   ├── raw
│       └── vehicle_data.csv          # Scraped raw data
│   ├── data_cleaning.py
│   ├── data_insertion.py
│   ├── db_connection.py              # PostgreSQL connection
│   ├── db_schema.py                  # Normalized DB schema creation (VIN as FK)
│   ├── _init_.py
├── routes/                           # Route handlers (API endpoints)
│   ├── vehicle_routes.py
│   ├── seller_routes.py
│   └── filter_routes.py
├── services/                         # Core business logic for each route
    ├── top_models_service.py
    ├── fuel_efficiency_service.py
    ├── seller_performance_service.py
    ├── damage_impact_service.py
    └── filter_options_service.py
└── requirements.txt                   # requirements file

```
## Database Design (Normalized)

- VehicleSpecs (master specs per VIN)

- Listings (individual car listings, references VIN and Seller)

- Sellers (seller metadata)




## 🚀 Setup Instructions


### 1. Clone the repo  
```bash
git clone https://github.com/yourusername/listcar-api.git
cd listcar-api

```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

```

### 3. Setup PostgreSQL  

- Create a PostgreSQL database (e.g., vehicle_data)

- Update data/db_connection.py with your credentials

### 4. Execute the Scrapper Pipeline  
```bash
python data_scraping_pipeline.py

```

### 5. Run the FastAPI  
```bash
uvicorn main:app --reload

```
- Visit http://127.0.0.1:8000/docs to explore.



## 📊 Example Endpoints

| Endpoint                        | Purpose                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| `GET /vehicles/top-models`      | List most frequently listed or high-priced car models        |
| `GET /vehicles/fuel-efficiency` | Compare MPG across car models/fuel types                     |
| `GET /sellers/performance`      | Analyze seller pricing, damage frequency, and mileage stats  |
| `GET /vehicles/damage-impact`   | Price difference between damaged and undamaged listings      |
| `GET /filters`                  | Fetch dropdown data for fuel type, drivetrain, color filters |

## 📘 Future Enhancements

- Dockerize for deployment

- OAuth2 authentication

- Admin dashboard for insights

