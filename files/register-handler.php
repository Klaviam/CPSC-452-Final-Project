<?php
// Takes care of inputs, text boxes and buttons, creates variables and formats inputs
function sanitizeFormPassword($inputText){
  $inputText = strip_tags($inputText);
  return $inputText;
}

function sanitizeFormUsername($inputText){
  // Doesnt allow html inputs
  $inputText = strip_tags($inputText);
  // Find this, replace with this, in username
  $inputText = str_replace(" ", "", $inputText);
  return $inputText;
}

function sanitizeFormString($inputText){
  $inputText = strip_tags($inputText);
  // Find this, replace with this, in username
  $inputText = str_replace(" ", "", $inputText);
  // Capitalize first letter
  $inputText = ucfirst(strtolower($inputText));
  return $inputText;
}

if(isset($_POST['registerButton'])){
  // Register button was pressed
  $username = sanitizeFormUsername($_POST['username']);
  $firstName = sanitizeFormString($_POST['firstName']);
  $lastName = sanitizeFormString($_POST['lastName']);
  $email = sanitizeFormString($_POST['email']);
  $email2 = sanitizeFormString($_POST['email2']);
  $password = sanitizeFormPassword($_POST['password']);
  $password2 = sanitizeFormPassword($_POST['password2']);

  // Calls register function, will return true or false to $wasSuccessful
  $wasSuccessful = $account->register($username, $firstName, $lastName, $email, $email2, $password, $password2); //call register function in Account.php file

  if($wasSuccessful == true){ //if there are no errors
    $_SESSION['userLoggedIn'] = $username;

    // Create a user database
  	$query = "create table IF NOT EXISTS " . $username . "_DB (
        id INT AUTO_INCREMENT,
        title VARCHAR(255),
        year VARCHAR(255),
        director VARCHAR(255),
        starringActor VARCHAR(255),
        PRIMARY KEY (id)
    )";
  	$result = mysqli_query($con, $query);


    header("Location: login.php");
  }
}
?>
