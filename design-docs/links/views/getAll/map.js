function(doc) {
    if (doc.type === 'link') {
        emit(doc.url, {
            title: doc.title,
            description: doc.description,
            url: doc.url,
            domain: doc.domain,
            tags: doc.tags
        });
    }
}