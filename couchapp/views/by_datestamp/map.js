function(doc) {
  if (doc.title) {
    emit([doc.datestamp.substring(0,10),doc.provider], null);
  }
};
