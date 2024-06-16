from azure.communication.sms import SmsClient
from ..config import AZURE_SMS_KEY


class AzureSMSCommunicationClient:
    client: SmsClient = SmsClient.from_connection_string(AZURE_SMS_KEY)

    @classmethod
    def send_sms(cls, msg: str, number: str = "+19802148908"):
        try:
            sms_responses = cls.client.send(
                from_="+18339063716",
                to=number,
                message=msg,
                enable_delivery_report=True,  # optional property
            )
        except:
            print("Failed to send SMS")
            return False

        if len(sms_responses) == 1:
            # typical use case, only one response
            response = sms_responses[0]
            if not bool(response.successful):
                return False
            return True
        elif len(response) == 0:
            # no responses?? edge case fs
            return False
        else:
            for text in sms_responses:
                if not bool(text.successful):
                    return False
