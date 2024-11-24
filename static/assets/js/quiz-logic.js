$(document).ready(function() {

  $('.start-quiz').click(function(e) {
    e.preventDefault();
    $.ajax({
        url: $(this).data("url"),
        method: 'GET',
        data: {
            "lesson_pk": $(this).data("lpk"),
        },
        dataType: 'json'
    }).done(function(data) {
      resetQuizUI();
      if ("question_data" in data) {
          loadQuiz(data);
      } else {
          $(".quiz-length").text(data.stars_earned_on_this_lesson);
          $(".question-index").text(data.stars_earned_on_this_lesson);
          $(".question").text("Congrats! You finished the quiz and got everything right! You can now move on to the next lesson or reset the quiz to do it again.");
          $(".quiz-close").removeClass("d-none");
          $(".btn-radio").addClass("d-none"); // Hide the answer options
          $(".quiz-submit").addClass("d-none"); // Hide the submit button if necessary
          $(".quiz-reset").removeClass("d-none"); // Hide the submit button if necessary
      }
    });
  });

  $('.quiz-again').click(function() {
    $.ajax({
        url: $(this).data("url"),
        method: 'GET',
        data: {
            "lesson_pk": $(this).data("lpk"),
        },
        dataType: 'json'
    }).done(function(data) {
      resetQuizUI();
      loadQuiz(data);
    });
  });

  $('.quiz-reset').click(function() {
     $.ajax({
        url: $(this).data("url"),
        method: 'GET',
        data: {
            "lesson_pk": $(this).data("lpk")
        },
        dataType: 'json'
     }).done(function(data) {
       resetQuizUI();
       loadQuiz(data);
     });
   });

  $('.quiz-submit').click(function() {
     var activeAnswer = $('.card-hover.active');
     $.ajax({
         url: $(this).data("url"),
         method: 'GET',
         data: {
             "index": $(this).data("quiz-index"),
             "active_answer_id": activeAnswer.data("answer-id"),
             "lesson_pk": $(this).data("lpk")
         },
         dataType: 'json'
     }).done(function(data) {
        $(".quiz-submit").addClass("d-none");
         if (data.answered_correctly) {
           $('.feedback').text("You got it right!").addClass("text-success");
           activeAnswer.addClass("bg-faded-success border-success");
           var stars = $('.question-index').data("stars") + 1;
           $('.question-index').data("stars", stars);
           $('.question-index').text(stars);
         } else {
           activeAnswer.addClass("bg-faded-danger border-danger");
           $('.feedback').text("Not quite right.").addClass("text-danger");
         }
          $(".quiz-submit").data("quiz-index", data.index);
          setTimeout(function () {
            $('.btn-radio').removeClass('active');
            $('.quiz-submit').removeClass('d-none');
            $(".feedback").text("");
            if ("question_data" in data) {
              $(".btn-radio").removeClass("bg-faded-success bg-faded-danger border-success border-danger");
              $(".feedback").removeClass("text-danger text-success");
              $(".quiz-submit").addClass("disabled");
              $('.card').removeClass('bg-primary bg-faded-primary border-primary');
              $(".question").text(data.question_data.text);
              $(".answer-1").text(data.question_data.answer_1);
              $(".answer-2").text(data.question_data.answer_2);
              $(".answer-3").text(data.question_data.answer_3);
            } else {
              $(".btn-radio").addClass("d-none");
              $(".quiz-close").removeClass("d-none");
              $(".quiz-submit").addClass("d-none"); // Hide the submit button if necessary
              if (data.all_correct) {
                $(".quiz-reset").removeClass("d-none"); // Hide the submit button if necessary
                $(".question").text("Congrats! You finished the quiz and got everything right! You can now move on to the next lesson or reset the quiz to do it again.");
              } else {
                $(".quiz-again").removeClass("d-none"); // Hide the submit button if necessary
                $(".question").text("You finished this quiz attempt. You can now move on to the next lesson or go over what you got wrong to earn more stars.");
              }
            }
          }, 1500);
     });
   });
  
  $('.btn-radio').click(function() {
    $(".btn-radio").removeClass("bg-faded-success bg-faded-danger border-success border-danger");
    $('.card').removeClass('bg-primary bg-faded-primary border-primary');
    $('.btn-radio').removeClass('active');
    $('.quiz-submit').removeClass('disabled');
    $(this).addClass('active');
    $(this).addClass('border-primary bg-faded-primary');
  });

  function resetQuizUI() {
    $(".btn-radio").removeClass("bg-faded-success bg-faded-danger border-success border-danger");
    $('.btn-radio').removeClass('active d-none');
    $('.card').removeClass('bg-primary bg-faded-primary border-primary');
    $(".feedback").removeClass("text-danger text-success");
    $(".feedback").text("");
    $(".quiz-submit").addClass("disabled");
    $(".quiz-submit").removeClass("d-none");
    $(".quiz-reset").addClass("d-none");
    $(".quiz-again").addClass("d-none"); // Hide the submit button if necessary
    $(".quiz-close").addClass("d-none");
  }
  
  function loadQuiz(data) {
    $(".question").text(data.question_data.text);
    $(".answer-1").text(data.question_data.answer_1);
    $(".answer-2").text(data.question_data.answer_2);
    $(".answer-3").text(data.question_data.answer_3);
    $(".quiz-length").text(data.total_stars_available);
    $(".quiz-submit").data("quiz-index", 0);
    $(".question-index").text(data.stars_earned_on_this_lesson);
    $(".question-index").data("stars", data.stars_earned_on_this_lesson);
  }
});