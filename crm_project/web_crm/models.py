from django.db import models


class Record(models.Model):
    created_at = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.first_name} {self.first_name}"
