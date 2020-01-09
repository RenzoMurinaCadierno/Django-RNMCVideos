from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from .models import Hall, Video
from .forms import VideoForm, SearchForm
import requests
import urllib

YOUTUBE_API_KEY = 'You yt api key here'


def home(request):

    # Query the database to retrieve the last 5 created halls.
    # Halls (galleries) are ordered by -id
    recent_galleries = Hall.objects.all().order_by('-id')[:5]

    # Get some random galleries as the most popular ones
    popular_galleries = [Hall.objects.get(pk=1), Hall.objects.get(pk=2)]

    # pass everything to the template and render it
    return render(
        request,
        'halls/home.html',
        {
            'recent_galleries': recent_galleries,
            'popular_galleries': popular_galleries
        }
    )


@login_required
def dashboard(request):

    # get all hall objects of the logged in user
    galleries = Hall.objects.filter(user=request.user)

    # render them as a context dictionary and return the view
    return render(request, 'halls/dashboard.html', {'galleries': galleries})


@login_required
def add(request, pk):

    # Call for the formset we just created
    form = VideoForm()

    # create the search videos form
    search_form = SearchForm()

    # Using the PK, get the current gallery
    gallery = Hall.objects.get(pk=pk)

    # A user can only add videos to their gallery
    if not gallery.user == request.user:

        raise Http404

    # If we get passed the previous if, then this is the correct user
    # in the correct gallery (the user in their gallery)
    if request.method == 'POST':

        # create the Form with the request POST data
        form = VideoForm(request.POST)

        # try to validate
        if form.is_valid():

            # create a video object
            video = Video()

            # We have the PK of the hall object in the params, we need
            # to go get it from the DB:
            video.hall = gallery

            # cleaned_data returns a dictionary with the valid user input
            video.url = form.cleaned_data['url']

            # Get the url and youtube_id of the video from the YT API.
            # a link is in the form of:
            # https://www.youtube.com/watch?v=XfFVIz38kho
            # Where the url is the whole link, and the id comes after v=

            # First, parse the url with the user submitted one as a param
            parsed_url = urllib.parse.urlparse(video.url)

            # grab the video's id from the 'v' parameter in the link
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')

            # if the statement was properly gotten.
            if video_id:

                # parse_qs returns is a list, where [0] the value of
                # the searched param
                video.youtube_id = video_id[0]

                # request Youtube API for the google video, passing
                # the above param as id, and the API KEY as key
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')

                # convert the response to json
                json = response.json()

                # get to the title in the JSON response.
                # It is inside 'items': 'snippet'
                title = json['items'][0]['snippet']['title']

                # assign the title to video.title
                video.title = title

                # save the form
                video.save()

                # redirect the user to its hall
                return redirect('detail_gallery', pk)

            # If we could not retrieve the statement
            else:

                # add the Error traceback of the 'url' field to
                # form's internal errors' list
                errors = form._errors.setdefault('url', ErrorList())

                # Assign some hints for the user
                errors.append('Only Youtube URLs are allowed.')

    # pass it to a template at any case
    return render(
        request,
        'halls/add.html',
        {'form': form, 'search_form': search_form, 'gallery': gallery}
    )


@ login_required
def search_video(request):

    # AJAX data comes from a GET request
    search_form = SearchForm(request.GET)

    # if we got the ajax correctly
    if search_form.is_valid():

        # get what is inside the search_term (the search input for AJAX)
        search_term = search_form.cleaned_data['search_term']

        # parse it to urllib
        encoded_search_term = urllib.parse.quote(search_term)

        # fetch the video URL using YT API KEY and the parsed
        # search term above
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBE_API_KEY}'
        )

        # Convert the response to JSON and return it as a JsonResponse
        return JsonResponse(response.json())

    # if the GET request could not be processed, also return a
    # JsonResponse, but with a failure
    return JsonResponse({'Error': 'Failed to retrieve information.'})


# A CBV to delete the videos
class DeleteVideo(LoginRequiredMixin, generic.DeleteView):

    # link the template, the model and the reverse when delete is successful
    model = Video
    template_name = 'halls/delete_video.html'
    success_url = reverse_lazy('dashboard')

    # a function that intercepts and overrides get_object() to perform
    # a check before returning the video object to delete.
    def get_object(self):

        # get the current video from the DB. DeleteView has the access.
        # call super().get_object() passing this class and object.
        video = super(DeleteVideo, self).get_object()

        # check for identity. If the logged in user is not the owner, 404.
        if not video.hall.user == self.request.user:
            raise Http404

        # The user is the owner, return the video and proceed with deletion.
        return video

class Signup(generic.CreateView):

    # Create and assign the user creation form
    form_class = UserCreationForm

    # If the user signed up in correctly, redirect to home, logged in
    success_url = reverse_lazy('dashboard')

    # Use as a django's default signup template for registration
    template_name = 'registration/signup.html'

    # If creates a user, autologin and redirect them to hall/create
    def form_valid(self, form):

        # Signup returns the view object we will return here later,
        # once we authenticate and log in the user.
        view = super(Signup, self).form_valid(form)

        # Get the username and the password1 from the form object
        username, password = \
            form.cleaned_data.get('username'), \
            form.cleaned_data.get('password1'),

        # Authenticate them
        user = authenticate(username=username, password=password)

        # log them in
        login(self.request, user)

        return view


class CreateHall(LoginRequiredMixin, generic.CreateView):

    # specify the model
    model = Hall

    # What fields are to be shown?
    fields = ['title']

    # Template name?
    template_name = 'halls/create_gallery.html'

    # On successful creation, reverse_lazy the user to:
    success_url = reverse_lazy('dashboard')

    # If the form is valid
    def form_valid(self, form):

        # Set up the user instance to be the request.user.
        # This adds the request user as the user variable in
        # Hall model.
        form.instance.user = self.request.user

        # Call for super(), pass this same class and this object
        # instance, and call for super().form_valid()
        super(CreateHall, self).form_valid(form)

        # Redirect them to their dashboard
        return redirect('dashboard')


# DetailView shows the details of the object you pass as a model
# by taking the int passed as a parameter to fetch it from the DB.
#   > It passes the lowercase name of the model (Hall) as the
#     object name to use in the template it renders.
class DetailHall(generic.DetailView):

    model = Hall

    template_name = 'halls/detail_gallery.html'


# The same as above, when getting a hall to update, the url will
# be /gallery/<int>/update
class UpdateHall(LoginRequiredMixin, generic.UpdateView):

    model = Hall

    template_name = 'halls/update_gallery.html'

    # Which fields to update?
    fields = ['title']

    # Where to redirect if they updated successfully?
    success_url = reverse_lazy('dashboard')

    def get_object(self):

        gallery = super(UpdateHall, self).get_object()

        if not gallery.user == self.request.user:
            raise Http404

        return gallery


class DeleteHall(LoginRequiredMixin, generic.DeleteView):

    model = Hall

    template_name = 'halls/delete_gallery.html'

    success_url = reverse_lazy('dashboard')

    def get_object(self):

        gallery = super(DeleteHall, self).get_object()

        if not gallery.user == self.request.user:
            raise Http404

        return gallery
