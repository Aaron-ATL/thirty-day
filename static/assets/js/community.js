$(document).ready(function() {
  $('#forum-submit').click(function(e) {
    var js_data = {"email": $("#forum-email").val()};
    e.preventDefault();
    $.ajax({
         type : 'POST',
         url : 'https://hooks.zapier.com/hooks/catch/19125887/2oh2jon/',  
         data: JSON.stringify({"data": js_data}),
         success: function (data) {
             if (data['status'] == 'success') {
               $.ajax({
                 url: $("#make_member_url").text(),
                 method: 'GET',
                 success: function (data) {
                   $("#forum-form").addClass("d-none");
                   $("#invite-sent").removeClass("d-none");
                 },
               });
             }
         },
     });
  });
});