import random
from dataclasses import dataclass

from django.views.generic import TemplateView, ListView

from core.models import Picture, Project, Paper


@dataclass
class Link:
    link: str
    display: str
    link_args: str = ''


links = [
    Link(link='projects', display='Projects'),
    Link(link='publications', display='Publications'),
    Link(link='gallery', display='Gallery'),
]


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = links
        images_of_location = Picture.objects.filter(location__isnull=False)
        context['central_image'] = random.choice(images_of_location)
        return context


class GalleryFrontPageView(HomePageView):
    template_name = 'gallery/gallery_front.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations = set(Picture.objects.filter(
            location__isnull=False).values_list('location', flat=True))
        context['links'] = [
            Link(link='city', link_args=location, display=location) for
            location in locations
        ]
        return context


class CityPageView(ListView):
    template_name = 'gallery/city.html'
    model = Picture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.kwargs['slug']
        context['location'] = location
        return context

    def get_queryset(self, *args, **kwargs):
        location = self.kwargs['slug']
        images_of_location = self.model.objects.filter(location=location)
        landscape_images = [i for i in images_of_location if i.orientation == 'Landscape']
        portrait_images = [i for i in images_of_location if i.orientation == 'Portrait']
        return [landscape_images[n:n+3] for n in range(0, len(landscape_images), 3)] + [
            portrait_images[n:n+3] for n in range(0, len(portrait_images), 3)]


class ProjectsPageView(ListView):
    template_name = 'projects.html'
    model = Project
    context_object_name = 'papers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        context['blurb'] = """This page details some of the programming projects
            I've worked on in my spare time. More to come in the not too distant future."""
        return context


class PublicationsPageView(ListView):
    template_name = 'publications.html'
    model = Paper
    context_object_name = 'papers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publications'
        context['blurb'] = """My research interests lie primarily in the field of non-commutative algebra.
                             I'm particularly interested in Hopf algebras of finite GK-dimension, quantum groups,
                             quantum homogeneous spaces and Poisson algebraic groups. 
                             My published research papers in this field are listed below."""
        return context


class ContactPageView(HomePageView):
    template_name = 'contact.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portrait'] = Picture.objects.get(title='Self portrait')
        return context
