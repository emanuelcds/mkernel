class Serializable(object):
    abstract = True

    def serialize(self):
        raise Exception("Not implemented!")


class SlotPrizeData(Serializable):
    paylines = []
    reelport = []

    def __init__(self):
        pass

    def serialize(self):
        pass
