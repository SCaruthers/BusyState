import BusyState as bs
import tkinter as tk
import tkinter.ttk as ttk  #make easy reference to ttk modules
import os
from tkinter import messagebox
from operator import or_
from functools import reduce
from sys import argv 

EXEC_STATE = bs.ES_AWAYMODE_REQUIRED     # Global Variable to hold Execution State Result
MAX_DAYS_TILL_REBOOT = 10                # Global Variable for # days after which to auto alert WinUpTime

help_msg = """
Read and Set the Thread Execution State.  
The following values can be used:\n
ES_AWAYMODE_REQUIRED 
Enables away mode. This value must be specified with ES_CONTINUOUS.
Away mode should be used only by media-recording and media-distribution 
applications that must perform critical background processing on desktop 
computers while the computer appears to be sleeping. See Remarks.

ES_CONTINUOUS
Informs the system that the state being set should remain in effect until the 
next call that uses ES_CONTINUOUS and one of the other state flags is cleared.

ES_DISPLAY_REQUIRED
Forces the display to be on by resetting the display idle timer.

ES_SYSTEM_REQUIRED
Forces the system to be in the working state by resetting the system idle timer.

NOTE:
Calling SetThreadExecutionState without ES_CONTINUOUS simply resets the idle timer; 
to keep the display or system in the working state, the thread must call 
SetThreadExecutionState periodically.

To run properly on a power-managed computer, applications such as fax servers, 
answering machines, backup agents, and network management applications must use 
both ES_SYSTEM_REQUIRED and ES_CONTINUOUS when they process events. Multimedia 
applications, such as video players and presentation applications, must use 
ES_DISPLAY_REQUIRED when they display video for long periods of time without 
user input. Applications such as word processors, spreadsheets, browsers, and 
games do not need to call SetThreadExecutionState.

The ES_AWAYMODE_REQUIRED value should be used only when absolutely necessary 
by media applications that require the system to perform background tasks such 
as recording television content or streaming media to other devices while the 
system appears to be sleeping. Applications that do not require critical background 
processing or that run on portable computers should not enable away mode because it 
prevents the system from conserving power by entering true sleep.

To enable away mode, an application uses both ES_AWAYMODE_REQUIRED and ES_CONTINUOUS; 
to disable away mode, an application calls SetThreadExecutionState with ES_CONTINUOUS 
and clears ES_AWAYMODE_REQUIRED. When away mode is enabled, any operation that would 
put the computer to sleep puts it in away mode instead. The computer appears to be 
sleeping while the system continues to perform tasks that do not require user input. 
Away mode does not affect the sleep idle timer; to prevent the system from entering 
sleep when the timer expires, an application must also set the ES_SYSTEM_REQUIRED value.

The SetThreadExecutionState function cannot be used to prevent the user from putting 
the computer to sleep. Applications should respect that the user expects a certain 
behavior when they close the lid on their laptop or press the power button.
"""

# Note: Command Line Argument handling below GUI code

def getExecState():
    """Function to call the imported function to read state"""
    return bs.getWinState()

def GetButtonAction():
    """Function to run when 'Get Current' button is clicked"""
    global EXEC_STATE
    #print('Get Button Press.  state = ', setCurrent_btn.state())
    SetBtnStatus(tk.DISABLED)
    
    EXEC_STATE = getExecState()
    # Set Button States based on EXEC_STATE value
    for i,k in enumerate(cb_items):
        cb_val[i].set(EXEC_STATE & cb_items[k])
    ReadBtns()

def SetButtonAction():
    global EXEC_STATE
    #print('Set Button Press.  state = ', setCurrent_btn.state())
    ChangeBtnStatus()
    EXEC_STATE = ReadBtns()
    if EXEC_STATE == 0:
        success = None
    else:
        success = bs.setWinState(EXEC_STATE)
    #print(success)
    if success == [] or success == None:
        messagebox.showerror(title='Error', message='Failed to set Event State')


def ChangeBtnStatus():
    """Function to swap state of 'Set Current' button"""
    if setCurrent_btn.instate([tk.DISABLED]):
        #print('it was DISABLED', setCurrent_btn.state())
        setCurrent_btn['state'] = tk.ACTIVE
    else:
        #print('it was NORMAL', setCurrent_btn.state())
        setCurrent_btn['state'] = tk.DISABLED

def SetBtnStatus(stat):
    """Function to set the state of 'Set Current' button"""
    # Should pass only tk.ACTIVE or tk.DISABLED
    setCurrent_btn['state'] = stat
    

def CheckedBtn():
    SetBtnStatus(tk.ACTIVE)
    ReadBtns()

def ReadBtns():
    """Function to read the Checkbuttons and calculate value"""
    v = [i.get() for i in cb_val]
    vv = reduce(or_, v)
    #print(v, vv)
    return vv

def DisplayHelp():
    global help_msg
    top = tk.Toplevel(window)
    top.geometry('535x790')
    top.title('Help...')
    ttk.Label(top, text=help_msg).pack()

def timeString():
    """Helper function to create the StringVar for the WinUpTime call"""
    u_name = os.environ.get('USERNAME')
    boot_time = bs.getWinBootTime() # returns [hr, min, sec] since boot
    days, hrs = divmod(boot_time[0], 24)
    oc = ' and '
    return_msg = f"\nWindows was started by {u_name.upper()}\n"
    if (days > 0):
        return_msg += f"{days} day{'' if (days==1) else 's'}, "
        oc = ', and '
    if (hrs > 0):
        return_msg += f"{hrs} hour{'s' if (hrs>1) else ''}, "
        return_msg += f"{boot_time[1]} minute{'' if (boot_time[1]==1) else 's'}, and "
    elif(boot_time[1] > 0):
        return_msg += f"{boot_time[1]} minute{'' if (boot_time[1]==1) else 's'}" + oc
    
    return_msg += f"{boot_time[2]} second{'' if (boot_time[2]==1) else 's'} ago."
    return return_msg

def DisplayWinUpTime():
    """Callback function to display a dialog box with the time since Windows was booted."""
    c_name = os.environ.get('COMPUTERNAME')
    top2 = tk.Toplevel(window)
    #my_msg = tk.StringVar(top2, timeString())
    top2.geometry('330x90')
    top2.minsize(270,90)
    top2.title(f"{c_name} Boot Time")
    top2.attributes('-topmost', 'true')
    msg_lbl = ttk.Label(top2, text='', anchor=tk.CENTER, justify=tk.CENTER, wraplength = 268)
    msg_lbl.pack()
    OK_btn = tk.Button(top2, text="OK", command=top2.destroy)
    OK_btn.pack(pady=7)
    top2.bind('<Return>', (lambda event: top2.destroy()))
    top2.focus()
    OK_btn.focus()
    updateTimeDWUT(top2, msg_lbl)

def updateTimeDWUT(wn, lbl):
    """Callback function to change the label lbl in window wn as time changes"""  
    if (wn.winfo_exists()):
        lbl['text'] = timeString()
        lbl['foreground'] = 'red3' if (bs.getWinBootTime()[0] >= 120) else 'dark green'
        wn.after(1000, lambda: updateTimeDWUT(wn, lbl))

def shortcutSetBusy():
    """Callback function to set state to 'busy' to prevent screen saver, etc."""
    # set only ES_CONTINUOUS and ES_DISPLAY_REQUIRED
    cb_val[0].set(bs.ES_CONTINUOUS)
    cb_val[1].set(0)
    cb_val[2].set(bs.ES_DISPLAY_REQUIRED)
    cb_val[3].set(0)
    
    # then "press" the Set State button.    
    setCurrent_btn['state'] = tk.ACTIVE
    setCurrent_btn.invoke()    
    return True

def shortcutSetNormal():
    """Callback function to set state to 'normal', e.g., to allow screen saver."""
    # set only ES_CONTINUOUS
    cb_val[0].set(bs.ES_CONTINUOUS)
    cb_val[1].set(0)
    cb_val[2].set(0)
    cb_val[3].set(0)
    
    # then "press" the Set State button.    
    setCurrent_btn['state'] = tk.ACTIVE
    setCurrent_btn.invoke()    
    return True

def CheckWinUpTime(d = 10):
    """Callback function to check Windows 'up time' since last reboot, and
    automatically open the alert window if greater than 'd' days."""
    if (bs.getWinBootTime()[0] >= (d*24)):
        DisplayWinUpTime()

# make main window and variables
window = tk.Tk()
window.geometry( "300x300" )
window.title( 'Thread Execution State' )
window.minsize(250,275)
greeting = ttk.Label(text='READ and CHANGE\nthe Thread Execution State', 
                    anchor=tk.CENTER, 
                    justify=tk.CENTER)
greeting.pack(pady=5)

# make button to read current state
getCurrent_btn = ttk.Button(window, 
                            text="Get Current State",
                            command=GetButtonAction,
                            padding=8,
                            width=30)
getCurrent_btn.pack()

# Create Frame to hold the Check Buttons:
frm = ttk.Frame(window, borderwidth=3, relief='ridge')
frm.pack(pady=10)

# Set up Radio Buttons for Readout Area
cb_val = []
cb = []
cb_items = {
            'ES_CONTINUOUS':bs.ES_CONTINUOUS, 
            'ES_SYSTEM_REQUIRED':bs.ES_SYSTEM_REQUIRED, 
            'ES_DISPLAY_REQUIRED':bs.ES_DISPLAY_REQUIRED, 
            'ES_AWAYMODE_REQUIRED':bs.ES_AWAYMODE_REQUIRED
            }
for i,k in enumerate(cb_items):
    cb_val.append(tk.IntVar())
    cb.append( ttk.Checkbutton(frm, 
                                variable=cb_val[i], 
                                text=k, 
                                onvalue=cb_items[k], 
                                padding=(40,5),
                                command=CheckedBtn) )
    cb[i].pack(anchor='w')

# make a button to set current values
setCurrent_btn = ttk.Button( window, 
                                text = "Set State", 
                                command = SetButtonAction, 
                                padding=8, 
                                width=30,
                                state=tk.DISABLED )
setCurrent_btn.pack()


# Create Menu Bar for Exit and Help
menubar = tk.Menu(window)
    # File Menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Quick Set Busy", command=shortcutSetBusy, underline=10)
filemenu.add_command(label="Quick Set Normal", command=shortcutSetNormal, underline=10)
filemenu.add_command(label="Exit", command=window.quit, underline=1)
    # Help Menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Time Since Boot", command = DisplayWinUpTime, underline=0)
helpmenu.add_command(label="Help", command = DisplayHelp, underline=0)
menubar.add_cascade(label="File", menu=filemenu, underline=0)
menubar.add_cascade(label="Help", menu=helpmenu, underline=0)
window.config(menu=menubar)


# Handle arguments if any sent, and assume it is good to go:
if (len(argv) >= 2):	        # User passed an argument 
    if ('--setBusy' in argv[1]):  # if it was "setBusy", then
        shortcutSetBusy()       # run that shortcut on start
        
# Check to see if the last reboot was too long ago
CheckWinUpTime(MAX_DAYS_TILL_REBOOT)


window.mainloop()

