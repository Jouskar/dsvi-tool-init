from django.db import models
from django.utils.translation import gettext_lazy as _


# Datasets should be sent via the rest framework to the react frontend
# Options are mainly affected by Leaflet options, so that should be handled via state through the frontend
# The type information is important enough to be passed to the front-end alongside the dataset
# Minimize total load on the front-end in terms of displaying the larger datasets by possibly adding a size field? TODO

class Dataset(models.Model):
    class Type(models.TextChoices):
        POINT = 'PT', _('Point')
        RASTER = 'RT', _('Raster')
        VECTOR = 'VT', _('Vector')

    fileName = models.CharField("file_name", max_length=240)
    name = models.CharField("name", max_length=240)
    type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.POINT  # Default as point data?
    )

    def __str__(self):
        return self.name
