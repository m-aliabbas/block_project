from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Products(models.Model):
    p_name = models.CharField(max_length=50)
    p_price = models.DecimalField(max_digits=100, decimal_places=2)
    p_desc = models.TextField()
    p_featured = models.ImageField(default='default.jpg', upload_to='product_pics')
    p_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,default=1)
    ToBeSell = models.BooleanField(default=True)

    def __str__(self):
        return self.p_name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

    @property
    def imageURL(self):
        try:
            url = self.p_featured.url
        except:
            url = ''
        return url