# How to Draw Chart Example

# Importing the matplotlb.pyplot
import matplotlib.pyplot as plt
  
# Declaring a figure "gnt"
fig, gnt = plt.subplots()
  
# Setting Y-axis limits
gnt.set_ylim(0, 60)
  
# Setting X-axis limits
gnt.set_xlim(0, 100)
  
# Setting labels for x-axis and y-axis
gnt.set_xlabel('seconds since start')
gnt.set_ylabel('Processor')
  
# Setting ticks on y-axis
gnt.set_yticks([15, 25, 35, 45])
# Labelling tickes of y-axis
gnt.set_yticklabels(['1', '2', '3', '4'])
  
# Setting graph attribute
gnt.grid(True)
  
# Declaring a bar in schedule
gnt.broken_barh([(4, 1)], (40, 9), facecolors =('tab:orange'))
# gnt.broken_barh([5, 5)], 
  
# Declaring multiple bars in at same level and same width
gnt.broken_barh([(11, 1), (15, 1)], (10, 9), facecolors ='tab:blue')
  
gnt.broken_barh([(1, 5), (10, 2), (13, 1)], (20, 9), facecolors =('tab:red'))

# plt.savefig("abcd.png")
fig, gnt = plt.subplots()
gnt.broken_barh([(1, 5), (10, 2), (13, 1)], (20, 9), facecolors =('tab:red'))
plt.show()