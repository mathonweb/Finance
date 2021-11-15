from fpdf import FPDF


class Report:
    def __init__(self):
        self._report = None

    def create_template_report(self):
        self._report = FPDF(orientation='P', unit='mm', format='A4')
        self._report.add_page()
        self._report.set_font("Arial", "B", 16)
        self._report.cell(40, 10, "Hello World !")
        self._report.output("financial_report.pdf", "F")


if __name__ == '__main__':
    report = Report()
    report.create_template_report()
