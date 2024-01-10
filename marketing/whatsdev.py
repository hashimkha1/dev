class Whatsapp_Dev(TimeStampedModel):
    # types
    TYPE_CHOICES = [
        ("investments", "investments"),
        ("data_analysis", "data_analysis"),
        ("coda", "coda"),
        ("Job_Support", "Job_Support"),
        ("interview", "interview"),
        ("mentorship", "mentorship"),
        ("other", "other"),
    ]
    group_id = models.CharField(max_length=100, null=True, blank=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    participants = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="other",
    )
    def __str__(self):
        return self.group_name