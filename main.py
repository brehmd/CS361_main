import csv
import os
import zmq

SCREEN_WIDTH = 90
BORDER_WIDTH = 5

def custom_print(text = ' ', mode = ' '):
    if mode == "center":
        if len(text) > SCREEN_WIDTH-(BORDER_WIDTH*2):
            for i in range(0, len(text), SCREEN_WIDTH-(BORDER_WIDTH*2)):
                print(text[i:i+SCREEN_WIDTH-(BORDER_WIDTH*2)].center(SCREEN_WIDTH))
            
        else: print(text.center(SCREEN_WIDTH))
    
    elif mode == "block":
        if len(text) > SCREEN_WIDTH-(BORDER_WIDTH*2):
            for i in range(0, len(text), SCREEN_WIDTH-(BORDER_WIDTH*2)):
                print(f"{' '*BORDER_WIDTH + text[i:i+SCREEN_WIDTH-(BORDER_WIDTH*2)] + ' '*BORDER_WIDTH}")
            
        else: print(f"{' '*BORDER_WIDTH + text + ' '*BORDER_WIDTH}")
        
    elif mode == "line":
        print(f"{"-"*SCREEN_WIDTH}")    
    
    return    

def print_logo(with_slogan = 0):
    logo1 = "             ____   __  __   __    "
    logo2 = "            / __ \\ / / /_ |  \\ \\   "
    logo3 = " _ __  _ __| |  | | |   | |   | |  "
    logo4 = "| '_ \\| '__| |  | | |   | |   | |  "
    logo5 = "| |_) | |  | |__| | |   | |   | |  "
    logo6 = "| .__/|_|   \\____/ \\ \\ |___| / /   "
    logo7 = "| |                                "
    
    if with_slogan: logo8 = "|_|   plan. realize. Simply.       "
    else: logo8 = "|_|                                "
    
    custom_print(logo1, "center")
    custom_print(logo2, "center")
    custom_print(logo3, "center")
    custom_print(logo4, "center")
    custom_print(logo5, "center")
    custom_print(logo6, "center")
    custom_print(logo7, "center")
    custom_print(logo8, "center")
    
    print()
    
    return

def show_homepage():
    print_logo(1)
    
    custom_print("Welcome to the ultimate planning program. prO(1) aims to save you time with a planner which integrates with your local file system and gives shortcuts for common tasks.", "center")
    print()
    
    custom_print("\"Human Time is more valuable than computing time.\"", "center")
    custom_print("- Pofessor Liang Huang (2024)", "center")
    print()
    
    input("Press Enter to Continue ...")
    
def main_menu():
    custom_print(mode = "line")
    
    print_logo()
    
    custom_print("Select from the following options using the \"|menu|:\" command line.", "center")
    
    print("\n1. View Planner")
    print("2. Create new Class or Task")
    print("3. Read helpful info about prO(1)")
    print("4. Exit prO(1)")
    print("OR use a shortcut command (more in Helpful info)")
    
    user_input = input("\n|menu|: ")
    
    return user_input

def mm_options(user_input):
    if user_input == "1":
        return view_planner()
    
    elif user_input == "2":
        return create_new()
    
    elif user_input == "3":
        return help()
        
    elif user_input == "4":
        return 0
    
    else:
        return shortcut_commands(user_input)


def help():
    custom_print(mode = "line")
    print_logo(0)
    
    custom_print("-- HELPFUL INFO --", "center")
    
    print()
    custom_print("- Purpose and overview -", "center")
    custom_print("prO(1) was designed to streamline organization for Computer Science students. It syncs your planner with your local file system so that valuable human time is not lost. The main features are currently to view the planner and add tasks or classes to the planner. However, both of these seeminly simple features are elevated with the student software engineer in mind.", "block")
    
    print()
    custom_print("- Viewing the Planner -", "center")
    custom_print("When viewing the planner you will be given a very high-level view. You will see all of your classes (including those with no tasks) and their tasks, but by name only. To see the details of a class or task: select View Class, View Task, or Filter. View class will give you the option to name the class you wish to get a detailed look at. This will display details about the class as well as detials about each task. View Task just gives information for the one task, however, it also will open any attached files to that task and allow the user to check it off. Lastly, the Filter feature will allow the user to filter the planner by 3 different metrics. Importance to your grade, urency of the due date, or the \"Priority\" which is calculated by both the importance and the urgency of the task. This will help students make informed choices.", "block")
    
    print()
    custom_print("- Creating new Classes or Tasks -", "center")
    custom_print("Creating a new class is a great way to organize your tasks. You will be asked to enter in a Name for the class as well as the total points available for the class. If the class or grouping does not explicitly have a point total, then I'd use a system of 100 points, and assign your tasks in the class arbitrary point values based on their perceived importance. Additinally, there is the choice to either use an existing folder or create a new folder on your local machine to represent this class. When creating a new task, there are more options to configure. It includes the task name, task points worth, the due date, the class that it belongs to, and optionally a file or folder location on your local machine. If you decide to create a file for a task, it will be placed within the folder for the class it belongs to.", "block")
    
    print()
    custom_print("- Using shortcut commands -", "center")
    custom_print("At any time, from any page, enter one of the following shortcut commands from the given page command line to execute a specific command. Notice: progress on the page from which you enter this command will be lost if not completed.", "block")
    custom_print("* 'view planner' - shows every class and attached tasks", "block")
    custom_print("* 'create class' - allows a user to create a class to add to planner", "block")
    custom_print("* 'create task' - allows a user to create a task to add to a class", "block")
    custom_print("* 'help' - opens up this help menu", "block")
    custom_print("* 'view class' - shows a specific class with more task details", "block")
    custom_print("* 'view task' - shows a specific task in more detail", "block")
    custom_print("* 'filter' - allows a user to look at ordered tasks from the planner", "block")
    custom_print("* 'update class' - gives user a prompt to correct or update class info", "block")
    custom_print("* 'update task' - gives user a prompt to correct or update task info", "block")
    custom_print("* 'complete task' - allows user to complete and remove task from planner", "block")
    custom_print("* 'main menu' - returns to the main menu", "block")
    custom_print("* 'exit' - ends prO(1)", "block")
    
    print()
    print("Press enter to return to main menu")
    user_input = input("|help|: ")
    
    return h_options(user_input)

def h_options(user_input):
    if user_input == "":
        pass
    
    else:
        return shortcut_commands(user_input)
        
    return 1

def view_planner():
    custom_print(mode = "line")
    print_logo()
    print()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555") 
    socket.send_string("view_planner")
    response = socket.recv_string()
    print(response)
    
    socket.close()
    context.term()
    
    print()
    print("Select from one of the following options:")
    print("1. View a Class")
    print("2. Complete Task")
    print("3. Start a new term")
    print("press enter to return to main")
    print()
    user_input = input("|view planner|: ")
    return vp_options(user_input)

def vp_options(user_input):
    if user_input == "1":
        return view_class()
    
    elif user_input == "2":
        return complete_task()
    
    elif user_input == "3":
        return new_term()
    
    elif user_input == "":
        return 1
    
    else:
        return shortcut_commands(user_input)


def view_class():
    custom_print(mode = "line")
    print_logo()
    print()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    socket.send_string("view_class")
    
    response = socket.recv_string()
    print(response)
    
    choose_class = input("|view class|: ")
    # validate input

    socket.send_string(choose_class)
    message = socket.recv_string()
    print()
    print(message)
    
    socket.close()
    context.term()
    
    print()
    print("Select from one of the following options:")
    print("1. View Planner")
    print("2. View another Class")
    print("3. Complete Task")
    print("4. Start a new term")
    print("press enter to return to main")
    print()
    user_input = input("|view class|: ")
    return vc_options(user_input)
    

def vc_options(user_input):
    if user_input == "1":
        return view_planner()
    
    elif user_input == "2":
        return view_class()
    
    elif user_input == "3":
        return complete_task()
    
    elif user_input == "4":
        return new_term()
    
    elif user_input == "":
        return 1
    
    else:
        return shortcut_commands(user_input)


def complete_task():
    custom_print(mode = "line")
    print_logo()
    print()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")
    socket.send_string("complete_task")
    
    response = socket.recv_string()
    print(response)
    
    choose_class = input("|complete task|: ")
    # validate input

    socket.send_string(choose_class)
    
    response1 = socket.recv_string()
    print(response1)
    
    choose_task = input("|complete task|: ")
    # validate input
    
    print()
    cancel = input("Are you sure you wish to delete this task? (y/n) ")
    if cancel == "y" or cancel == "":
        socket.send_string(choose_task)
        message = socket.recv_string()
        print()
        print(message)
    
    socket.close()
    context.term()
    
    print()
    print("Select from one of the following options:")
    print("1. View Planner")
    print("2. View a Class")
    print("3. Complete another Task")
    print("4. Start a new term")
    print("press enter to return to main")
    print()
    user_input = input("|complete task|: ")
    return complete_task_options(user_input)

def complete_task_options(user_input):
    if user_input == "1":
        return view_planner()
    
    elif user_input == "2":
        return view_class()
    
    elif user_input == "3":
        return complete_task()
    
    elif user_input == "4":
        return new_term()
    
    elif user_input == "":
        return 1
    
    else:
        return shortcut_commands(user_input)


def new_term():
    custom_print(mode = "line")
    print_logo()
    print()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")
    socket.send_string("new_term")
    
    response = socket.recv_string()
    print(response)
    
    choose_rollover = input("|new term|: ")
        
    # validate input

    socket.send_string(choose_rollover)
    message = socket.recv_string()
    print()
    print(message)
    
    socket.close()
    context.term()
    
    print()
    print("Select from one of the following options:")
    print("1. View Planner")
    print("2. View a Class")
    print("3. Complete Task")
    print("press enter to return to main")
    print()
    user_input = input("|new term|: ")
    return nt_options(user_input)

def nt_options():
    if user_input == "1":
        return view_planner()
    
    elif user_input == "2":
        return view_class()
    
    elif user_input == "3":
        return complete_task()
    
    elif user_input == "":
        return 1
    
    else:
        return shortcut_commands(user_input)


def create_new():
    custom_print(mode = "line")
    print("Select from one of the following options:")
    print("1. Create Class")
    print("2. Create Task")
    
    print()
    user_input = input("|create|: ")
    return cn_options(user_input)

def cn_options(user_input):
    if user_input == "1":
        return create_class()
    
    elif user_input == "2":
        return create_task()
    
    else:
        return shortcut_commands(user_input)



def create_class():
    custom_print(mode = "line")
    print_logo()
    print()
    custom_print("-- CREATE CLASS --", "center")
    
    custom_print("Enter information for the class you wish to add. Any field with a '*' means it is required and a blank entry will cancel the command. Otherwise, a blank entry will give a default value as specified.", "block")
    print()
    class_name = input("* Name of Class: ")
    if class_name == '': return 1
    # if os.path.exists(f"./{class_name}/"):
    #     custom_print(mode = 'line')
    #     custom_print("This class already exists", "block")
    
    class_points = input("Points tied to class (def = 100): ")
    if class_points == '': class_points = 100
    
    class_file = input("Enter class local folder location (def = create new): ")
    if class_file == '':
        os.mkdir(f"./{class_name}", 0o755)
        class_file = f"./{class_name}"
        with open(f"{class_file}/tasklist.csv", mode = 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerows([["Task_Name", "Class", "Points", "Due_Date", "Notes", "Linked_File"]])
        file.close()
            
    with open(f"./planner.csv", mode = 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows([[class_name, class_points, class_file]])
    file.close()

    print()
    print("Press enter to return to main menu")
    user_input = input("|create class|: ")
    return cc_options(user_input)

def cc_options(user_input):
    if user_input == "":
        return 1
    
    else:
        return shortcut_commands(user_input)


def create_task():
    custom_print(mode = "line")
    print_logo()
    print()
    custom_print("-- CREATE TASK --", "center")
    
    custom_print("Enter information for the task you wish to add. Any field with a '*' means it is required and a blank entry will cancel the command. Otherwise, a blank entry will give a default value as specified.", "block")
    print()
    task_name = input("* Name of Task: ")
    if task_name == '': return 1
    
    task_class = input("* Belongs to Class: ")
    if task_class == '': return 1
    
    class_location = ''
    with open(f"./planner.csv", mode = 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == task_class:
                class_location = row[2]
    file.close()
    if class_location == '':
        custom_print(mode = "line")
        custom_print("No class matches that name, try again from main menu", "center")
        return 1
    
    task_points = input("Points for task (def = 0): ")
    if task_points == '': task_points = 0
    
    task_date = input("Due date (mmdd) for task (def = 1231): ")
    if task_date == '': task_date = "1231"
    
    task_notes = input("Additional notes for Task (def = none): ")
    
    task_file = input("Enter task local file location (def = none): ")
    if task_file != '':
        if not os.path.exists(task_file):
            with open(f"{task_file}", mode = 'w', newline = '') as file:
                file.write("")
            file.close()
            
    with open(f"{class_location}/tasklist.csv", mode = 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows([[task_name, task_class, task_points, task_date, task_notes, task_file]])
    file.close()

    print()
    print("Press enter to return to main menu")
    user_input = input("|create class|: ")
    return cc_options(user_input)

def ct_options():
    if user_input == "":
        return 1
    
    else:
        return shortcut_commands(user_input)


def shortcut_commands(user_input):
    uniform_input = user_input.lower()
    
    if uniform_input == "view planner":
        return view_planner()
    
    elif uniform_input == "create task":
        return create_task()
    
    elif uniform_input == "create class":
        return create_class()
    
    elif uniform_input == "view class":
        return view_class()
    
    elif uniform_input == "view task": # remove
        pass
    
    elif uniform_input == "help":
        return help()
    
    elif uniform_input == "main menu":
        return 1
    
    elif uniform_input == "filter": # change to edit planner
        pass
    
    elif uniform_input == "update task": # remove
        pass
    
    elif uniform_input == "update class": # remove
        pass
    
    elif uniform_input == "complete task":
        complete_task()
    
    elif uniform_input == "exit":
        return 0
    
    else:
        custom_print(mode = 'line')
        custom_print("Not a valid option, try again from Main Menu", "block")
    
    return 1


if __name__ ==  "__main__":
    if not os.path.exists("./planner.csv"):
        with open("./planner.csv", mode = 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerows([["Class_Name", "Total_Points", "Directory_Address"]])
        file.close()
    
    show_homepage()
    
    is_repeat = 1
    
    while(is_repeat):
        user_input = main_menu()
        is_repeat = mm_options(user_input)
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555") 
    socket.send_string("end")
    socket.recv_string()
    socket.close()
    context.term()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556") 
    socket.send_string("end")
    socket.recv_string()
    socket.close()
    context.term()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557") 
    socket.send_string("end")
    socket.recv_string()
    socket.close()
    context.term()
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558") 
    socket.send_string("end")
    socket.recv_string()
    socket.close()
    context.term()
    
    custom_print(mode = "line")
    custom_print("Thank you for using prO(1), all progress is saved.", "center")
    custom_print(mode = "line")

#              ____   __  __   __
#             / __ \ / / /_ |  \ \
#  _ __  _ __| |  | | |   | |   | |
# | '_ \| '__| |  | | |   | |   | |
# | |_) | |  | |__| | |   | |   | |
# | .__/|_|   \____/ \ \ |___| / /
# | |                      
# |_|

# Microservices:
# A. Load and Display Planner
# B. Load and Display Task
# C. Load and Display Class
# D. Filter Planner