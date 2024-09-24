import os
import ctypes

STD_OUTPUT_HANDLE    = -11
FOREGROUND_GREEN     = 0x000A

# Define Windows State Codes (bit fields):
# for more details, see https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate
ES_CONTINUOUS        = 0x80000000
ES_SYSTEM_REQUIRED   = 0x00000001
ES_DISPLAY_REQUIRED  = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040

def setWinState(new_mode=(ES_CONTINUOUS|ES_DISPLAY_REQUIRED)):
    """Set Windows Mode, e.g., to inform the system that it is in use, 
    thereby preventing the system from entering sleep or turning off 
    the display while the application is running.  If no parameter
    is passed, the default is ES_CONTINUOUS|ES_DISPLAY_REQUIRED.
    Returns the previous mode or NULL if unsuccessful in setting new mode."""
    # Set Windows Mode to control Screen Save / Screen Lock using cytpes and WinDLL call
    # Default, set to "Busy" and "Continuous" to prevent Screen Lock (0x80000002)
    # Returns the current mode, which can be used to set back. Or...
    # To return to "normal" (idle), use ES_CONTINUOUS with all other bits cleared (i.e., 0x80000000)
    
    old_mode = ctypes.windll.kernel32.SetThreadExecutionState(new_mode)
    old_mode = ctypes.c_ulong(old_mode).value
    return old_mode

def getWinState():
    """Returns the current state value for Thread Execution as a 4-byte value
    combining the following bit values:
        ES_CONTINUOUS        = 0x80000000
        ES_SYSTEM_REQUIRED   = 0x00000001
        ES_DISPLAY_REQUIRED  = 0x00000002
        ES_AWAYMODE_REQUIRED = 0x00000040"""
    # since there is no "GET" Thread Execution State, just 
    # set it to the default, getting the current in return; then,
    # re-set it back to the current.
    current_mode = setWinState()
    temp = setWinState(current_mode)
    current_mode = ctypes.c_ulong(current_mode).value
    return current_mode
    
def getWinBootTime():
    """Returns the time, as [hours, minutes, seconds], since Windows was restarted."""
    up_time_ms = ctypes.windll.kernel32.GetTickCount64()
    up_time = int(str(up_time_ms)[:-3])      # truncate the ms
    
    # extract the hours, minutes and seconds from up_time (which is in seconds)
    mins, sec = divmod(up_time, 60)
    hrs, mins = divmod(mins, 60)
    
    return [hrs, mins, sec]
    
def main():
    # Set the command window title
    ctypes.windll.kernel32.SetConsoleTitleW("Keeping Windows from Sleeping...")

    # Change text color to green
    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE),FOREGROUND_GREEN)

    # Disable Windows Screen Saver, to protect burning process
    winModeOrig = setWinState()             # using default setting

    print('\nPrior mode: ',hex(winModeOrig))
    print('\nSet Windows mode to busy.\n')
    temp = input('Hit Enter to return to prior mode.')

    setWinState(winModeOrig)

if __name__ == '__main__':
    main()