# reference: https://tma15.github.io/blog/2020/11/14/pythonargparseの使い方-入門編/
import argparse
# Use pickle to save and extract data
import pickle

# To record what time a new task object is created 
import time

class Task:
  """Representation of a task
  
  Attributes:
    created: date
    completed: date
    name: string
    unique id: number
    priority: int value of 1, 2, or 3; 1 is default
    due date: date, this is optional
  """
  def __init__(self,name,priority,due_date):
    # record the time the new object is created
    
    # set the id black at first
    self.id = ""
    # store the time the object is created 
    self.created = time.ctime()
    self.completed = "not completed"
    self.name = name
    self.priority = priority
    self.due_date = due_date
    

class Tasks:
    """A list of `Task` objects.
    
    Attributes:
     tasks: list of tasks
    """

    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = [] 
        # your code here
        # open .todo.pickle file
        with open('.todo.pickle','rb') as f:
            self.tasks = pickle.load(f)

    def pickle_tasks(self):
        """Picle your task list to a file"""
        # your code here
        with open('.todo.pickle','wb') as f:
            pickle.dump(self.tasks,f)

    def add(self,task):
        """Add the command input to self.tasks"""
        
        # pick up an object with the largest id from tasks
        ids = []
        for i in self.tasks:
            try: 
                id = int(i.id)
                ids.append(id)
            except:
                pass
    
        # add an id that's one bigger than the largest id
        try:
            task.id = max(ids) + 1
        except:
            task.id = 1

        self.tasks.append(task)
        print("Created task")
    
    def list(self):
        print("ID  Age  Due Date  Priority  Task")
        print("--  ---  --------  --------  ----")
        for i in self.tasks:
            if i.completed == "not completed":            
                try:
                    print("{} {} {} {} {}".format(i.id,i.created,i.due_date,i.priority,i.name))
                except:
                    print("{} {} {}".format(i.due_date,i.priority,i.name))
            else:
                pass

    def done(self,id):
        """change the "completed element" into "done"""
        new_list = []
        for i in self.tasks:
            try:
                # if the object's id matches the user input, change the status
                if i.id == int(id):
                    i.completed = "done"
                    new_list.append(i)
                else:
                    new_list.append(i)
            except:
                new_list.append(i)

        self.tasks = []
        for i in new_list:
            print(i.name)
            print(i.completed)
            self.tasks.append(i)

        #for i in self.tasks:
        #    print(i.name)
        #    print(i.completed)

    def delete(self,id):
        """delele a selected task"""
        new_list = []
        for i in self.tasks:
            try:
                # if the object's id matches the user input, skip adding to the new list
                if i.id == int(id):
                    pass
                else:
                    new_list.append(i)
            except:
                pass
        
        self.tasks = new_list

    def report(self):
        print("ID  Age  Due Date  Priority  Task  Created  Completed")
        print("--  ---  --------  --------  ----  -------  ---------")
        for i in self.tasks:            
            try:
                print("{} {} {} {} {} {} {}".format(i.id,i.created,i.due_date,i.priority,i.name, i.created,i.completed))
            except:
                print("{} {} {}".format(i.due_date,i.priority,i.name))

# Make a Task instance 

# print(y.name)

# Make a Tasks instance 
x = Tasks()

parser = argparse.ArgumentParser('Task Manager')

parser.add_argument('--list', help='input', action ='store_true')
parser.add_argument('--report', help='input', action ='store_true')
parser.add_argument('--done', help='input', type=int)
parser.add_argument('--delete', help='input', type=int)
parser.add_argument('--query', help='input', action ='store_true')
parser.add_argument('--add', help='input')
parser.add_argument('--due_date', help='input')
parser.add_argument('--priority', help='input', type=int)
args = parser.parse_args()

# Depending on the command the user chooses, execute a different function 
# reference: https://tma15.github.io/blog/2020/11/14/pythonargparseの使い方-入門編/#指定必須の引数を定義する
if args.list:
    x.list()
elif args.report:
    x.report()
elif args.done:
    x.done(args.done)
    x.pickle_tasks()
elif args.delete:
    x.delete(args.delete)
    x.pickle_tasks()
elif args.query:
    print('Query')
else: 
    if args.add and args.priority:
        y = Task(args.add,args.priority,args.due_date)
        x.add(y)
        x.pickle_tasks()
    else:
        print("You need to input task name and priority")
    


# parser.add_argument('--query', help='input')

# parser.add_argument('x')  # 位置引数
# parser.add_argument('-i')  # optional引数



# x.add(y)
# x.pickle_tasks()
# if args.list:   
    


# check if the pickle file contains anything
# temp = []
# with open('.todo.pickle','rb') as f:
#    temp = pickle.load(f)
#    for i in temp:
#        print(i)
