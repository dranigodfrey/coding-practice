from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Job
from .forms import ScraperForm
from .scraper import LinkedInScraper

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            number_of_job = form.cleaned_data['number_of_job']
                       
            # Initialize and run the scraper
            scraper = LinkedInScraper()
            jobs_data = scraper.scrape_job(number_of_job)
            new_jobs_count = scraper.save_jobs_to_db(jobs_data)
            
            messages.success(request, f"Scraped {len(jobs_data)} jobs. Added {new_jobs_count} new jobs to the database.")
            return redirect('job_list')
    else:
        form = ScraperForm()
    
    return render(request, 'scraper/index.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'scraper/job_list.html', {'jobs': jobs})