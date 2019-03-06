import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []

with open('./toy/fourComponents/points.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        print(row)
        x.append(int(row[0]))
        y.append(int(row[1]))
        z.append(float(row[2]))

plt.scatter(x,y,c=z)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
