function postSuccess(results) {
    console.log(results);
    alert("postResults success; results in console log");
}
function postError() {
    alert("postResults error");
}
function postResults(url, params) {
    var xdr, args, results,
        params_string = JSON.stringify(params);
    if (window.XDomainRequest) {
        xdr = new XDomainRequest();
        xdr.open("GET", url + "?params=" +    params_string);
        xdr.onload = function () {
            results = $.parseJSON(xdr.responseText);
            postSuccess(results);
        };
        xdr.onerror = postError;
        xdr.onprogress = $.noop();
        xdr.ontimeout = $.noop();
        setTimeout(function () {
            xdr.send();
        }, 0);
    } else {
        args = {params: params_string};
        $.ajax(url, {
            type: 'POST',
            data: args,
            crossDamain: true,
            success: postSuccess,
            error: postError
        });
    }
}
var url = "http://data.rcc-acis.org/StnData",
    params = {sid:"KNYC", date:"2012-07-04", elems:"maxt,mint,pcpn"};
postResults(url, params);