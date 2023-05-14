import sqlite3
from fire import Cause, Fire, datetime, time

class Database:

    def row_factory(self, cursor, row) -> dict:
        fields = [column[0] for column in cursor.description]
        return {k: v for k, v in zip(fields, row)}

    def __init__(self) -> None:
        self.conn = sqlite3.connect("fires.sqlite")
        self.cursor = self.conn.cursor()
        self.conn.row_factory = self.row_factory

    def _transform(self, row: tuple) -> Fire:
        return Fire(
            row[3], 
            row[14],
            row[25],
            datetime.strptime("{} {}".format(row[21], row[23]), "%m/%d/%Y %H%M"),
            row[23],
            row[22],
            datetime.strptime("{} {}".format(row[27], row[29]), "%m/%d/%Y %H%M"),
            row[29],
            row[28],
            row[30],
            row[32],
            row[33],
            row[35])

    def get_fire_by_id(self, fire_id: str) -> Fire:
        res = self.cursor.execute("SELECT * FROM `Fires` WHERE `fire_id` = ?", fire_id)
        row = res.fetchone()
        return self._transform(row)

    def get_all_fires(self) -> list:
        fires = list()
        res = self.cursor.execute("SELECT * FROM `Fires`")
        rows = res.fetchall()
        for row in rows:
            fires.append(self._transform(row))
        return fires
    
    def get_training_testing_set(self, samples: int) -> list:
        query = '''SELECT * FROM `Fires` WHERE 
                `DISCOVERY_DATE` IS NOT NULL AND 
                `DISCOVERY_TIME` IS NOT NULL AND
                `CONT_DATE` IS NOT NULL AND 
                `CONT_TIME` IS NOT NULL
                LIMIT {}'''.format(samples)
        res = self.cursor.execute(query)
        rows = res.fetchall()
        fires = list()
        for row in rows:
            fires.append(self._transform(row))
        return fires

    def get_all_clean_fires(self) -> list:
        query = '''SELECT * FROM `Fires` WHERE 
                `DISCOVERY_DATE` IS NOT NULL AND 
                `DISCOVERY_TIME` IS NOT NULL AND
                `CONT_DATE` IS NOT NULL AND 
                `CONT_TIME` IS NOT NULL
                LIMIT 5000'''
        res = self.cursor.execute(query)
        rows = res.fetchall()
        fires = list()
        for row in rows:
            fires.append(self._transform(row))
        return fires

    def _test(self) -> None:
        for fire in self.get_all_clean_fires():
            fire.pretty_print()
