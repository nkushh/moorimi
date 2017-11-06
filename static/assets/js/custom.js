// Validation for new cattle form
function nameLengthValidation(){
	var invalid = 0;
	var name = document.getElementById("name").value;

	if(name.length > 20 ){
		document.getElementById("name-error").innerHTML = "* Cattle name shouldn't exceed 20 characters";
		invalid  = 1;
	}else{
		document.getElementById("name-error").innerHTML = "";
	}

	if(invalid != 0){
		return false;
	}else{
		return true;
	}
}

// Validation for milk sale form
function milkSoldValidation(){
	var invalid = 0;
	var sold = document.getElementById("milk_sold").value;

	if(isNaN(sold)){
		document.getElementById("milk_error").innerHTML = "* Value must be a number";
		invalid  = 1;
	}else{
		document.getElementById("milk_error").innerHTML = "";
	}

	if(invalid != 0){
		return false;
	}else{
		return true;
	}
}

function priceSoldValidation(){
	var invalid = 0;	
	var amount = document.getElementById("price").value;

	if(isNaN(amount)){
		document.getElementById("price_error").innerHTML = "* Value must be a number";
		invalid  = 1;
	}else{
		document.getElementById("price_error").innerHTML = "";
	}

	if(invalid != 0){
		return false;
	}else{
		return true;
	}
}