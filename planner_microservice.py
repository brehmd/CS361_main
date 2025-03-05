import csv
import os
import zmq
import json

def read_planner_csv(file_path="planner.csv"):
    """read planner csv and return data"""
    planner_data = []

    try:
        # open csv file
        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)

            # stop reading the header
            headers = next(csv_reader)

            # read the data
            for row in csv_reader:
                if len(row) >= 3:
                    class_name = row[0]
                    total_points = row[1]
                    directory = row[2]
                    planner_data.append((class_name, total_points, directory))

        return planner_data

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def read_tasklist_csv(directory):
    """read tasklist csv from the directory"""
    tasks = []

    try:
        # get the directory
        file_path = os.path.join(directory, "tasklist.csv")

        # is it real or are we just dreaming?
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return []
        
        # open and read
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # stop reading the header
            headers = next(csv_reader)
            
            # read the data
            for row in csv_reader:
                if len(row) >= 5:
                    task_name = row[0]
                    class_name = row[1]
                    points = row[2]
                    due_date = row[3]
                    notes = row[4]
                    tasks.append((task_name, class_name, points, due_date, notes))

        return tasks

    # handle exceptions
    except Exception as e:
        print(f"Error reading tasklist: {e}")
        return []

def format_planner_data(data):
    """Format planner data into a table before sending it"""
    
    # error check
    if not data:
        return "No planner data available."

    # find the maximum column widths
    col_widths = [max(len(str(row[i])) for row in data) for i in range(len(data[0]))]

    # create formatted table
    formatted_table = []
    for idx, row in enumerate(data):
        line = "  ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        formatted_table.append(line)

        # add separator after the header row
        if idx == 0:
            separator = "  ".join("-" * col_widths[i] for i in range(len(row)))
            formatted_table.append(separator)

    # join altogether and return
    return "\n".join(formatted_table)

def create_planner_array():
    """making the array"""
    
    # read the planner data
    planner_data = read_planner_csv()
    
    if not planner_data:
        return [["Class", "Total Points", "Tasks"]]

    result = []
    result.append(["Class", "Total Points", "Tasks"])

    # process the data
    for class_data in planner_data:
        class_name = class_data[0]
        total_points = class_data[1]
        directory = class_data[2]

        # read the tasklist
        tasks = read_tasklist_csv(directory)

        # add the class data
        task_count = len(tasks) if tasks else 0
        result.append([class_name, total_points, task_count])

        # each task
        if tasks:
            for task in tasks:
                task_name = task[0]
                points = task[2]
                due_date = task[3]
#####################################################################################################
                # format due date                                                                   #
                if due_date.isdigit() and len(due_date) == 4:       # Convert 0210 -> 02/10         #
                    due_date = f"{due_date[:2]}/{due_date[2:]}"     # Convert 0210 -> 02/10         #
                                                                                                    #
                result.append([f"  {task_name}", points, f"Due: {due_date}"])                       #
#####################################################################################################
    return result

def start_server():
    """using ZeroMQ"""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Waiting for requests...")

    try:
        while True:
            # wait for request
            message = socket.recv_string()
            print(f"Received request: {message}")

            # process the request
            if message == "view_planner":
                # get the array
                planner_array = create_planner_array()
                
                # convert to table
                formatted_response = format_planner_data(planner_array)
                
                # send formatted table as response
                socket.send_string(formatted_response)

            elif message == "end":
                # end the server
                socket.send_string("Ending server")
                break

            else:
                # ???
                socket.send_string("Unknown request")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # close it all
        socket.close()
        context.term()
        print("Server closed")

if __name__ == "__main__":
    start_server()
