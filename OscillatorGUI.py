#region TODO


''' 
MAIN 
- init variables
- set up UI
- set up chart/plotter
- set up COM port

SYSTEM TIMER
- Send Requests every interval

PLOT
- plot the arduino data

COM PORT
- find active com ports
- open the com ports
- read the com ports

DATA PROCESSING
- change arduino analog data to volts
- add a time field to the array
- maximum value
- average value

DEBUG FUNCTIONALITY
- stopwatch/timer
- metrics (delay, scan time, total time per read, etc.)

'''

#endregion


#region DOCUMENTATION


'''
lol u thought i was actually gonna put docs here?
imagine having time for that
couldn't be me fr
'''
#endregion


#region IMPORTS
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()
import serial
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


#endregion


#region VARIABLES

#Arduino Related Variables  
SerialPortnum =  '3'
SerialPort = 'COM' + SerialPortnum
vref = 5.2
baudRate = 2000000
numSamples = 500
scanTimeBufferms = 50

#scope in application
yAxisMax = 5
root = ttk.Window(themename = "cosmo")
root.geometry('1280x720')
root.title('Software Oscilloscope')

#app variables
markers = ttk.IntVar(root, value = 0)
isDcCoupled = ttk.BooleanVar(root)
isSingleClicked = ttk.BooleanVar(root)
debug = ttk.BooleanVar(root)
scanTimems = ttk.IntVar(root)


#Burst related variables
endOfData = False
burstDurationms = 50
rawInputDataList = []
msPerSample = 0.1   

#Debug Mode Toggle

#endregion






#region GUI
def singleclick():
    isSingleClicked = True

def UpdateSecond():
    scanTimems = SecondsMeter.amountusedvar


#Fix this later, add mechanism to find currently used COM ports
allComPorts = ttk.StringVar(root,value = 'The Following COM ports were found\n COM4 - quantum reactor \n COM6 - Multidimensional Hyperloop \n COM33 - Yo Mama')


# This contains all the options
optionContainer = ttk.Notebook(root, width = '350', height = '650')


# First tab
comFrame = ttk.Frame(optionContainer,height = 650, width = 350, bootstyle = 'secondary')
comFrame.pack(fill = 'both')
comEntry = ttk.Entry(master = comFrame, textvariable = SerialPortnum)
comEntryLabel = ttk.Label(master = comFrame, text = 'Enter Com Port')
currentPortsLabel = ttk.Label(master = comFrame, textvariable = allComPorts, width = 300, justify = 'left', anchor = 'center', font = 30)
OpenPortButton = ttk.Button(comFrame, text='OPEN PORT', bootstyle=PRIMARY)
comEntryLabel.pack(side = 'top')
currentPortsLabel.pack(side = 'bottom')
comEntry.pack(side = 'top')    
OpenPortButton.pack( padx=5, pady=5)


# second tab
settingsFrame = ttk.Frame(optionContainer,height = 650, width = 350, bootstyle = 'secondary')
settingsFrame.pack(fill = 'both')

vertiScale = ttk.Scale(settingsFrame, orient = HORIZONTAL, length=300)
ScaleLabel = ttk.Label(master = settingsFrame, text = 'Vertical  Scale', width = 70, justify = 'center',anchor = 'center', font = 30)
SecondsMeter2 = ttk.Meter(master = settingsFrame,bootstyle="info", metertype = 'semi', stripethickness = 5, amounttotal = 1.5, interactive= True, textright = 'seconds')
SecondsButton = ttk.Button(master = settingsFrame, command = UpdateSecond, text = 'Update')
SecondsMeter = ttk.Meter(master=settingsFrame,metersize=180,padding=5,amountused=1000 ,amounttotal=1500,subtext='Scan Milliseconds',textright='ms',bootstyle='info',stripethickness=10,interactive=True)
samplesEntry = ttk.Entry(master = settingsFrame, textvariable = numSamples)
vrefEntry = ttk.Entry(master = settingsFrame, textvariable = vref)
samplesEntryLabel = ttk.Label(master = settingsFrame, text = 'No.of Samples', width = 70, justify = 'center')
vrefEntryLabel = ttk.Label(master = settingsFrame, text = 'Arduino Vref', width = 70, justify = 'center')


ScaleLabel.pack(side = 'bottom', padx = 15)
vertiScale.pack(side = 'bottom', pady = 20)
SecondsButton.pack(side = 'bottom', pady = 20)
SecondsMeter.pack(side = 'bottom', pady = 20)
samplesEntryLabel.pack(side = 'top')
samplesEntry.pack(side = 'top', padx = 20, pady = 30)
vrefEntryLabel.pack(side = 'top')
vrefEntry.pack(side = 'top', padx = 20, pady = 30)



#third tab
checksFrame = ttk.Frame(optionContainer,height = 650, width = 350, bootstyle = 'secondary')
checksFrame.pack(fill = 'both')

DCCheckButton = ttk.Checkbutton(checksFrame, text = "DC", variable = isDcCoupled, onvalue = True, offvalue = False,  width = 100)
ACCheckButton = ttk.Checkbutton(checksFrame, text = "AC", variable = isDcCoupled, onvalue = False, offvalue = True,  width = 100)
debugCheckButton = ttk.Checkbutton(checksFrame, text = "Debug Mode", variable = debug, onvalue = True, offvalue = False,  width = 30)
markerCheckButton = ttk.Checkbutton(checksFrame, text = "Markers", variable = markers, onvalue = 1, offvalue = 0,  width = 30)
SingleButton = ttk.Button(master = checksFrame, text = 'Single',command = singleclick)
dccbLabel = ttk.Label(checksFrame, text = 'Coupling', width = 70, justify = 'center')

dccbLabel.pack(side = 'top', pady = 10)
DCCheckButton.pack(side = 'top',pady = 2)
ACCheckButton.pack(side = 'top', pady = 2)
debugCheckButton.pack(pady = 40, padx = 40)
markerCheckButton.pack(side = 'top',pady = 40)
SingleButton.pack(padx = 40, pady = 40)

optionContainer.add(comFrame, text = 'COM port')
optionContainer.add(settingsFrame, text = 'Settings')
optionContainer.add(checksFrame, text = 'Checks and Debug')
optionContainer.pack(side = 'left')

# This contains the generated waveform
waveFrame = ttk.Frame(root,height = 650, width = 150, bootstyle = 'secondary')

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

canvas = FigureCanvasTkAgg(f, waveFrame)
canvas.draw()
waveFrame.pack(side = 'right')
canvas.get_tk_widget().pack(side=ttk.BOTTOM, fill=ttk.BOTH, expand=True)




root.mainloop()
#endregion