$(document).ready(function(){
    $(".botSuggestion").hide();
    //https://stackoverflow.com/questions/4220126/run-javascript-function-when-user-finishes-typing-instead-of-on-key-up
    var typingTimer;
    var timeoutMS = 250;
    //on keyup, start the countdown
    $("#guess").on('keyup', function () {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(doneTyping, timeoutMS);
    });

    //on keydown, clear the countdown
   $("#guess").on('keydown', function () {
      clearTimeout(typingTimer);
    });

    //user is "finished typing," do something
   function doneTyping () {
        $.ajax({
            type:"GET",
            url:"getByName",
            data: {"name": $("#guess").val()},
            success: function (response){
                $(".botSuggestion").hide();
                let i = 0
                for (i; i<response["robots"].length; i++) {
                    $("#suggestion"+(i+1)).show();
                    $("#suggestion"+(i+1)+"Name").text(response["robots"][i]["name"]);
                    $("#suggestion"+(i+1)+"ID").text(response["robots"][i]["id"]);
                    $("#suggestion"+(i+1)+"Img").attr("src",response["robots"][i]["image"]);
                };
                $("#descriptionSpacer").css("height",50+(3-i)*(200-16)+"px");
            }
        })
    }

    var guessNumber = 1;
    var guessUnlocked = true;
    var guessed = [];

    function showColour (field,response,callback){
        $("#"+field+guessNumber).transition({"rotateY":90},250,"linear", function(){
            if (response[field] == "match") $("#"+field+guessNumber).css("background","green");
            else {
                if (response[field] == "close") $("#"+field+guessNumber).css("background","yellow");
                else $("#"+field+guessNumber).css("background","red");
            }
        }).transition({"rotateY":180},250,"linear",function(){
            callback();
        });
    };

   $(".botSuggestion").click(function(){
        let suggestionNum = $(this).attr("id")[$(this).attr("id").length-1]
        let botID = $("#suggestion"+suggestionNum+"ID").text();
        if (guessUnlocked && !guessed.includes(botID)){
        guessUnlocked = false;
        $.ajax({
            type:"GET",
            url:"match",
            data: {"id": botID},
            success: function (response){
                guessed.push(botID)
                $("#guessFeedback"+guessNumber).text($("#suggestion"+suggestionNum+"Name").text());
                now = new Date();
                now.setDate(now.getDay() + 1);
                now.setHours(0,0,0);
                document.cookie = "expires=" + now.toUTCString();
                document.cookie = "guessed=" + guessed;
                console.log("cookie: "+document.cookie);

                showColour("letter",response, function(){
                 showColour("debut",response, function(){
                  showColour("weapon",response,function(){
                   showColour("finish",response,function(){
                    showColour("colour",response, function (){
                     showColour("country",response, function (){
                      guessNumber++;
                      guessUnlocked = true;
                     })
                    })
                   })
                  })
                 })
                })
            }
        });
        }
   });
})