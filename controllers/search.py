# Search Controller
import datetime

def getnames():
    # for ajax search -  find list of images - match on search string
    # (need to return list in json format ??)
    print '*************  processing ajax request *********** at %s' %datetime.datetime.now().ctime()

    sval =''
    if  request.vars['q']:
        sval = request.vars['q']

        #queries with %LIKE% ****HERE BE THE DRAGONS!!!!******

        images = db(db.image.title.like(sval+'%')).select()
    else:
        images = db(db.image.ALL).select()

#    html =  XML( <img src="{{=URL('download', args=image.file)}}" width="120"  height="100"  for image in images)

#    print '***************   html **********' html
  
    r = images[0]

    # return image and title for all matches
    #return XML(DIV(LI(*[IMG(_src=URL('default','download', args= r.file), _width="120", _height="100" ) for r in images])))

    #s = "<div class='myclass'>"
    #s =""
    s = "<ul id='albumlist'>"
    for r in images:
        print  s
        s += LI(IMG(_src=URL('default','download', args= r.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=r.id))).xml()
        #s +=  ', '
        #s += A(r.title, _href=URL('default','show',args=r.id)).xml()
    s += "</UL>"
    print s
    return XML(s)

#    return XML(UL(LI([IMG(_src=URL('default','download', args= r.file), _width="120", _height="100" ) \
#    for r in images])))

    # working 
    #return XML(DIV(LI(*[IMG(_src=URL('default','download', args= r.file), _width="120", _height="100" ) \
    #for r in images])))



# A(r.title, _href=URL('default','show',args=r.id)))))


    # return image and title as link  - one image
    #return XML(DIV(LI(IMG(_src=URL('default','download', args= r.file), _alt="", _width="120",  _height="100"), A(r.title, _href=URL('default','show',args=r.id)))))






#    return XML( A(IMG(_src=URL('default','download', args= r.file), _alt="", _width="120",  _height="100"), _href=URL('default','index')))

    

#<li><img  src="{{=URL('download', args=image.file)}}" width="120"  height="100" />{{=A(image.title, _href=URL("show", args=image.id))}}
#</li>


    # Can I do a redirect from ajax request with the search results ??
    #redirect (URL('default', 'showcss'))

    # Note the URL Syntax here to create a link to a different controller (the default)
    # How to show thumbnails for selected images here as well ??
#    return XML(UL(*[LI(A('%s ' % (img.title),_href=URL('default','show',args=img.id)))\
#                    for img in images]))


