function buildXhr(successCB, errorCB) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            successCB(JSON.parse(xhr.responseText));
        } else {
            errorCB();
        }
    }
    return xhr;
}

function doGet(url, successCB, errorCB) {
    var xhr = buildXhr(successCB, errorCB);
    xhr.open('GET', url);
    xhr.send();
}
