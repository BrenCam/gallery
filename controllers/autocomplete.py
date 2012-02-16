__author__ = 'brencam'

def actest():
    return dict()


def tagselector():
    '''
    Auto complete test controller -
    Uses Ajax calls to populate a test control with a list of possible tag values
    '''

    #request.vars.tag ='P'
    print 'AutoComplete:tagselector - Process AC request: %s' %request.vars
    if not request.vars.tagInput:
        print '#### No Tag Search Specified ###'
        return
    #pattern = request.vars.tagInput.capitalize() + '%'
    pattern = request.vars.tagInput + '%'

    selected = [row.name for row in db(db.tag.name.like(pattern)).select()]
    return ''.join([DIV(k,
        #_onclick="prepareonetag()",
        #XHRGET('#tag').val('%s')" % k,
        _onclick="jQuery('#tagInput').val('%s')" % k,
        _onmouseover="this.style.backgroundColor='yellow'",
        _onmouseout="this.style.backgroundColor='white'"
    ).xml() for k in selected])




  