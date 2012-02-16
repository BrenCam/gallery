# Search Controller
import datetime

def listtags():
    '''
    List tags for each image
    Build dict of images and tags
    see: https://groups.google.com/forum/#!searchin/web2py/tag$20examples/web2py/j7Gy5gmf1EY/crQnrLzAooYJ
    '''

    query = db.image.id>0
    tags_d = db(db.tag.id>0).select(cache=(cache.ram,600)).as_dict()
    image_d = db(query).select().as_dict()
    links = db(db.tag.image.belongs(image_d.keys())).select()
    rows=[]
    for link in links:
         if rows and rows[-1][0].id==link.tag.image:
             tags=rows[-1][1]
         else:
             tags=[]
             rows.append((image_d[link.tag.image],tags))
         if link.tag.tag: tags.append(tags_d[link.tag.tag])

    for row in rows:
         print 'image object:', row[0], 'list of tags', row[1]
    return ""

def getjson():
    # return array of matching tag results
    tlist =['People','Places','Pears', 'Potatoes', 'Autos', 'Apricots', 'Apples']
    slist = []
    for item in tlist:
    #for row in db(db.tag.name.like(pattern)).select(distinct=True):
      #item = row 
      d = {}
      d['abbr'] = item[0:3]
      d['name'] = item
      slist.append(d)

    slist = []
    ddict = {}

    for row in db(db.tag.name.like('%')).select(distinct=True):
      #item = row 
      # remove any duplicates
      # build dict of tag names
      d = {}
      tdict = {}
      tdict['name'] = row.name
             
      d['abbr'] = row.name
      d['name'] = row.name
      slist.append(d)

      ddict[row.name] = row.name

    slist = []
    #for item in ddict.itervalues():
    for item in sorted(ddict.values()):

      d = {}       
      d['abbr'] = item[0:3]
      d['name'] = item       
      slist.append(d)

    dd ={}
    dd['identifier'] = 'abbr'
    dd['label']= 'name'
    dd['items'] = slist
    return dd


def fruittest():
  '''
      Simple json test for combobox
  '''
  flist =['oranges','apples','pears', 'apricots']
  dd = {}
  slist = []
  for item in flist:
    d = {}
    d['abb'] = item[0:3]
    d['name'] = item
    slist.append(d)

  dd['ident'] = "abb"
  dd['label'] = "name"

  dd['items'] = slist
  #return dict(taglist=dd)
  return dd


# auto complete for tag search - using Dojo here in lieu  of JQuery
def tagselect():
    if not request.vars.tag:
        print '#### No Tag Search Specified ###'
        return ''
    pattern = request.vars.tag.capitalize() + '%'
    selected = [row.name for row in db(db.tag.name.like(pattern)).select()]
    return ''.join([DIV(k,
        _onclick="prepareonetag()",
        #XHRGET('#tag').val('%s')" % k,
        #_onclick="jQuery('#tag').val('%s')" % k,
        _onmouseover="this.style.backgroundColor='yellow'",
        _onmouseout="this.style.backgroundColor='white'"
    ).xml() for k in selected])


def tagselectjson():
    # json version for filtering select autocomplete

    print "##### tagselectjson #####"
    if not request.vars.tag:
        print '#### No Tag Search Specified ###'
        pattern = '%'
    else:    
        #return ''
        #pattern = request.vars.tag.capitalize() + '%'
        pattern = request.vars.tag + '%'
    print "##### tagselectjson  - pattern: %s #####" %pattern
    #pattern = 'P%'
    #selected = [row.name for row in db(db.tag.name.like(pattern)).select()]
    #selected = [{['name']=row.name for row in db(db.tag.name.like(pattern)).select()}]
    s =[]
    for row in db(db.tag.name.like(pattern)).select():
        d={}
        d['abbr'] = row.name[0:3]
        d['name'] = row.name
        print 'abbr: %s, name: %s ' %(row.name[0:3], row.name)
        s.append(d)

    # return array of matching tag results
    tlist =['People','Places','Pears', 'Potatoes', 'Autos', 'Apricots']
    slist = []
    for item in tlist:
    #pattern = '%'
    #for row in db(db.tag.name.like(pattern)).select():
      #item = row 
      d = {}
      d['abbr'] = item[0:3]
      d['name'] = item
      slist.append(d)

    # return list of matching tags
    #print '#### Selection: %s' %selected
    #print '#### Selection: %s' %s

#
#    { identifier: 'abbr',
#      label: 'name',
#      items: [
#              { abbr:'ec', name:'Ecuador',           capital:'Quito' },
#              { abbr:'eg', name:'Egypt',             capital:'Cairo' },
#              { abbr:'sv', name:'El Salvador',       capital:'San Salvador' },
#              { abbr:'gq', name:'Equatorial Guinea', capital:'Malabo' },
#              { abbr:'er', name:'Eritrea',           capital:'Asmara' },
#              { abbr:'ee', name:'Estonia',           capital:'Tallinn' },
#              { abbr:'et', name:'Ethiopia',          capital:'Addis Ababa' }
#      ]}

    dd ={}
    dd['identifier'] = 'abbr'
    dd['label']= 'name'
    #dd['items'] = selected
    dd['items'] = slist
    #return dict(taglist=dd)
    return dd

#def assigntags(image_id, *tags):
def assigntags():

    """
    Created: 11/26/2011 - BC
    Assign a list of user specified tags to an image
    (User can enter a comma delimited list of tags - ??autocomplete??)
    If tag does not already exist
    Create a new tag entry before creating a tagref entry
    """

    print '### assigntags: %s ### ' %request.vars['q']
    if not request.vars['q']:
        print ('######## no data received from caller #######')
        return

    print '### Decode Json '
    import json
    # decode the incoming json request
    # convert json to python object (dictionary)
    rq = json.loads (request.vars['q'])

    image_id = rq['imageid']    #request.args(0)
    tags =  rq['tags']
    print 'tags: %s' %tags
    #tags =  rq['tags'].split(",")

    for tag in tags:
        print '### Iterate ### Tag: %s' %tag.strip()

        # check for empty tag
        if tag == '':
            continue

        # check if tag already exists
        # get tagid from table as we need this to create the tagref entry
        tid = 0
        if (db(db.tag.name==tag).count() == 0):
            # remove leading/trailing chars
            tid = db.tag.insert(name=tag.strip())
            print "### (1) Tag ID: %s" %(tid)

        else:
            # Formatting gotcha here - need to extract the value component only
            # as object returned is of type row
            tid = db(db.tag.name==tag.strip()).select(db.tag.id)[0]['id']
            print "### (2) Tag ID: %s" %(tid)

        # Ignore any duplicate tag request - skip to next request
        print "### assign tags: Image: %s, Tag: %s" %(image_id, tid)

        if (db(db.tagref.tag==tid)(db.tagref.image==image_id).count() > 0):
            print '### Duplicate Request Found: Image: %s, Tag: %s' %(image_id, tid)
            continue

        # create tag ref entry to assign tag to image
        tagref = 0
        tagref = db.tagref.insert(image=image_id,tag=tid)
        print '### Created new tagref rec: %s for image: %s' %(tid, image_id)
    return buildtagtable(image_id)


def buildtagtable(image_id):
    """
    After tag creation refresh tag list with updated results
    Build a formatted table of tag names and checkboxes for an image
    """

    # get list of currently assigned tags
    imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==image_id).select(db.tag.name)

    # Add dummy col - used for the checkbox
    arr = []
    for item in imgtags:
        s = [[item.name , '<input id="%s" />' %item.name]]
        chbx = (INPUT( _type='checkbox', _name= 'chk%s' %item.name, _id='chk%s_id' %item.name))
        arr.append ([[item.name],[ chbx]])

    xmlstr =""
    # build data elements as a single table row
    for item in arr:
        xmlstr += TD(item[0]).xml() +  TD(item[1]).xml()
    s2 = (TABLE(xmlstr))
    print '### XML String: %s' %xmlstr
    print '### XML String2: %s' %s2

    pfx = '<table id="tagtable" class="taglist"><tr>'
    sfx = '</tr></table>'

    xres2 = pfx + xmlstr + sfx


    #xres =   XML(TABLE(*[TR(*r) for r in arr], _id = 'tagtable'))
    #print '### XML String3: %s' %xres
    print '\n ***** XML String3: %s' %xres2
    #return XML(TABLE(*[TR(*r) for r in arr], _id = 'tagtable'))
    return xres2

    # how to display as a single row
    #return XML(TABLE(*[TD(*r) for r in arr], _id = 'tagtable'))

#
#    rows=db(query).select(*fields).as_list()
#    if rows:
#        table=TABLE(*[TR(TH(field),*[TD(row[field]) for row in rows]) for field in row[0].keys()])
#        table=TABLE(*[TD(row[field]) for row in rows]) for field in row[0].keys())
#    else:
#        table="nothing to see here"
#    return dict(table=table)
    #return XML(TABLE(*[TD (r[0], r[1]) for r in arr], _id='tagtable'))


def removetags():
    """
    Decode the incoming JSON string and convert the result
    to an object using a JSON parser for the language of your choice.
    At http://www.json.org, you'll find JSON parsers for many modern programming languages.
    The methods available depend upon which parser you are using.
    See the parser's documentation for details.        
    Remove tag(s) from selected image.
    Request is a json format containing image id and tag names/ids
    This is converted to a Python Dictionary
    On completion update/refresh the view to reflect the changes
    """

    print '### removetags: %s ### ' %request.vars['q']
    if not request.vars['q']:
        print ('######## no data received from caller #######')
        return
    
    import json
    #rq = json.dumps(request.vars['q'])

    # convert json to python object (dictionary)
    rq = json.loads (request.vars['q'])
    
    print '#### Json Remove Tags Request: %s' %rq
    
    image_id = rq['imageid']    #request.args(0)
    tagnames =  rq['tags']
    # need to convert tag names here to tagids here as tag name is passed from client

    #ldict = db(db.tag.name.belongs(['Places','Cars'])).select(db.tag.id).as_dict()
    tagdict = db(db.tag.name.belongs(tagnames)).select(db.tag.id).as_dict()
    # npw get the keys
    taglist = tagdict.keys()
    #taglist = [1]
    # Select/Delete matching images
    res =  db(db.tagref.image==image_id)(db.tagref.tag.belongs((taglist))).delete()
    #res =  db(db.tagref.image==image_id)(db.tagref.tag.belongs((taglist)))._delete()
    #res =  db(db.tagref.image==image_id)(db.tagref.tag.belongs((taglist)))._select()

    print '**** Deleting requested tags: %s' %res

    # after tag removal refresh tag list with updated results
    return buildtagtable(image_id)

def addtags():
    """
    Add new tag(s) to selected image.
    If tag already exists add to tagref tbl. Some tag checks:
    - Duplicate name, Proper Name, Case Match,  
    Otherwise create new tag rec and related tagref entry    
    """
    pass

def getnames():
    
    sval =''
    if  request.vars['q']:
        sval = request.vars['q']

        #queries with %LIKE% ****HERE BE THE DRAGONS!!!!******
        print '****** GetNames matching: %s **********' %sval
        images = db(db.image.title.like(sval+'%')).select()
    else:
        #images = db(db.image.ALL).select()
        print '****** Get All ********' 
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
    
def cbxtest():
    # get list of tagnames from tag table
    tags  = db().select(db.tag.id, db.tag.name)   #return XML(tags)
    return dict(taglist=tags)   

   
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

def getimgtagsastable():

    """
    #    get tags associated with the selected image
    #    expect ajax request; json response from show image page
    #    rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5)
    #    .select(orderby=db.tagref.image)
    #    return result as formatted table

    """

    #   rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5).select()
    print '#### getimgtagsastable #### '
    #imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select(db.tag.name)

    # after tag removal refresh tag list with updated results
    image_id = request.vars['q']
    return buildtagtable(image_id)


def getimgtags():

    """
    #    get tags associated with the selected image
    #    expect ajax request; json response from show image page
    #    rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5)
    #    .select(orderby=db.tagref.image)
    """

    #   rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5).select()
    print '#### getimgtags #### '
    #imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select()
    imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select(db.tag.name)
    return dict(imgtags=imgtags)


def gettagsummary():
    """
    Get list of tags and related counts (from tagref table) - user can then view by tag
    (similar to Stack Overflow tag view??) 
    """
    count = db.tagref.tag.count()
    tagsummary = db(db.tagref.tag==db.tag.id).select(db.tagref.tag, db.tag.name, count, \
                    groupby=db.tagref.tag)

#    tagsum = db(db.tagref.tag==db.tag.id).select(db.tagref.tag, db.tag.name, count, \
#                    groupby=db.tagref.tag).as_list()

    # build custom list of dicts here  
    tlist = []

    for item in tagsummary:                
        d = {}
        tagid = item.tagref.tag
        name = item.tag.name
        d['count'] = item[count]    # <-- note the syntax
        #d['name'] = item.tag.name
        d['name'] = A( XML(name), _href='/gallery/search/getbytag/%s' %tagid).xml()        
        #d['name'] = A( XML(name), _href='/gallery/default/getbytag/%s' %tagid).xml()        
        d['id'] = tagid
        tlist.append(d)
    
#    for debugging
#    import json
#    str = json.dumps(tlist)
#    print '\n **** JSON %s: ' %str

    # return custom results
    return dict(tagsummary=tlist)

def getbytag():
    """
        Return detail list of images matching selected tag
    """ 

    if  request.args(0):
        tagval = request.args(0)

        #queries with %LIKE% ****HERE BE THE DRAGONS!!!!******
        images = db(db.tagref.tag==db.tag.id)(db.tag.id==tagval)(db.image.id==db.tagref.image).select(db.image.ALL)
    else:
        images = db(db.image.ALL).select()

    s = "<ul id='albumlist'>"
    for r in images:
        print  s
        s += LI(IMG(_src=URL('default','download', args= r.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=r.id))).xml()
    s += "</UL>"

    # explicity specify the view
    # response.view = 'default/index.html'
    response.view = 'search/tagmatches.html'

    # response.render (view,dict)
 

    # return ajax response
    #return XML(s)

    # ?? redirect required here ??    
    # return dictionary of results
    #redirect (URL(r=request, f='/default/index'))

    # need to set the img url to point to the correct/download directory
    #imglist =[]
    
    return dict(images=images)

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
        #print  s
        s += LI(IMG(_src=URL('default','download', args= r.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=r.id))).xml()
        #s +=  ', '
        #s += A(r.title, _href=URL('default','show',args=r.id)).xml()
    s += "</UL>"
    #print s
    return XML(s)


