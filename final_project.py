# reference: https://tma15.github.io/blog/2020/11/14/pythonargparseの使い方-入門編/
import argparse
# Use pickle to save and extract data
import pickle
# To record what time a new task object is created 
import time
# To show in table formats 
from tabulate import tabulate

def time_format(input):
    """Format the time in a certain way"""
    s = time.localtime(input)
    # format the time in XXX
    # reference: https://www.tutorialspoint.com/python/time_strftime.htm1 (650) 889-0583
    created_format = time.strftime("%a %b %d %H:%M:%S %Z %Y ", s)  
    return created_format

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

    # set the id blank at first
    self.id = ""
    # store the time the object is created 
    # reference: https://note.nkmk.me/python-datetime-timedelta-measure-time/
    self.created = time.time()
    # First, set the status as "-"
    self.completed = "-"
    # To record the time it's completed 
    self.completed_time = "-"
    self.name = name
    self.priority = priority

    # if due_date is blank, put "-" instead
    if due_date == False:
        self.due_date = "-"
    else:
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
        # if there's no content, skip the loading
        try: 
            # open .todo.pickle file
            with open('.todo.pickle','rb') as f:
                self.tasks = pickle.load(f)
        except:
            pass

    def pickle_tasks(self):
        """Picle your task list to a file"""
        # write the tasks to the file
        with open('.todo.pickle','wb') as f:
            pickle.dump(self.tasks,f)

    def add(self,task):
        """Add the command input to self.tasks"""
        
        # pick up a taks with the largest id from tasks
        ids = []
        for i in self.tasks:
            try: 
                id = int(i.id)
                ids.append(id)
            except:
                pass
    
        # add an id that is one bigger than the largest id
        try:
            task.id = max(ids) + 1
        except:
            task.id = 1
        # add the task to the tasks
        self.tasks.append(task)
        print("Created task {}".format(task.id))
    
    def list(self):
        """Show the data in a table format""" 
        # Put elements of each task in data
        data = []
        for i in self.tasks:
            
            # If the status of a task is completed, put the task in the data list
            if i.completed == "-":                      
                # Record the time to calculate the age of a task 
                now = time.time()
                # result is in minutes so divide by all the seconds in a day
                age = round((now - i.created)/ (60*24*60))
                # The elements are id, due date, priority and task name
                line = (i.id, '%sd'%age, i.due_date, i.priority, i.name )
                data.append(line)

            # If the status is not completed, do not put the task in the list        
            else:
                pass
        
        # sort the data by due date (third element)
        # reference: https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
        sorted_by_third = sorted(data, key=lambda tup: tup[2], reverse=True)

        # Print out in a table format using "tabulate"
        # reference: https://dev.classmethod.jp/articles/python-tabulate/
        print(tabulate(sorted_by_third, headers=['ID','Age', 'Due Date', 'Priority', 'Task']))

    def done(self,id):
        """change the "completed" element into "done"""
        # Create a new list to which I put renewed tasks 
        new_list = []
        for i in self.tasks:
            # if the object's id matches the user input, change the status
            if i.id == int(id):
                # record it as done
                i.completed = "done"
                # record the time it's marked done
                i.completed_time = time.time()
                new_list.append(i)
            else:
                new_list.append(i)

        self.tasks = []
        for i in new_list:
            self.tasks.append(i)

    def delete(self,id):
        """delete a selected task"""
        
        new_list = []
        for i in self.tasks:
            # if the object's id matches the user input, skip adding to the new list
            if i.id == int(id):
                pass
            else:
                new_list.append(i)

        # put the new list into the tasks    
        self.tasks = new_list

    def report(self):
        
        data = []
        for i in self.tasks:
            now = time.time()
            # The result is in minutes so divide by all the seconds in a day
            age = round((now - i.created)/ (60*24*60))
            # if the task is not completed, do not show the completed time
            if i.completed == "-":
                line = (i.id, '%sd'%age, i.due_date, i.priority, i.name, time_format(i.created),"-")
            else:
                line = (i.id, '%sd'%age, i.due_date, i.priority, i.name, time_format(i.created),time_format(i.completed_time))
            data.append(line)
        
        # sort the data by due date (third element)
        # reference: https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
        sorted_by_third = sorted(data, key=lambda tup: tup[2], reverse=True)
        
        print(tabulate(sorted_by_third, headers=['ID','Age', 'Due Date', 'Priority', 'Task', 'Created', 'Completed' ]))
            
    def query(self,word):
        
        list = []
        # for every string o
        for w in word:

            for i in self.tasks:
                
                # if the queried word matches a task name and the task is not completed
                if w == i.name and i.completed == "-":
                    list.append(i)
        
        data = []
        for i in list:            
            now = time.time()
            # result is in minutes so divide by all the seconds in a day
            age = round((now - i.created)/ (60*24*60))
            line = (i.id, '%sd'%age, i.due_date, i.priority, i.name)
            data.append(line)

        # sort the data by due date (third element)
        # reference: https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
        sorted_by_third = sorted(data, key=lambda tup: tup[2], reverse=True)

        print(tabulate(sorted_by_third, headers=['ID','Age', 'Due Date', 'Priority', 'Task']))

# Make a Tasks instance 
x = Tasks()

# Use argparse to take user input
# reference: https://tma15.github.io/blog/2020/11/14/pythonargparseの使い方-入門編/
parser = argparse.ArgumentParser('Task Manager')

parser.add_argument('--list', help='input', action ='store_true')
parser.add_argument('--report', help='input', action ='store_true')
parser.add_argument('--done', help='input', type=int)
parser.add_argument('--delete', help='input', type=int)
parser.add_argument('--query', type=str, required=False, nargs="+", help="priority of task; default value is 1")
parser.add_argument('--add', help='input')
parser.add_argument('--due_date', default="-", help='input')
# reference: https://stackoverflow.com/questions/15301147/python-argparse-default-value-or-specified-value
parser.add_argument('--priority', help='input', type=int, default=1)
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
    x.query(args.query)
else: 
    if args.add:
        y = Task(args.add,args.priority,args.due_date)
        x.add(y)
        x.pickle_tasks()
    else:
        print("You need to input task name")