function getCost(programs,sponsorship_duration,sponsorship_level) {
    //var xhttp = new XMLHttpRequest();
    //xhttp.onreadystatechange = function() {
    //    if (xhttp.readyState == 4 && xhttp.status == 200) {
    //        //document.getElementById("demo").innerHTML = xhttp.responseText;
    //        console.log(xhttp.responseText)
    //        response = xhttp.responseText;
    //        gauge1.update(response);
    //    }
    //};
    //xhttp.open("POST", "/sponsorship/calculate_cost", false);
    var data = {
        "programs":programs,
        "sponsorship_duration":sponsorship_duration,
        "sponsorship_level":sponsorship_level
    };
    //xhttp.send(data);


    $.ajax({
        "type":"POST",
        "url":"/sponsorship/calculate_cost",
        "cache":false,
        "contentType": "application/json;charset=utf-8",
        "data":JSON.stringify(data),
        "dataType":"json",
        "success":function(sponsor_dict){
            gauge1.update(sponsor_dict['org_sponsor_pcnt'])
            //console.log(results)
        }
    });
}
//
//function getOrgSponsorship(num_programs,sponsorship_duration,sponsorship_level) {
//    var xhttp = new XMLHttpRequest();
//    xhttp.onreadystatechange = function() {
//        if (xhttp.readyState == 4 && xhttp.status == 200) {
//            response = xhttp.responseText;
//            return response;
//        }
//    };
//    xhttp.open("GET", "/sponsorship/calculate_cost", true);
//    var data = {
//        "num_programs":num_programs,
//        "sponsorship_duration":sponsorship_duration,
//        "sponsorship_level":sponsorship_level
//    }
//    xhttp.send(data);
//}