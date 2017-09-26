import serial  # for communication with Arduino
import struct  # for interpreting the bytes sent byt Arduino
import matplotlib.pyplot as plt  # for plotting the data in a heatmap
import numpy as np  # also for plotting the data
import os  # for reading the filesystem to save files
import sys  # for early terminations
import math

filePath = "/home/rsharman/Documents/POE/3Dscanner"
# this is the directory where data and plot files will be saved
serialPort = "/dev/ttyUSB0"  # the serial port the Arduino connects to


def getData():
    # read and interpret all the data from the Arduino (includes one full scan)
    data = []
    print('Waiting for Arduino...')
    while not port.in_waiting:  # wait for the Arduino to connect
        pass
    characters = []
    while port.in_waiting:  # if there's stuff in the serial port, read it
        characters.append(str(port.read(1), 'utf-8'))
    line = ''
    line = line.join(characters).strip()
    print(line)  # Arduino sends "Arduino ready!" when it is ready

    if line == 'Arduino ready!':
        response = input('Continue? y/n: ')  # wait for user to start scan
        if(response.lower() == 'y'):
            pass
        else:
            sys.exit()  # quit the program
        print('Starting scan')
        port.write(1)  # sending anyhthing to the serial port starts the Arduino
        running = True
        while running:  # save data from Arduino until Arduino says it's finished
            line = port.read(6)  # each data point contains 6 bytes
            line = struct.unpack('<cci', line)
            # the first two bytes are chars (pan and tilt data)
            # the last four bytes are the distance information
            point = [ord(line[0]), ord(line[1]), line[2]]  # convert to numbers
            print(point)
            if point[2] < 0:
                # the Arduino sends (255, 255, -1) after the last point
                running = False
            else:
                data.append(point)

        return data


def writeToFile(data):  # save the raw data to a .txt
    files = os.listdir(filePath)  # make a list of all the files that already exist
    lastFile = 0
    for item in files:  # figure out the number of the last file
        if item[:8] == 'ScanData' and item[10:] == '.txt':
            fileNumber = int(item[8:10])
            if fileNumber > lastFile:
                lastFile = fileNumber
    num = str(lastFile + 1)
    if lastFile < 9:
        num = '0' + num
    fileName = 'ScanData' + num + '.txt'  # name the next file with the next number
    dataFile = open(filePath+'/'+fileName, 'w')
    for line in data:
        dataFile.write(str(line) + '\n')  # write the list to the file
    dataFile.close()
    return num


def convertToDist(data):  # scale the distance based on calibration tests
    scaledData = []
    for line in data:
        inp = line[2]
        dist = 8.1158 * 10**-9 * inp**4 + -1.3606 * 10**-5 * inp**3 + .0084 * inp**2 + -2.3375 * inp + 292.3818
        # attempts at converting to cartesian coordinates:
        pan = (line[0])*(math.pi/180)
        tilt = (line[1])*(math.pi/180)
        # x = dist * math.sin(pan) * math.cos(tilt)
        # y = dist * math.sin(tilt) * math.cos(pan)
        depth = dist * math.cos(pan) * math.cos(tilt)
        newLine = [line[0], line[1], depth]
        scaledData.append(newLine)
    return scaledData


def convertToNPArray(dataArray):  # convert the data to a numpy array for plotting

    x = []
    y = []
    z = []
    map_value = {}

    for point in dataArray:
        temp_x = float(point[0])
        temp_y = float(point[1])
        temp_z = float(point[2])
        x.append(temp_x)
        y.append(temp_y)
        z.append(temp_z)
        map_value[(temp_x, temp_y)] = temp_z

    return x, y, map_value


def draw_heatmap(x, y, map_value):  # make the heatmap graphic with matplotlib

    plt_x = np.asarray(list(set(x)))
    plt_y = np.asarray(list(set(y)))
    plt_z = np.zeros(shape=(len(plt_x), len(plt_y)))

    for i in range(len(plt_x)):
        for j in range(len(plt_y)):
            if ((plt_x.item(i), plt_y.item(j))) in map_value:
                plt_z[i][j] = map_value[(plt_x.item(i), plt_y.item(j))]

    z_min = plt_z.min()
    z_max = plt_z.max()
    plt_z = np.transpose(plt_z)

    plot_name = "Depth Scan"

    color_map = plt.cm.gist_heat_r
    # other colormap options: plt.cm.rainbow plt.cm.hot plt.cm.gist_heat
    plt.clf()
    plt.pcolor(plt_x, plt_y, plt_z, cmap=color_map, vmin=z_min, vmax=z_max)
    # plt.axis([plt_x.max(), plt_x.min(), plt_y.min(), plt_y.max()])
    plt.title(plot_name)
    plt.xlabel('Pan angle (deg)')
    plt.ylabel('Tilt angle (deg)')
    plt.colorbar().set_label('Distance from scanner (cm)')
    ax = plt.gca()
    ax.set_aspect('equal')
    figure = plt.gcf()
    plt.show()
    return figure


if __name__ == "__main__":
    port = serial.Serial(serialPort)  # open serial port
    print("Connected to " + port.name)
    running = True
    while running:
        selection = input('Scan, Load from file, or Quit? (s/l/q): ').lower()
        if selection == 's':  # scan an object, save the file, plot it, and save the plot
            rawData = getData()  # scan the object
            fileNum = writeToFile(rawData)  # save the data
            scaledData = convertToDist(rawData)  # scale the data
            x, y, map_value = convertToNPArray(scaledData)  # convert the data so it can be plotted
            plot = draw_heatmap(x, y, map_value)  # make the plot
            plot.savefig(filePath + '/' + 'Scan' + fileNum + '.png')  # save the plot
        elif selection == 'l':  # read a text file and plot the data
            dataPath = input('Enter the path of the desired data file: ')
            dataFile = open(dataPath)  # open the path specified
            textData = dataFile.readlines()
            rawData = []
            for element in textData:  # read each line as a list and add it to another list
                line = eval(element)
                rawData.append(line)
            dataFile.close()
            scaledData = convertToDist(rawData)
            # for line in scaledData:
            #     print(line)
            x, y, map_value = convertToNPArray(scaledData)
            plot = draw_heatmap(x, y, map_value)
        else:
            running = False
