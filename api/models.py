from django.db import models
from users.models import CustomUser

class ShotList(models.Model):
    SHOT_TYPE_CHOICES = (
        ('Extreme Close Up Shot', 'Extreme Close Up Shot'),
        ('Close Up Shot', 'Close Up Shot'),
        ('Medium Shot', 'Medium Shot'),
        ('Wide Shot', 'Wide Shot'),
        ('Extreme Wide Shot', 'Extreme Wide Shot'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="shot_lists", default=1)
    shot_description = models.TextField(blank=True, null=True)
    shot_type = models.CharField(max_length=512, choices=SHOT_TYPE_CHOICES, blank=True, null=True)
    image_reference = models.ImageField(blank=True, null=True, upload_to="images/reference_image")
    is_done = models.BooleanField(default=False)  # Boolean field for marking the shot as done

    def __str__(self):
        return f"{self.shot_description} - {self.shot_type}"

class ConsentForm(models.Model):
    subject_name = models.CharField(max_length=1000, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    photographer_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="consent_forms")
    date = models.DateTimeField(auto_now_add=True, null=True)
    # agency_logo = models.ImageField(null=True, blank=True, upload_to="images/agency_logo")
    agency_name = models.CharField(max_length=1000, null=True, blank=True)
    subject_address = models.TextField(blank=True, null=True)
    subject_photograph = models.ImageField(upload_to="images/subject_photograph")
    subject_signature = models.ImageField(upload_to="images/signature")

    def __str__(self):
        return f"{self.subject_name} - {self.photographer_name}"

class Project(models.Model):
    project_name = models.CharField(max_length=512)
    project_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=1000, unique=True)
    shot_list = models.ManyToManyField(ShotList, related_name="projects", blank=True)  # Changed to ManyToManyField
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")
    project_type = models.CharField(max_length=512, blank=True, null=True)
    # consent_form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE, related_name="projects", null=True, blank=True)

    def __str__(self):
        return self.project_name
