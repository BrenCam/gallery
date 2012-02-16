def getimgtagsastable():

    '''
    #    get tags associated with the selected image
    #    expect ajax request; json response from show image page
    #    rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5)
    #    .select(orderby=db.tagref.image)

    #    return result as formatted table


    '''

    #   rows = db(db.tagref.tag==db.tag.id)(db.tagref.image>=5).select()
    print '#### getimgtags #### '
    #imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select()
    imgtags = db(db.tagref.tag==db.tag.id)(db.tagref.image==request.vars['q']).select(db.tag.name)

    res = (TABLE(*[TR(*r) for r in imgtags])).xml()
 
    return dict(imgtags=res)
