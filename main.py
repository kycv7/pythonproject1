import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default="iframe"
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )
    
    # Asegurar que las fechas estén en formato datetime
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    # Add stock price trace
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data_specific.Date),
            y=stock_data_specific.Close.astype("float"),
            name="Share Price"
        ),
        row=1, col=1
    )

    # Add revenue trace
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data_specific.Date),
            y=revenue_data_specific.Revenue.astype("float"),
            name="Revenue"
        ),
        row=2, col=1
    )

    # Update axes
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    # Layout
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )

    # Display the graph
    fig.show()

tsla=yf.Ticker("TSLA")
tsla_data=tsla.history(period="max")
tsla_data=tsla.history(period="max")
tsla_data.head()
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNe\twork/labs/project/revenue.htm"
data=requests.get(url).text
print(data)
soup=BeautifulSoup(data,'html.parser')
datos2=pd.read_html(str(soup))
tesla_revenue=datos2[0]
tesla_revenue.columns = ["Year", "Revenue"]
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r'[,\$]', '', regex=True)
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype(float)
tesla_revenue.dropna(inplace=True)
tesla_revenue.tail(5)
gme=yf.Ticker("GME")
gme_data=gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head(5)
url2="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsN\etwork/labs/project/stock.html"
data2=requests.get(url2).text
print(data2)
soup=BeautifulSoup(data2,'html.parser')
datos3=pd.read_html(str(soup))
gme_revenue=datos3[0]
gme_revenue.columns = ["Year", "Revenue"]
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(r'[,\$]', '', regex=True)
gme_revenue["Revenue"] = gme_revenue["Revenue"].astype(float)
gme_revenue.dropna(inplace=True)
gme_revenue.tail(5)

tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
pio.renderers.default = "browser"
make_graph(tsla_data, tesla_revenue, "Tesla Stock Data and Revenue (Up to June 2021)")

gme_revenue.columns = ["Date", "Revenue"]
gme_revenue["Date"] = pd.to_datetime(gme_revenue["Date"])
make_graph(gme_data, gme_revenue, "Gme Stock Data and Revenue (Up to June 2021)")

