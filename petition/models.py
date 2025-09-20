from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Petition(models.Model):
    """
    Represents a user petition to add a specific movie to the site.
    """
    movie_title = models.CharField(
        max_length=255,
        help_text="The title of the movie the user is petitioning for."
    )
    # Track the user who created the petition
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='petitions'
    )
    # Track which users have liked the petition
    likes = models.ManyToManyField(
        User,
        related_name='liked_petitions',
        blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time the petition was created."
    )

    def __str__(self):
        """String representation of the Petition object."""
        return f'"{self.movie_title}" by {self.user.username}'

    class Meta:
        # Orders petitions by most recent first
        ordering = ['-created_at']