import datetime

import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import json
import os

DataName = "BDOData"
Goal = 100
Fail = 0


def loadPastData():
    if not os.path.exists(DataName + '.json'):
        return {'time': [], 'viewers': []}
    with open(DataName + '.json', 'r') as infile:
        data = json.loads(infile.read())
    return data


def savePastData(data):
    with open(DataName + '.json', 'w') as outfile:
        json.dump(data, outfile)


def timeString(min):
    day, rem = divmod(min, 1440)
    hour, min = divmod(rem, 60)
    day = math.floor(day)
    hour = math.floor(hour)
    min = math.floor(min)
    return str(day) + "D " + str(hour) + "H " + str(min) + "M"


def runPredict(x, y, PredictionTimeFrame):
    i = 0
    currentNow = datetime.datetime.now()
    while i < len(x):
        t = currentNow - x[i]
        if t <= PredictionTimeFrame:
            break
        i += 1

    if i == len(x):
        return x[i-1], y[i-1]   #return junk

    startTime = x[i]
    startValue = (float)(y[i])

    endTime = x[len(x) - 1]
    endValue = (float)(y[len(y) - 1])

    dT = endTime - startTime
    dV = endValue - startValue

    dTmin = dT.total_seconds() / 60

    dTV = dV / dTmin #xp per minute

    Vremaining = Goal - endValue

    Tremaining = Vremaining / dTV
    # print(timeString(Tremaining) + " Minutes Remaining")

    projectedTime = currentNow + datetime.timedelta(minutes=math.floor(Tremaining))

    return [endTime, projectedTime], [endValue, Goal], timeString(Tremaining)


def matplotGraph(x, y):
    x = np.asarray(x)
    fig, ax = plt.subplots()

    x4, y4, WeekString = runPredict(x,y, datetime.timedelta(days=7))
    x2, y2, DayString = runPredict(x,y, datetime.timedelta(days=1))
    x3, y3, HourString = runPredict(x,y, datetime.timedelta(hours=1))

    print("Weekly:\t"+WeekString+" Remaining")
    print("Daily:\t"+DayString+" Remaining")
    print("Hourly:\t"+HourString+" Remaining")

    #ax.plot(x, y)
    ax.plot(x, y, '-', x2, y2, '--', x3, y3, ':', x4, y4, '-.')

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_minor_locator(mdates.HourLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    plt.xlabel('Time')
    # plt.ylabel('Viewers')
    # plt.title('Viewers over time on ' + DataName)
    try:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
        plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)
    except:
        pass

    plt.grid(True, which='both')
    plt.savefig("test.png")
    plt.show()


v = loadPastData()
data = input("Enter your data (Numeric):")
if not data == "":
    v['viewers'].append(data)
    v['time'].append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    savePastData(v)

for x in range(0, len(v['time'])):
    v['time'][x] = datetime.datetime.strptime(v['time'][x], "%Y-%m-%d %H:%M:%S.%f")
matplotGraph(v['time'], v['viewers'])
