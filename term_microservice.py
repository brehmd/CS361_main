import csv
import os
import zmq

# get planner_dict
def get_planner_as_dict():
    planner_dict = {}
    
    with open("planner.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        
        headers = next(csv_reader)
        
        for row in csv_reader:
            if len(row) == 3:
                class_name, total_points, directory = row
                task_list = []
                planner_dict[class_name] = (total_points, directory, task_list)
                
    csv_file.close()
    
    return planner_dict

def get_tasks(planner_dict, class_name):
    total_points, directory, task_list = planner_dict[class_name]
    
    with open(f"{directory}/tasklist.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        
        headers = next(csv_reader)
        
        for row in csv_reader:
            if len(row) >= 6:
                task_name, _, points, due_date, notes, linked_file = row
                task_list.append((task_name, points, due_date, notes, linked_file))
                
    return (total_points, task_list)

def all_tasks(planner_dict):
    task_array = []
    total_points = 0
    
    for class_name in planner_dict:
        print(class_name)
        task_list = get_tasks(planner_dict, class_name)
        for task in task_list:
            print(task)
            task_array.append(task)
            total_points += task[1]
        
    return task_array, total_points

# ask user if they want to "rollover" old assignments to the new term under the class "prev term"

# overwrite current planner either empty or with old assignments (class points should sum up to all prev assignments)
def overwrite_new_term(task_list, total_points):
    
    if len(task_list) > 0: 
        os.mkdir(f"./Previous term", 0o755)
        with open(f"Previous term/tasklist.csv", mode = 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerows([["Task_Name", "Class", "Points", "Due_Date", "Notes", "Linked_File"]])
            for task in task_list:
                writer.writerows([[task[0], "Previous term", task[1], task[2], task[3], task[4]]])
        file.close()
    
    with open(f"./planner.csv", mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows([["Class_Name", "Total_Points", "Directory_Address"]])
        if len(task_list) > 0: 
            writer.writerows([["Previous term", total_points, "./Previous term"]])
    file.close()
    
    return

# send user a message of completion

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")

    print("Waiting for requests...")
    
    while 1:
        message = socket.recv_string()
        print(f"Received request: {message}")
        
        if message == "new_term":
            planner_dict = get_planner_as_dict()
            
            task_array, total_points = all_tasks(planner_dict)
            socket.send_string(f"Do you want to roll-over the {len(task_array)} from last term? (y/n)")
            rollover = socket.recv_string()
            
            rollover_points = 0
            rollover_tasks = []
            if rollover == "y":
                rollover_points = total_points
                rollover_tasks = task_array
                
            overwrite_new_term(rollover_tasks, rollover_points)
            
            socket.send_string("New Term started. Good luck!")
        
        elif message == "end":
            socket.send_string("Ending Server")
            break
        
        else:
            # unknown request
            socket.send_string("Unknown request")
    
    socket.close()
    context.term()
    print("Server Closed")

if __name__ == "__main__":
    main()