import csv
import os
import zmq

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

def choose_class(planner_dict):
    string = "Choose from one of the following Classes, by name:\n"
    
    for class_name in planner_dict:
        string += f"- {class_name}\n"
    
    return string
    

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
    


def format_class(class_object, class_name):
    total_points, task_list = class_object
    
    string = ""
    string += f"{class_name} has a total of {total_points} points. There are {len(task_list)} current assignments.\n"
    for i, task in enumerate(task_list):
        task_name, points, due_date, notes, linked_file = task
        string += f"{i+1}. {task_name}"
        if(linked_file):
            string += f" ({linked_file})\n"
        else:
            string += "\n"
        string += f"\t- worth {points} points\n"
        string += f"\t- due {due_date[:2]}/{due_date[2:]}\n"
        if(notes):
            string += f"\t- {notes}\n"
    
    return string

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("Waiting for requests...")
    
    while 1:
        message = socket.recv_string()
        print(f"Received request: {message}")
        
        if message == "view_class":
            planner_dict = get_planner_as_dict()
            
            choose_string = choose_class(planner_dict)
            socket.send_string(choose_string)
            class_name = socket.recv_string()
            # get by index option not working ... ?
            
            class_object = get_tasks(planner_dict, class_name)
            
            formatted_class = format_class(class_object, class_name)
            
            socket.send_string(formatted_class)
        
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