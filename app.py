import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dash_table, dcc, html

# ---------- Data ----------
df = pd.read_csv("data/sales.csv", parse_dates=["date"])
df["revenue"] = df["quantity"] * df["unit_price"]

regions = sorted(df["region"].unique())
reps = sorted(df["salesperson"].unique())


def filter_data(region_vals, rep_vals, start, end):
    d = df[df["region"].isin(region_vals or regions) & df["salesperson"].isin(rep_vals or reps)]
    if start:
        d = d[d["date"] >= pd.to_datetime(start)]
    if end:
        d = d[d["date"] <= pd.to_datetime(end)]
    return d


def kpi_card(title, value_id):
    return html.Div(
        [html.Div(title, style={"color": "#666"}), html.H2(id=value_id, style={"margin": 0})],
        style={"flex": 1, "padding": "16px", "background": "#f5f7fa",
               "borderRadius": "8px", "textAlign": "center"},
    )


# ---------- Layout ----------
app = Dash(__name__)
app.title = "Sales Dashboard"

app.layout = html.Div(
    style={"maxWidth": "1200px", "margin": "auto", "padding": "20px", "fontFamily": "sans-serif"},
    children=[
        html.H1("Sales Dashboard"),

        html.Div(style={"display": "flex", "gap": "12px", "marginBottom": "20px"}, children=[
            dcc.Dropdown(regions, multi=True, placeholder="All regions", id="region", style={"flex": 1}),
            dcc.Dropdown(reps, multi=True, placeholder="All salespeople", id="rep", style={"flex": 1}),
            dcc.DatePickerRange(
                id="dates",
                min_date_allowed=df["date"].min(),
                max_date_allowed=df["date"].max(),
                start_date=df["date"].min(),
                end_date=df["date"].max(),
            ),
        ]),

        html.Div(style={"display": "flex", "gap": "12px", "marginBottom": "20px"}, children=[
            kpi_card("Total revenue", "kpi-revenue"),
            kpi_card("Orders", "kpi-orders"),
            kpi_card("Avg order value", "kpi-aov"),
        ]),

        dcc.Graph(id="monthly"),

        html.Div(style={"display": "flex", "gap": "12px"}, children=[
            dcc.Graph(id="products", style={"flex": 1}),
            dcc.Graph(id="regions", style={"flex": 1}),
        ]),

        dcc.Graph(id="reps"),

        html.Button("Download CSV", id="download-btn"),
        dcc.Download(id="download"),
        dash_table.DataTable(
            id="table", page_size=10, sort_action="native", filter_action="native",
            style_table={"overflowX": "auto", "marginTop": "12px"},
        ),
    ],
)


# ---------- Callbacks ----------
@app.callback(
    Output("kpi-revenue", "children"),
    Output("kpi-orders", "children"),
    Output("kpi-aov", "children"),
    Output("monthly", "figure"),
    Output("products", "figure"),
    Output("regions", "figure"),
    Output("reps", "figure"),
    Output("table", "data"),
    Input("region", "value"),
    Input("rep", "value"),
    Input("dates", "start_date"),
    Input("dates", "end_date"),
)
def update(region_vals, rep_vals, start, end):
    d = filter_data(region_vals, rep_vals, start, end)

    revenue = f"${d['revenue'].sum():,.0f}"
    orders = f"{d['order_id'].nunique():,}"
    aov = f"${d['revenue'].mean():,.2f}" if len(d) else "$0.00"

    monthly = d.resample("MS", on="date")["revenue"].sum().reset_index()
    fig_monthly = px.line(monthly, x="date", y="revenue", markers=True, title="Monthly revenue")

    top = d.groupby("product")["revenue"].sum().sort_values().reset_index()
    fig_products = px.bar(top, x="revenue", y="product", orientation="h", title="Revenue by product")

    by_region = d.groupby("region")["revenue"].sum().reset_index()
    fig_regions = px.pie(by_region, names="region", values="revenue", hole=0.4, title="Revenue by region")

    by_rep = d.groupby("salesperson")["revenue"].sum().sort_values(ascending=False).reset_index()
    fig_reps = px.bar(by_rep, x="salesperson", y="revenue", title="Salesperson leaderboard")

    table = d.assign(date=d["date"].dt.strftime("%Y-%m-%d")).to_dict("records")

    return revenue, orders, aov, fig_monthly, fig_products, fig_regions, fig_reps, table


@app.callback(
    Output("download", "data"),
    Input("download-btn", "n_clicks"),
    Input("region", "value"),
    Input("rep", "value"),
    Input("dates", "start_date"),
    Input("dates", "end_date"),
    prevent_initial_call=True,
)
def download(n_clicks, region_vals, rep_vals, start, end):
    from dash import ctx
    if ctx.triggered_id != "download-btn":
        return None
    d = filter_data(region_vals, rep_vals, start, end)
    return dcc.send_data_frame(d.to_csv, "filtered_sales.csv", index=False)


if __name__ == "__main__":
    app.run(debug=True)