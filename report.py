import pandas as pd

from utils.s3_client import get_file, send_file


class Figures:
    def __init__(self):
        self._annual_total_return = self._get_annual_total_return()

    def _get_annual_total_return(self):
        filename = get_file("annual_total_return.csv")
        return pd.read_csv(filename)

    def create_annual_return_graph(self):
        pass

    def create_annual_return_table(self):
        return self._annual_total_return.to_html(index=False)


class Report:
    def __init__(self):
        self.figures = Figures()

    def create_report(self):

        f = open("financial_report.html", "w")

        report = "<html>" + \
                 " <head> <title>Rapport de finance</title> </head>" +\
                 " <body> <h2>Annual Total Return</h2>" + \
                 self.figures.create_annual_return_table() + \
                 "</body>" + \
                 "</html>"

        f.write(report)

        f.close()

    def send_report(self):
        send_file("financial_report.html")


if __name__ == '__main__':

    report = Report()
    report.create_report()
    report.send_report()
