function(doc) {
  if (doc.title) {
    emit(null, doc);
  }
};
