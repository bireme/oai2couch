function(doc, req) {  
    var ddoc = this;
    var Mustache = require('vendor/couchapp/lib/mustache');
    
    start({
        "headers":{
            "Content-Type": "text/xml; charset=utf-8"
        }
    });
    
    var creators = [];
    var titles = [];
    
    for each (var value in doc.creator)
        creators.push({'name':value});
    for each(var value in doc.title)
        titles.push({'title':value});            

    var result = {
                id: doc._id,
                creators: creators,
                titles: titles,
                }
    
    result.type = "part";
    var html = Mustache.to_html(ddoc.templates.solr_doc, result);

    return {
        "headers" : {"Content-Type" : "application/xml"},
        "body" : html
    }    
}
