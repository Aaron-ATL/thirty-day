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
          appear($(".quiz-close"));
          vanish($(".btn-radio")); // Hide the answer options
          vanish($(".quiz-submit")); // Hide the submit button if necessary
          appear($(".quiz-reset")); // Hide the submit button if necessary
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
        vanish($(".quiz-submit"));
         if (data.answered_correctly) {
           $(".feedback").removeClass("text-success").html('You got it right! <i class="bx bxs-star" style="vertical-align: -1px; color: #ffba08;"></i>');
           activeAnswer.addClass("bg-faded-success border-success");
           var stars = $('.question-index').data("stars") + 1;
           $('.question-index').data("stars", stars);
           $('.question-index').text(stars);
         } else {
           activeAnswer.addClass("bg-faded-danger border-danger");
           $('.feedback').text("That's not right.").addClass("text-danger");
         }
          $(".quiz-submit").data("quiz-index", data.index);
          setTimeout(function () {
            $('.btn-radio').removeClass('active');
            appear($('.quiz-submit'));
            $(".feedback").text("");
            if ("question_data" in data) {
              updateAudioPlayer(data);
              $(".btn-radio").removeClass("bg-faded-success bg-faded-danger border-success border-danger");
              $(".feedback").removeClass("text-danger text-success");
              $(".quiz-submit").addClass("disabled");
              $('.card').removeClass('bg-primary bg-faded-primary border-primary');
              $(".question").text(data.question_data.text);
              $(".answer-1").text(data.question_data.answer_1);
              $(".answer-2").text(data.question_data.answer_2);
              $(".answer-3").text(data.question_data.answer_3);
            } else {
              vanish($(".btn-radio"));
              vanish($(".audio-player"));
              appear($(".quiz-close"));
              vanish($(".quiz-submit")); // Hide the submit button if necessary
              if (data.all_correct) {
                appear($(".quiz-reset")); // Hide the submit button if necessary
                $(".question").text("Congrats! You finished the quiz and got everything right! You can now move on to the next lesson or reset the quiz to do it again.");
              } else {
                appear($(".quiz-again")); // Hide the submit button if necessary
                $(".question").text("You finished this quiz attempt. You can now move on to the next lesson or go over what you got wrong to earn more stars.");
              }
            }
          }, 1500);
     });
   });
  
  $('.btn-radio').click(function() {
    $(".btn-radio").removeClass("bg-faded-success bg-faded-danger border-success border-danger");
    $('.card').removeClass('bg-primary bg-faded-primary border-primary');
    appear($('.btn-radio'));
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
    appear($(".quiz-submit"));
    vanish($(".quiz-reset"));
    vanish($(".quiz-again")); // Hide the submit button if necessary
    vanish($(".quiz-close"));
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
    updateAudioPlayer(data);
  }
  
  function updateAudioPlayer(data) {
    if (data.question_data.audio_file) {
      appear($(".audio-player"));
      $(".audio-player").css("--seek-before-width", "0%");
      $(".ap-current-time").text("0:00");
      $(".ap-seek-slider").val(0);
      var staticPrefix = $("audio").data("path");
      var audios = $("audio")
      audios.attr("src", staticPrefix + data.question_data.audio_file)
      audios.each((i, a) => {
        a.pause()    
        a.currentTime = 0
      });
    } else {
      vanish($(".audio-player"));
    }
  }
  
  function vanish(e) {
    e.addClass("d-none");
  }
  
  function appear(e) {
    e.removeClass("d-none");
  }

});