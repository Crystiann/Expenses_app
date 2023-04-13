from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QDialog
from PyQt5 import QtGui, QtWidgets, QtCore
import db
import chart
import data


class GuiMainWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.read_from_db = ReadFromDB().show
        self.operations_db = OperationsDB().show
        self.display_calendar = CalendarDisplay("Calendar", "green", "Clock").show

        self.setWindowTitle(self.title)
        self.resize(405, 266)
        self.central_widget = QtWidgets.QWidget(self)

        self.gridLayout_3 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout = QtWidgets.QGridLayout()

        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 383, 221))

        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 363, 177))

        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)

        self.psb_read_from_db = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.psb_read_from_db.setText("READ FROM DB")
        self.gridLayout_4.addWidget(self.psb_read_from_db, 1, 0, 1, 1)
        self.psb_read_from_db.clicked.connect(self.read_from_db)

        self.psb_operations_db = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.psb_operations_db.setText("OPERATIONS DB")
        self.gridLayout_4.addWidget(self.psb_operations_db, 3, 0, 1, 1)
        self.psb_operations_db.clicked.connect(self.operations_db)

        self.psb_calendar = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.psb_calendar.setText("CALENDAR")
        self.gridLayout_4.addWidget(self.psb_calendar, 4, 0, 1, 1)
        self.psb_calendar.clicked.connect(self.display_calendar)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.addWidget(self.scrollArea_2, 1, 0, 1, 1)
        self.label_current_db = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_current_db.setText(f"{db.DB().db_name} database is connected")
        self.gridLayout_2.addWidget(self.label_current_db, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.setCentralWidget(self.central_widget)


class OperationsDB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mdb = db.DB()
        self.insert_value_to_db = InsertUpdateFourToDB(
            "Insert New Value To Expenses",
            f"Existing categories to choose from:\nFixed Expenses:\n{' / '.join(self.mdb.display_categories('fixed'))}\n",
            "Value(use numeric)", "Category", "Type: fixed or not_fixed", "Description",
            f"Not Fixed Expenses:\n{' / '.join(self.mdb.display_categories('not_fixed'))}",
            self.mdb.insert_new_expense).show

        self.delete_expense_not_fixed = InsertUpdateFourToDB(
            "Delete Expense", "", "Value(use numeric)", "Category", "Type: fixed or not_fixed", "Date(DD-MM-YYY)", "",
            self.mdb.delete_expense).show

        self.update_value = InsertUpdateFourToDB(
            "Update Value For Existing Expense", "", "Existing Value", "Category", "Date(DD-MM-YYY)", "New Value", "",
            self.mdb.update_value).show

        self.update_category_name = InsertUpdateFourToDB(
            "Update Category Name",
            f"Existing categories to choose from:\nFixed Expenses:\n{' / '.join(self.mdb.display_categories('fixed'))}\n",
            "Value", "Existing Category", "Date(DD-MM-YYY)", "New Category",
            f"Not Fixed Expenses:\n{' / '.join(self.mdb.display_categories('not_fixed'))}",
            self.mdb.update_category_name).show

        self.update_description = InsertUpdateFourToDB(
            "Update Description",
            f"Existing categories to choose from:\nFixed Expenses:\n{' / '.join(self.mdb.display_categories('fixed'))}\n",
            "Value(use numeric)", "Category", "Date", "New Description",
            f"Not Fixed Expenses:\n{' / '.join(self.mdb.display_categories('not_fixed'))}",
            self.mdb.update_expense_description).show

        self.update_date = InsertUpdateFourToDB(
            "Change Date",
            f"Existing categories to choose from:\nFixed Expenses:\n{' / '.join(self.mdb.display_categories('fixed'))}\n",
            "Value", "Category", "Date(DD-MM-YYY)", "New Date(DD-MM-YYY)",
            f"Not Fixed Expenses:\n{' / '.join(self.mdb.display_categories('not_fixed'))}",
            self.mdb.update_date).show

        self.update_type = InsertUpdateFourToDB(
            "Change Expense Type", "Choose Between:", "Existing Type", "Category", "Date", "New Type",
            "- Fixed\n- Not_Fixed",
            self.mdb.update_category_type).show

        self.setWindowTitle("Operations")
        self.central_widget = QtWidgets.QWidget(self)

        self.gridLayout_3 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)

        self.psb_insert_new_expense = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_insert_new_expense, 0, 0, 1, 1)
        self.psb_insert_new_expense.setText("Insert New Expense")
        self.psb_insert_new_expense.clicked.connect(self.insert_value_to_db)

        self.psb_delete_expense = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_delete_expense, 0, 1, 1, 1)
        self.psb_delete_expense.setText("Delete expense")
        self.psb_delete_expense.clicked.connect(self.delete_expense_not_fixed)

        self.psb_update_value = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_update_value, 0, 2, 1, 1)
        self.psb_update_value.setText("Update Value Expenses")
        self.psb_update_value.clicked.connect(self.update_value)

        self.psb_update_category_name = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_update_category_name, 2, 0, 1, 1)
        self.psb_update_category_name.setText("Update Category Name")
        self.psb_update_category_name.clicked.connect(self.update_category_name)

        self.psb_update_description = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_update_description, 2, 1, 1, 1)
        self.psb_update_description.setText("Update Description Not Fixed")
        self.psb_update_description.clicked.connect(self.update_description)

        self.psb_update_date = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_update_date, 2, 2, 1, 1)
        self.psb_update_date.setText("Update Date")
        self.psb_update_date.clicked.connect(self.update_date)

        self.psb_update_type = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.psb_update_type, 3, 0, 1, 1)
        self.psb_update_type.setText("Update Type")
        self.psb_update_type.clicked.connect(self.update_type)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.addWidget(self.scrollArea_2, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.setCentralWidget(self.central_widget)


class ReadFromDB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mdb = db.DB()
        self.table_display_all_expenses = DisplayTable("Table All Expenses", 5,
                                                       self.mdb.read_all_expenses(),
                                                       "Value", "Category", "Type", "Description", "Date").show
        self.table_display_fixed = DisplayTable("Table All Expenses Fixed", 5,
                                                self.mdb.read_all_expenses_by_type("fixed"),
                                                "Value", "Category", "Type", "Description", "Date").show
        self.table_exp_in_month_in_year = InsertDisplayTableTwo(
            "Expenses In A Month In An Year", 5, "", "",
            self.mdb.read_all_expenses_in_month_per_year, "Month", "Year",
            val="Value", cat="Category", type="Type", description="Description", date="Date").show

        self.table_exp_by_date = InsertDisplayTable(
            "Insert Date", "Expenses By Date", 5, "Use following format for date:", "DD-MM-YYYY",
            self.mdb.read_expenses_by_date, "Date",
            val="Value", cat="Category", type="Type", des="Description", date="Date").show
        self.table_exp_cat_month = InsertDisplayTableTwo(
            "Insert month and year", 4, "", "",
            self.mdb.read_expenses_month_per_year_by_category, "Month", "Year",
            val="Value", cat="Category", type="Type", month="Month", year="Year").show
        self.chart_exp_cat_month = InsertDisplayChartTwo("Insert month and year", "", "Month", "Year", "", "Category",
                                                         "Values",
                                                         self.mdb.read_expenses_month_per_year_by_category).show
        self.table_exp_cat_year = InsertDisplayTable("Insert year", "Expenses By Category Per Year", 2, "", "",
                                                     self.mdb.read_expenses_per_year_by_category, "Year",
                                                     val="Value", cat="Category").show
        self.chart_exp_cat_year = InsertDisplayChart("Insert year", "", "Year", "", "Category", "Values",
                                                     self.mdb.read_expenses_per_year_by_category).show
        self.table_display_total_category = DisplayTable("Total Expenses Per Category", 2,
                                                         self.mdb.read_total_expenses_by_category(),
                                                         "Value", "Category").show
        self.chart_total_category = chart.ChartDisplay("Chart Total Expenses Per Category", "Category", "Values",
                                                       self.mdb.read_total_expenses_by_category())
        self.table_exp_month_year = InsertDisplayTable("Insert year", "Expenses By Month Per Year", 2, "", "",
                                                       self.mdb.read_total_expenses_month_per_year, "Year",
                                                       val="Value", cat="Month").show
        self.chart_exp_month_year = InsertDisplayChart("Insert year", "", "Year", "", "Category", "Values",
                                                       self.mdb.read_total_expenses_month_per_year).show
        self.table_display_total_year = DisplayTable("Table Total Expenses Per Year", 2,
                                                     self.mdb.read_total_expenses_year(),
                                                     "Value", "Year").show
        self.chart_total_year = chart.ChartDisplay("Chart Total Expenses Per Year", "Year", "Values",
                                                   self.mdb.read_total_expenses_year())

        self.setWindowTitle("Display Expenses")
        self.central_widget = QtWidgets.QWidget(self)

        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.VLine)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_1_display_expenses = QtWidgets.QGridLayout()
        self.gridLayout_2_display_expenses = QtWidgets.QGridLayout()

        self.psb_table_all_expenses = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_1_display_expenses.addWidget(self.psb_table_all_expenses, 0, 1, 1, 1)
        self.psb_table_all_expenses.setText("Table All Expenses")
        self.psb_table_all_expenses.clicked.connect(self.table_display_all_expenses)

        self.psb_table_fixed = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_1_display_expenses.addWidget(self.psb_table_fixed, 1, 1, 1, 1)
        self.psb_table_fixed.setText("Table Fixed")
        self.psb_table_fixed.clicked.connect(self.table_display_fixed)

        self.psb_exp_in_month_in_year = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_1_display_expenses.addWidget(self.psb_exp_in_month_in_year, 2, 1, 1, 1)
        self.psb_exp_in_month_in_year.setText("Expense in a month")
        self.psb_exp_in_month_in_year.clicked.connect(self.table_exp_in_month_in_year)

        self.psb_exp_by_date = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_1_display_expenses.addWidget(self.psb_exp_by_date, 3, 1, 1, 1)
        self.psb_exp_by_date.setText("Expenses By Date")
        self.psb_exp_by_date.clicked.connect(self.table_exp_by_date)

        self.psb_exp_cat_month_year_table = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_exp_cat_month_year_table, 2, 0, 1, 1)
        self.psb_exp_cat_month_year_table.setText("Expenses Per Category Per Month In An Year")
        self.psb_exp_cat_month_year_table.clicked.connect(self.table_exp_cat_month)

        self.psb_exp_cat_month_year_chart = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_exp_cat_month_year_chart, 2, 1, 1, 1)
        self.psb_exp_cat_month_year_chart.setText("Expenses Per Category Per Month In An Year")
        self.psb_exp_cat_month_year_chart.clicked.connect(self.chart_exp_cat_month)

        self.psb_exp_cat_year_table = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_exp_cat_year_table, 6, 0, 1, 1)
        self.psb_exp_cat_year_table.setText("Expenses Per Category In An Year")
        self.psb_exp_cat_year_table.clicked.connect(self.table_exp_cat_year)

        self.psb_exp_cat_year_chart = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_exp_cat_year_chart, 6, 1, 1, 1)
        self.psb_exp_cat_year_chart.setText("Expenses Per Category In An Year")
        self.psb_exp_cat_year_chart.clicked.connect(self.chart_exp_cat_year)

        self.psb_total_exp_cat_table = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_total_exp_cat_table, 7, 0, 1, 1)
        self.psb_total_exp_cat_table.setText("Total Expenses Per Category")
        self.psb_total_exp_cat_table.clicked.connect(self.table_display_total_category)

        self.psb_total_exp_cat_chart = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_total_exp_cat_chart, 7, 1, 1, 1)
        self.psb_total_exp_cat_chart.setText("Total Expenses Per Category")
        self.psb_total_exp_cat_chart.clicked.connect(self.chart_total_category.bar_line_chart)

        self.psb_total_exp_month_year_table = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_total_exp_month_year_table, 8, 0, 1, 1)
        self.psb_total_exp_month_year_table.setText("Total Expenses  Per Month In An Year")
        self.psb_total_exp_month_year_table.clicked.connect(self.table_exp_month_year)

        self.psb_total_exp_month_year_chart = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_total_exp_month_year_chart, 8, 1, 1, 1)
        self.psb_total_exp_month_year_chart.setText("Total Expenses  Per Month In An Year")
        self.psb_total_exp_month_year_chart.clicked.connect(self.chart_exp_month_year)

        self.psb_total_exp_year_table = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_total_exp_year_table, 9, 0, 1, 1)
        self.psb_total_exp_year_table.setText("Total Expenses Per Year")
        self.psb_total_exp_year_table.clicked.connect(self.table_display_total_year)

        self.psb_total_exp_year_chart = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.gridLayout_2_display_expenses.addWidget(self.psb_total_exp_year_chart, 9, 1, 1, 1)
        self.psb_total_exp_year_chart.setText("Total Expenses Per Year")
        self.psb_total_exp_year_chart.clicked.connect(self.chart_total_year.bar_line_chart)

        self.display_exp_label_table = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.display_exp_label_table.setTextFormat(QtCore.Qt.AutoText)
        self.display_exp_label_table.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2_display_expenses.addWidget(self.display_exp_label_table, 1, 0, 1, 1)
        self.display_exp_label_table.setText("Table")

        self.display_exp_label_chart = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.display_exp_label_chart.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2_display_expenses.addWidget(self.display_exp_label_chart, 1, 1, 1, 1)
        self.display_exp_label_chart.setText("Chart")

        self.gridLayout_1_display_expenses.addLayout(self.gridLayout_2_display_expenses, 4, 1, 1, 1)

        self.display_total_expenses_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.gridLayout_1_display_expenses.addWidget(self.display_total_expenses_label, 5, 1, 1, 1)
        self.display_total_expenses_label.setText(
            f"TOTAL EXPENSES FROM {self.mdb.read_earliest_latest_years()[0]} to "
            f"{self.mdb.read_earliest_latest_years()[-1]} are {self.mdb.total_value_expenses()} EUR")

        self.gridLayout.addLayout(self.gridLayout_1_display_expenses, 0, 0, 2, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.setCentralWidget(self.central_widget)


class InsertDisplayTable(QDialog):
    def __init__(self, title_insert, title_display, columns_number, label_name, label_data, item_data, *args, **kwargs):
        super().__init__()
        self.title_insert = title_insert
        self.title_display = title_display
        self.label_name = label_name
        self.label_data = label_data
        self.item_data = item_data
        self.columns_number = columns_number

        self.item_list_args = [n for n in args]
        self.item_list_kwargs = [n[1] for n in kwargs.items()]
        self.tableMainCentralWidget = QtWidgets.QMainWindow()
        self.tableCentralWidget = QtWidgets.QWidget(self.tableMainCentralWidget)
        self.tableVerticalLayout = QtWidgets.QVBoxLayout(self.tableCentralWidget)
        self.tableWidget = QtWidgets.QTableWidget(self.tableCentralWidget)

        self.setWindowTitle(self.title_insert)
        self.btn = QPushButton("Commit")
        self.display_item = self.label_data
        self.label_item = QtWidgets.QLabel(self)

        vbox = QVBoxLayout()

        for val in self.item_list_args:
            self.item_1 = QLineEdit()
            self.item_1.setPlaceholderText(val)
            self.item_1.setFont(QtGui.QFont("Arial", 15))
            vbox.addWidget(self.item_1)

        self.label_item.setText(f"{self.label_name}\n{self.display_item}")
        vbox.addWidget(self.label_item)

        self.btn.setFont(QtGui.QFont("Arial", 10))
        self.btn.clicked.connect(self.display_table)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def display_table(self):
        self.tableMainCentralWidget.setWindowTitle(f"{self.item_1.text()}")
        self.tableWidget.setColumnCount(self.columns_number)

        for i, val in enumerate(self.item_list_kwargs):
            item_2 = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item_2)
            item_2.setText(val)

        self.tableVerticalLayout.addWidget(self.tableWidget)
        self.tableMainCentralWidget.setCentralWidget(self.tableCentralWidget)

        self.tableWidget.setRowCount(0)

        for row in self.item_data(self.item_1.text()):
            self.tableWidget.insertRow(0)
            for column in range(self.columns_number):
                self.tableWidget.setItem(0, column, QtWidgets.QTableWidgetItem(row[column]))
        self.close()
        self.tableMainCentralWidget.show()


class InsertDisplayTableTwo(QDialog):
    def __init__(self, title_insert, columns_number, label_name, label_data, item_data, *args, **kwargs):
        super().__init__()
        self.title_insert = title_insert
        self.label_name = label_name
        self.label_data = label_data
        self.item_data = item_data
        self.columns_number = columns_number

        self.item_list_args = [n for n in args]
        self.item_list_kwargs = [n[1] for n in kwargs.items()]
        self.tableMainCentralWidget = QtWidgets.QMainWindow()
        self.tableCentralWidget = QtWidgets.QWidget(self.tableMainCentralWidget)
        self.tableVerticalLayout = QtWidgets.QVBoxLayout(self.tableCentralWidget)
        self.tableWidget = QtWidgets.QTableWidget(self.tableCentralWidget)

        self.setWindowTitle(self.title_insert)
        self.btn = QPushButton("Commit")
        self.display_item = self.label_data
        self.label_item = QtWidgets.QLabel(self)

        self.item_1 = QLineEdit()
        self.item_2 = QLineEdit()
        vbox = QVBoxLayout()

        self.item_1.setPlaceholderText(self.item_list_args[0])
        self.item_1.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.item_1)

        self.item_2.setPlaceholderText(self.item_list_args[1])
        self.item_2.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.item_2)

        self.label_item.setText(f"{self.label_name}\n{self.display_item}")
        vbox.addWidget(self.label_item)

        self.btn.setFont(QtGui.QFont("Arial", 10))
        # self.btn.clicked.connect(lambda: self.display_table(self.item_list_args))
        self.btn.clicked.connect(self.display_table)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def display_table(self):
        self.tableMainCentralWidget.setWindowTitle(f"{self.item_1.text()} - {self.item_2.text()}")
        self.tableWidget.setColumnCount(self.columns_number)

        for i, val in enumerate(self.item_list_kwargs):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(val)

        self.tableVerticalLayout.addWidget(self.tableWidget)
        self.tableMainCentralWidget.setCentralWidget(self.tableCentralWidget)

        self.tableWidget.setRowCount(0)

        for row in self.item_data(self.item_1.text(), self.item_2.text()):
            self.tableWidget.insertRow(0)
            for column in range(self.columns_number):
                self.tableWidget.setItem(0, column, QtWidgets.QTableWidgetItem(row[column]))
        self.close()
        self.tableMainCentralWidget.show()


class InsertDisplayChart(QDialog):
    def __init__(self, title, label_name, item_1, label_data, x_axis, y_axis, item_data):
        super().__init__()
        self.title = title
        self.label_name = label_name
        self.label_data = label_data
        self.item_data = item_data
        self.x_axis = x_axis
        self.y_axis = y_axis

        self.item_1 = item_1

        self.setWindowTitle(self.title)
        self.btn = QPushButton("Commit")
        self.display_item = self.label_data

        self.first_item = QLineEdit()
        self.label_item = QtWidgets.QLabel(self)

        vbox = QVBoxLayout()

        self.first_item.setPlaceholderText(self.item_1)
        self.first_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.first_item)

        self.label_item.setText(f"{self.label_name}\n{self.display_item}")
        vbox.addWidget(self.label_item)

        self.btn.setFont(QtGui.QFont("Arial", 10))
        self.btn.clicked.connect(lambda: self.insert_data(self.first_item.text()))
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def insert_data(self, first):
        self.chart_display = chart.ChartDisplay(
            f"{self.first_item.text()}", self.x_axis, self.y_axis, self.item_data(first)).bar_line_chart()
        self.close()


class InsertDisplayChartTwo(QDialog):
    def __init__(self, title, label_name, item_1, item_2, label_data, x_axis, y_axis, item_data):
        super().__init__()
        self.title = title
        self.label_name = label_name
        self.label_data = label_data
        self.item_data = item_data
        self.x_axis = x_axis
        self.y_axis = y_axis

        self.item_1 = item_1
        self.item_2 = item_2

        self.setWindowTitle(self.title)
        self.btn = QPushButton("Commit")
        self.display_item = self.label_data

        self.first_item = QLineEdit()
        self.second_item = QLineEdit()
        self.label_item = QtWidgets.QLabel(self)

        vbox = QVBoxLayout()

        self.first_item.setPlaceholderText(self.item_1)
        self.first_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.first_item)

        self.second_item.setPlaceholderText(self.item_2)
        self.second_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.second_item)

        self.label_item.setText(f"{self.label_name}\n{self.display_item}")
        vbox.addWidget(self.label_item)

        self.btn.setFont(QtGui.QFont("Arial", 10))
        self.btn.clicked.connect(lambda: self.insert_data(self.first_item.text(), self.second_item.text()))
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def insert_data(self, first, second):
        self.chart_display = chart.ChartDisplay(
            f"{self.first_item.text()} - {self.second_item.text()}", self.x_axis, self.y_axis,
            self.item_data(first, second)).bar_line_chart()
        self.close()


class DisplayTable(QMainWindow):
    def __init__(self, title, columns_number, expense_type, *args):
        super().__init__()
        self.title = title
        self.columns_number = columns_number
        self.expense_type = expense_type
        self.item_list = [n for n in args]

        self.setWindowTitle(self.title)

        self.centralWidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)

        self.tableWidget.setColumnCount(self.columns_number)

        for i, val in enumerate(self.item_list):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(val)

        self.verticalLayout.addWidget(self.tableWidget)
        self.setCentralWidget(self.centralWidget)

        for row in self.expense_type:
            self.tableWidget.insertRow(0)
            for column in range(self.columns_number):
                self.tableWidget.setItem(0, column, QtWidgets.QTableWidgetItem(row[column]))


class InsertUpdateFourToDB(QDialog):
    def __init__(self, title, label_name, item_1, item_2, item_3, item_4, label_data, item_data):
        super().__init__()
        self.title = title
        self.label_name = label_name
        self.label_data = label_data
        self.item_data = item_data
        self.item_1 = item_1
        self.item_2 = item_2
        self.item_3 = item_3
        self.item_4 = item_4

        self.setWindowTitle(self.title)
        self.btn = QPushButton("Commit")
        self.display_item = self.label_data

        self.first_item = QLineEdit()
        self.second_item = QLineEdit()
        self.third_item = QLineEdit()
        self.fourth_item = QLineEdit()
        self.label_item = QtWidgets.QLabel(self)

        vbox = QVBoxLayout()

        self.first_item.setPlaceholderText(self.item_1)
        self.first_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.first_item)

        self.second_item.setPlaceholderText(self.item_2)
        self.second_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.second_item)

        self.third_item.setPlaceholderText(self.item_3)
        self.third_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.third_item)

        self.fourth_item.setPlaceholderText(self.item_4)
        self.fourth_item.setFont(QtGui.QFont("Arial", 15))
        vbox.addWidget(self.fourth_item)

        self.label_item.setText(f"{self.label_name}\n{self.display_item}")
        vbox.addWidget(self.label_item)

        self.btn.setFont(QtGui.QFont("Arial", 10))
        self.btn.clicked.connect(self.insert_data)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def insert_data(self):
        self.item_data(
            self.first_item.text(),
            self.second_item.text(),
            self.third_item.text(),
            self.fourth_item.text()
        )
        QMessageBox.about(self, "Inserted", "Done")
        self.close()


class CalendarDisplay(QMainWindow):
    def __init__(self, title, colour, time_label):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(631, 472)

        self.central_widget = QtWidgets.QWidget(self)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.central_widget)
        self.hour_display_lcd = QtWidgets.QLCDNumber(self.central_widget)
        self.hour_display_label = QtWidgets.QLabel(self.central_widget)

        self.calendarWidget.setGeometry(QtCore.QRect(40, 80, 541, 341))

        self.hour_display_lcd.setGeometry(QtCore.QRect(40, 30, 91, 23))
        self.hour_display_lcd.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hour_display_lcd.setStyleSheet(f"background:{colour}")
        self.hour_display_lcd.display(data.TODAY_TIME)

        self.hour_display_label.setGeometry(QtCore.QRect(40, 10, 81, 18))
        self.hour_display_label.setText(time_label)

        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = GuiMainWindow("Main Window")
    ui.show()
    sys.exit(app.exec_())
