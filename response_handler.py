class ResponseHandler:
    def __init__(self, obj):
        self.pduData = obj
        self.resp_dict = {

            # positive responses - starting with 1
            "100": self.acknowledgeConnectionAction(self.pduData),
            "110": self.authenticationSuccessfulAction(),
            "120": self.receivingMessageAction(),
            "130": self.receiveListOfChannelsAction(),
            "140": self.receiveQueuedMessagesAction(),
            "150": self.receivePositiveAcknowledgmentAction(),
            "160": self.receivePrivateChatMessageAction(),

            # negative responses - starting with 2
            "200": self.authenticationFailedAction(),
            "210": self.serverDoesNotAcknowledgeAction(),
            "220": self.receiveNegativeAcknowledgementAction(),

            # error codes
            "300": self.receiveGeneralErrorCodeAction(),
            "310": self.receiveUnknownCommandErrorAction(),
            "320": self.recieveSyntaxErrorAction()
        }

    def acknowledgeConnectionAction(self, data):
            print self.pduData.payload

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
