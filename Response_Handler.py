class ResponseHandler:


    pduData = PDUData()

    def __init__(self):
        self.resp_dict = {

            # positive responses - starting with 1
            "100": self.acknowledgeConnectionAction(pduData),
            "110": self.authenticationSuccessfulAction(pduData),
            "120": self.receivingMessageAction(pduData),
            "130": self.receiveListOfChannelsAction(pduData),
            "140": self.receiveQueuedMessagesAction(pduData),
            "150": self.receivePositiveAcknowledgmentAction(pduData),
            "160": self.receivePrivateChatMessageAction(pduData),

            # negative responses - starting with 2
            "200": self.authenticationFailedAction(pduData),
            "210": self.serverDoesNotAcknowledgeAction(pduData),
            "220": self.receiveNegativeAcknowledgementAction(pduData),

            # error codes
            "300": self.receiveGeneralErrorCodeAction(pduData),
            "310": self.receiveUnknownCommandErrorAction(pduData),
            "320": self.recieveSyntaxErrorAction(pduData)
        }

    def acknowledgeConnectionAction(self):
        print("Acknowledged")

    def authenticationSuccessfulAction(self):
        pass

    def authenticationFailedAction(self):
        pass

    def serverDoesNotAcknowledgeAction(self):
        pass

    def receivingMessageAction(self):
        pass

    def receivePrivateChatMessageAction(self):
        pass

    def receiveListOfChannelsAction(self):
        pass

    def receiveQueuedMessagesAction(self):
        pass

    def receivePositiveAcknowledgmentAction(self):
        pass

    def receiveNegativeAcknowledgementAction(self):
        pass

    def receiveGeneralErrorCodeAction(self):
        pass

    def receiveUnknownCommandErrorAction(self):
        pass

    def recieveSyntaxErrorAction(self):
        pass