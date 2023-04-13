import sqlite3
import os
from prettytable import PrettyTable
import data
import pandas as pd


class DB:
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.db_name = data.DB_NAME
        self.conn = sqlite3.connect(f"{self.path}/{self.db_name}.db")
        self.cursor = self.conn.cursor()

    def create_table(self):

        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {data.TABLE}(
                value INTEGER NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                date INTEGER,
                month INTEGER NOT NULL,
                monthName TEXT NOT NULL,
                year INTEGER NOT NULL
                )""")

    def insert_data(self, data_to_insert):
        try:
            self.cursor.executemany(f"""
                INSERT INTO {data.TABLE} values(?, ?, ?, ?, ?, ?, ?, ?)""",
                                    data_to_insert)

        except sqlite3.IntegrityError:
            print(f"Table {data.TABLE} already exist or there is a typing error.")
        self.conn.commit()

    def delete_db(self):
        os.remove(f"{self.path}/{self.db_name}.db")
        print(f"{self.db_name} deleted")

    @staticmethod
    def print_table(data_table, **kwargs):
        table = PrettyTable([n[1] for n in kwargs.items()])
        for n in data_table:
            table.add_row(n[:])
        print(table)

    @staticmethod
    def get_month_name(month):
        return data.month_dict[int(month)]

    def display_categories(self, expense_type):
        return [n[0] for n in self.cursor.execute(f"SELECT category FROM {data.TABLE} "
                                                  f"WHERE type = '{expense_type.upper()}' "
                                                  f"GROUP by category").fetchall()]

    """READ"""

    def read_earliest_latest_years(self):
        return sorted([n[0] for n in self.cursor.execute(f"SELECT year FROM {data.TABLE}").fetchall()])

    def read_all_expenses(self):
        return self.cursor.execute(f"SELECT CAST(value AS text), category, type, description, date FROM {data.TABLE} "
                                   f"ORDER BY month, year ASC").fetchall()

    def read_all_expenses_by_type(self, expense_type):
        return self.cursor.execute(
            f"SELECT CAST(value AS text), category, type, description, date "
            f"FROM {data.TABLE} WHERE type = '{expense_type.upper()}' "
            f"ORDER BY date ASC").fetchall()

    def read_expenses_by_date(self, date):
        return self.cursor.execute(
            f"SELECT CAST(value AS text), category, type, description, date FROM {data.TABLE} "
            f"WHERE date = '{date}'").fetchall()

    def read_all_expenses_in_month_per_year(self, month, year):
        return self.cursor.execute(f"SELECT CAST(value AS text), category, type, description, date "
                                   f"FROM {data.TABLE} "
                                   f"WHERE month = {month} AND year = {year}  "
                                   f"GROUP BY date, category "
                                   f"ORDER BY date").fetchall()

    def read_expenses_month_per_year_by_category(self, month, year):
        return self.cursor.execute(f"SELECT CAST(sum(value) AS text), category, type, monthName "
                                   f"FROM {data.TABLE} "
                                   f"WHERE month = {month} AND year = {year}  "
                                   f"GROUP BY category "
                                   f"ORDER BY type").fetchall()

    def read_expenses_per_year_by_category(self, year):
        return self.cursor.execute(f"SELECT CAST(sum(value) AS text), category, type AS total_value "
                                   f"FROM {data.TABLE} "
                                   f"WHERE year = {year} "
                                   f"GROUP BY category "
                                   f"ORDER BY type").fetchall()

    def read_total_expenses_by_category(self):
        return self.cursor.execute(f"SELECT CAST(sum(value) AS text), category, type "
                                   f"FROM {data.TABLE} "
                                   f"GROUP BY category "
                                   f"ORDER BY type").fetchall()

    def read_total_expenses_month_per_year(self, year):
        return self.cursor.execute(
            f"SELECT CAST(sum(value) AS text), monthName "
            f"FROM {data.TABLE} "
            f"WHERE YEAR = {year} "
            f"GROUP BY month "
            f"ORDER BY month ASC").fetchall()

    def read_total_expenses_year(self):
        return self.cursor.execute(
            f"SELECT CAST(sum(value) AS text), CAST(year AS text) "
            f"FROM {data.TABLE} "
            f"GROUP BY year "
            f"ORDER BY year").fetchall()

    """OPERATIONS"""

    def insert_new_expense(self, value, category, expense_type, description):
        self.cursor.execute(f"INSERT INTO {data.TABLE} "
                            f"VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (value, category.upper(), expense_type.upper(), description.upper(), data.TODAY_DATE,
                             data.MONTH, data.MONTH_NAME, data.YEAR))
        self.conn.commit()

    def delete_expense(self, value, category, expense_type, date):
        self.cursor.execute(f"DELETE FROM {data.TABLE} WHERE "
                            f"value=? AND category=? AND type=? and date=?",
                            (value, category.upper(), expense_type.upper(), date))
        self.conn.commit()

    def update_value(self, existing_value, category, date, new_value):
        self.cursor.execute(
            f"UPDATE {data.TABLE} SET value = ? WHERE value = ? AND category = ? AND date = ?",
            (new_value, existing_value, category.upper(), date))
        self.conn.commit()

    def update_category_name(self, value, category, date, new_category):
        self.cursor.execute(
            f"UPDATE {data.TABLE} SET category = ? WHERE value = ? AND category = ? AND date = ?",
            (new_category.upper(), value, category.upper(), date))
        self.conn.commit()

    def update_category_type(self, existing_type, category, date, new_type):
        self.cursor.execute(
            f"UPDATE {data.TABLE} SET type = ? WHERE type = ? AND category = ? AND date = ?",
            (new_type.upper(), existing_type.upper(), category.upper(), date))
        self.conn.commit()

    def update_expense_description(self, value, category, date, new_description):
        self.cursor.execute(
            f"UPDATE {data.TABLE} SET description = ? WHERE value = ? AND category = ? AND date = ?",
            (new_description.upper(), value, category.upper(), date))
        self.conn.commit()

    def update_date(self, value, category, date, new_date):
        self.cursor.execute(
            f"UPDATE {data.TABLE} SET date = ? WHERE value = ? AND category = ? AND date = ?",
            (new_date, value, category.upper(), date)
        )
        self.cursor.execute(
            f"UPDATE {data.TABLE} SET month = ?, monthName = ?, year = ? WHERE value = ? AND category = ? AND date = ?",
            (new_date.split('-')[1], self.get_month_name(new_date.split('-')[1]).capitalize(), new_date.split('-')[2],
             value, category.upper(), new_date)
        )
        self.conn.commit()
        print(self.get_month_name(new_date.split('-')[1]).capitalize())

    def total_value_expenses(self):
        return sum([int(value[0]) for value in self.cursor.execute(f"SELECT value FROM {data.TABLE}").fetchall()])


def import_xls(file_name, sheet_name):
    df = pd.read_excel(file_name, sheet_name)
    imported_data = df.values.tolist()
    return imported_data


if __name__ == "__main__":
    db = DB()
    # db.create_table()
    # db.insert_data(data.expenses_list)
    # db.insert_data(import_xls("expenses_import.xls", "october_2022"))
    # db.insert_data(import_xls("expenses_import.xls", "september_2022"))
    # db.delete_db()

    # db.delete_expense("1500", "food", 'not_fixed', "16-11-2022")
    # db.insert_new_expense(500, "others", "not_fixed", "test 07.11.22_2")
    # db.update_value(0, "new_cleaning", "07-11-2022", 10)
    # db.update_category_name(0, "cleaning", "07-11-2022", "new_cleaning")
    # db.update_category_type("fixed", "phone", "07-11-2022", "not_fixed")
    # db.update_expense_description("test 07.11.22", "food", "07-11-2022", "test_2 07.11.22")
    #
    # db.print_table(db.display_categories("fixed"),
    #                col1="fixed")
    # db.print_table(db.display_categories("not_fixed"),
    #                col1="not_fixed")
    # db.print_table(db.read_all_expenses(),
    #                col1="1",
    #                col2="2",
    #                col3="3",
    #                col4="4",
    #                col5="5",
    #                )
    # db.print_table(db.read_all_expenses_by_type("fixed"),
    #                col1="1",
    #                col2="2",
    #                col3="3",
    #                col4="4",
    #                col5="5",
    #                )
    # db.print_table(db.read_all_expenses_by_type("not_fixed"),
    #                col1="1",
    #                col2="2",
    #                col3="3",
    #                col4="4",
    #                col5="5",
    #                )
    # db.print_table(db.read_expenses_by_date("07-11-2022"),
    #                col1="1",
    #                col2="2",
    #                col3="3",
    #                col4="4",
    #                col5="5",
    #                )

    # db.print_table(db.read_all_expenses_in_month_per_year(10, 2022),
    #                col1="1",
    #                col2="2",
    #                col3="3",
    #                col4="4",
    #                col5="5",
    #                )

    # for n in db.read_all_expenses_in_month_per_year(10, 2022):
    #     print(n)

    # db.print_table(db.read_expenses_month_per_year_by_category(10, 2022),
    #                col1="1",
    #                col2="2",
    #                col3="3"
    #                )
    # db.print_table(db.read_expenses_per_year_by_category(2022),
    #                col1="1",
    #                col2="2",
    #                col3="3"
    #                )
    # db.print_table(db.read_total_expenses_by_category(),
    #                col1="1",
    #                col2="2",
    #                col3="3"
    #                )
    # db.print_table(db.read_total_expenses_month_per_year(2022),
    #                col1="1",
    #                col2="2"
    #                )
    # db.print_table(db.read_total_expenses_year(),
    #                col1="1",
    #                col2="2"
    #                )
    #
    # print(db.total_value_expenses())
    # print(db.read_earliest_latest_years())
    # print(db.get_month_name(12))
