from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25,default="")
    #uid = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'






class Alert(models.Model):
    ALERT_NAME_CHOICES = [
        ('TEMP_RISE', 'Temperature Rise'),
        ('RAINING', 'Raining'),
        ('THUNDERSTORM', 'Thunderstorm'),
    ]

    CONDITION_CHOICES = [
        ('GT', 'Greater Than'),
        ('LT', 'Less Than'),
        ('EQ', 'Equals'),
    ]

    alert_name = models.CharField(max_length=50, choices=ALERT_NAME_CHOICES)
    city_names = models.ForeignKey(City, on_delete=models.CASCADE, default=None, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    threshold = models.FloatField(default=0)

    def __str__(self):
        return f"{self.alert_name} - {self.city_names}"



        