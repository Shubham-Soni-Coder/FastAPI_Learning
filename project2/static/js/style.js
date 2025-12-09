const emailinput =  document.getElementById("usergmail");
const passwordinput = document.getElementById("password");


// Check for valid gmail 
emailinput.addEventListener("input",()=>{
  const value = emailinput.value;
  const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  if (emailRegex.test(value)){
    emailinput.setCustomValidity("")
    console.log("Login successfull")
  }else{
    emailinput.setCustomValidity("Please enter a valid gmail address")
    console.log("Login unsuccessfull")
  }
})

