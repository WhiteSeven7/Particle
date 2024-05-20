PointI = tuple[int, int]
PointF = tuple[float, float]

def getOffset(point0: PointI, point1: PointI) -> PointI:
    return point1[0] - point0[0], point1[1] - point0[1]

def dotProduct(vectA: PointI, vectB: PointI):
    return vectA[0] * vectB[0] + vectA[1] * vectB[1]

def differentSide(p0: PointI, p1: PointI, p2: PointI) -> bool:
    a = p1[0] * p0[1] - p1[1] * p0[0] > 0
    b = p2[0] * p0[1] - p2[1] * p0[0] > 0
    return a ^ b

class Segment:
    def __init__(self, p0: PointI, p1: PointI) -> None:
        self.p0 = p0
        self.p1 = p1
        self.offset = self.p1[0] - self.p0[0], self.p1[1] - self.p0[1]

    @staticmethod
    def isIntersect(one: 'Segment', other: 'Segment'):
        v0 = one.offset
        v1 = getOffset(one.p0, other.p0)
        v2 = getOffset(one.p0, other.p1)
        d1 = differentSide(v0 ,v1, v2)

        v0 = other.offset
        v1 = getOffset(other.p0, one.p0)
        v2 = getOffset(other.p0, one.p1)

        d2 = differentSide(v0 ,v1, v2)
        return d1 and d2
    
    @staticmethod
    def getIntersectPoint(one: 'Segment', other: 'Segment') -> PointI:
        useX = 0
        try:
            k1 = (one.p1[1] - one.p0[1]) / (one.p1[0] - one.p0[0])
            b1 = one.p0[1] - k1 * one.p0[0]
        except ZeroDivisionError:
            useX = 1
        try:
            k2 = (other.p1[1] - other.p0[1]) / (other.p1[0] - other.p0[0])
            b2 = other.p0[1] - k2 * other.p0[0]
        except ZeroDivisionError:
            useX = 2
        if useX == 0:
            x = (b1 - b2) / (k2 - k1)
            y = ((k1 * x + b1) + (k2 * x + b2)) / 2
        elif useX == 1:
            x = one.p0[0]
            y = k2 * x + b2
        else:
            x = other.p1[0]
            y = k1 * x + b1
        return x, y

    @staticmethod
    def antipole(ray: 'Segment', mirror: 'Segment') -> PointI:
        v0 = mirror.offset
        v1 = getOffset(mirror.p0, ray.p1)
        k = dotProduct(v0, v1) / dotProduct(v0, v0)
        v1_5 = k * v0[0], k * v0[1]
        v2x = 2 * v1_5[0] - v1[0]
        v2y = 2 * v1_5[1] - v1[1]
        return v2x + mirror.p0[0], v2y + mirror.p0[1]