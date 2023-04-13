from matplotlib import pyplot as plt


class ChartDisplay:
    def __init__(self, window_title, x_label, y_label, data_period):
        self.window_title = window_title
        self.x_label = x_label
        self.y_label = y_label
        self.data_period_value = [float(n[0]) for n in data_period]
        self.data_period = [n[1] for n in data_period]

    def bar_line_chart(self):
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
        ax1.plot(self.data_period, self.data_period_value, marker="o", linewidth=2)
        ax2.bar(self.data_period, self.data_period_value, width=0.5)
        ax1.grid(True), ax2.grid(True)
        ax1.fill_between(self.data_period, self.data_period_value)
        ax1.set_ylabel(self.y_label.upper()), ax2.set_ylabel(self.y_label.upper()), ax2.set_xlabel(self.x_label.upper())
        plt.xticks(rotation=90)
        plt.get_current_fig_manager().set_window_title(self.window_title)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    from db import DB
    mdb = DB()
    chart_year = ChartDisplay("Chart Year", "Year", "Expenses", mdb.read_total_expenses_year())
    chart_month_year = ChartDisplay("Chart Month", "Month", "Expenses", mdb.read_total_expenses_month_per_year(2022))
    chart_cat_month_year = ChartDisplay("Chart Month", "Month", "Expenses",
                                        mdb.read_expenses_month_per_year_by_category(11, 2022))
    chart_category = ChartDisplay("Chart Category", "Category", "Expenses", mdb.read_total_expenses_by_category())

    # chart_year.bar_line_chart()
    # chart_month_year.bar_line_chart()
    chart_category.bar_line_chart()
    # chart_cat_month_year.bar_line_chart()
    # chart_category.bar_chart()

    # chart_month = ChartMonth(2022)
    # chart_month.bar_chart("Expenses per month")
    # chart_month.line_chart("Expenses per month")
    # print(chart_month.data_period_value)
    # print(chart_month.data_period)
    # chart_month.bar_line_chart()

    # char_day = ChartDay()
    # char_day.bar_chart("Expense per category - month, year")
    # char_day.line_chart("Expense per category - month, year")
    # char_day.bar_line_chart("Expense per category - month, year")
    # char_day.bar_line_chart()

    # import gui_main_window
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # SecondaryWindow = QtWidgets.QMainWindow()
    # ui = gui_main_window.ReadFromDB().display_table_expenses_all_columns_fixed()
    # # ui.setupUi(SecondaryWindow)
    # SecondaryWindow.show()
    # sys.exit(app.exec_())
