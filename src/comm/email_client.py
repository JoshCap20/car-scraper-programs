from azure.communication.email import EmailClient
from ..config import AZURE_EMAIL_KEY


class AzureEmailCommunicationClient:
    client: EmailClient = EmailClient.from_connection_string(AZURE_EMAIL_KEY)

    @classmethod
    def send_email(
        cls,
        message: str,
        to_email: str = "jcaponigro20@gmail.com",
        from_email: str = "tickets@scanbandz.com",
        subject: str = "Search Alert",
    ) -> None:
        msg = cls.create_plain_email_message(to_email, from_email, subject, message)

        try:
            cls.client.begin_send(msg)
        except Exception as ex:
            raise Exception(f"Failed to send email: {ex}")

    @classmethod
    def create_plain_email_message(
        cls, to_email: str, from_email: str, subject: str, message: str
    ) -> dict:
        return {
            "senderAddress": from_email,
            "recipients": {
                "to": [{"address": to_email}],
            },
            "content": {
                "subject": subject,
                "plainText": message,
            },
            "replyTo": [
                {
                    "address": "support@scanbandz.com",
                    "displayName": "ScanBandz Support",
                }
            ],
        }
