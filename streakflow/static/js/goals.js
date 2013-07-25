$(document).ready(function() {
});

$(document).on('click', ".goal-objective", function(event) {

    var data = {};
    $(this).find('input').each(function() {
      data[$(this).attr('name')] = $(this).attr('value');
    });
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
    $.ajax({
      url:url,
      type:"post",
      data: data,
      dataType: "json",
      success: function(response) {
        obj.find(".goal-obj-info").text(response["completed"]);
        obj.attr("completed",response["completed"]);
        $("#goal-consecutive").text(response.consecutive);
      },
    });


});


