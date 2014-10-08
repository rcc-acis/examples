/*
javascript metadata example
Created by Natalie Umphlett

This example shows how to generate a 
metadata table for each station
within a bounding box. 
The resulting table list the station name
and the start/end dates
inbetween which the station recorded precipitation data.

jsfiddle link
http://jsfiddle.net/wsr57yL0/1/
*/

/*global $, window, XDomainRequest */

/*
html code

<div id="jresults"></div>
<table id="JSONACIS" border="1"></table>
*/

/*
css

#jresults {
    font: 12px monospace;
}
*/

//web services success callback
function postSuccess(results) {
    //This will store the html string that will be inserted into 
    //the table id JSONACIS
    var tableString = '<tr><th>Name</th><th>Station Start</th><th>Station End</th></tr>';

    //Loop through the results and for each station
    for (var key in results.meta) {
        //add a new row.
        tableString = tableString + '<tr><td>' + results.meta[key].name + '</td><td>' + results.meta[key].valid_daterange[0][0] + '</td><td>' + results.meta[key].valid_daterange[0][1] + '</td></tr>';
    }

    //This call will inject the html string back into the page 
    //so that it can be seen.
    $('#JSONACIS ').html(tableString);
}

//web services failure callback
function postError(xhr, textStatus, error) {
    $("#jresults").empty().html("<p>Web services call failed: " + error + "</p>");
}

//submit web services request
function postResults(url, params) {
    var xdr, args, results,
    params_string = JSON.stringify(params);
    if (window.XDomainRequest) {
        xdr = new XDomainRequest();
        xdr.open("GET", url + "?params=" + params_string);
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
        args = {
            params: params_string
        };
        $.ajax(url, {
            type: 'POST',
            data: args,
            crossDamain: true,
            success: postSuccess,
            error: postError
        });
    }
}

var url = "http://data.rcc-acis.org/StnMeta",
    params = {
        bbox: "-108,42.5,-110,44",
        meta: "name,sids,ll,valid_daterange",
        elems: "pcpn"
    };
postResults(url, params);
