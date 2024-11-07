from django.db import models
import requests
from django.core.exceptions import ValidationError
from app.utils import validate_video_file_size


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    start_date = models.DateField()
    end_date = models.DateField()
    trailer = models.FileField(
        upload_to='course_trailers/',
        validators=[validate_video_file_size],
        blank=True,
        null=True,
        help_text="Upload a trailer video (up to 100MB)"
    )

    def __str__(self):
        return self.title
    

class HelpGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    chat_id = models.CharField(max_length=50, help_text="Telegram group chat ID")

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    details = models.TextField()
    help_group = models.ForeignKey(HelpGroup, on_delete=models.CASCADE, related_name="contacts", help_text="Select the Telegram group", blank=True, null=True)

    def __str__(self):
        return self.name

    def send_to_telegram(self, bot_token):
        # Format the message with contact details
        message = (
            f"<b>Yangi Xabar</b>\n"
            f"<b>FIO</b>: {self.name}\n"
            f"<b>Telefon nomer</b>: {self.phone_number}\n"
            f"<b>Xabar</b>: {self.details}"
        )
        
        # Ensure help_group and chat_id exist
        if not self.help_group or not self.help_group.chat_id:
            raise ValidationError("No valid Telegram group assigned to this contact.")
        
        # Send message using Telegram's sendMessage API
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': self.help_group.chat_id,
            'text': message,
            'parse_mode': 'HTML'  # Enable Markdown parsing
        }
        
        # Send the request
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"Failed to send message: {e}")

    def save(self, *args, **kwargs):

        if self.help_group is None:
            try:
                latest_help_group = HelpGroup.objects.latest('id')
                self.help_group = latest_help_group
            except HelpGroup.DoesNotExist:
                raise ValidationError("No HelpGroup available to assign.")
        
        is_new = self.pk is None
        
        # Save the instance first to ensure it has a primary key
        super().save(*args, **kwargs)

        # After saving, attempt to send to Telegram if it's a new instance
        if is_new:
            from django.conf import settings
            bot_token = settings.TELEGRAM_BOT_TOKEN  # Ensure TELEGRAM_BOT_TOKEN is in settings
            try:
                self.send_to_telegram(bot_token)
            except ValidationError as e:
                # Log or handle error as needed
                print(f"Error sending to Telegram: {e}")
