import datetime

class TraficoTCP_UDP:
    macAddress = str
    ## direction="original"
    originalDirection         = str
    #layer 3
    originalProtoum_Layer3    = str
    originalProtoname_Layer3  = str
    originalSRC_Layer3        = str
    originalDST_Layer3        = str
    #layer 4
    originalProtoum_Layer4    = str
    originalProtoname_Layer4  = str
    originalSPORT_Layer4      = str
    originalDPORT_Layer4      = str
    #counters
    originalPackets           = str
    originalBytes             = str

    ## direction = "reply"
    replyDirection         = str
    #layer 3
    replyProtoum_Layer3    = str
    replyProtoname_Layer3  = str
    replySRC_Layer3        = str
    replyDST_Layer3        = str
    #layer 4
    replyProtoum_Layer4    = str
    replyProtoname_Layer4  = str
    replySPORT_Layer4      = str
    replyDPORT_Layer4      = str
    #counters
    replyPackets           = str
    replyBytes             = str

    ## direction="independent"
    independentDirection = str
    state   = str
    timeout = str
    mark    = str
    use    = str
    id      = str
    date = str

    def __init__(self):
        self.macAddress = ""
        ## direction="original"
        self.originalDirection = ""
        self.originalProtoum_Layer3 = ""
        self.originalProtoname_Layer3 = ""
        self.originalSRC_Layer3 = ""
        self.originalDST_Layer3 = ""
        # layer 4
        self.originalProtoum_Layer4 = ""
        self.originalProtoname_Layer4 = ""
        self.originalSPORT_Layer4 = ""
        self.originalDPORT_Layer4 = ""
        # counters
        self.originalPackets = ""
        self.originalBytes = ""

        ## direction = "reply"
        self.replyDirection = ""
        # layer 3
        self.replyProtoum_Layer3 = ""
        self.replyProtoname_Layer3 = ""
        self.replySRC_Layer3 = ""
        self.replyDST_Layer3 = ""
        # layer 4
        self.replyProtoum_Layer4 = ""
        self.replyProtoname_Layer4 = ""
        self.replySPORT_Layer4 = ""
        self.replyDPORT_Layer4 = ""
        # counters
        self.replyPackets = ""
        self.replyBytes = ""

        ## direction="independent"
        self.independentDirection = ""
        self.state = ""
        self.timeout = ""
        self.mark = ""
        self.use = ""
        self.id = ""
        self.assured = ""
        self.unreplied = ""

