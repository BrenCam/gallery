# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

#def index():
#    return dict(message=T('Hello World'))
    
    
def index():    
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

# dojo test form
def sendform():
    return dict()

def count():
    session.counter = (session.counter or 0) + 1
    return dict(counter=session.counter, now=request.now)

   
def show_v0():
    # need to check for valid selection here
    # ??display error/redirect??
    if not request.args(0):
        redirect(URL(r=request, f='index'))  
    image = db(db.image.id==request.args(0)).select().first()
    # builds a form for the specified fields
    form = SQLFORM(db.comment)
    # Add ref field explicitly as it's not part of the list 
    form.vars.image_id = image.id
    if form.process().accepted:
        response.flash = 'your comment is posted'
    # retrieve all comments for this image
    comments = db(db.comment.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

#    
#   New/CRUD Version of Show - simplifies Form Creation
#   next arg specifies URL to redirect to after form acceptance
#
def show():
    image = db.image(request.args(0)) or redirect(URL('index'))
    db.comment.image_id.default = image.id
    form = crud.create(db.comment,
                       message='your comment is posted',
            next=URL(args=image.id))
    comments = db(db.comment.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

def showcss():
    """
    CSS  Image View Photo View  
    Retrieve all images and pass to view
    """
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)        
    
def showjq():
    """
    JQuery Carousel Photo View  
    Retrieve all images and pass to view
    """
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)
        
def showdojo():
    """
    Dojo Carousel Photo View  
    Retrieve all images and pass to view
    """
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
