"""
This module implements the sql serialization.
"""

# Internal modules #
import track
from track.serialize import Serializer
from track.common import make_file_names

################################################################################
class SerializerSQL(Serializer):
    def __enter__(self):
        self.buffer = []
        self.current_track = None
        self.current_chrom = None
        self.file_paths = make_file_names(self.path)
        return self

    def __exit__(self, errtype, value, traceback):
        if self.current_track: self.closeCurrentTrack()

    def defineFields(self, fields):
        self.fields = fields
        #TODO

    def newTrack(self, attributes=None):
        # Close previous track #
        if self.current_track: self.closeCurrentTrack()
        # Get a name #
        path = self.file_paths.next()
        # Add it to the result #
        self.tracks.append(path)
        # Create it #
        self.current_track = track.new(path)
        # Add the metadata #
        #TODO

    def newFeature(self, chrom, feature):
        if chrom == self.current_chrom and len(self.buffer) < 1000:
            self.buffer.append(feature)
        else:
            self.flushBuffer()
            self.current_chrom = chrom
            self.buffer.append(feature)

    #-----------------------------------------------------------------------------#
    def closeCurrentTrack(self):
        # Empty buffer #
        self.flushBuffer()
        # Add the chromosome metadata #
        #TODO
        # Commit changes #
        self.current_track.save()
        self.current_track.close()
        # Reset varaibles #
        self.current_track = None
        self.current_chrom = None

    def flushBuffer(self):
        if self.buffer: self.current_track.write(self.current_chrom, self.buffer, self.fields)

#-----------------------------------#
# This code was written by the BBCF #
# http://bbcf.epfl.ch/              #
# webmaster.bbcf@epfl.ch            #
#-----------------------------------#
