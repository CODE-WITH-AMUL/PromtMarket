from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify


PRODUCTION_PROMPT_REQUIREMENTS = (
    "\n\nProduction Requirements:\n"
    "- Use clean, modular, maintainable architecture.\n"
    "- Include robust error handling and input validation.\n"
    "- Follow security best practices and avoid hardcoded secrets.\n"
    "- Add clear comments/docstrings for non-trivial logic.\n"
    "- Include tests and edge-case handling.\n"
    "- Optimize for readability, scalability, and performance."
)


def enforce_production_prompt(text: str) -> str:
    """
    Append production requirements only once.
    """
    if not text:
        return text

    marker = "production requirements:"
    if marker in text.lower():
        return text

    return f"{text.strip()}{PRODUCTION_PROMPT_REQUIREMENTS}"


class TimeStampModel(models.Model):
    """
    Base model for automatic timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Promt(TimeStampModel):
    title = models.CharField(
        max_length=255,
        db_index=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="prompts/",
        null=True,
        blank=True
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"

    def clean(self):
        """
        Custom validation.
        """

        if self.image:
            max_size = 5 * 1024 * 1024

            if self.image.size > max_size:
                raise ValidationError({
                    "image": "Image must be less than or equal to 5MB."
                })

    def generate_unique_slug(self):
        """
        Generate unique slug:
        Example:
        ai-builder
        ai-builder-1
        ai-builder-2
        """

        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while Promt.objects.filter(slug=slug).exclude(
            pk=self.pk
        ).exists():

            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        """
        Override save method.
        """

        self.description = enforce_production_prompt(
            self.description
        )

        if not self.slug:
            self.slug = self.generate_unique_slug()

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title