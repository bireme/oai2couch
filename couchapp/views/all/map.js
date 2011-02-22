function(doc) {
  if (doc.title) {
    emit(doc.id, null);
  }
};
