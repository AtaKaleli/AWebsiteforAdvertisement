function validateRegister(event){

	var username = document.forms["registrationform"]["username"].value;
	var password = document.forms["registrationform"]["password"].value;
    var fullname = document.forms["registrationform"]["fullname"].value;
	var email = document.forms["registrationform"]["email"].value;
	var telno = document.forms["registrationform"]["telno"].value;




    if(username == ""){
        displayError("Username is required!");
        return false;
    }
    else if(password == ""){
        displayError("Password is required!");
        return false;
    }
    else if(fullname == ""){
        displayError("Fullname is required!");
        return false;
    }
    else if(email == ""){
        displayError("Email is required!");
        return false;
    }
    else if(telno == ""){
        displayError("Telephone Number is required!");
        return false;
    }


	else if(countUpperCaseLetters(password) < 1){
        document.getElementById("errorLabel").innerHTML = "Error!"
        document.getElementById("passwordError").innerHTML = "The password must include at least one uppercase character!"
		return false;
	}
	else if(countLowerCaseLetters(password) < 1){
        document.getElementById("errorLabel").innerHTML = "Error!"
        document.getElementById("passwordError").innerHTML = "The password must include at least one lowercase character!"
		return false;
	}


	else if(countDigits(password) < 1){
        document.getElementById("errorLabel").innerHTML = "Error!"
        document.getElementById("passwordError").innerHTML = "The password must include at least one digit!"
		return false;
	}

	else if(countSymbols(password) < 1){
        document.getElementById("errorLabel").innerHTML = "Error!"
        document.getElementById("passwordError").innerHTML = "The password must include at least one of these symbol (+,!,*,-)!"
		return false;
	}

	else if(password.length < 10){
        document.getElementById("errorLabel").innerHTML = "Error!"
        document.getElementById("passwordError").innerHTML = "Password length must be at least 10 characters!"
		return false;
	}

	return true;
}


function countLowerCaseLetters(password) {
    var i = 0;
    var counter = 0;
    for (; i < password.length; i++) {
        if (/[a-z]/.test(password[i])) {
            counter++;
        }
    }

    return counter;
}


function countUpperCaseLetters(password) {
    var i = 0;
    var counter = 0;
    for (; i < password.length; i++) {
        if (/[A-Z]/.test(password[i])) {
            counter++;
        }
    }

    return counter;
}




function countDigits(password){
	var i = 0;
	var counter = 0;
	for(; i<password.length; i++){
		if(/[0-9]/.test(password[i]))
			counter++;
	}

	return counter;
}


function countSymbols(password) {
    var i = 0;
    var counter = 0;
    for (; i < password.length; i++) {
        if (/[+!*-]/.test(password[i])) {
            counter++;
        }
    }

    return counter;
}


function displayError(errorMessage){
document.getElementById("errorLabel").innerHTML = "Error!"
document.getElementById("passwordError").innerHTML = errorMessage

}

 document.forms["registrationform"].addEventListener("submit", function () {
        document.getElementById("usernameError").style.display = "none";
 });

function showHint(str){
        if (str.length == 0){
            document.getElementById("txtHint").innerHTML = "";
            return;
        }
        else{
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.onreadystatechange = function(){
                if(this.readyState == 4 && this.status == 200){
                    document.getElementById("txtHint").innerHTML = this.responseText;
                }
            };
            xmlhttp.open("GET","/gethint?q=" + str, true);
            xmlhttp.send();
        }
}