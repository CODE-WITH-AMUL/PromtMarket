from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from .models import enforce_production_prompt
from .services.prompt_catalog import get_prompt_catalog


BASE_DIR = Path(__file__).resolve().parent.parent


def home_view(request):
    template_name = 'home.html'
    return render(request, template_name)


def docs_page(request):
    return render(request, 'docs/docs.html')


def health_check(request):
    return JsonResponse({'status': 'ok'}, status=200)


@login_required
def show_prompts(request):
    csv_path = BASE_DIR / 'Dataset' / 'cleaned_datasets.csv'
    selected_domain = request.GET.get("domain")
    rows, domains = get_prompt_catalog(csv_path, selected_domain)

    if selected_domain and selected_domain not in domains:
        selected_domain = None
        rows, domains = get_prompt_catalog(csv_path, selected_domain)

    paginator = Paginator(rows, 25)
    page_obj = paginator.get_page(request.GET.get('page'))
    data = list(page_obj.object_list)

    for row in data:
        prompt_text = row.get("prompt_text")
        if isinstance(prompt_text, str):
            row["prompt_text"] = enforce_production_prompt(prompt_text)

    return render(request, "prompts.html", {
        "data": data,
        "domains": domains,
        "selected_domain": selected_domain,
        'page_obj': page_obj,
    })