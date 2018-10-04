class Person:
    def __init__(self, id_num, last, first, uid1=None, uid2=None):
        self.id_num = id_num
        self.last = last
        self.first = first
        self.uid1 = uid1
        self. uid2 = uid2

    def get_name(self):
        return "%s%s" % (self.last, self.first)

    def get_name_and_uid(self):
        if uid1 is not None:
            if uid2 is not None:
                return "%s%s%s%s" % (self.last, self.first, self.uid1, self.uid2)
            return "%s%s%s" % (self.last, self.first, self.uid1)
        return get_name()
