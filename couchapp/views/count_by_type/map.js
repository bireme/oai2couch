function(doc) {
  if (doc.type) {
    emit(doc.type[0], 1);
  }
};
