$(document).on('click', ".demo-goal-objective", function(event) {
    var obj = $(this);
    if ($(this).attr('completed') == "true") {
      var asdf = check_all_complete(obj.parents(".goal-overview"));
      obj.find(".goal-obj-img").attr("src","/static/img/square75x75.png");
      obj.attr("completed","false");
      var num_completed = obj.parents(".goal-overview").find(".goal-consecutive").text();
      if (check_all_complete(obj.parents(".goal-overview")) != asdf) {
        obj.parents(".goal-overview").find(".goal-consecutive").text(parseInt(num_completed)-1);
        obj.parents(".goal-overview").find(".complete-label").removeClass("label-success").addClass("label-important").text("INCOMPLETE");
      }
    }
    else {
      obj.find(".goal-obj-img").attr("src","/static/img/square75x75c.png");
      obj.attr("completed","true");
      var num_completed = obj.parents(".goal-overview").find(".goal-consecutive").text();
      console.log(check_all_complete(obj.parents(".goal-overview")));
      if (check_all_complete(obj.parents(".goal-overview")) == "true") {
        obj.parents(".goal-overview").find(".goal-consecutive").text(parseInt(num_completed)+1);
        obj.parents(".goal-overview").find(".complete-label").removeClass("label-important").addClass("label-success").text("COMPLETE");
      }
    }

});

function check_all_complete(obj) {
  var retval = "true"
  obj.find(".demo-goal-objective").each(function() {
    if ($(this).attr("completed") == "false") {
      retval = "false";
      return false;
    }
  });
  return retval;
}



$(document).on('click', "#advance-time", function(event) {
  var exp1 = "THIS FRAME EXPIRES: ";
  var exp2 = " days, 5 hours from now";
  var exp3 = "5 hours from now";

  var week_exp = parseInt($(".week-time").attr("exp"));
  var month_exp = parseInt($(".month-time").attr("exp"));

  var new_week_exp = (week_exp + 6) % 7;
  var new_month_exp = (month_exp + 30) % 31;

  //need to check if we reset the tihngs
  $(".goal-overview").each(function() {
      var expires = parseInt($(this).siblings().find(".exp-time").attr("exp"));
      if (expires == 0) {
        if (check_all_complete($(this)) == "false") {
          //set consecutive to 0
          $(this).find(".goal-consecutive").text("0");
        }
        $(this).find(".demo-goal-objective").attr("completed","false");
        $(this).find(".goal-obj-img").attr("src","/static/img/square75x75.png");
        $(this).find(".complete-label").removeClass("label-success").addClass("label-important").text("INCOMPLETE");
      }
  });

  if (new_week_exp == 0) {
    $(".week-time").text(exp1 + exp3);
  }
  else {
    $(".week-time").text(exp1 + new_week_exp.toString() + exp2);
  }
  $(".week-time").attr("exp",new_week_exp.toString());

  if (new_month_exp == 0) {
    $(".month-time").text(exp1 + exp3);
  }
  else {
    $(".month-time").text(exp1 + new_month_exp.toString() + exp2);
  }
  $(".month-time").attr("exp",new_month_exp.toString());

});

