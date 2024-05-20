from math import sqrt

PointI = tuple[int, int]
PointF = tuple[float, float]

class LineSegment:
    def __init__(self, start: PointF, end: PointF):
        self.start = start
        self.end = end

# gpt给的，看不懂
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def getOffset(p0: PointI, p1: PointI) -> PointI:
    return p1[0] - p0[0], p1[1] - p0[1]

def differentSide(p0: PointI, p1: PointI, p2: PointI) -> bool:
    a = p1[0] * p0[1] - p1[1] * p0[0] > 0
    b = p2[0] * p0[1] - p2[1] * p0[0] > 0
    return a ^ b

def isIntersect(one: LineSegment, other: LineSegment):
    v0 = getOffset(one.start, one.end)
    v1 = getOffset(one.start, other.start)
    v2 = getOffset(one.start, other.end)
    d1 = differentSide(v0 ,v1, v2)

    v0 = getOffset(other.start, other.end)
    v1 = getOffset(other.start, one.start)
    v2 = getOffset(other.start, one.end)
    d2 = differentSide(v0 ,v1, v2)
    return d1 and d2

def on_segment(p, q, r):
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False

def intersect(directed: LineSegment, undirected: LineSegment):
    if not isIntersect(directed, undirected):
        return None
    # Line segments intersect
    x1, y1, x2, y2 = directed.start[0], directed.start[1], directed.end[0], directed.end[1]
    x3, y3, x4, y4 = undirected.start[0], undirected.start[1], undirected.end[0], undirected.end[1]
    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if det == 0:
        return None  # Line segments are collinear, no unique intersection point
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / det
    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    return x, y

def intersect_antipole(directed: LineSegment, undirected: LineSegment) \
    -> tuple[PointF, PointF] | None:
    
    # p1, q1, p2, q2 = directed.start, directed.end, undirected.start, undirected.end
    # o1 = orientation(p1, q1, p2)
    # o2 = orientation(p1, q1, q2)
    # o3 = orientation(p2, q2, p1)
    # o4 = orientation(p2, q2, q1)

    # if o1 != o2 and o3 != o4:
    intersection_point = intersect(directed, undirected)
    if intersection_point is None:
        return None
    x, y = intersection_point

    # Calculate the symmetric point
    ax = directed.end[0] - x
    ay = directed.end[1] - y
    vx = undirected.end[0] - undirected.start[0]
    vy = undirected.end[1] - undirected.start[1]
    shadow = (ax * vx + ay * vy) / (vx * vx + vy * vy)
    a_shadow_x = shadow * vx
    a_shadow_y = shadow * vy
    symmetric_x = 2 * a_shadow_x - ax + x
    symmetric_y = 2 * a_shadow_y - ay + y
    symmetric_point = (symmetric_x, symmetric_y)

    return intersection_point, symmetric_point

def intersect_antipole_velocity(vector: PointF, mid: tuple[PointF, PointF] | None) \
    -> tuple[PointF, PointF, PointF] | None:
    if mid is None:
        return None
    p0, p1 = mid
    dirction = p1[0] - p0[0], p1[1] - p0[1]
    k = sqrt(vector[0] ** 2 + vector[1] ** 2) / sqrt(dirction[0] ** 2 + dirction[1] ** 2)
    resultVelocity = dirction[0] * k, dirction[1] * k
    return p0, p1, resultVelocity


def antipole(vector: PointF, segment: LineSegment) -> PointF:
    vx, vy = vector
    mx = segment.end[0] - segment.start[0]
    my = segment.end[1] - segment.start[1]
    shadow = (vx * mx + vy * my) / (mx * mx + my * my)
    v_shadow_x = shadow * mx
    v_shadow_y = shadow * my
    symmetric_x = 2 * v_shadow_x - vx
    symmetric_y = 2 * v_shadow_y - vy
    return symmetric_x, symmetric_y
                                              
# 示例用法
if __name__ == "__main__":
    directed_segment = LineSegment((1, 1), (3, 3))
    undirected_segment = LineSegment((2, 1), (2, 4))

    result = intersect_antipole(directed_segment, undirected_segment)
    intersection_point, symmetric_point = result
    print(intersection_point)
    print(symmetric_point)
