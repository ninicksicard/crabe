import OpenGlViewer
import cv2

def open_file(scene='scene5.ply'):
    with open(scene) as f:
        lines = f.readlines()
        values = []
        cloud = []
        res_div = 5
        dot = 0
        for line in lines:
            dot += 1
            if dot >= res_div:
                values = line.split(' ')
                if len(values) > 4:
                    cloud.append((values[0], values[1], values[2], values[3], values[4], values[5]))
                dot = 0
    OpenGlViewer.begin(cloud)

def map_one_frame(matte, frame, edge, dept, cloud):
    matte = cv2.cvtColor(matte, cv2.COLOR_BGR2HSV)
    edge = cv2.cvtColor(edge, cv2.COLOR_BGR2HSV)
    treshold = 120
    line = 0

    while line < len(matte):
        pixel=0
        while pixel < len(matte[line]):
            if matte[line][pixel][0]>treshold and edge[line][pixel][0]>treshold:
                cloud.append((pixel/100,line/100,dept/10, frame[line][pixel][0], frame[line][pixel][1], frame[line][pixel][2]))
            pixel += 1

        line += 1
    return cloud


def view_map(cloud):
    OpenGlViewer.begin(cloud)

# open_file()
