store_fr est une spécialisation de django-oscar pour le e-commerce français :
- TVA et affichage du TTC
- Opt-in pour les CGV à chaque vente

TODO :
- Template facture
- Extract compta

(liste dynamique à consulter et à compléter dans le bugtracker)

Installation :
==============


dependencies : `python-virtualenv libjpeg-dev libpq-dev python-dev postgresql-9.1 postgresql-contrib`


    virtualenv mystorert # Name your env as you want, it's a private python runtime

    . ./mystorert/bin/activate
    pip install pillow
    pip install django-oscar
    pip install psycopg2



    #  paypal custom component
    git clone https://github.com/nka11/django-oscar-paypal
    cd django-oscar-paypal
    python setup.py develop
    cd ..
    # store_fr
    git clone https://github.com/nka11/oscar-store-fr
    cd oscar-store-fr
    python setup.py develop
    cd ..

You can now start your django project and add to your settings.py :

    from oscar import get_core_apps

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.flatpages',
        'django.contrib.admin',
        'paypal',
        'south',
        'compressor',
        'yourapp',
    ] + get_core_apps([
        'partner',
        'shipping',
        'order',
        'basket',
        'checkout',
        'customer',
       ])

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'oscar.apps.basket.middleware.BasketMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    )


and your urls.py should look like :

    from django.conf.urls import include, url

    from django.contrib import admin
    admin.autodiscover()

    from app import application
    from paypal.express.dashboard.app import application as express_dashboard
    from checkout.views import OptInCGV

    admin.autodiscover()

    urlpatterns = [
        url(r'^i18n/', include('django.conf.urls.i18n')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^checkout/paypal/', include('paypal.express.urls')),
        url(r'^checkout/optinCgv/', OptInCGV.as_view()),
        url(r'^dashboard/paypal/express/', include(express_dashboard.urls)),
        url(r'', include(application.urls)),
    ]
