from urllib.parse import urlencode

from django.conf import settings
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

    def get_public_url(self):
        """Absolute public URL for this listing (used for sharing links and OG tags)."""
        site_url = getattr(settings, 'SITE_URL', '').rstrip('/')
        return f"{site_url}{self.get_absolute_url()}"

    def get_whatsapp_share_url(self):
        """wa.me share link with the property link already pre-filled in the message."""
        message = f"Check out this property:\n{self.get_public_url()}"
        return f"https://wa.me/?{urlencode({'text': message})}"


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


class ProjectPromo(models.Model):
    """Promotional project cards shown above the property listings (managed in the admin)."""

    builder_name = models.CharField(max_length=120, help_text="e.g. Lodha Group")
    project_name = models.CharField(max_length=200, help_text="e.g. Lodha Malad Heights")
    location = models.CharField(max_length=255, help_text="e.g. Malad West, Mumbai")
    configuration = models.CharField(
        max_length=120, blank=True, help_text="e.g. 2 & 3 BHK"
    )
    starting_price = models.CharField(
        max_length=80, blank=True, help_text="e.g. ₹1.25 Cr onwards"
    )
    highlight = models.CharField(
        max_length=120, blank=True, help_text="e.g. Most Selling in Malad (shown as the card's badge)"
    )
    highlights = models.TextField(
        blank=True,
        help_text="2-4 short project highlights to show on the card — one per line.",
    )
    image = models.ImageField(
        upload_to='promos/',
        blank=True,
        help_text="Large project/building photo. Optional — a styled placeholder shows if left empty.",
    )
    link_url = models.URLField(
        blank=True,
        help_text="Where the 'View Project' button goes. Leave blank to scroll to the property listings.",
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text="Uncheck to hide this promotional card from the public site without deleting it.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Project promos'

    def __str__(self):
        return self.project_name

    @property
    def highlights_list(self):
        """Highlights as a list (one line = one highlight), empties filtered out."""
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]


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