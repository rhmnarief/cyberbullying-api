class ResponseMessage(object):
    def __init__(self, reasons, messages):
        self.reasons = reasons
        self.messages = messages
    
    def send(self):
        response = {
            'validated' : f"{self.reasons}",
            'messages' : f"{self.messages}",
        }
        return response
