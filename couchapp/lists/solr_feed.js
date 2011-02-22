function(head, req) {
    var ddoc = this;
    var Mustache = require('vendor/couchapp/lib/mustache');
    var head_list = [];
    var rows = [];
    var row;

    start({
        "headers":{
            "Content-Type": "text/xml; charset=utf-8"
        }
    });

    for(k in head){
        head_list.push({'key':k,'value':head[k]});
    }

    while(row = getRow()) {

        rows.push({
                    id: row.doc.id,                    
                    provider: row.doc.provider,
                    datestamp: row.doc.datestamp,
                    publisher: row.doc.publisher,
                    date_list: create_list(row.doc.date),
                    format_list: create_list(row.doc.format),
                    creator_list: create_list(row.doc.creator),
                    contributor_list: create_list(row.doc.contributor),
                    title_list: create_list(row.doc.title),
                    description_list: create_list(row.doc.description),
                    language_list: create_list(row.doc.language),
                    identifier_list: create_list(row.doc.identifier),
                    subject_list: create_list(row.doc.subject),
                    type_list: create_list(row.doc.type),
                   });
    }
    
    var view = {
        head: head_list,
        rows: rows,
    }
    
    var html = Mustache.to_html(ddoc.templates.solr_doc_list, view);
    return(html);               
};

function create_list(field){
    value_list = []
    
    for each (var value in field)
       value_list.push({'content':value});
       
    return value_list;
}
