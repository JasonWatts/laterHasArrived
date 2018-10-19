#coding: utf8
#
# A class to keep track of the multiple identifiers associated with one of the people in the adjacency matrix.
#


class Person:
    def __init__(self, id_num, last, first, uid1=None, uid2=None):
        self.id_num = id_num
        self.last = last
        self.first = first
        self.uid1 = uid1
        self.uid2 = uid2
        self.duplicate = False

    def get_name(self):
        if self.duplicate:
            if self.uid1 is not None:
                if self.uid2 is not None:
                    return "%s, %s, %s, %s" % (self.last, self.first, self.uid1, self.uid2)
                return "%s, %s, %s" % (self.last, self.first, self.uid1)
        else:
            return "%s, %s" % (self.last, self.first)

    def set_duplicate(self):
        self.duplicate = True

    def get_duplicate(self):
        return self.duplicate
