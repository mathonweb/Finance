import configparser

import pandas as pd
import pdfkit
import matplotlib.pyplot as plt

from finance.utils.s3_client import get_file, send_file


class Figures:
    def __init__(self):
        self._annual_total_return = self._get_annual_total_return()

    def _get_annual_total_return(self):
        config = configparser.ConfigParser()
        config.read_file(open('config.ini'))

        filename = get_file(config['DEFAULT']['annual_returns_file'])
        return pd.read_csv(filename)

    def create_annual_return_graph(self):
        plt.style.use("bmh")
        fig, ax = plt.subplots()
        ax.plot(self._annual_total_return["Year"], self._annual_total_return["Total return %"], marker="o")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total return %")
        fig.savefig("total_return.png")

    def create_annual_return_table(self):
        return self._annual_total_return.pivot_table(columns="Year").to_html()


class Report:
    def __init__(self):
        self.figures = Figures()

    def create_report(self):

        f = open("financial_report.html", "w")

        report = "<html>" + \
                 " <head> <title>Rapport de finance</title> </head>" + \
                 " <body> <h2>Performance</h2>" + \
                 " <body> <h3>Annual Total Return</h3>" + \
                 self.figures.create_annual_return_table() + \
                 "<img src="'total_return.png'">" + \
                 "</body>" + \
                 "</html>"

        f.write(report)

        f.close()

        self.figures.create_annual_return_graph()

        pdfkit.from_file("financial_report.html", "financial_report.pdf")

    def send_report(self):
        send_file("financial_report.html")
        send_file("financial_report.pdf")


if __name__ == '__main__':

    report = Report()
    report.create_report()
    report.send_report()
