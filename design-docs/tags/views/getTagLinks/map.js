function(doc) {
    var permute = function(v, m) {
        for (var j, l = v.length, i = (1 << l) - 1, r = new Array(i); i;)
            for (r[--i] = [], j = l; j; i + 1 & 1 << --j && (r[i].push(m ? j : v[j])));
        return r;
    };
    var raw_tags = doc.tags
    var tags = {};
    for (var i in raw_tags) {
        var word = raw_tags[i].toLowerCase();
        if (word == "") continue;
        if (!tags[word]) {
            tags[word] = 1;
        } else {
            tags[word]++;
        }
    }
    var tag_set = [];
    for (var tag in tags) {
        tag_set.push(tag);
    }
    var permutations = permute(tag_set, 0);
    for (var i in permutations) {
        emit(permutations[i], {
            title: doc.title,
            description: doc.description,
            url: doc.url,
            domain: doc.domain,
            tags: doc.tags
        });
    }
}