const emailinput =  document.getElementById("usergmail");
const passwordinput = document.getElementById("userpassword");

// Check for valid gmail 
emailinput.addEventListener("input",()=>{
  const value = emailinput.value;
  const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  if (emailRegex.test(value)){
    emailinput.setCustomValidity("")
  }else{
    emailinput.setCustomValidity("Please enter a valid gmail address")
  }
})

// Check for valid password
passwordinput.addEventListener("input",()=>{
  const value = passwordinput.value;
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
  if (passwordRegex.test(value)){
    passwordinput.setCustomValidity("")
  }else{
    passwordinput.setCustomValidity("Please enter a valid password")
  }
})