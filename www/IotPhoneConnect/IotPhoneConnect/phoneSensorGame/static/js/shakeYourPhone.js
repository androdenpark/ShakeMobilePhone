(function(window){
var userID =  document.getElementById("theID").innerHTML;
var theHighestScore=0;

document.getElementById("bestScore").innerHTML= theHighestScore.toString();

var playingFlag=false;
var beatTimer=0;
var heartBeatInterval=2000;
//[Speed, Score,MaxValue,MinValue]
var xList=[0,0], yList=[0,0], zList=[0,0];
var lastTime=0;

var xdataArray=new Array();
var ydataArray=new Array();
var zdataArray=new Array();



document.getElementById("startBut").onclick=startPlay;
document.getElementById("stopBut").onclick=stopPlay;
document.getElementById("historyBut").onclick=getHistoryScores;
document.getElementById("learnMoreImg").onclick=learnMore;


function osCheck(){
	osPlatform = navigator.platform;
	if(osPlatform.indexOf("Win") == 0 || osPlatform.indexOf("Mac") == 0){
		window.location = "../sorry";
	}
}


var historyChart=new JSChart("graphID","bar");
//alert(document.body.clientWidth.toString());
function intialHistoryGraph(){
	var colors=['#AF0202', '#EC7A00', '#FCD200', '#81C714', '#DE42C5'];
	historyChart.setDataArray(new Array(["NAN",10],["NAN",20],["NAN",30],["NAN",10],["NAN",50]));
	historyChart.colorizeBars(colors);
	historyChart.setTitleColor('#8E8E8E');
	historyChart.setAxisNameX('');
	historyChart.setAxisNameY('');
	historyChart.setAxisColor('#C4C4C4');
	//historyChart.setAxisNameFontSize(16);
	historyChart.setAxisNameColor('#999');
	historyChart.setTitle("");
	historyChart.setAxisValuesColor('#7E7E7E');
	historyChart.setBarValuesColor('#7E7E7E');
	historyChart.setAxisPaddingTop(15);
	historyChart.setAxisPaddingRight(0);
	historyChart.setAxisPaddingLeft(5);
	historyChart.setAxisPaddingBottom(15);
	//historyChart.setTextPaddingLeft(0);
	//historyChart.setTitleFontSize(11);
	historyChart.setBarBorderColor('#C4C4C4');
	//historyChart.setBarSpacingRatio(15);
	historyChart.setGrid(false);
	var displayWidth=document.body.clientWidth*0.985/1;
	historyChart.setSize(displayWidth,displayWidth*0.6/1 );
	//historyChart.setBackgroundImage('chart_bg.jpg');
	historyChart.draw();
}


function refreshHistoryGraph(historyData){
	var historyDict=JSON.parse(historyData);
	var historyData=historyDict["historyList"];
	if(historyData.length >=5){
		historyChart.setDataArray(historyData.slice(-5));
	}else{
		historyChart.setDataArray(historyData);
	}
	historyChart.draw();
}



window.onload=startHeartBeat;

function startHeartBeat(){
	osCheck();
	heartBeatInterval=3000;
	beatTimer=window.setInterval(heartBeat,heartBeatInterval);
	intialHistoryGraph();
}



function heartBeat(){

	//if(document.hidden){
	//stopPlay();
	//}

	if(!playingFlag ){
		return;
	}else{
		processCurrentData();
	}
	theHighestScore=maxValue>theHighestScore?maxValue:theHighestScore;
	document.getElementById("theScore").innerHTML= maxValue.toString();
	document.getElementById("bestScore").innerHTML= theHighestScore.toString();
}

function resetCollectionData(){

	xList[0]=0;
 	yList[0]=0;
 	zList[0]=0;

	xList[1]=0;
 	yList[1]=0;
 	zList[1]=0;
	
	xdataArray=new Array();
	ydataArray=new Array();
	zdataArray=new Array();
}

function processCurrentData(){

	var lastValue=xdataArray[0]-xList[0];
	var currentValue=xdataArray[0]-xList[0];
	//var debugInfo=""
	for( var index in xdataArray){
		currentValue=xdataArray[index]-xList[0];
		//debugInfo += currentValue.toFixed(3)+",";
		if(currentValue*lastValue < 0 && Math.abs(currentValue) >0.1 ){
		xList[1] +=1;
		lastValue=currentValue;
		}
		
	}
	//document.getElementById("xdebug").innerHTML=debugInfo;

	lastValue=ydataArray[0]-yList[0];
	currentValue=ydataArray[0]-yList[0];
	for( var index in ydataArray){
		currentValue=ydataArray[index]-yList[0];
		if(currentValue*lastValue < 0 && Math.abs(currentValue) >0.1 ){
		yList[1] +=1;
		lastValue=currentValue;
		}
		
	}

	lastValue=zdataArray[0]-zList[0];
	currentValue=zdataArray[0]-zList[0];
	for( var index in zdataArray){
		currentValue=zdataArray[index]-zList[0];
		if(currentValue*lastValue < 0 && Math.abs(currentValue) >0.1 ){
		zList[1] +=1;
		lastValue=currentValue;
		}
		
	}

	maxValue=(xList[1]+yList[1]+zList[1])*5;	
	resetCollectionData();
	
}




 function deviceMotionHandler(eventData) {

	var currentTime = new Date().getTime();
	var timeDelta = parseInt(currentTime-lastTime);

	if(xdataArray.length>50 ||  timeDelta<30){
	return;
	}
	
	lastTime = currentTime;

       	var acceleration =eventData.accelerationIncludingGravity;	
	
	var xData=acceleration.x ;
	var yData=acceleration.y ;
	var zData=acceleration.z +9.8;

	document.getElementById("xCurrentValue").innerHTML=xData.toFixed(2);
	document.getElementById("yCurrentValue").innerHTML=yData.toFixed(2);
	document.getElementById("zCurrentValue").innerHTML=zData.toFixed(2);
	
	if(playingFlag){
		xList[0]  = (xList[0]*xdataArray.length+xData)/(xdataArray.length+1);
		yList[0]  = (yList[0]*ydataArray.length+yData)/(ydataArray.length+1);
		zList[0]  = (zList[0]*zdataArray.length+zData)/(zdataArray.length+1);

		xdataArray.push(xData);
		ydataArray.push(yData);
		zdataArray.push(zData);
	}
	
}


function startPlay(){
	document.getElementById("startBut").disabled=true;
	document.getElementById("startBut").innerHTML="PLAYING";
	document.getElementById("stopBut").disabled=false;

	resetCollectionData();
    	if (window.DeviceMotionEvent) {
        	window.addEventListener('devicemotion',deviceMotionHandler, false);
		playingFlag=true;
		lastTime=new Date().getTime();  
    	}else{
		alert("your device doesn't support this game!");
    	}
}

function stopPlay(){
	document.getElementById("stopBut").disabled=true;
	document.getElementById("stopBut").innerHTML="PROCESSING...";
	document.getElementById("startBut").innerHTML="PLAY";
	document.getElementById("startBut").disabled=false;

	if(!playingFlag){
	return;
	}
	playingFlag=false;
	sendScore();
}

function sendScore(){
	var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange=function(){
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
				if(xmlhttp.responseText.indexOf('Error')<0){
						rankResult = xmlhttp.responseText.split("%");	
						document.getElementById("rankValue").innerHTML= rankResult[0]+" of "+rankResult[1];
						document.getElementById("stopBut").innerHTML="RANK";

						if (rankResult[0] ==1){
							document.getElementById("command").innerHTML="Well done, you are the first!";
							document.getElementById("theImg").src="/shakemobilegame/static/img/d.jpg";
						}
						else{
							document.getElementById("command").innerHTML="Come on, you can get a better score!";
							document.getElementById("theImg").src="/shakemobilegame/static/img/e.jpg";
						}		
				}else{
					alert("Lose connection with server, try to login again!");
					window.location = "../deviceRegister";
				}
			
		}
	}

	try{
		xmlhttp.open('POST', '../dataPost/', true);
		xmlhttp.withCredentials = true;
		var data2Send = new FormData();
		data2Send.append('postScore',"");
		data2Send.append('theID', userID)
		data2Send.append('scoreData',theHighestScore);
		xmlhttp.send(data2Send);
		theHighestScore = 0;
	}catch(exception){
		alert("Lose connection with server, try to login again!");
		window.location = "../deviceRegister";
	}	
}

function getHistoryScores(){
	document.getElementById("historyBut").innerHTML="Wait...";
	var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange=function(){
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
				if(xmlhttp.responseText.indexOf('Error')<0){
						refreshHistoryGraph(xmlhttp.responseText);
				}else{
						alert(xmlhttp.responseText);	
				}

		document.getElementById("historyBut").innerHTML="Get History Scores";
			
		}
	}

	try{
		xmlhttp.open('POST', '../dataPost/', true);
		xmlhttp.withCredentials = true;
		var data2Send = new FormData();
		data2Send.append('getScoreHistory',"");
		data2Send.append('userID', userID)
		xmlhttp.send(data2Send);
	}catch(exception){
		alert("Lose connection with server, try to login again!");
		window.location = "../deviceRegister";
	}
}



function learnMore(){
	var theURL="../demo/"+userID+"DEMO";
	window.open(theURL);

}

}(window));



