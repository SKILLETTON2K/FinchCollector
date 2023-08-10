from django.db import models
from django.urls import reverse
from datetime import date

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})

class Bird(models.Model):
  name = models.CharField(max_length=100)
  family = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  toys = models.ManyToManyField(Toy)

  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'bird_id': self.id})

# Add new Feeding model below Bird model
class Feeding(models.Model):
  date = models.DateField('feeding date ')
  meal = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=MEALS,
    # set the default value for meal to be 'B'
    default=MEALS[0][0]
  )
    # Create a bird_id FK
  bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
  
  def _str__(self):
    return f"{self.get_meal_display()} on {self.date}"
  class Meta:
    ordering =['-date']