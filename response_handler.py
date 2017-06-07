class ResponseHandler:
    def __init__(self, obj):
        self.pduData = obj


    def runResponseCodeAction(self, resp_code):
        if resp_code == "100":
            return self.acknowledgeConnectionAction(self.pduData)
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
        elif resp_code == "300":
            return self.receiveGeneralErrorCodeAction()
        elif resp_code == "310":
            return self.receiveUnknownCommandErrorAction()
        elif resp_code == "320":
            return self.recieveSyntaxErrorAction()



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
        print "Choose Group"
        chatList = self.pduData.payload
        for i in range(0, len(chatList)):
            print i+1, ":", chatList[i]

    def receiveQueuedMessagesAction(self):
        print self.pduData.payload

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
        # print self.pduData.payload
        pass

    def joinGroupFailedAction(self):
        print self.pduData.payload

    def groupJoinedAction(self):
        print "Group joined successfully"
