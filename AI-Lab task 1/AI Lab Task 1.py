def to_do_list():
    tasks=[]
    while True:
        print("This is the menu")
        print("1. To add task")
        print("2. To remove one task")
        print("3. To clear all tasks")
        print("4. To show tasks")
        print("5. To end task")
        choice=input("choose a number from the menu:")
        if choice=="1":
            task=input("Enter the task:")
            tasks.append(task)
            print("Your task is added")
        elif choice=="2":
            task=input("Enter the task to remove:")  
            if task in tasks:
                tasks.remove(task)
                print("Your task is removed")
            else:
                print("it was not the part of your task enter 1 to add it into your tasks")  
        elif choice=="3":
            tasks.clear()   
            print("tasks cleared successfully")
        elif choice=="4":
            if len(tasks)==0:
                print("oh sorry no task is added yet")
            else:
                print("Your tasks are:")
                for i in range(len(tasks)):
                  print(f"{i+1}.{tasks[i]}")
        elif choice=="5":
            print("program ended")
            break
        else:
            print("invalid choice") 
to_do_list()                   
