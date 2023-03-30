import psycopg2
from psycopg2 import extras

class imageAverage:
    def __init__(self, db_config):
        self.db_config = db_config

    def average(self):
        conn_string = "host={0} port={1} dbname={2} user={3} password={4}".format(
            self.db_config["hostname"],
            self.db_config["port_id"],
            self.db_config["database"],
            self.db_config["username"],
            self.db_config["pwd"]
         )

        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        # Get all distinct assigned_names in the results table
        cur.execute("SELECT DISTINCT assigned_name, shift FROM results WHERE response = '1'")
        results = cur.fetchall()

        shifts = ["Day", "Afternoon", "Night"]

        # Create empty lists to store the average times for each shift
        avg_times_day = []
        avg_times_afternoon = []
        avg_times_night = []

        # For each assigned_name, calculate the average of the last 5 time_elapsed values for each shift
        for assigned_name in set(result[0] for result in results):
            for shift in shifts:
                # Query the last 5 time_elapsed values for the current assigned_name and shift
                cur.execute(f"SELECT time_elapsed FROM results WHERE assigned_name = '{assigned_name}' AND shift = '{shift}' AND response = '1' ORDER BY timestamp DESC LIMIT 5")
                last_five_times = [result[0] for result in cur.fetchall()]

                average_time = 0
                
                # Calculate the average of the last 5 time_elapsed values
                if last_five_times:
                    average_time = sum(last_five_times) / len(last_five_times)
                    # Round the average to two decimal places
                    average_time = round(average_time, 2)

                # Add the average time to the appropriate list based on the shift
                if shift == "Day":
                    avg_times_day.append(average_time)
                elif shift == "Afternoon":
                    avg_times_afternoon.append(average_time)
                elif shift == "Night":
                    avg_times_night.append(average_time)

        # Close the database cursor and connection    
        cur.close()    
        conn.close()

        # Check if a shift has no values and replace the list with an empty list
        if not avg_times_day:
            avg_times_day = []
        if not avg_times_afternoon:
            avg_times_afternoon = []
        if not avg_times_night:
            avg_times_night = []

        # Print the lists of average times for each shift
        print("Day Shift:", avg_times_day)
        print("Afternoon Shift:", avg_times_afternoon)
        print("Night Shift:", avg_times_night)

        return (avg_times_day, avg_times_afternoon, avg_times_night)
