from django.db import models

# Create your models here.

class LogEntry(models.Model):
    user = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    message = models.CharField(max_length=255)
    api_name = models.CharField(max_length=100)
    api_type = models.CharField(max_length=100)
    send_data = models.CharField(max_length=100)
    get_data = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log Entry"           
        verbose_name_plural = "Log Entries"  
        ordering = ['-date_time']  
    
    def __str__(self):
        return f"{self.user} - {self.api_name} - {self.date_time}"
