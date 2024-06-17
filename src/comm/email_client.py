from azure.communication.email import EmailClient
from ..config import AZURE_EMAIL_KEY


class AzureEmailCommunicationClient:
    @property
    def client() -> EmailClient:
        return EmailClient.from_connection_string(AZURE_EMAIL_KEY)

    def send_email(
        self,
        message: str,
        to_email: str = "jcaponigro20@gmail.com",
        from_email: str = "tickets@scanbandz.com",
        subject: str = "Search Alert",
    ) -> None:
        msg = self.create_plain_email_message(to_email, from_email, subject, message)

        try:
            self.client.begin_send(msg)
        except Exception as ex:
            raise Exception(f"Failed to send email: {ex}")

    @staticmethod
    def create_plain_email_message(
        to_email: str, from_email: str, subject: str, message: str
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
