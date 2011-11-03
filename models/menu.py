# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.title = request.application
#request.application= "Image Gallery"
response.title = "My Photo Gallery Demo"
response.subtitle = T('Web2py and CSS, JQuery vs Dojo Image Gallery Demo')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu += [
    (T('Home'), False, URL('default','index'), []),
    (T('Gallery - CSS'), False, URL('default','showcss'), []),
    (T('Gallery - JQuery'), False, URL('default','showjq'), []),
    (T('Gallery - Dojo'), False, URL('default','index'), []),
    (T('AjaxSearch - Dojo'), False, URL('default','sendform'), []),
    (T('Admin'), False, URL('admin','default','index'), [])

    ]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller    
    # useful links to internal admin and appadmin pages
   

    # useful links to external resources
#    response.menu+=[
# 
#    ]

_()
