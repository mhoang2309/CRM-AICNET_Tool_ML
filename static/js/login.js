console.clear();


const loginBtn = document.getElementById('login');
const signupBtn = document.getElementById('signup');

const submitBtnlogin = document.getElementsByClassName("login-btn")
const submitBtnsignup = document.getElementsByClassName("signup-btn")

const loginusername  = document.getElementById("form-holder-login").getElementsByClassName("input").email
const loginpassword  = document.getElementById("form-holder-login").getElementsByClassName("input").password

const signupusername  = document.getElementById("form-holder-signup").getElementsByClassName("input").email
const signuppassword  = document.getElementById("form-holder-signup").getElementsByClassName("input").password
const signupcode  = document.getElementById("form-holder-signup").getElementsByClassName("input").code

var notificationElements = document.getElementsByClassName("form-notification");
var errorElements = document.getElementsByClassName("form-error");

loginusername.addEventListener('click', (e) =>{
	for (var i = 0; i < errorElements.length; i++) {
		errorElements[i].style.display = "none";
	}
})

loginpassword.addEventListener('click', (e) =>{
	for (var i = 0; i < errorElements.length; i++) {
		errorElements[i].style.display = "none";
	}
})

signupBtn.addEventListener('click', (e) => {
	signupusername.value = ""
	signupcode.value = ""
	signuppassword.value = ""
	let parent = e.target.parentNode;
	Array.from(e.target.parentNode.classList).find((element) => {
		if(element !== "slide-up") {
			parent.classList.add('slide-up')
		}else{
			loginBtn.parentNode.parentNode.classList.add('slide-up')
			parent.classList.remove('slide-up')
		}
	});
});

loginBtn.addEventListener('click', (e) => {
	notificationElements[0].style.display = "none"
	let parent = e.target.parentNode.parentNode;
	Array.from(e.target.parentNode.parentNode.classList).find((element) => {
		if(element !== "slide-up") {
			parent.classList.add('slide-up')
		}else{
			signupBtn.parentNode.classList.add('slide-up')
			parent.classList.remove('slide-up')
		}
	});
});

submitBtnlogin[0].addEventListener('click', (e) =>{
	if (loginusername.value && loginpassword.value){
		
		var myHeaders = new Headers();
		myHeaders.append("Content-Type", "application/json");
	
		var raw = JSON.stringify({
		"username": loginusername.value,
		"password": loginpassword.value
		});
	
		var requestOptions = {
		method: 'POST',
		headers: myHeaders,
		body: raw,
		redirect: 'follow'
		};
	
		fetch("/api/login", requestOptions)
		.then(response => response.json())
		.then(result => {
			if (result["login"] == true) {
				localStorage.setItem("_authorization", result["authorization"]);
				window.location.replace("./")
			}
			else{
				for (var i = 0; i < errorElements.length; i++) {
					errorElements[i].style.display = "block";
					errorElements[i].innerHTML = "Login false";
				}
			}
		})
		.catch(error => console.log('error', error));
	}
	else{
		for (var i = 0; i < errorElements.length; i++) {
			errorElements[i].style.display = "block";
			errorElements[i].innerHTML = "Email and password not none";
		}
	}
});

submitBtnsignup[0].addEventListener('click', (e) =>{
	var myHeaders = new Headers();
	myHeaders.append("Content-Type", "application/json");

	var raw = JSON.stringify({
	"username": signupusername.value,
	"code":signupcode.value,
	"password": signuppassword.value
	});

	var requestOptions = {
	method: 'PUT',
	headers: myHeaders,
	body: raw,
	redirect: 'follow'
	};
	fetch("/api/signup", requestOptions)
	.then(response => response.json())
	.then(result => {
		if (result["signup"] == true) {
			signupusername.value = "";
			signupcode.value = "";
			signuppassword.value = "";
			for (var i = 0; i < notificationElements.length; i++) {
				notificationElements[i].style.display = "block";
				notificationElements[i].innerHTML = "Sign up for an account";
			}
			document.getElementsByClassName("form-holder")[0].style.display = "none";
			submitBtnsignup[0].style.display = "none";
		}
		else{
			for (var i = 0; i < notificationElements.length; i++) {
				notificationElements[i].style.display = "block";
				notificationElements[i].style.color = "red";
				notificationElements[i].innerHTML = "Sign up for an account false";
			}
		}
		})
	.catch(error => console.log('error', error));
	});
// document.querySelector('input[name="code"]').setAttribute('autocomplete','none');
