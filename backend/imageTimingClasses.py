import time
from flask import Flask
from sqlalchemy import create_engine, MetaData, inspect
from database_model.models import db, TimingStation100, TimingStation120
import pdb
import xlwings as xw

#Database stuff
time_app = Flask(__name__)

db.init_app(time_app)

time_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instances/martinrea.db'

def create_table():
    with time_app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('Station100_Timing') and not inspector.has_table('Station120_Timing'):
            db.create_all()

create_table()

#Class for timing
class timeLog:

    def __init__(self, station, partList) -> None:
        with time_app.app_context():
            self.record = [0] * (len(partList)+1)
            self.startTime = time.time()
            self.maxTime = 0
            self.station = station

    #Method that checks when the a part is first confirmed in a cycle. After a part is placed, it is assumed it is not removed and the timing will no longer update for it
    #THe timing array has one more than the number of aprts and thats to see how long it takes between final part palcement and clamp closing
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
            
            #More database stuff
            if 0 not in self.record:
                new_partLists100 = ['TopPart', 'LeftPart', 'BottomPart', 'RightPart', 'ClampState']
                new_partLists120 = ['TopRightPart', 'TopLeftPart', 'LeftPart', 'BottomLeftPart', 'BottomRightPart', 'RightPart', 'ClampState']
                
                # create an instance to put it in the database
                if self.station == 'station100':
                    row = [
                        TimingStation100(TopPart=self.record[0], LeftPart=self.record[1], BottomPart=self.record[2], RightPart=self.record[3], ClampState=self.record[4])
                    ]
                    for new_row in row:
                        try:
                            db.session.add(new_row)
                            db.session.commit()
                            print(f'New timing has been inserted successfully for station 100!')
                        except Exception as e:
                            db.session.rollback()
                            print(f'Found error while inserting new timing for station 100 with error: {e}')
                elif self.station == 'station120':
                    row = [
                        TimingStation120(TopRightPart=self.record[0], TopLeftPart=self.record[1], LeftPart=self.record[2], BottomLeftPart=self.record[3], BottomRightPart=self.record[4], RightPart=self.record[5], clampState=self.record[6])
                    ]
                    for new_row in row:
                        try:
                            db.session.add(new_row)
                            db.session.commit()
                            print(f'New timing has been inserted successfully for station 120!')
                        except Exception as e:
                            print(f'Found error while inserting new timing for station 120 with error: {e}')
                
                
                ### Excel stuff
                wb = xw.Book("stationsExcel.xlsx")
                if self.station == 'station100':
                    sht = wb.sheets['100']
                    i = 2
                    while sht['A{}'.format(i)].value !=None:
                        i+=1
                    sht['A{}'.format(i)].value = self.record[0]
                    sht['B{}'.format(i)].value = self.record[1]
                    sht['C{}'.format(i)].value = self.record[2]
                    sht['D{}'.format(i)].value = self.record[3]
                    sht['E{}'.format(i)].value = self.record[4]
                    

                elif self.station == 'station120':
                    sht = wb.sheets['120']
                    i = 2
                    while sht['A{}'.format(i)].value !=None:
                        i+=1
                    sht['A{}'.format(i)].value = self.record[0]
                    sht['B{}'.format(i)].value = self.record[1]
                    sht['C{}'.format(i)].value = self.record[2]
                    sht['D{}'.format(i)].value = self.record[3]
                    sht['E{}'.format(i)].value = self.record[4]
                    sht['E{}'.format(i)].value = self.record[5]
                    sht['E{}'.format(i)].value = self.record[6]
           
                wb.save(r"stationsExcel.xlsx")
                wb.close()

                return True, self.record

            return False, self.record


        
