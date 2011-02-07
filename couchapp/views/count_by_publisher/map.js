function(doc) {
  if (doc.publisher) {
    emit(doc.publisher[0], 1);
  }
};
