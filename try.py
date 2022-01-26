from sys import *

start = ".circuit" #start of the circuit description
end = ".end" #end of circuit description

#showing error message in case of invalid input
if(len(argv)!=2):
	print("Please provide the name of the netlist file\nThe right usage is %s <your_file_name>" % argv[0])
	exit()

#analysing circuit
def analyse(line):
	print(line)
	print("Analysis")
	words = line.split() #words is a list containing each entry of the MNA matrix
	source = words[0][0] #source contains the letter code indicating type of element
	if(len(words)==6): #if it is a dependent source
		print("Dependent source")
		maps = {"E": ["VCVS",1,2,3,4,5], #maps is a dictionary containing the type of element and indexes of the nodes and values
			"G": ["VCCS",1,2,3,4,5]}
		print("%s\nNode 1: %s\nNode 2: %s\nNode 3: %s\nNode 4: %s\nValue: %s\n" % (maps[source][0],
												words[maps[source][1]],
												words[maps[source][2]],
												words[maps[source][3]],
												words[maps[source][4]],
												words[maps[source][5]]))
	elif(len(words)==5): #for ccvs and cccs
		print("Dependent source")
		maps = {"H": ["CCVS",1,2,3,4], 
			"F": ["CCCS",1,2,3,4]}
		print("%s\nNode 1: %s\nNode 2: %s\nVoltage source: %s\nValue: %s\n" % (maps[source][0],
											words[maps[source][1]],
											words[maps[source][2]],
											words[maps[source][3]],
											words[maps[source][4]]))

	else: #in the case of an independent element
		maps = {"R": "Resistor",
			"L": "Inductor",
			"C": "Capacitor",
			"V": "Independent Voltage Source",
			"I": "Independent Current Source"}
		print("Type of Element: %s\nFrom node: %s\nTo node: %s\nValue: %s\n" % (maps[source],
											words[1],
											words[2],
											words[3]))
			
		
def reversing(list_x): #reverses the lines, and the words in each line
	list_x.reverse()
	for line in list_x:
		words = line.split() #splitting each line into words
		words = list(reversed(words)) 
		print(" ".join(words))

try:
	with open(argv[1]) as netlist: #finds the indexes of the starting and end points of the lines to be read, stores into begin and finish
		lines = netlist.readlines()
		begin = -1; finish = -5
		for line in lines:              
			if start == line[:len(start)]:
	    			begin = lines.index(line)
			elif end == line[:len(end)]:
	    			finish = lines.index(line)
	    			break
		if begin >= finish: #this only happens when the file doesnt contain a .circuit and .end line       
			print('Circuit not defined correctly')
			exit()
		x = []
		for line in lines[begin+1:finish]: #x is a list, each entry contains the lines of the portion of the file to be read 
			x.append(line.split('#')[0])
			analyse(line.split('#')[0])
		reversing(x)
except IOError: #invoked when the file provided cannot be opened 
	print('Please provide the right file name')
	exit()
