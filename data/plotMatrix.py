import sys
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import util

DEFAULT_POINT_SIZE = 10

def printInstructions():
    print("Invalid args. Please use:")
    print("-evecFile <file>")
    print("-evecCols <colA> <colB> ...")
    print("Optional:")
    print("-dataFile <file2>")
    print("-dataCols <colA> <colB> ...")
    print("-color <colorFile>")
    print("-pointSize <pointSize>")

args = util.parseArgs(sys.argv, requiredArgs = ["evecFile", "evecCols"])

if not args:
    printInstructions()
else:
    evecFile = args["evecFile"][0]
    evecCols = args["evecCols"]
    util.toIntArray(evecCols)
    evec = util.readColsFromFile(evecFile, evecCols)

    data = {}
    if "dataFile" in args and "dataCols" in args:
        dataFile = args["dataFile"][0]
        dataCols = args["dataCols"]
        util.toIntArray(dataCols)
        data = util.readColsFromFile(dataFile, dataCols)

    allData = {}
    for i in evec:
        key = "evec " + str(i)
        allData[key] = evec[i]
    for i in data:
        key = "data " + str(i)
        allData[key] = data[i]
    varsToPlot = list(allData.keys())

    color = None
    palette = None
    if "color" in args:
        color = "color"
        colorFile = args["color"][0]
        colorData = util.readColFromFile(colorFile, 0)
        util.labelsToIndices(colorData)
        allData["color"] = colorData

        colorRange = max(colorData) - min(colorData) + 1
        palette = sns.light_palette("navy", colorRange)

    pointSize = DEFAULT_POINT_SIZE
    if "pointSize" in args:
        pointSize = int(args["pointSize"][0])

    df = pd.DataFrame(allData)
    height = 6.0/len(varsToPlot)
    plot_kws = {"edgecolor":"none", "s":pointSize}
    sns.pairplot(df, hue=color, palette=palette, vars=varsToPlot, height=height, plot_kws=plot_kws)

    sns.set(style="ticks")
    plt.rcParams["patch.force_edgecolor"] = False

    plt.show()
