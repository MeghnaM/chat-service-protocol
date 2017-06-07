class ResponseHandler:
    """ResponseHandler class is used by the client to handle all the incoming responses from the server. 
    Almost all functions of ResponseHandler would be printing something to notify the client"""

    def __init__(self, obj):
        self.obj = obj

    def runResponseCodeAction(self, resp_code):
        if resp_code == "100":
            return self.acknowledgeConnectionAction(self.obj)
        elif resp_code == "110":
            return self.authenticationSuccessfulAction()
        elif resp_code == "120":
            return self.receivingMessageAction()
        elif resp_code == "130":
            return self.receiveListOfChannelsAction()
        elif resp_code == "140":
            return self.receiveQueuedMessagesAction()
        elif resp_code == "150":
            return self.receivePositiveAcknowledgmentAction()
        elif resp_code == "160":
            return self.receivePrivateChatMessageAction()
        elif resp_code == "170":
            return self.newGroupCreatedAction()
        elif resp_code == "180":
            return self.groupJoinedAction()
        elif resp_code == "190":
            return self.leftGroupAction()
        elif resp_code == "191":
            return self.banSuccessAction()
        elif resp_code == "192":
            return self.kickSuccessAction()
        elif resp_code == "200":
            return self.authenticationFailedAction()
        elif resp_code == "210":
            return self.serverDoesNotAcknowledgeAction()
        elif resp_code == "220":
            return self.receiveNegativeAcknowledgementAction()
        elif resp_code == "230":
            return self.groupCreationFailedAction()
        elif resp_code == "240":
            return self.joinGroupFailedAction()
        elif resp_code == "250":
            return self.banFailedAction()
        elif resp_code == "260":
            return self.kickFailedAction()
        elif resp_code == "300":
            return self.receiveGeneralErrorCodeAction()
        elif resp_code == "310":
            return self.receiveUnknownCommandErrorAction()
        elif resp_code == "320":
            return self.recieveSyntaxErrorAction()
        elif resp_code == "330":
            return self.incompatibleVersionAction()

    def banSuccessAction(self):
        print "****", self.obj.payload, "****"

    def banFailedAction(self):
        print "****", self.obj.payload, "****"

    def kickSuccessAction(self):
        print "****", self.obj.payload, "****"

    def kickFailedAction(self):
        print "****", self.obj.payload, "****"

    def acknowledgeConnectionAction(self, data):
        print self.obj.payload

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
        print "Choose Group"
        chatList = self.obj.payload
        for i in range(0, len(chatList)):
            print i+1, ":", chatList[i]

    def receiveQueuedMessagesAction(self):
        print self.obj.payload

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

    def newGroupCreatedAction(self):
        pass

    def groupCreationFailedAction(self):
        # print self.obj.payload
        pass

    def joinGroupFailedAction(self):
        print "****", self.obj.payload, "****"

    def groupJoinedAction(self):
        print "****", self.obj.payload, "****"
        print "-> ",

    def leftGroupAction(self):
        print "****", self.obj.payload, "****"
        print ""

    def incompatibleVersionAction(self):
        print "****", self.obj.payload, "****"