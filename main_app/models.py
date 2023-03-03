from django.db import models
from django.urls import reverse

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.

#class inheritance
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id' : self.id})
    
# Add new Feeding model below Cat model
class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(
        choices= MEALS,
        default= MEALS[0][0],
        max_length=1
    )
    #add cat foreign key reference
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.get_meal_display()} on {self.date}'
