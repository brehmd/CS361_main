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
    
def choose_task(task_list):
    string = "Choose from one of the following tasks, by index:\n"
    
    for i, task_name in enumerate(task_list):
        string += f"{i+1}. {task_name[0]}\n"
    
    return string

def remove_task(task_index, planner_dict, class_name):
    total_points, directory, task_list = planner_dict[class_name]
    
    del task_list[task_index]
    
    with open(f"{directory}/tasklist.csv", mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows([["Task_Name", "Class", "Points", "Due_Date", "Notes", "Linked_File"]])
        for task in task_list:
            writer.writerows([[task[0], class_name, task[1], task[2], task[3], task[4]]])
    
    return

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    print("Waiting for requests...")
    
    while 1:
        message = socket.recv_string()
        print(f"Received request: {message}")
        
        if message == "complete_task":
            planner_dict = get_planner_as_dict()
            
            class_string = choose_class(planner_dict)
            socket.send_string(class_string)
            class_name = socket.recv_string()
            # get by index option not working ... ?
            
            class_points, task_list = get_tasks(planner_dict, class_name)
            
            task_string = choose_task(task_list)
            socket.send_string(task_string)
            task_index = int(socket.recv_string()) - 1
            
            task_name = task_list[task_index][0]
            
            remove_task(task_index, planner_dict, class_name)
            
            socket.send_string(f"Completed {task_name}. Good Work! Updated {class_name}.")
        
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