# Search Controller
import datetime

def getnames():
    sval =''
    if  request.vars['q']:
        sval = request.vars['q']

        #queries with %LIKE% ****HERE BE THE DRAGONS!!!!******

        images = db(db.image.title.like(sval+'%')).select()
    else:
        #images = db(db.image.ALL).select()
        images = db().select(db.image.ALL)


    # finally - got a working syntax - watch out for (mis) matching parens 
    # combine IMG and A tags in generated XML that is passed to the view
    # tricky syntax
    # the LI [] structure below creates a list from the generator created by the inner for 
    # !!GOTCHA!! - Assignment of params is position dependent - ???forum qn???
    # Note the assignment of '_id' below needs to be at the end, not at the beginning
    # ??Web2py documentation issue??

    return XML( UL(*LI ([ (IMG (_src=URL('default','download', args= img.file), _width="120", _height="100"  ), A(img.title,_href=URL('default','show', args=img.id))) for img in images]) , _id='albumlist'))

    # the LI [] structure below creates a list from the generator created by the inner for 
    #return XML( UL(*LI ([ (IMG (_src=URL('default','download', args= img.file), _width="120", _height="100"  ), A(img.title,_href=URL('default','show', args=img.file))) for img in images])))
    
    
def gettags():
    # get list of tagnames from tag table
    tags  = db().select(db.tag.id, db.tag.name)
    #return XML(tags)
    return dict(tags=tags)        
 
def xmlgettags():
    # get list of tagnames from tag table
    # return in json format
    tags  = db().select(db.tag.id, db.tag.name).as_list()
    #return XML(tags)

    #return dict(id='1', name='places')

    return dict(taglist=tags)


    #return dict(id='1', name='places')


    #return dict(id=tags.id, name=tags.name)
    #return dict(item=tags)
    #return XML(tags)
    #return tags


def getimgtags():

    '''
    #    get tags associated with the selected image
    #    expect ajax request; json response from show image page
    #    rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5)
    #    .select(orderby=db.tagref.image)
    '''

    #   rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5).select()
    print '#### getimgtags #### '
    #imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select()
    imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select(db.tag.name)
    return dict(imgtags=imgtags)



def gettagsummary():
    '''
    Get list of tags and related counts (from tagref table) - user can then view by tag
    (similar to Stack Overflow tag view??) 
    '''
    count = db.tagref.tag.count()
    tagsummary = db(db.tagref.tag==db.tag.id).select(db.tagref.tag, db.tag.name, count, \
                    groupby=db.tagref.tag)

    rows =[]    
    # build array of tuples, then cvt to json?
    for r in tagsummary:
        res=[]
        res.append(('id',r.tagref.tag))
        res.append(('name',r.tag.name))
        res.append(('count',r[count]))
        rows.append(res)

    # passing too many data elements here to the view
    return dict(tagsummary=tagsummary)
    #return dict(tagsummary=rows)


def gettagdlt():
    '''
        Return detail list of images matching selected tag
    '''   
    pass


def getnames_v2():
    sval =''
    if  request.vars['q']:
        sval = request.vars['q']

        #queries with %LIKE% ****HERE BE THE DRAGONS!!!!******

        images = db(db.image.title.like(sval+'%')).select()
    else:
        images = db(db.image.ALL).select()
    # finally - got a working syntax - watch out for (mis) matching parens 
    # combine IMG and A tags in generated XML that is passed to the view
    # tricky syntax
    # the LI [] structure below creates a list from the generator created by the inner for 
    s = "<ul id='albumlist'>"
    for r in images:
        print  s
        s += LI(IMG(_src=URL('default','download', args= r.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=r.id))).xml()
        #s +=  ', '
        #s += A(r.title, _href=URL('default','show',args=r.id)).xml()
    s += "</UL>"
    #print s
    return XML(s)



def zz_getnames():
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
    #print s

    # finally - got a working syntax - watch out for (mis) matching parens 
    # combine IMG and A tags in generated XML that is passed to the view
    # tricky syntax
    # the LI [] structure below creates a list from the generator created by the inner for 
    return XML( UL(*LI ([ (IMG (_src=URL('default','download', args= img.file), _width="120", _height="100"  ), A(img.title,_href=URL('default','show', args=img.file))) for img in images])))
    


    #str = LI(IMG(_src=URL('default','download', args= r.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=r.id)))
    #print str.xml()

#    return XML(LI(IMG(_src=URL('default','download', args= img.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=img.id))) for img in images)
    #return x

    #return XML(s)

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


