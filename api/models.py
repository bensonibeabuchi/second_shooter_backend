from django.db import models
from users.models import CustomUser
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver


class ShotList(models.Model):
    SHOT_TYPE_CHOICES = (
        ('Extreme Close Up', 'Extreme Close up'),
        ('Close Up', 'Close Up'),
        ('Medium Shot', 'Medium Shot'),
        ('Wide Shot', 'Wide Shot'),
        ('Extreme Wide Shot', 'Extreme Wide Shot'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="shot_lists", default=1)
    shot_description = models.TextField(blank=True, null=True)
    shot_type = models.CharField(max_length=512, choices=SHOT_TYPE_CHOICES, blank=True, null=True)
    image_reference = models.URLField(blank=True, null=True,)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


    def __str__(self):
        return f"{self.shot_description} - {self.shot_type}"
    
    class Meta:
        ordering = ['-created_at']

class ConsentForm(models.Model):
    subject_name = models.CharField(max_length=1000, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    photographer_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="consent_forms")
    date = models.DateTimeField(auto_now_add=True, null=True)
    agency_logo = models.ImageField(null=True, blank=True, upload_to="images/agency_logo")
    agency_name = models.CharField(max_length=1000, null=True, blank=True)
    subject_address = models.TextField(blank=True, null=True)
    subject_photograph = models.ImageField(upload_to="images/subject_photograph", null=True, blank=True)
    subject_signature = models.ImageField(upload_to="images/signature", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - {self.photographer_name}"
    
    class Meta:
        ordering = ['-updated_at']



class Project(models.Model):
    project_name = models.CharField(max_length=512)
    project_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    shot_list = models.ManyToManyField(ShotList, related_name="shot_lists", blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")
    project_type = models.CharField(max_length=512, blank=True, null=True)
    consent_form = models.ManyToManyField(ConsentForm, related_name="projects", blank=True)
    collaborators = models.ManyToManyField(CustomUser, related_name="collaborated_projects", blank=True,)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return self.project_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a unique slug by slugifying the project_name
            base_slug = slugify(self.project_name)
            slug = base_slug
            counter = 1

            # Ensure the slug is unique by appending a counter if necessary
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Assign the unique slug to the field
            self.slug = slug
        
        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at']