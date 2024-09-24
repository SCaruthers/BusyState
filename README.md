# BusyState
Python GUI script to change Windows' busy state, e.g., to prevent screen saver from coming on during online meetings

# Help Text from Script
Read and Set the Thread Execution State.  

The following values can be used:

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
