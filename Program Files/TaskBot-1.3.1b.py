from tkinter import *
import time
import pickle
import random


# noinspection SpellCheckingInspection
def TaskGUI(task):
    DueDate = task['DueDate']
    DueDateString = str(DueDate[0]) + '.' + str(DueDate[1]) + '.' + str(DueDate[2]) + ' ' + str(DueDate[3]) + ':' + str(
        DueDate[4])
    if task['Upload']:
        UploadString = 'Ja'
    else:
        UploadString = 'Nein'
    if task['Done']:
        DoneString = 'Ja'
    else:
        DoneString = 'Nein'
    TaskTk = Tk()
    TaskTk.title('Aufgabe - ' + task['Name'])
    Label(TaskTk, text='Aufgabe: ' + task['Name']).grid(column=0, row=0)
    Label(TaskTk, text='Beschreibung: ' + task['Description']).grid(column=0, row=1)
    Label(TaskTk, text='Zu erledigen bis: ' + DueDateString).grid(column=1, row=0)
    Label(TaskTk, text='Priorität: ' + task['Priority']).grid(column=1, row=2)
    Label(TaskTk, text='Erledigt: ' + DoneString).grid(column=1, row=3)
    Label(TaskTk, text='Hochzuladen: ' + UploadString).grid(column=1, row=4)

    def Done():
        load = open('tasks.dat', 'rb')
        tasks = pickle.load(load)
        load.close()
        for x in range(0, len(tasks)):
            Task = tasks[x]
            if Task['Name'] == task['Name']:
                Task['Done'] = True
                write = open('tasks.dat', 'wb')
                tasks[x] = Task
                pickle.dump(tasks, write)
                write.close()
                TaskTk.destroy()
                TaskGUI(Task)
                break

    Button(TaskTk, text='Erldeigt', command=Done).grid(column=0, row=2)
    Button(TaskTk, text='Schließen', command=TaskTk.destroy).grid(column=0, row=3)


def PingGUI(task):
    def show():
        TaskGUI(task)

    DueDate = task['DueDate']
    DueDateString = str(DueDate[0]) + '.' + str(DueDate[1]) + '.' + str(DueDate[2]) + ' ' + str(DueDate[3]) + ':' + str(
        DueDate[4])
    Name = task['Name']
    Description = task['Description']
    Ping = Tk()
    Ping.title('Erinnerung - ' + Name)
    Label(Ping, text='Aufgabe: ' + Name).pack()
    Label(Ping, text='Beschreibung: ' + Description).pack()
    if task['Upload']:
        Label(Ping, text='Die Aufgabe muss bis zum ' + DueDateString + ' abgeben und hoch geladen werden.').pack()
    else:
        Label(Ping, text='Die Aufgabe muss bis zum ' + DueDateString + 'abgeben werden.')
    Button(Ping, text='Anzeigen', command=show).pack()
    Button(Ping, text='Schließen', command=Ping.destroy).pack()


def DayDiffTODAY(Time):
    due = time.mktime(Time)
    today = time.mktime(time.localtime())
    secDiff = int(due - today)
    if secDiff < 1:
        return 'ERROR'
    return secDiff


def TopTask():
    loadTasks = open('tasks.dat', 'rb')
    try:
        Tasks = pickle.load(loadTasks)
    except EOFError:
        Tasks = list()
    loadTasks.close()
    NotDoneTasks = []
    if not Tasks:
        return None
    for x in range(0, len(Tasks)):
        Task = Tasks[x]
        if not Task['Done']:
            NotDoneTasks.append(Task)
    DateObjective = []
    SelectedTasks = []
    for x in range(0, len(NotDoneTasks)):
        Task = NotDoneTasks[x]
        Date = Task['DueDate']
        Diff = DayDiffTODAY((Date[2], Date[1], Date[0], Date[3], Date[4], 0, 0, 0, 0))
        if Diff == 'ERROR':
            pass
        else:
            DateObjective.append(Diff)
    for x in range(0, len(DateObjective)):
        Task = NotDoneTasks[x]
        Date = Task['DueDate']
        Diff = DayDiffTODAY((Date[2], Date[1], Date[0], Date[3], Date[4], 0, 0, 0, 0))
        if Diff == 'ERROR':
            pass
        elif Diff[2] == min(DateObjective):
            SelectedTasks.append(Task)
    SelectedTasks_OLD = SelectedTasks
    Red = []
    Yellow = []
    Green = []
    for x in range(0, len(SelectedTasks_OLD)):
        Task = SelectedTasks_OLD[x]
        Priority = Task['Priority']
        if Priority == 'Rot':
            Red.append(Task)
        elif Priority == 'Gelb':
            Yellow.append(Task)
        elif Priority == 'Grün':
            Green.append(Task)
    if not Red:
        if not Yellow:
            SelectedTasks = Green
        else:
            SelectedTasks = Yellow
    else:
        SelectedTasks = Red
    random.shuffle(SelectedTasks)
    try:
        return SelectedTasks[0]
    except IndexError:
        return {
            'Name': 'Du hast alle Aufgaben erledigt oder noch keine eingetragen',
            'DueDate': '--------'
        }


def callTop():
    topTask = TopTask()
    TaskGUI(topTask)


def addTask(name, description, dueDate, priority, upload):
    Date = [time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year, time.localtime().tm_hour,
            time.localtime().tm_min]
    Done = False
    loadTask = open('tasks.dat', 'rb')
    tasks = pickle.load(loadTask)
    loadTask.close()
    Task = {
        'Name': name,
        'Description': description,
        'DueDate': dueDate,
        'Priority': priority,
        'Upload': upload,
        'Date': Date,
        'Done': Done,
        'DoneDate': []
    }
    tasks.append(Task)
    saveTask = open('tasks.dat', 'wb')
    pickle.dump(tasks, saveTask)
    saveTask.close()
    confirm = Tk()
    confirm.title('Aufgabe hinzugefügt!')
    Label(confirm, text='Die Aufgabe ' + name + ' wurde hinzugefügt.').pack()
    Button(confirm, text='OK', command=confirm.destroy).pack()


def NewTask():
    newTask = Tk()
    newTask.title('Neue Aufgabe')
    Label(newTask, text='Aufgabe:').grid(column=0, row=0)
    Task = Entry(newTask, width=100)
    Task.grid(column=1, row=0)
    Label(newTask, text='Beschreibung:').grid(column=0, row=1)
    Description = Entry(newTask, width=100)
    Description.grid(column=1, row=1)
    Label(newTask, text='     Zu erledigen bis:').grid(column=2, row=0)
    Day = Entry(newTask, width=2)
    Day.grid(column=3, row=0)
    Label(newTask, text='.').grid(column=4, row=0)
    Month = Entry(newTask, width=2)
    Month.grid(column=5, row=0)
    Label(newTask, text='.').grid(column=6, row=0)
    Year = Entry(newTask, width=4)
    Year.grid(column=7, row=0)
    Label(newTask, text=' ').grid(column=8, row=0)
    Hour = Entry(newTask, width=2)
    Hour.grid(column=9, row=0)
    Label(newTask, text=':').grid(column=10, row=0)
    Minute = Entry(newTask, width=2)
    Minute.grid(column=11, row=0)
    Priorities = (
        'Rot',
        'Gelb',
        'Grün'
    )
    Priority = StringVar(newTask)
    Priority.set('Auswählen')
    Label(newTask, text='Priorität:').grid(column=2, row=1)
    OptionMenu(newTask, Priority, *Priorities).grid(column=3, row=1)
    Upload = IntVar(newTask)
    Checkbutton(newTask, text='Hochladen?', variable=Upload).grid(column=3, row=2)

    def Format():
        addTask(Task.get(), Description.get(),
                [int(Day.get()), int(Month.get()), int(Year.get()), int(Hour.get()), int(Minute.get())], Priority.get(),
                bool(Upload.get()))
        newTask.destroy()

    Button(newTask, text='Hinzufügen', command=Format).grid(column=1, row=2)
    Button(newTask, text='Zurück', command=newTask.destroy).grid(column=1, row=3)


def listNames():
    loadTasks = open('tasks.dat', 'rb')
    try:
        Tasks = pickle.load(loadTasks)
    except EOFError:
        Tasks = list()
    loadTasks.close()
    Names = list()
    for x in range(0, len(Tasks)):
        Task = Tasks[x]
        Names.append(Task['Name'])
    return Names


def checkPing():
    loadTasks = open('tasks.dat', 'rb')
    try:
        Tasks = pickle.load(loadTasks)
    except EOFError:
        Tasks = list()
    loadTasks.close()
    for x in range(0, len(Tasks)):
        Task = Tasks[x]
        if not Task['Done']:
            DueDate = Task['DueDate']
            Time = (DueDate[2], DueDate[1], DueDate[0], DueDate[3], DueDate[4], 0, 0, 0, 0)
            secDiff = DayDiffTODAY(Time)
            if secDiff == 'ERROR':
                pass
            elif secDiff <= 259200:
                PingGUI(Task)


def ManageTasks():
    seeTask = Tk()
    seeTask.title('Aufgabe anzeigen')
    Tasks = listNames()
    if Tasks != list():
        Selected = StringVar(seeTask)
        Selected.set('--Auswählen--')
        OptionMenu(seeTask, Selected, *Tasks).pack()

        # noinspection PyShadowingNames
        def call():
            loadTasks = open('tasks.dat', 'rb')
            try:
                Tasks = pickle.load(loadTasks)
            except EOFError:
                Tasks = list()
            loadTasks.close()
            for x in range(0, len(Tasks)):
                Task = Tasks[x]
                if Task['Name'] == Selected.get():
                    TaskGUI(Task)

        Button(seeTask, text='Aufgabe öffnen', command=call).pack()
        Button(seeTask, text='Zurück', command=seeTask.destroy).pack()
        Label(seeTask,
              text='                                                                                       ').pack()
    else:
        Label(seeTask, text='Du hast keine Aufgaben eingetragen')


def main():
    tk = Tk()
    tk.title('TaskBot')
    Button(tk, text='Aufgabe hinzufügen', command=NewTask).pack()
    Label(tk, text='===============================================').pack()

    def displayTopTask():
        topTask = TopTask()
        if topTask is not None:
            Label(tk, text=topTask['Name']).pack()
            DueDate = topTask['DueDate']
            DueDateString = str(DueDate[0]) + '.' + str(DueDate[1]) + '.' + str(DueDate[2]) + ' ' + str(
                DueDate[3]) + ':' + str(DueDate[4])
            Label(tk, text=DueDateString).pack()
            Button(tk, text='Anzeigen', command=callTop).pack()
        else:
            Label(tk, text='Du hast anscheinend keine Aufgaben gespeichert.').pack()
            Button(tk, text='Aktualisieren', command=displayTopTask).pack()

    Label(tk, text='===============================================').pack()
    Button(tk, text='Aufgaben vervalten', command=ManageTasks).pack()
    Label(tk, text='===============================================').pack()
    Button(tk, text='Benachrichtigungen prüfen', command=checkPing).pack()
    Label(tk, text='===============================================').pack()
    Button(tk, text='Schließen', command=exit).pack()
    Label(tk, text='===============================================').pack()
    Label(tk, text='Version 1.3.1b | TaskBot | 18.03.2021 | 11:30').pack()
    checkPing()
    mainloop()


def install():
    try:
        start = open('tasks.dat', 'xb')
    except FileExistsError:
        start = open('tasks.dat', 'wb')
    empty = list()
    pickle.dump(empty, start)
    start.close()
    main()


try:
    test = open('tasks.dat', 'wb')
except FileNotFoundError:
    install()

main()
