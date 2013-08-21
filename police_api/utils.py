def encode_polygon(points):
    return ':'.join(['%s,%s' % p for p in points])
