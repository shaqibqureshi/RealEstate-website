from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from urllib.parse import urlencode

from .forms import ContactForm
from .models import ProjectPromo, Property


def home(request):
    return render(request, "home.html", {})


def about(request):
    return render(request, "about.html", {})


def property_list(request):
    """
    Renders properties.html.
    Supports ?type=buying / selling / renting and ?page=N,
    both of which the template already links to.
    """
    properties_qs = Property.objects.filter(is_published=True)

    listing_type = request.GET.get('type')
    if listing_type in ('buying', 'selling', 'renting'):
        properties_qs = properties_qs.filter(listing_type=listing_type)

    paginator = Paginator(properties_qs, 9)  # 9 per page = clean 3x3 grid
    properties = paginator.get_page(request.GET.get('page'))

    # Promotional project slides shown above the listings (managed in the admin).
    promo_projects = ProjectPromo.objects.filter(is_published=True)

    # 'properties' is a Page object here, so properties.has_next,
    # properties.number, etc. all work directly in the template.
    return render(request, 'properties.html', {
        'properties': properties,
        'promo_projects': promo_projects,
    })


def property_detail(request, pk):
    """Renders property_detail.html for a single listing."""
    property_obj = get_object_or_404(Property, pk=pk, is_published=True)

    related_properties = Property.objects.filter(
        is_published=True,
        listing_type=property_obj.listing_type,
    ).exclude(pk=property_obj.pk)[:3]

    og_url = request.build_absolute_uri(property_obj.get_absolute_url())

    description = property_obj.description.strip()
    if not description:
        description = (
            f"{property_obj.title} — {property_obj.location}. "
            f"{property_obj.bedrooms} bedroom, {property_obj.bathrooms} bathroom, "
            f"{property_obj.area_sqft} sqft."
        )
    if len(description) > 200:
        description = description[:197].rstrip() + "..."
    og_image = (
        request.build_absolute_uri(property_obj.image.url)
        if property_obj.image
        else ""
    )

    share_url = (
        f"https://wa.me/?"
        f"{urlencode({'text': f'Check out this property:\n{og_url}'})}"
    )

    context = {
        'property': property_obj,
        'related_properties': related_properties,
        'share_url': share_url,
        'og': {
            'title': property_obj.title,
            'description': description,
            'image': og_image,
            'url': og_url,
        },
    }
    return render(request, 'property_detail.html', context)


def privacy_policy(request):
    return render(request, "privacy.html", {})


def terms_and_conditions(request):
    return render(request, "terms.html", {})


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot filled → it's a bot. Pretend success, do nothing.
            if form.cleaned_data.get('website'):
                return redirect('contact')

            message_obj = form.save()

            # Notify the owner email without ever breaking the page
            # if email is not configured (e.g. local console backend).
            if settings.CONTACT_TO_EMAIL:
                try:
                    send_mail(
                        subject=f"New enquiry from Marina Realty: {message_obj.name}",
                        message=(
                            f"Name: {message_obj.name}\n"
                            f"Phone: {message_obj.phone}\n"
                            f"Email: {message_obj.email}\n"
                            f"Interested in: {message_obj.get_service_display()}\n"
                            f"Preferred date: {message_obj.preferred_date}\n"
                            f"Preferred time: {message_obj.preferred_time}\n"
                            f"Message: {message_obj.message}"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_TO_EMAIL],
                        fail_silently=True,
                    )
                except Exception:
                    pass  # never let a mail failure break the page

            messages.success(
                request,
                "Thanks — your request has been received. "
                "We'll confirm your appointment by email shortly.",
            )
            return redirect('contact')

    return render(request, 'contact.html', {'form': form})