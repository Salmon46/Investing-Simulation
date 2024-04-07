from flet import *
from config import *
import plotly.graph_objects as go
from dash import *
from flet.plotly_chart import PlotlyChart

class Search_Result:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.close_price = ticker_lookup(ticker)
    
    def insert_values(self, list):
        list.append(
            DataRow(
                cells=[
                    DataCell(Text(value=self.ticker)),
                    DataCell(Text(value=f"${self.close_price}"))
                ]
            )
        )

    

def main(page: Page) -> None:
    page.title = 'Investing Simulation'

    """Home Page Config"""
    title = Text(value="Welcome to your Investing Simulation!", color="green", theme_style=TextThemeStyle.DISPLAY_LARGE, font_family='Aharoni')

    go_to_portfolio_button = FilledTonalButton(text="View Portfolio", on_click=lambda _:page.go('/Portfolio'))

    intro_page= Row(
        [
            Column(
                [
                    title,
                    go_to_portfolio_button
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
        ],
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=VerticalAlignment.CENTER
    )


    """Portfolio Page Config"""
    portfolio_title = Text(value="Your Portfolio", color="white", theme_style=TextThemeStyle.HEADLINE_LARGE, font_family='Aptos Black')


    def make_pie_chart():
        investments = retrieve_values()

        tickers = []
        investment_values = []

        for investment in investments:
            tickers.append(f"{investment[0]} ({investment[1]})")
            investment_values.append(investment[2])

        fig = go.Figure(data=[go.Pie(labels=tickers, values=investment_values)])
        fig.update_layout(plot_bgcolor="#000000")

        return PlotlyChart(fig, expand=True)
    
    pie_chart = make_pie_chart()


    ticker_field = TextField(label="Ticker", width=90)
    shares_field = TextField(label="Shares", width=90)
    ticker_field2 = TextField(label="Ticker", width=90)
    shares_field2 = TextField(label="Shares", width=90)

    def on_buy(e):
        ticker = str(ticker_field.value)
        shares = float(shares_field.value)
        buy(ticker, shares)
        portfolio_update()
        time.sleep(5)
        pie_Chart = make_pie_chart()
        page.update()

    def on_sell(e):
        ticker2 = str(ticker_field2.value)
        shares2 = float(shares_field2.value)
        sell(ticker2, shares2)
        portfolio_update()
        time.sleep(5)
        pie_chart = make_pie_chart()
        page.update()

    buy_button = FilledTonalButton(text="Buy", on_click=on_buy)
    go_to_search_page_button = FilledTonalButton(text="Search a ticker", on_click=lambda _:page.go('/Search'))
    sell_button = FilledTonalButton(text="Sell", on_click=on_sell)
    go_to_home_button = FilledTonalButton(text="Go to home", on_click=lambda _:page.go('/'))

    buy_container = Container(
        Column(
            [
                ticker_field,
                shares_field,
                buy_button,
                go_to_search_page_button
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
    )

    sell_container = Container(
        Column(
            [
                ticker_field2,
                shares_field2,
                sell_button,
                go_to_home_button
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
    )

    investments = retrieve_values()
    investment_worth = 0
    for investment in investments:
        investment_worth = investment_worth + investment[2]
    portfolio_value_display = Text(value=f"Value: ${investment_worth}", color='white', theme_style=TextThemeStyle.HEADLINE_SMALL, font_family='Aptos Black')
    

    portfolio_page = Row(
        [
            buy_container,
            Column(
                [
                    portfolio_title,
                    pie_chart,
                    portfolio_value_display
                ],
                alignment=MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=CrossAxisAlignment.CENTER
            ), 
            sell_container,
        ],
        expand=True,
        alignment=MainAxisAlignment.SPACE_AROUND,
        vertical_alignment=CrossAxisAlignment.CENTER
    )


    """Search Result Page Config"""
    search_box = TextField(label="Enter the ticker of the stock your would like to look up", width=360)

    table_values = []
    table = Container(
        content=DataTable(
            columns=[
                DataColumn(Text(value="Ticker")),
                DataColumn(Text(value="Last Close Price"), numeric=True)
            ],
            rows=table_values,
        ),
        width=450
    )
    def on_search(e):
        search_result = Search_Result(search_box.value)
        table_values.clear()
        search_result.insert_values(table_values)
        page.update()
    search_button = FilledTonalButton(text="Search", on_click=on_search)

    search_result_page = Column(
        [
            Row(
                [
                    go_to_portfolio_button,
                    search_box,
                    search_button
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER
            ),
            table
        ],
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        """Home Page"""
        page.views.append(
            View(
                route='/',
                controls=[
                    intro_page
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )

        """Portfolio Page"""
        if page.route == '/Portfolio':
            page.views.append(
            View(
                route='/Portfolio',
                controls=[
                    portfolio_page
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )
            
        if page.route == '/Search':
            page.views.append(
                View(
                    route='/Search',
                    controls=[
                        search_result_page
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == '__main__':
    app(main)