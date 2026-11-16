##### Sales Dashboard ######

Hello!!!!


## Structure
```
sales_dashboard/
├── app.py
├── generate_data.py
├── requirements.txt
└── data/
    └── sales.csv
```

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install dash pandas plotly numpy
mkdir data
python generate_data.py
python app.py
```
Mac/Linux activate: `source venv/bin/activate`

Open http://127.0.0.1:8050     "Make sure the address is entered correctly!"

## Your Own Data 
"I have provided a sample csv data file replace it with yours!"
Use a CSV with these columns:
`order_id, date, product, region, salesperson, quantity, unit_price`

## Stack
Python, Dash, pandas, Plotly, NumPy

## Roadmap
- Period-over-period KPIs
- File upload
- Forecasting
- Database and login
