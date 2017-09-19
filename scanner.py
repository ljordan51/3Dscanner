import serial
import struct
import matplotlib.pyplot as plt
import numpy as np
import os
# import time

filePath = "/home/rsharman/Documents/POE/3Dscanner"
serialPort = "/dev/ttyUSB0"


def getData():
    data = []
    print('Waiting for Arduino...')
    while not port.in_waiting:
        pass
    characters = []
    while port.in_waiting:
        characters.append(str(port.read(1), 'utf-8'))
    line = ''
    line = line.join(characters).strip()
    print(line)

    if line == 'Arduino ready!':
        response = input('Continue? y/n: ')
        if(response.lower() == 'y'):
            pass
        else:
            return
        print('Starting scan')
        port.write(1)
        running = True
        while running:
            line = port.read(6)
            line = struct.unpack('<cci', line)
            point = [ord(line[0]), ord(line[1]), line[2]]
            print(point)
            if point[2] < 0:
                running = False
            else:
                data.append(point)

        return data


def writeToFile(data):
    files = os.listdir(filePath)
    lastFile = 0
    for item in files:
        if item[:8] == 'ScanData':
            item[10:]
            if item[10:] == '.txt':
                fileNumber = int(item[8:10])
                if fileNumber > lastFile:
                    lastFile = fileNumber
    num = str(lastFile + 1)
    if lastFile < 9:
        num = '0' + num
    fileName = 'ScanData' + num + '.txt'
    dataFile = open(filePath+'/'+fileName, 'w')
    for line in data:
        dataFile.write(str(line) + '\n')
    return num


def convertToNPArray(dataArray):

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


def draw_heatmap(x, y, map_value):

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

    color_map = plt.cm.gist_heat  # plt.cm.rainbow #plt.cm.hot #plt.cm.gist_heat
    plt.clf()
    plt.pcolor(plt_x, plt_y, plt_z, cmap=color_map, vmin=z_min, vmax=z_max)
    plt.axis([plt_x.min(), plt_x.max(), plt_y.min(), plt_y.max()])
    plt.title(plot_name)
    plt.colorbar().set_label(plot_name, rotation=270)
    ax = plt.gca()
    ax.set_aspect('equal')
    figure = plt.gcf()
    plt.show()
    return figure


if __name__ == "__main__":
    port = serial.Serial(serialPort)
    print("Connected to " + port.name)
    #rawData = getData()
    #x, y, map_value = convertToNPArray(rawData)
    #plot = draw_heatmap(x, y, map_value)
    running = True
    while running:
        rawData = getData()
        fileNum = writeToFile(rawData)
        x, y, map_value = convertToNPArray(rawData)
        plot = draw_heatmap(x, y, map_value)
        plot.savefig(filePath + '/' + 'Scan' + fileNum + '.png')
        response = input('Scan again? y/n: ')
        if(response.lower() != 'y'):
            running = False
