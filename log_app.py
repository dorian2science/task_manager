import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from babel.dates import format_datetime
import task_manager as tm
from pandastable import Table, TableModel

def format_pretty_table(df):
    # Define custom formatting for header
    def bold_header(col):
        return f"\033[1m{col}\033[0m"

    # Apply custom formatting to the header
    formatted_columns = [bold_header(col) for col in df.columns]

    # Display the header with column separation using bars
    header_str = ' | '.join(formatted_columns)

    # Display the data
    data_str = df.to_string(index=False, header=False, justify='left')

    # Concatenate the header and data
    result = f"{header_str}\n{data_str}"
    return result

def change_text(widget,text):
    widget['state'] = 'normal'
    # df = format_pretty_table(df)
    widget.delete("1.0", "end")
    widget.insert(tk.END,text)
    widget['state'] = 'disabled'

def update():
    # print('updating')
    tm.DF_LOG_HOURS = tm.format_log_hours()
    # print('update',tm.DF_LOG_HOURS[['t1','task']].head())
    df = tm.DF_LOG_HOURS[['debut','fin','time elapsed','task','categorie']].head()
    change_text(df_log,df.to_string())

    change_text(log_week,tm.get_hours_in_week().to_string())

    change_text(log_month,tm.get_total_hours_weeks().to_string())

    nb_working_days_text.set(str(tm.get_nb_working_days_month()))

    d = tm.get_hours_avrg_day()
    hours_avr_txt.set(str(d['mean']))
    hours_min_txt.set(str(d['min']))
    hours_max_txt.set(str(d['max']))
    nb_days_count_txt.set(str(d['count']))

    change_text(log_cat,tm.get_hours_per_categorie().to_string())

def start():
    text_content = task_fill_area.get("1.0", tk.END)  # Get text content from the beginning to the end
    tm.add_task(text_content)
    task_fill_area.delete("1.0", tk.END)
    update()

def stop():
    tm.complete_job()
    task_fill_area.delete("1.0", tk.END)
    # messagebox.showinfo("Info", "Stop function triggered")

def on_key_press(event):
    # print('entered on key press')
    # print(event.keysym)
    # print(event.state)
    if event.keysym == "Return" and event.state == 12:  # Check for Ctrl+Enter
        start()
    if event.keysym == "f" and event.state == 12:  # Check for Ctrl+Enter
        stop()

def predefined_task(task):
    # messagebox.showinfo("Info", f"Button clicked: {task}")
    task_fill_area.delete("1.0", "end")  # Clear existing text
    task_fill_area.insert("1.0", task)
    # start()

# Create main application window
root = tk.Tk()
# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate window size to be half of the screen size
window_width = round(screen_width / 1.5)
window_height = round(screen_height / 1.5)

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{window_width//4}+{window_height//4}")
root.title("Task Manager")

# Create a Notebook widget
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill='both')

tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Tasks fill')

task_fill_area = tk.Text(tab1, width=50, height=5)
task_fill_area.place(x=0, y=0, relwidth=0.8, relheight=0.5)

button_frame = tk.Frame(tab1)
button_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

button1 = tk.Button(button_frame, text="work_planification",font=("Arial", 12),command=lambda: predefined_task("work_planification"))
button1.pack(fill=tk.X)

button2 = tk.Button(button_frame, text="meeting",font=("Arial", 12),command=lambda: predefined_task("meeting_"))
button2.pack(fill=tk.X)

button3 = tk.Button(button_frame, text="issue_smartsupervision",font=("Arial", 12),command=lambda: predefined_task("issue_smartsupervision_"))
button3.pack(fill=tk.X)

button4 = tk.Button(button_frame, text="issue_setupmanagement",font=("Arial", 12),command=lambda: predefined_task("issue_setupmanagement_"))
button4.pack(fill=tk.X)

button5 = tk.Button(button_frame, text="pause",font=("Arial", 12),command=lambda: predefined_task("pause"))
button5.pack(fill=tk.X)


start_finish_frame = tk.Frame(tab1)
start_finish_frame.place(x=0, rely=0.5)
# Create start button
start_button = tk.Button(start_finish_frame, text="Start task", command=start, height=2, width=20)  # Adjust button size
start_button.grid(row=0,column=0)
finish_button = tk.Button(start_finish_frame, text="Finish task", command=stop, height=2, width=20)  # Adjust button size
finish_button.grid(row=0,column=1)
# finish_button.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)


frame_df = tk.Frame(tab1)
frame_df.place(x=0, rely=0.62,relwidth=1)

# canvas = tk.Canvas(frame_df)
# canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

df_log = tk.Text(frame_df, font=("Courier", 15), wrap="none",width=150)
df_log.pack()


# pt = Table(canvas, dataframe=pd.read_csv(FULL_LOG,index_col=0).head(), showtoolbar=True, showstatusbar=True)
# pt.show()
#
# scrollbar = tk.Scrollbar(frame_df, orient="vertical", command=canvas.yview)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# canvas.configure(yscrollcommand=scrollbar.set)
# canvas.create_window((0, 0), window=pt, anchor="nw")
# pt.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.bind("<Return>", on_key_press)
root.bind("<f>", on_key_press)

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Work Summary')

tk.Label(tab2, text='Hours every day this week:').pack()
log_week = tk.Text(tab2,font=("Courier", 15),width=50,height=8)
log_week.pack()

tk.Label(tab2, text='Total hours spent each week this month:').pack()
log_month = tk.Text(tab2, font=("Courier", 15),width=50,height=7)
log_month.pack()


def create_frame_label(tab,label_txt,w):
    f_workdays = ttk.Frame(tab)
    f_workdays.pack()
    lm=tk.Label(f_workdays, text=label_txt)
    txt_var = tk.StringVar()
    em=tk.Entry(f_workdays,textvar=txt_var,  font=("Courier", 15),width=w,state='readonly')
    lm.grid(row=0,column=0)
    em.grid(row=0,column=1)
    return txt_var

nb_working_days_text = create_frame_label(tab2,'Number of working days this month:',5)
hours_avr_txt = create_frame_label(tab2,'hours in average:',5)
hours_max_txt = create_frame_label(tab2,'max hours:',5)
hours_min_txt = create_frame_label(tab2,'min hours:',5)
nb_days_count_txt = create_frame_label(tab2,'count days:',5)

tk.Label(tab2, text='Total hours spent on each categorie this month').pack()
log_cat = tk.Text(tab2,font=("Courier", 15),width=50,height=15)
log_cat.pack()

# Lift the window to the front
root.lift()

# Run the application
import threading
import time
class SetInterval:
    '''
    Run the function *action* every *interval* seconds.
    Start on a multiple of *interval*
    Skip intermediate calls if the action takes longer for the interval to start stack.

    :param int interval: time interval
    :param str action: function to execute
    :param args: arguments for function *action*
    '''
    def __init__(self,interval,action,*args):
        self.argsAction=args
        self.interval  = interval
        self.action    = action
        self.stopEvent = threading.Event()
        self.thread    = threading.Thread(target=self.__SetInterval)

    def start(self):
        '''
        Start a new thread
        '''
        self.thread.start()

    def __SetInterval(self):
        nextTime=time.time()
        while not self.stopEvent.wait(nextTime-time.time()):
            self.action(*self.argsAction)
            nextTime+=self.interval
            while nextTime-time.time()<0:
                nextTime+=self.interval

    def stop(self):
        '''
        Stop the active thread
        '''
        self.stopEvent.set()
        self.thread.join()

update_t = SetInterval(60,update)
update_t.start()

def on_closing():
    update_t.stop()
    # print("Executing function on window close")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
