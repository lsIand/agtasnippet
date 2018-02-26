import tkinter as tk
from collections import deque
import numpy as np
import copy as cp

root = tk.Tk()

step = 0

#P_MAT = [[-1, 1], [1, -1]]
#P_MAT_2 = [[1, -100], [-1, 1]]
P_MAT = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
P_MAT_2 = [[0, 1, -1], [-1, 0, 1], [1, -1, 0]]
P_MAT = np.asarray(P_MAT)
P_MAT_2 = np.asarray(P_MAT_2)

amtss = []
canv = tk.Canvas(root, height=500, width=1000, bg='white')
canv.pack()

lines_p1 = []
lines_p2 = []
line_tuples_p1 = []
line_tuples_p2 = []

for row in range(len(P_MAT)):
    p1strat = np.zeros(len(P_MAT))
    p1strat[row] = 1
    for col in range(len(P_MAT[0])):
        new_amt = [1]
        p2strat = np.zeros(len(P_MAT[0]))
        p2strat[col] = 1
        new_amt.append(np.copy(p1strat))
        new_amt.append(p2strat)
        amtss.append(new_amt)
        line_tuples_p1.append(deque())
        line_tuples_p2.append(deque())

print(line_tuples_p1)

prev_amts = cp.deepcopy(amtss)

scale_mul = 500
scale = scale_mul/10
for x in range(0, 10):
    canv.create_text(990, 500 - x*scale - 10, text=str(x/10), fill='black')
    canv.create_line(0, x*scale, 1000, x*scale, fill='gray')


def smooth_amounts(am):
    nu_1 = []
    for elem in am[1]:
        nu_1.append('%.5f' % (elem/am[0]))
    nu_2 = []
    for elem in am[2]:
        nu_2.append('%.5f' % (elem/am[0]))
    return [nu_1, nu_2]

MCT = 8


def calculate():
    global step, canv, line_tuples_p1, line_tuples_p2, lines_p1, lines_p2, amtss, prev_amts
    for nm, amts in enumerate(amtss):
        amts[0] += 1

        p1_distr = amts[1]/amts[0]
        p2_distr = amts[2]/amts[0]

        p1_strat = 0
        p2_strat = 0

        p1_big = -1000000
        p2_big = -1000000

        for row in range(len(P_MAT)):
            smm = np.sum(np.multiply(p2_distr, P_MAT[row]))
            if smm > p1_big:
                p1_big = smm
                p1_strat = row

        for col in range(len(P_MAT[0])):
            smm = np.sum(np.multiply(p1_distr, np.swapaxes(P_MAT_2, 0, 1)[col]))
            if smm > p2_big:
                p2_big = smm
                p2_strat = col

        amts[1][p1_strat] += 1
        amts[2][p2_strat] += 1

        print(nm, "-> ", smooth_amounts(amts), amts[0])

    step += 1

    if step > 1000/MCT:
        step = 1000/MCT
        for l in line_tuples_p1:
            l.popleft()
        for l in line_tuples_p2:
            l.popleft()
        for nm, amts in enumerate(amtss):
            line_tuples_p1[nm].append(np.copy(amts[1])/amts[0])
            line_tuples_p2[nm].append(np.copy(amts[2])/amts[0])

            for value in range(len(amts[1])):
                initval = 0
                end_tuple = []
                for num, tup in enumerate(line_tuples_p1[nm]):
                    end_tuple.append(initval)
                    end_tuple.append(500 - scale_mul * line_tuples_p1[nm][num][value])
                    initval += MCT
                if step > 1:
                    canv.coords(lines_p1[nm][value], tuple(end_tuple))

            for value in range(len(amts[2])):
                initval = 0
                end_tuple = []
                for num, tup in enumerate(line_tuples_p2[nm]):
                    end_tuple.append(initval)
                    end_tuple.append(500 - scale_mul * line_tuples_p2[nm][num][value])
                    initval += MCT
                if step > 1:
                    canv.coords(lines_p2[nm][value], tuple(end_tuple))
    else:
        for nm, amts in enumerate(amtss):
            line_tuples_p1[nm].append(np.copy(amts[1])/amts[0])
            line_tuples_p2[nm].append(np.copy(amts[2])/amts[0])
            if step == 1:
                lp1 = []
                lp2 = []
                for value in range(len(amts[1])):
                    lp1.append(canv.create_line(0, 0, 0, 0, fill='blue'))
                for value in range(len(amts[2])):
                    lp2.append(canv.create_line(0, 0, 0, 0, fill='red'))
                lines_p1.append(lp1)
                lines_p2.append(lp2)
            else:
                for value in range(len(amts[1])):
                    initval = 0
                    end_tuple = []
                    for num, tup in enumerate(line_tuples_p1[nm]):
                        end_tuple.append(initval)
                        end_tuple.append(500 - scale_mul * line_tuples_p1[nm][num][value])
                        initval += MCT
                    if step > 1:
                        canv.coords(lines_p1[nm][value], tuple(end_tuple))

                for value in range(len(amts[2])):
                    initval = 0
                    end_tuple = []
                    for num, tup in enumerate(line_tuples_p2[nm]):
                        end_tuple.append(initval)
                        end_tuple.append(500 - scale_mul * line_tuples_p2[nm][num][value])
                        initval += MCT
                    if step > 1:
                        canv.coords(lines_p2[nm][value], tuple(end_tuple))

    prev_amts = cp.deepcopy(amtss)
    root.after(1, calculate)


root.after(0, calculate)
root.mainloop()
