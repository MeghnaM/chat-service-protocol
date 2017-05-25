def acknowledgeConnectionAction():
    pass

def authenticationSuccessfulAction():
    pass

def authenticationFailedAction():
    pass

def serverDoesNotAcknowledgeAction():
    pass

def receivingMessageAction():
    pass

def receivePrivateChatMessageAction():
    pass

def receiveListOfChannelsAction():
    pass

def receiveQueuedMessagesAction():
    pass

def receivePositiveAcknowledgmentAction():
    pass

def receiveNegativeAcknowledgementAction():
    pass

def receiveGeneralErrorCodeAction():
    pass

def receiveUnknownCommandErrorAction():
    pass

def recieveSyntaxErrorAction():
    pass

resp_dict = {

    # positive responses - starting with 1
    "100": acknowledgeConnectionAction(),
    "110": authenticationSuccessfulAction(),
    "120": receivingMessageAction(),
    "130": receiveListOfChannelsAction(),
    "140": receiveQueuedMessagesAction(),
    "150": receivePositiveAcknowledgmentAction(),
    "160": receivePrivateChatMessageAction(),

    # negative responses - starting with 2
    "200": authenticationFailedAction(),
    "210": receiveNegativeAcknowledgementAction(),
    "220": serverDoesNotAcknowledgeAction(),

    # error codes
    "300": receiveGeneralErrorCodeAction(),
    "310": receiveUnknownCommandErrorAction(),
    "320": recieveSyntaxErrorAction()
}
