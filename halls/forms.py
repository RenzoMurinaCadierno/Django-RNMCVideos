from .models import Video
from django import forms

# Model-based form
class VideoForm(forms.ModelForm):

    # Meta class are the attributes ModelForm needs to display
    # the form linked to the model correctly.
    class Meta:

        # you pass a model and the form is created automatically.
        model = Video

        # Specify the fields to be shown. The Hall linked as a pk is
        # not passed since it is already linked to the hall this site
        # will be called from, via its hall variable.
        fields = ['url']

        # show this labels
        labels = {'url': 'YouTube URL:'}


# Regular form
class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=256, label="Search:")
