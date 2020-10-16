var url = $feature.url;
var lowerCaseTitleWords = ['a', 'an', 'of', 'and', 'on', 'the', 'in', 'for', 'from', 'to'];

function addWord(currentTitle, word) {
    var splitWordParts = split(word, '.');
    if (currentTitle != "" && indexof(lowerCaseTitleWords, lower(splitWordParts[0])) > -1) {
        currentTitle += lower(splitWordParts[0]) + ' ';
    } else if (IsNan(Number(splitWordParts[0])) || (Number(splitWordParts[0])) < 10000) {
        currentTitle += Proper(splitWordParts[0]) + ' ';
    }
    return currentTitle;
}

var title = "";
var list = Split(url, '/', -1, true);

for (var i = count(list) - 1; i >= 0; i--) {
    var urlTitle = replace(list[i], "_", "-");
    var title2 = Split(urlTitle, '-');

    if (count(title2) > 1) {
        for (var j = 0; j < count(title2); j++) {
            console(title2[j]);
            title = addWord(title, title2[j]);
        }
        return title;
    }
}