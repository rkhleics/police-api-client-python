def encode_polygon(points):
    return ':'.join(['{0},{1}'.format(*p) for p in points])
