import cv2
import numpy as np
import os
import math

############################################
# FUNÇÕES AUXILIARES
############################################
def draw_polygon_and_lines(frame, area_points):
    if len(area_points) < 4:
        return

    pts = np.array(area_points, dtype=np.int32)
    cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 255), thickness=2)

    A1, A2 = area_points[0], area_points[1]
    B1, B2 = area_points[2], area_points[3]
    midA = ((A1[0]+A2[0])//2, (A1[1]+A2[1])//2)
    midB = ((B1[0]+B2[0])//2, (B1[1]+B2[1])//2)

    cv2.putText(frame, "Line A", midA,
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, "Line B", midB,
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)


def orientation(p, q, r):
    val = ((q[1] - p[1])*(r[0] - q[0])) - ((q[0] - p[0])*(r[1] - q[1]))
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
        min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
        return True
    return False

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True
    return False

def lines_intersect(line_p1, line_p2, box_p1, box_p2):
    return do_intersect(line_p1, line_p2, box_p1, box_p2)


def any_corner_in_polygon(x1, y1, x2, y2, polygon_points):
    # 4 cantos do bbox
    corners = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
    polygon = np.array(polygon_points, dtype=np.int32)

    for cx, cy in corners:
        inside = cv2.pointPolygonTest(polygon, (cx, cy), False) >= 0
        if inside:
            return True
    return False


def salvar_veiculo(frame, x1, y1, x2, y2, nome):
    pasta = "imagens_salvas"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    recorte = frame[y1:y2, x1:x2]
    caminho = os.path.join(pasta, f"{nome}.jpg")
    cv2.imwrite(caminho, recorte)
    print(f"[INFO] Imagem salva: {caminho}")  
    
    
def distance_point_to_line(px, py, x1, y1, x2, y2):
    numerator = abs((x2 - x1)*(y1 - py) - (x1 - px)*(y2 - y1))
    denominator = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if denominator == 0:
        return 9999999
    return numerator / denominator

""" def end():
        file = open(speed_record_file_location, "a")
        file.write("\n-------------\n")
        file.write("-------------\n")
        file.write("SUMMARY\n")
        file.write("-------------\n")
        file.write("Total Vehicles :\t" + str(count) + "\n")
        file.write("Exceeded speed limit :\t" + str(exceeded))
        file.close()
 """