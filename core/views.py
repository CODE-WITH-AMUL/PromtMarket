from pathlib import Path

import polars as pl
from django.shortcuts import render

from .models import enforce_production_prompt


BASE_DIR = Path(__file__).resolve().parent.parent


def Home(request):
    template_name = 'home.html'
    return render(request, template_name)


def docs_page(request):
    return render(request, 'docs/docs.html')

def show_prompts(request):
    csv_path = BASE_DIR / 'Dataset' / 'prompts_production_ready.csv'

    if not csv_path.exists():
        return render(request, "prompts.html", {
            "data": [],
            "domains": [],
            "selected_domain": None
        })

    df = pl.read_csv(csv_path)

    if "Domain" in df.columns:
        df = df.rename({"Domain": "domain"})
    elif "domain" not in df.columns:
        return render(request, "prompts.html", {
            "data": [],
            "domains": [],
            "selected_domain": None
        })

    domains = df["domain"].unique().to_list()

    selected_domain = request.GET.get("domain")

    if selected_domain:
        df = df.filter(pl.col("domain") == selected_domain)

    data = df.to_dicts()

    for row in data:
        prompt_text = row.get("prompt_text")
        if isinstance(prompt_text, str):
            row["prompt_text"] = enforce_production_prompt(prompt_text)

    return render(request, "prompts.html", {
        "data": data,
        "domains": domains,
        "selected_domain": selected_domain
    })