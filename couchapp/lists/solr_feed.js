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
        var creators = [];
        var titles = [];
        var descriptions = [];
        
        for each (var value in row.value.creator)
            creators.push({'name':value});
        for each(var value in row.value.title)
            titles.push({'title':value});            
        for each(var value in row.value.description)
            descriptions.push({'description':value});            

        rows.push({
                    id: row.value._id,
                    creators: creators,
                    titles: titles,
                    descriptions: descriptions,
                    type: row.value.type,
                   });
    }
    
    var view = {
        head: head_list,
        rows: rows,
    }
    
    var html = Mustache.to_html(ddoc.templates.solr_doc_list, view);
    return(html);               
};
