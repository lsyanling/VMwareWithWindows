"""Representation of cause-effect chains."""


class CauseEffectChain:
    """Cause-effect chain."""

    def __init__(self, id, chain, interconnected=[]):
        """Initialize a cause-effect chain."""
        self.id = id  # unique identifier
        self.chain = chain  # list of all tasks in the chain
        # List of local cause-effect chains and communication tasks. (Only in
        # the interconnected case.)
        self.interconnected = interconnected

        # Analysis results: (Are added during the analysis.)
        self.davare = 0  # Davare
        self.duerr_age = 0  # Duerr max data age
        self.duerr_react = 0  # Duerr max reaction time
        self.our_age = 0  # Our max data age
        self.our_react = 0  # Our max reaction time
        self.our_red_age = 0  # Our reduced max data age
        self.inter_our_age = 0  # Our max data age for interconn
        self.inter_our_red_age = 0  # Our reduced max data age for interconn
        self.inter_our_react = 0  # Our max reaction time for interconn
        self.kloda = 0  # Kloda

        self.DBAge = 0
        self.deltaBound = 0
        self.inter_detaBound = 0

        self.davareTime = 0

        self.duerrAgeTime = 0
        self.duerrReactionTime = 0

        self.gunzelAgeTime = 0
        self.gunzelReactionTime = 0

        self.klodaTime = 0

        self.DBAgeTime = 0
        self.deltaBoundTime = 0
        self.inter_detaBoundTime = 0

        self.multi_Kloda = 0
        self.multi_KlodaTime = 0

        self.multi_DBAge = 0
        self.multi_DBAgeTime = 0

        self.multi_DeltaBound = 0
        self.multi_DeltaBoundTime = 0

        self.multi_GunzelAge = 0
        self.multi_GunzelAgeTime = 0

        self.multi_GunzelReaction = 0
        self.multi_GunzelReactionTime = 0

        self.multi_DuerrAge = 0
        self.multi_DuerrAgeTime = 0

        self.multi_DuerrReaction = 0
        self.multi_DuerrReactionTime = 0

        self.processor = 0 # 处理器编号

    def length(self):
        """Compute the length of a cause-effect chain."""
        return len(self.chain)

    @property
    def chain_disorder(self):
        """Compute the chain disorder. (Not explained in our paper.)

        The disorder of a chain is the number of priority inversions along
        the data propagation path.
        """
        return sum(1 if self.chain[i].priority > self.chain[i+1].priority
                   else 0 for i in range(len(self.chain)-1))
