########################
#
# Functions to fit
# a line to a three
# dimenstional scatter
# of data points.
#
# written by:
# Kyle Boucher
# Started 21 May, 2012
#
# Functioning version
# finished on
# 26 May, 2012
#
# Major changes made
# 27 May, 2012
#
# Accurate version done
# 28 May, 2012
#
########################
#
# The function at the 
# very end of the file
# is the useful one.
# All the other
# function support it.
#
########################

import SpacePointADC as sp
import squares as sqr # support module
import math


def normgen(theta,phi):
    """ Returns a unit vector represented by a list of three elements.
    Its direction is defined in spherical coordinates by the given theta
    and phi angles. (Theta meaured as angle from x axis in xy plane, phi
    meausured as angle from z axis.)
    """
    vnorm = [0,0,0]
    vnorm[0] = math.cos(theta) * math.sin(phi)
    vnorm[1] = math.sin(theta) * math.sin(phi)
    vnorm[2] = math.cos(phi)
    return vnorm


def recurse_theta(eventscatter, start, wedge, phi, acc, partition=4, recurse='half'):
    """ Takes an event of (list of SpacePoint objects) a starting theta
    (in radians), a starting wedge (in radians), a
    constant phi angle (in radians), and a percent change between trials
    (as a decimal) that the function should stop at.
    Returns a tuple with the sum of squared distances as the first element
    and the best theta value that gives the least squares for a given
    phi as the second element.
    The argument partition takes an integer. It is the number of partitions
    the test should use.
    The argument recurse takes an integer 1 <= recurse <= partition.
    Its default is 'half', meaning half of the partition number, rounding
    up.
    """
    partition = float(partition)
    startsquare = sqr.squares(eventscatter,normgen(start,phi))
    if startsquare < 1:
        return (startsquare,start)
    thetatrials = []
    for i in range(int(partition)):
        thetatrials.append((start - (wedge/2.0)) + ((wedge/partition)*i))
    squaresresults = []
    for angle in thetatrials:
        squaresresults.append(sqr.squares(eventscatter,normgen(angle,phi)))
    pairs = zip(squaresresults,thetatrials) # for each tuple in this list,
    # index 0 in the sum of squares and index 1 is the value of the
    # variable theta that gives that sum (for a given phi).
    pairs.sort()
    if math.fabs(startsquare - pairs[0][0]) / startsquare < acc and math.fabs(startsquare - pairs[1][0]) / startsquare < acc:
        return pairs[0]
    if recurse == 'half':
        splitnum = int(math.ceil(partition/2.0))
    elif recurse == 'all':
        splitnum = int(partition)
    else:
        splitnum = int(recurse)
    split_result = []
    for i in range(int(splitnum)):
        split_result.append(recurse_theta(eventscatter,pairs[i][1],(2 * (wedge/partition)),phi,acc,partition,recurse))
    split_result.sort()
    return split_result[0]


def recurse_phi(eventscatter, start, wedge, theta, acc, partition=4, recurse='half'):
    """ Takes an event of (list of SpacePoint objects) a starting phi
    (in radians), a starting wedge (in radians), a
    constant theta angle (in radians), and a percent change between trials
    (as a decimal) that the function should stop at.
    Returns a tuple with the sum of squared distances as the first element
    and the best phi value that gives the least squares for a given
    theta as the second element.
    The argument partition takes an integer. It is the number of partitions
    the test should use.
    The argument recurse takes an integer 1 <= recurse <= partition.
    Its default is 'half', meaning half of the partition number, rounding
    up.
    """
    partition = float(partition)
    startsquare = sqr.squares(eventscatter,normgen(theta,start))
    if startsquare < 1:
        return (startsquare,start)
    phitrials = []
    for i in range(int(partition)):
        phitrials.append((start - (wedge/2.0)) + ((wedge/partition)*i))
    squaresresults = []
    for angle in phitrials:
        squaresresults.append(sqr.squares(eventscatter,normgen(theta,angle)))
    pairs = zip(squaresresults,phitrials) # for each tuple in this list,
    # index 0 in the sum of squares and index 1 is the value of the
    # variable phi that gives that sum (for a given theta).
    pairs.sort()
    if math.fabs(startsquare - pairs[0][0]) / startsquare < acc and math.fabs(startsquare - pairs[1][0]) / startsquare < acc:
        return pairs[0]
    if recurse == 'half':
        splitnum = int(math.ceil(partition/2.0))
    elif recurse == 'all':
        splitnum = int(partition)
    else:
        splitnum = int(recurse)
    split_result = []
    for i in range(int(splitnum)):
        split_result.append(recurse_phi(eventscatter,pairs[i][1],(2 * (wedge/partition)),theta,acc,partition,recurse))
    split_result.sort()
    return split_result[0]


def bestline(eventscatter,acc=0.02,partition=4,recurse='half'):
    """ Takes in a list with points as SpacePoint objects and finds the
    line of best fit, represented as a vector (magnitude 1) parallel to the line of best fit. Returns two endpoints of the line as SpacePoint
    objects.
    """
    best_theta = recurse_theta(eventscatter,0.0,math.pi,math.pi/2.0,acc, partition=partition, recurse=recurse)[1]
    best_phi = recurse_phi(eventscatter,0.0,math.pi,best_theta,acc, partition=partition, recurse=recurse)[1]
    best_vnorm = normgen(best_theta,best_phi)
    alongaxis = []
    for point in eventscatter:
        alongaxis.append(sqr.vorthdistance(point,best_vnorm,scalar_proj=True))
    alongaxis.sort()
    leastdist = alongaxis[0][0]
    greatestdist = alongaxis[len(alongaxis) -1][0]
    initial = sqr.vposition_of_centroid(eventscatter,best_vnorm)[0]
    pointA = sp.SpacePoint(x=((leastdist * best_vnorm[0]) + initial[0]), y=((leastdist * best_vnorm[1]) + initial[1]), z=((leastdist * best_vnorm[2]) + initial[2]))
    pointB = sp.SpacePoint(x=((greatestdist * best_vnorm[0]) + initial[0]), y=((greatestdist * best_vnorm[1]) + initial[1]), z=((greatestdist * best_vnorm[2]) + initial[2]))
    return (pointA, pointB)
