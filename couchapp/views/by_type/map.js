function(doc) {
  if (doc.title) {
    emit(doc.type[0], null);
  }
};
