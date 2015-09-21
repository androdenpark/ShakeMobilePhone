(function(window){



//document.getElementById("submitBut").onclick=formSubmit(event);
//document.getElementById("registerBut").onclick=registerUser();
$("#submitBut").click(formSubmit);
$("#registerBut").click(registerUser);

function osCheck(){
	osPlatform = navigator.platform;
	if(osPlatform.indexOf("Win") == 0 || osPlatform.indexOf("Mac") == 0){
		window.location = "../sorry";
	}
}



var userID = "";


function formSubmit(event){
	if(!formCheck()){
		stopDefault(event);
		stopBubble(event);	
		return false;
	}
	document.getElementById("submitBut").value = "Logining...";
	return true;	
}

function stopDefault(event){
	if(event && event.preventDefault){
	event.preventDefault();
	}else if(window.event && window.event.returnValue){
		window.eventReturnValue=false;
	
	}
	
}

function stopBubble(event){
	if(event && event.stopPropagation){
	event.stopPropagation();
	}else{
	window.event.cancelBubble=true;
	}
}


function formCheck(){
	try{
		if(document.getElementById("userID").value.length < 1){
			alert("your device does not have an id now, please register first!");
			return false;			
		}

		return true;
	}catch(exception){
		return false;
	}
}


function registerUser(){

	var userNameObj=document.getElementById("userName");
	if(userNameObj.value.length < 2 ){
		alert("Your input name is too short!");
		userNameObj.focus();
		return false;
	}

	document.getElementById("registerBut").disabled = true;
	document.getElementById("registerBut").innerHTML= "Processing...";
	var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.onreadystatechange=function(){
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
				if(xmlhttp.responseText.indexOf('Error')<0){		
					userID = xmlhttp.responseText;				
					document.getElementById("userID").value = userID;
					saveUserInfo();
					alert("Your device registered success, device ID: "+userID);
				}else{
					alert("Sorry, failed to get an ID, try again later!");
				}
		document.getElementById("registerBut").disabled = false;	
		document.getElementById("registerBut").innerHTML = "Get an ID";
		}

	}
	xmlhttp.open('POST', '../dataPost/', true);
	xmlhttp.withCredentials = true;
	var data2Send = new FormData();
	data2Send.append('deviceIDRequest',"");
	data2Send.append('deviceID',userID);
	data2Send.append('userName',userNameObj.value );
	xmlhttp.send(data2Send);
}


function saveUserInfo(){
	document.cookie="IBMuserInfo="+document.getElementById("userName").value+"%"+userID;
}


window.onload=loadUserInfo;

function loadUserInfo(){
	osCheck();
	//document.getElementById("userID").type="hidden";
	try{
	var allcookies=document.cookie;
	var namePos=allcookies.indexOf("IBMuserInfo=");
	if(namePos != -1){
		var start = namePos+"userName=".length;
		var end =allcookies.indexOf(";", start);
		if(end == -1){
		end=allcookies.length;
		}
		stringGet=allcookies.substring(start,end).split("%");
		if(stringGet.length ==2){
			document.getElementById("userName").value=(stringGet[0].split("="))[1];
			userID = stringGet[1];
			document.getElementById("userID").value=stringGet[1];
			return;
		}		
	}else{
		
		//alert("No device ID found, click the [Get an ID] button to get one");
		
	}
	}catch(exception){
		//alert("No device ID found, click the [Get an ID] button to get one");
	}

}

}(window));
