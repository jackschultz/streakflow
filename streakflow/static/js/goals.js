$(document).ready(function() {
});

$(document).on('click', ".goal-objective", function(event) {

    var data = {};
    $(this).find('input').each(function() {
      data[$(this).attr('name')] = $(this).attr('value');
    });
    data['oid'] = $(this).attr('oid');
    var oid = data['oid'];
    data['gid'] = $(this).attr('gid');
    var gid = data['gid'];
    data['tfid'] = $(this).attr('tfid');
    var tfid = data['tfid'];
    var url = "/goals/" + gid + "/timeframe/" + tfid + "/objectives/" + oid;
    var obj = $(this);
    $.ajax({
      url:url,
      type:"post",
      data: data,
      dataType: "json",
      success: function(response) {
        console.log(response);
        obj.find(".goal-obj-info").text(response["completed"]);
      },
    });


});




