var curr;
var hovered;

var KANJI_WIDTH = 100;
var KANJI_HEIGHT = 100;

function get_svg(v, link) {
    if (link) {
        return '<a class="kanji" href="javascript:update(' + v + ', true)" id="' + v + '"><object data="{{ site.baseurl }}/svg/' + v + '.svg" width="' + KANJI_WIDTH + '" height="' + KANJI_HEIGHT + '" type="image/svg+xml" /></a> ';
    } else {
        return '<object data="{{ site.baseurl }}/svg/' + v + '.svg" width="' + KANJI_WIDTH + '" height="' + KANJI_HEIGHT + '" type="image/svg+xml" />';
    }
}

function update_dict(v) {
    doGet("{{ site.baseurl }}/dict/" + v + ".json",
        function(data) {
            var text = "";
            if (data['character']) {
                text += "unicode: " + data['character'] + "<br />";
            }
            if (data['meanings']) {
                text += "meaning: " + data['meanings'].toLowerCase() + "<br />";
            }
            if (data['readings'] && (data['readings']['on'] || data['readings']['kun'])) {
                text += "reading: ";
                if (data['readings']['on']) {
                    text += data['readings']['on'] + " (on) "
                }
                if (data['readings']['kun']) {
                    text += data['readings']['kun'] + " (kun) ";
                }
            }
            if (v == hovered) {
                document.getElementById('dict').innerHTML = text;
            }
        },
        function() {
            if (v == hovered) {
                document.getElementById('dict').text = "";
            }
        });
}

function update_curr(v) {
    document.getElementById("curr").innerHTML = get_svg(v, false);
}

function update(next, clear_help) {
    curr = next;

    update_curr(curr);
    update_dict(curr);

    var next_refs = elements[next.toString()];
    var refs_0_el = document.getElementById("refs_0");
    refs_0_el.innerHTML = "";
    for (var i = 0; i < next_refs[0].length; i++) {
        refs_0_el.innerHTML += get_svg(next_refs[0][i], true);
    }
    var refs_1_el = document.getElementById("refs_1");
    refs_1_el.innerHTML = "";
    for (var i = 0; i < next_refs[1].length; i++) {
        refs_1_el.innerHTML += get_svg(next_refs[1][i], true);
    }

    if (clear_help) {
        document.getElementById("help").text = "";
    }

    window.location.hash = "#" + curr;

    for (const a of document.querySelectorAll("a.kanji")) {
        a.addEventListener('mouseover', function() { hovered = this.id; update_curr(hovered); update_dict(hovered); });
        a.addEventListener('mouseout', function() { hovered = curr; update_curr(hovered); update_dict(hovered); });
    }
}

function get_random_element() {
    var max = 0;
    for (k in elements) {
        if (parseInt(k) > max) {
            max = k;
        }
    }

    var r;
    do {
            r = (Math.floor(Math.random() * max) + 1).toString();
    } while (!elements.hasOwnProperty(r));

    return r;
}

function update_from_hash() {
    if (window.location.hash == "") {
        update(get_random_element(), false);
    } else {
        update(window.location.hash.substring(1), false);
    }
}

