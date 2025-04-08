from django import forms

class ScraperForm(forms.Form):
    number_of_job = forms.IntegerField(
        min_value=1,
        max_value=100,
        label="Number of jobs to scrape",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
 
