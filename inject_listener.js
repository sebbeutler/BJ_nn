// __SESSION_ID__ = localStorage["evo.video.flv.bwSessionId"]
// https://babylonstk.evo-games.com/frontend/evo/r2/#table_id=___TABLE_ID___&category=blackjack&game=blackjack&EVOSESSIONID=__SESSION_ID__
// #game-container

pulse = function(arg) {
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", "http://localhost:2121", true);
    xmlHttp.send(JSON.stringify(arg[0]));
}

console.stdlog = console.log.bind(console);
console.logs = [];
console.log = function(){
    console.logs.push(Array.from(arguments));
    console.stdlog.apply(console, arguments);
    pulse(Array.from(arguments));
}

var intervalId = window.setInterval(function(){
  document.querySelector("#root > div > div > div > div.wrapper--2LGax > div.clickable--3IFrf").click();
}, 5000);