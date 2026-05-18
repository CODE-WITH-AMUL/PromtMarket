from django.db import models
from django.contrib.auth.models import User


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
    if not text:
        return text

    marker = "production requirements:"
    if marker in text.lower():
        return text

    return f"{text.strip()}{PRODUCTION_PROMPT_REQUIREMENTS}"


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Promt(TimeStampModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='prompts/', null=True, blank=True)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        # Ensure every stored prompt description asks for production-level output.
        self.description = enforce_production_prompt(self.description)
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.title