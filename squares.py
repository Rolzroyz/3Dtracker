# written by Kyle Boucher
# This module includes the squares function and its support functions to
# calculate the sum of the squared distances from data points projected
# onto a plane to the centroid of all the projected points. The plane is
# defined by a normal, unit vector.


def vorthdistance(point,vnorm,scalar_proj=False):
    """ Takes a SpacePoint object and the normal vector of a plane and
returns the orthogonal distance from the point to the plane as a
vector (list data structure [x, y, z]) pointing with head at the
data point and tail at the plane. The normal vector normalv should
also be a unit vector. If scalar_proj is set to True, returns a
tuple of the dotproduct and the given point object.
"""
    dotprod = (vnorm[0] * point.x) + (vnorm[1] * point.y) + (vnorm[2] * point.z)
    if scalar_proj == True:
        return (dotprod,point)
    vdist = [(dotprod * vnorm[0]), (dotprod * vnorm[1]), (dotprod * vnorm[2])]
    # vdist is the vector projection of the data point position vector
    # onto the normal vector.
    return vdist


def vposition_of_projection(point,vnorm):
    vdist = vorthdistance(point,vnorm)
    vprojposit = [(point.x - vdist[0]), (point.y - vdist[1]), (point.z - vdist[2])]
    return vprojposit


def vposition_of_centroid(eventscatter,vnorm):
    list_vprojposit = []
    for point in eventscatter:
        list_vprojposit.append(vposition_of_projection(point,vnorm))
    net_vprojposit = [0,0,0]
    for vector in list_vprojposit:
        for i in range(3):
            net_vprojposit[i] += vector[i]
    pointcount = len(eventscatter)
    for i in range(3):
        net_vprojposit[i] = (net_vprojposit[i] / (pointcount * 1.0))
    return (net_vprojposit, list_vprojposit)


def squares(eventscatter,vnorm):
    (vcentroid, list_vprojposit) = vposition_of_centroid(eventscatter,vnorm)
    squaresum = 0
    for vector in list_vprojposit:
        squaresum += (vector[0]-vcentroid[0])**2 + (vector[1]-vcentroid[1])**2 + (vector[2]-vcentroid[2])**2
    # Add the magnitude squared of difference of the position vectors of
    # the projected point and the centroid, for each data point.
    return squaresum