from django.db import models
from django.urls import reverse


class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ('buying', 'Buying'),
        ('selling', 'Selling'),
        ('renting', 'Renting'),
    ]

    STATUS_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
        ('Sold', 'Sold'),
        ('Rented', 'Rented'),
    ]

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='properties/')

    price = models.DecimalField(max_digits=12, decimal_places=2)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='For Sale')

    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this listing from the public site without deleting it."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()})"

    def get_absolute_url(self):
        return reverse('property_detail', args=[self.pk])


class PropertyImage(models.Model):
    """
    Extra gallery photos for a listing. Property.image stays as the
    main cover photo shown on the listings grid; these show up on the
    detail page as additional photos.
    """
    property = models.ForeignKey(
        Property, related_name='images', on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='properties/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Photo for {self.property.title}"


class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ('buying', 'Buying'),
        ('selling', 'Selling'),
        ('renting', 'Renting'),
        ('other', 'Something else'),
    ]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES, blank=True)
    agent = models.CharField(max_length=120, blank=True, help_text="Preferred agent, if any")
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"