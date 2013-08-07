$(document).ready(function() {


});

function getGoalInfo() {
  var url = "http://streakflow.com";///accounts/login/";
  data = {};
  data['csrfmiddlewaretoken'] = $.cookie('csrftoken');
  data['username'] = 'jackschultz';
  data['password'] = 'asdf';
  headers = {};
  headers['X-CSRFToken'] = $.cookie('csrftoken');
  $.ajax({
    url: url,
    //type: "post",
    type: "get",
    //headers: headers,
    //dataType: 'jsonp',
    contentType: "application/json",
    //data: data,
    data: {csrfmiddlewaretoken:$.cookie('csrftoken'), username:'jackschultz',password:'asdf'},
    success: function(data) {
     // console.log(data);
    },
    error: function(data) {
     // console.log(data);
    }
  });

}


function populateData(data) {
  tmpl = $("#shit_tmpl").html();
  output = Mustache.to_html(tmpl, data);
  $("#shit").append(output);
};

$(function() {
//  populateData(data);
//getGoalInfo();
});


$(document).on('click', ".goal-objective", function(event) {

    var data = {};
    if ($(this).attr('completed') == "true") {
      data['completed'] = "0";
    }
    else {
      data['completed'] = "1";
    }
    data['oid'] = $(this).attr('oid');
    var oid = data['oid'];
    data['gid'] = $(this).attr('gid');
    var gid = data['gid'];
    var url = "/api/goals/" + gid + "/update/" + oid;
    var obj = $(this);
    data['csrfmiddlewaretoken'] = $.cookie('csrftoken');
    $.ajax({
      url:url,
      type:"post",
      data: data,
      dataType: "json",
      success: function(response) {
        obj.attr("completed",response.completed);
        obj.parents(".goal-overview").find(".goal-consecutive").text(response.consecutive);
        if (response.all_complete) {
          obj.parents(".goal-overview").find(".complete-label").removeClass("label-important").addClass("label-success").text("COMPLETE");
        }
        else {
          obj.parents(".goal-overview").find(".complete-label").removeClass("label-success").addClass("label-important").text("INCOMPLETE");
        }
        if (response.completed) {
          obj.find(".goal-obj-img").attr("src","/static/img/square75x75c.png");
        }
        else {
          obj.find(".goal-obj-img").attr("src","/static/img/square75x75.png");
        }
      },
    });


});


