class Voxel(object):
    """Creates an object representing a voxel that has the five attributes:
volume, row, column, bucket, adc. These values are all integers.
"""
    def __init__(self,volume=0,row=0,column=0,bucket=0,adc=0):
        self.volume = volume
        self.row = row
        self.column = column
        self.bucket = bucket
        self.adc = adc

    def __str__(self):
        print '(volume = %d, row = %d, column = %d, bucket = %d, adc = %d)' % (self.volume, self.row, self.column, self.bucket, self.adc)


