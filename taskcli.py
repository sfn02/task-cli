import datetime
import json
import argparse

current_id = 1

class Task:
    ids = set()

    def __init__(self, id, description, status, createdAt, updatedAt):
        if id in Task.ids:
            raise ValueError(f"Id {id} already taken")  
        else:
            self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        Task.ids.add(id)

    def __str__(self):
        return f'''{{
            id : {self.id},
            description : {self.description},
            status : {self.status},
            createdAt : {self.createdAt},
            updatedAt : {self.updatedAt}
        }}'''

    def taskToJSON(self):
        return {
        'id' : self.id,
        'description' : self.description,
        'status' : self.status,
        'createdAt' : self.createdAt,
        'updatedAt' : self.updatedAt
    }


    def update_task(self, description):
        self.description = description
        self.updatedAt = str(datetime.date.today())        

    def mark_in_progress(self):
        self.status = "in-progress"
        self.updatedAt = str(datetime.date.today())

    def mark_done(self):
        self.status = "done"   
        self.updatedAt = str(datetime.date.today())     

    def __del__(self):
        Task.ids.remove(self.id)
        
def load_data():
    global current_id
    tasks = []
    try:
        with open('tasks.txt','r') as file:
            tasks = json.load(file)
            if tasks:
                current_id = tasks[-1]['id']+1
            file.close()    
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return tasks    

def save_data(data):
    with open('tasks.txt','w') as file:
        json.dump(data, file, indent=4)
        file.close()





def add_task(description):
    global current_id
    tasks = load_data()
    date_today = str(datetime.date.today())
    tsk = Task(current_id, description, "todo", date_today, date_today)
    current_id += 1
    tasks.append(tsk.taskToJSON())
    save_data(tasks)

    


def update_task(id, description):
    tasks = load_data()
    for tsk in tasks:
        if tsk['id'] == id:
            task = Task(**tsk)
            task.update_task(description)
            tsk.update(task.taskToJSON())
            save_data(tasks)

def mark_in_progress(id):
    tasks = load_data()  
    print(tasks)
    for tsk in tasks:
        if tsk["id"] == id:
            task = Task(**tsk) 
            task.mark_in_progress() 
            tsk['status'] = task.status
            tsk['updatedAt'] = task.updatedAt
            save_data(tasks)  
            print(f"Task with ID {id} marked as in-progress.")
            return 
    print(f"Task with ID {id} not found.")

def mark_done(id):
    tasks = load_data()
    for tsk in tasks:
        if tsk['id'] == id:
            task = Task(**tsk)
            task.mark_done()
            tsk['status'] = task.status
            tsk['updatedAt'] = task.updatedAt
            save_data(tasks) 
            print(tsk) 
            print(f"Task with ID {id} marked as done.")
            return 
    print(f"Task with ID {id} not found.")  


def delete_task(id):
    tasks = load_data()
    for tsk in tasks:
        if tsk['id'] == id:
            tasks.remove(tsk)
            save_data(tasks)    
            print(f"task with id {id} deleted successfully >_") 
            return
    print(f"task with id {id} was not fount :'(")   

def list_task(status):
    tasks = load_data()
    for tsk in tasks:
        if tsk['status'] == status:
            print(tsk)

def list_all():
    tasks = load_data()
    for tsk in tasks:
        print(tsk)

def main():
    global tasks
    
    parser = argparse.ArgumentParser(description="CLI task manager")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('task', help='What task you would like to do')

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('status', choices=['todo', 'in-progress', 'done'], nargs='?')

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('id', type=int, help='ID of the task')
    update_parser.add_argument('description', help='New description of the task')

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('id', type=int, help='ID of the task to delete')

    mark_in_progress_parser = subparsers.add_parser('mark-in-progress')
    mark_in_progress_parser.add_argument('id',help='id of the task to mark in progress')

    mark_done_parser = subparsers.add_parser('mark-done')
    mark_done_parser.add_argument('id',help='id of the task to mark done')

    args = parser.parse_args()

    command = args.command

    match command:
        case 'add':
            add_task(args.task)
            print(f"task added successfully :)")

        case 'update':
            update_task(args.id, args.description)
            list_task("todo")  
        case 'delete':
            delete_task(int(args.id)) 
            

        case 'mark-in-progress':
            mark_in_progress(int(args.id))

        case 'mark-done':
            mark_done(int(args.id))
            
        case 'list':
            if args.status is None:
                list_all()
            else:
                list_task(args.status)

if __name__ == "__main__":
    main()

