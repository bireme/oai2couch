function(doc, req) {  
    var ddoc = this;
    var Mustache = require('vendor/couchapp/lib/mustache');
    
    start({
        "headers":{
            "Content-Type": "text/xml; charset=utf-8"
        }
    });
    

    var result = {
                id: doc._id,
                provider: doc.provider,
                datestamp: doc.datestamp,
                publisher: doc.publisher,
                date_list: create_list(doc.date),
                format_list: create_list(doc.format),
                creator_list: create_list(doc.creator),
                contributor_list: create_list(doc.contributor),
                title_list: create_list(doc.title),
                description_list: create_list(doc.description),
                language_list: create_list(doc.language),
                identifier_list: create_list(doc.identifier),
                subject_list: create_list(doc.subject),
                type_list: create_list(doc.type),
                }
    
    
    var html = Mustache.to_html(ddoc.templates.solr_doc, result);

    return {
        "headers" : {"Content-Type" : "application/xml"},
        "body" : html
    }    
}


function create_list(field){
    value_list = []
    
    for each (var value in field)
       value_list.push({'content':value});
       
    return value_list;
}
