class Whatsapp_Groups(models.Model):
    # types
    CATEGORY_CHOICES = [
        ("Finance", "Finance"),
        ("IT", "IT"),
        ("Internal", "Internal"),
        ("Political", "Political"),
        ("Business", "Business"),
        ("other", "other"),
    ]
    TYPE_CHOICES = [
        ("investments", "investments"),
        ("data_analysis", "data_analysis"),
        ("coda", "coda"),
        ("Job_Support", "Job_Support"),
        ("interview", "interview"),
        ("mentorship", "mentorship"),
        ("other", "other"),
    ]
    id = models.AutoField(primary_key=True)
    group_id = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True,unique=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    participants = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(
        max_length=25,
        choices=CATEGORY_CHOICES,
        default="other",
    )
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="other",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    def __str__(self):
        return self.group_name
