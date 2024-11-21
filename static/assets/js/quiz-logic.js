$(document).ready(function() {
  
  $('.btn-radio').click(function() {
    resetQuiz();
    $('.quiz-submit[data-ln="'+ $(this).data("ln") +'"]').removeClass('disabled');
    $(this).addClass('active');
    $(this).addClass('border-primary bg-faded-primary');
  });

  $('.quiz-submit').click(function() {
    var activeAnswer = $('.card-hover.active[data-ln="'+ $(this).data("ln") +'"]');
    if (activeAnswer.data("yhw") == "27") {
      activeAnswer.addClass("bg-faded-success border-success");
      $('.feedback[data-ln="'+ $(this).data("ln") +'"]').text("You nailed it!").addClass("text-success");
    } else {
      activeAnswer.addClass("bg-faded-danger border-danger");
      var correctAnswer = $('.card-hover[data-ln="'+ $(this).data("ln") +'"][data-yhw="27"]');
      correctAnswer.addClass("bg-faded-success border-success");
      $('.feedback[data-ln="'+ $(this).data("ln") +'"]').text("Not quite right. Listen to the correct answer highlighted in green:").addClass("text-danger");
    }

    $(this).addClass('d-none');
    $('.quiz-close[data-ln="'+ $(this).data("ln") +'"]').text("Back to overview");
  });
  $(document).on('hidden.bs.modal', function (e) {
        resetQuiz();
        $(".quiz-submit").addClass("disabled");
        $(".quiz-submit").removeClass("d-none");
        $(".btn-radio").removeClass("bg-faded-success bg-faded-danger border-success border-danger");
        $(".feedback").removeClass("text-danger text-success");
        $(".feedback").text("Listen to the examples and choose the correct answer:");
    });
  function resetQuiz() {
    $('.btn-radio').removeClass('active');
    $('.card').removeClass('bg-primary bg-faded-primary border-primary');
  }
});