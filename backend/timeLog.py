import time
from flask import Flask
from sqlalchemy import create_engine, MetaData, inspect
from database_model.models import db, TimingStation100, TimingStation120

time_app = Flask(__name__)

db.init_app(time_app)

time_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/martinrea.db'

def create_table():
    with time_app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('Station100_Timing') and not inspector.has_table('Station120_Timing'):
            db.create_all()

create_table()

class timeLog:

    def __init__(self, station, partList) -> None:
        with time_app.app_context():
            self.record = [0] * (len(partList)+1)
            self.startTime = time.time()
            self.maxTime = 0
            self.station = station

    def log(self, results, clampClosed):
        with time_app.app_context():
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


        
