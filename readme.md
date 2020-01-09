RNMC Videos
========================================

Overview
----------------------------------------

A website where you can create galleries and add YouTube videos to them. They will be there anytime you want to watch them, without the need to look for them up again.

You can paste the URLs of the videos or search for keywords/fragments of the title you remember. The latter will make a list of six videos to pop up for you to add to your gallery. I have kept it at six, a small number indeed, because I am using a free YouTube API version, since this project is just to learn and practice.

Ajax via JQuery is used to fetch youtube results some seconds after you finish typing, and widget-tweaks module to beautify the forms. Anything that works with the database is handled by Class-Based Views and what tends to do tasks not related to models, by Function-Based Views. The user's data, videos and galleries are all protected from other users.

As for my other projects, please feel free to go to [my GitHub page](https://github.com/RenzoMurinaCadierno) to check them out. I am still on my learning tracks, so you will see new projects frequently. I specialize in Python and Javascript, and whatever I upload is normally related to web, game and app development, or Python scripting for multiple purposes.

I have put together this project up following Nick Walter's proposed exercise on his ['Mastering Django Part 1 - AJAX, Forms, CBV'](https://www.udemy.com/course/mastering-django-part-1-forms-class-based-views-ajax/) Udemy course. Definitely check it out if you want to learn some advanced concepts to deal with on this framework, specially the AJAX part. It was enlightening.

Instructions
------------------------------------------

Either go to [my hosted version](https://rnmcvideos.herokuapp.com/), or clone the project yourself.

If you decide to clone this project, do not forget to install the requirements mentioned in Pipfile, and ***KEEP IN MIND*** that this project is configured for Heroku deployment!

That means it will not work if you try to run it on a local server like it is. I suggest you create a heroku app, push it and work with it from the URL they give you.

Once inside, home page will not work, since it is configured to display the first two galleries as the most popular ones by default. No worries, though. go to your-heroku-site/signup, create an account and two galleries. From there on, everything should work.

What can you do in this project?
------------------------------------------

As an **anonymous user** you can:

- Sign up and, once you do so, log in. Needless to say, logging out is also an option.
- Search for and view other users's galleries.
- Watch other user's videos.

As a **logged-in user** you can:

- Everything an anonymous user can do.
- Create as many galleries as you like. They are designed to hold YouTube videos only. 
- Search for videos like the regular YouTube search bar, in which case six results will pop out on each search (due to YouTube API's free version), or you can paste the direct link to the video, which will automatically show it for you to add.
- Add or remove videos and galleries. You can also rename the galleries if you please.
- You are forbidden to modify any other user's data, galleries or videos. Access is restricted.

What I learned from this project
------------------------------------------
- AJAX is marvelous. Simulating the experience of a SPA is really something worth of UX. From now on, I will surely use it more frequently.
- Class-Based Views are well suited for operations that deal with the database exclusively, like CRUD instructions. Function-Based Views are to be applied in more generic tasks, or when you are not dealing with models.py directly.
- It is bit tricky to specify css classes on forms components with DJango. Fortunately, we have some modules to aid with the task.
- Rather than spamming the same class over and over again everywhere, just put it in a parent component and let all of their children inherit from it. I already knew this, but my mind was somewhere else when "beautifying" the website.
- To watch entity-relationship models closely, and name them all the same. This tends to avoid confusion and render everything up properly. The first thing to deal with on a Django project asides from the front-end sketching, are the models. Extremely important, since they are hard to modify later on.
- I miss Javascript, it has been a while since I have done something in the language. This little AJAX made me remember why I like it so much. I will try to add React to handle the views in upcoming projects.

### Thank you for reading and for taking your time to check this project out!