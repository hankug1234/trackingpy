import numpy as np
import math

def normalize(a):
 c = [0,0]
 c[0] = a[0] / math.sqrt((a[0]**2) + (a[1]**2))
 c[1] = a[1] / math.sqrt((a[0]**2) + (a[1]**2))
 return c;


def crossMultipleLength2D(a, b):
 return a[0] * b[1] - a[1] * b[0];


def ccw(a, c, d):
 n1 = c - a
 n2 = d - a
 n1 = normalize(n1);
 n2 = normalize(n2);

 crossV = crossMultipleLength2D(n1, n2);

 if (crossV > 0):
    return False;
 else:
    return True;

def re_arrange(imgpoints):

        criteria1 = imgpoints[0][0][0][0]
        criteria2 = imgpoints[0][1][0][0]
        m = criteria1 - criteria2
        if m < 0:
            ss = False
        else:
            ss = True
        count = 1
        for imgp in imgpoints[0][1:]:
            m = criteria1 - imgp[0][0]
            if m < 0:
                s = False
            else:
                s = True
            if s == ss:
                count+=1
                criteria1 = imgp[0][0]
            else:
                break;

        candidate = []
        candidate.append((0,imgpoints[0][0][0]))
        candidate.append((1,imgpoints[0][count - 1][0]))
        candidate.append((2,imgpoints[0][-count][0]))
        candidate.append((3,imgpoints[0][-1][0]))

        arrange = list()
        arrange.append(candidate[0])
        state = False
        for candi in candidate[1:]:
            for e, arran in enumerate(arrange):
                if arran[1][0] > candi[1][0]:
                    arrange.insert(e,candi)
                    state = True
                    break
            if state == False:
                arrange.append(candi)
            else:
                state = False

        if arrange[0][1][1] <= arrange[1][1][1]:
            temp = arrange[1]
            arrange[1] = arrange[0]
            arrange[0] = temp

        if arrange[2][1][1] <= arrange[3][1][1]:
            temp = arrange[3]
            arrange[3] = arrange[2]
            arrange[2] = temp

        horizontal = ccw(candidate[0][1], candidate[1][1], candidate[3][1])
        index = arrange[0][0]
        size = count

        print(index)
        print(horizontal)

        if (index == 0 and horizontal == True):
            objp = np.zeros((size * size, 3), np.float32)
            objp[:, :2] = np.mgrid[0:size, 0:size].T.reshape(-1, 2)

        elif (index == 0 and horizontal == False):
            objp = np.zeros((size * size, 3), np.float32)
            x, y = np.mgrid[0:size, 0:size]
            n = np.array([y, x])
            n = n.T.reshape(-1, 2)
            objp[:, :2] = n
            objp = [objp]

        elif (index == 1 and horizontal == True):
            objp = np.zeros((size * size, 3), np.float32)
            n = np.mgrid[0:size, 0:size].T
            for s in range(0, len(n)):
                n[s] = np.sort(n[s], axis=0)[::-1]
            objp[:, :2] = n.reshape(-1, 2)
            objp = [objp]

        elif (index == 1 and horizontal == False):
            objp = np.zeros((size * size, 3), np.float32)
            x, y = np.mgrid[0:size, 0:size]
            n = np.array([y, x])
            n = n.T
            for s in range(0, len(n)):
                n[s] = np.sort(n[s], axis=0)[::-1]
            objp[:, :2] = n.reshape(-1, 2)
            objp = [objp]

        elif (index == 2 and horizontal == True):
            objp = np.zeros((size * size, 3), np.float32)
            n = np.mgrid[0:size, 0:size]
            n = n.T
            n = n[::-1]
            objp[:, :2] = n.reshape(-1, 2)
            objp = [objp]

        elif (index == 2 and horizontal == False):
            objp = np.zeros((size * size, 3), np.float32)
            x, y = np.mgrid[0:size, 0:size]
            n = np.array([y, x])
            n = n.T
            n = n[::-1]
            objp[:, :2] = n.reshape(-1, 2)
            objp = [objp]

        elif (index == 3 and horizontal == True):
            objp = np.zeros((size * size, 3), np.float32)
            n = np.mgrid[0:size, 0:size]
            n = n.T
            n = n[::-1]
            for s in range(0, len(n)):
                n[s] = np.sort(n[s], axis=0)[::-1]
            objp[:, :2] = n.reshape(-1, 2)
            objp = [objp]

        else:
            objp = np.zeros((size * size, 3), np.float32)
            x, y = np.mgrid[0:size, 0:size]
            n = np.array([y, x])
            n = n.T
            n = n[::-1]
            for s in range(0, len(n)):
                n[s] = np.sort(n[s], axis=0)[::-1]
            objp[:, :2] = n.reshape(-1, 2)
            objp = [objp]

        return objp







