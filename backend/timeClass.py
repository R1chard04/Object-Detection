import time
from flask import Flask
<<<<<<<< HEAD:backend/timeLog.py
========
from sqlalchemy import create_engine, MetaData, inspect
>>>>>>>> 1a6a83f5f72ec3c90564aaae26e5cf313308f713:backend/timeClass.py
from database_model.models import db, TimingStation100, TimingStation120
import pdb

time_app = Flask(__name__)
time_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///martinrea.db'

db.init_app(time_app)

def create_tables():
    # create all the tables based on the models if they didn't exist yet
    with time_app.app_context():
      inspector = inspect(db.engine)
      if not inspector.has_table('Station100_timing') and not inspector.has_table('Station120_timing'):
        db.create_all()

create_tables()

class timeLog:

    def __init__(self, station, partList) -> None:
        with time_app.app_context():
            self.record = [0] * (len(partList)+1)
            self.startTime = time.time()
            self.maxTime = 0
            self.station = station

<<<<<<<< HEAD:backend/timeLog.py
    def log(self, results, clampClosed):
        with app.app_context():
========
    def result_record(self, results, clampClosed):
        with time_app.app_context():
>>>>>>>> 1a6a83f5f72ec3c90564aaae26e5cf313308f713:backend/timeClass.py
            elapsedTime = time.time() - self.startTime

            for i in range(len(results)):
                if results[i] == 1 and self.record[i] == 0:
                    self.record[i] = elapsedTime

                    if elapsedTime > self.maxTime:
                        self.maxTime = elapsedTime

            if clampClosed == True:
                self.record[-1] = elapsedTime - self.maxTime

            print(self.record)
            
            if 0 not in self.record:
                new_partLists100 = ['TopPart', 'LeftPart', 'BottomPart', 'RightPart', 'ClampState']
                new_partLists120 = ['TopRightPart', 'TopLeftPart', 'LeftPart', 'BottomLeftPart', 'BottomRightPart', 'RightPart', 'ClampState']
                
                # create an instance to put it in the database
                if self.station == 'station100':
                    j = 0
                    for i in new_partLists100:
                        row = {i : self.record[j]}
                        j += 1
                        db.session.add(row)
                        db.session.commit()
                
                elif self.station == 'station120':
                    k = 0
                    for i in new_partLists120:
                        row = {i : self.record[k]}
                        k += 1
                        db.session.add(row)
                        db.session.commit()
                
                return True

            return False

        
