var request = require("request");
var moment = require("moment");

var sunbaseURL = "http://api.sunrise-sunset.org/json?";
var moonbaseURL = "http://api.usno.navy.mil/moon/phase?date=";
var weatherbaseURL = "api.openweathermap.org/data/2.5/weather?";
var weatherAPI = "5d4c2904312725cfbaa3afa9583f0211";

var lat = 43.048122;
var lon = -76.147424;

var alexa = require('alexa-app');
var app = new alexa.app('astronomer');

app.launch(function(request, response){
  response.say("Welcome to Astronomer! I can tell you when sunrise and sunset are, the current phase of the moon, or conditions for stargazing.");
});

app.intent('GetSunrise',
  function(alexaRequest, alexaResponse){
    var url = sunbaseURL + "lat=" + lat + "&lng=" + lon;
    var date = alexaRequest.slot('Date');
    if(date != ""){
        url = url + "&date=" + date;
    }

    request({
      url: url,
      json: true
    }, function(error, response, body) {
        if(!error && response.statusCode === 200){
          alexaResponse.say("Sunrise for that day in Syracuse will be at " + moment(body.results.sunrise, "HH:mm:ss A").subtract(4, "hours").format('LTS'));
          alexaResponse.send();
        }
    });
    return false;
});

app.intent('GetSunset',
  function(alexaRequest, alexaResponse){
    var url = sunbaseURL + "lat=" + lat + "&lng=" + lon;
    var date = alexaRequest.slot('Date');
    if(date != ""){
        url = url + "&date=" + date;
    }
    request({
      url: url,
      json: true
    }, function(error, response, body) {
        if(!error && response.statusCode === 200){
          alexaResponse.say("Sunset for that day in Syracuse will be at " + moment(body.results.sunset, "HH:mm:ss A").subtract(4, "hours").format('LTS'));
          alexaResponse.send();
        }
    });
    return false;
});

app.intent('GetMoonPhase',
  function(alexaRequest, alexaResponse){
    var url = moonbaseURL + moment().format("MM/DD/YYYY") + "&nump=1";
    request({
      url: url,
      json: true
    }, function(error, response, body) {
        if(!error && response.statusCode === 200){
          alexaResponse.say("The moon is currently in the phase " + body.phasedata[0].phase);
          alexaResponse.send();
        }
    });
    return false;
});

app.intent('GetGoodGazingNight',
  function(alexaRequest, alexaResponse){
    var url = weatherbaseURL + "lat=" + lat + "&lon=" + lon + "&APPID=" + weatherAPI;
    request({
      url: url,
      json: true
    }, function(error, response, body) {
        if(!error && response.statusCode === 200){
          if(body.clouds.all  < 30){
            alexaResponse.say("Weather seems okay for stargazing right now.");
          } else{
            alexaResponse.say("Weather might not be so good for stargazing right now.");
          }
          alexaResponse.send();
        }

    });
    return false;
});

app.intent('AMAZON.HelpIntent',
  function(alexaRequest, alexaResponse){
    alexaResponse.say("I can tell you when sunrise and sunset are, the current phase of the moon, or conditions for stargazing.");
});

app.intent('AMAZON.StopIntent',
  function(alexaRequest, alexaResponse){
      alexaResponse.say("Goodybe, and happpy stargazing.");
  });

app.error = function(exception, request, response) {
    response.say("Lol get rekt noob.");
};

exports.handler = app.lambda();
module.exports = app;
