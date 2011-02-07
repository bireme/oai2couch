function(doc) {
  if (doc.provider) {
    emit(doc.provider, 1);
  }
};
