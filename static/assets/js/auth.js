var validEmailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
$(document).ready(function () {

$("#signup-btn").on('click', function(e){
	e.preventDefault();
	var first_name, last_name, email, password, cpassword, term_condition;
	first_name = $("#first_name").val()
	last_name = $("#last_name").val()
	email = $("#email").val()
	password = $("#password").val()
	cpassword = $("#cpassword").val()
	term_condition = $("#term_condition").get(0).checked

	if((first_name == '') || (last_name == '') || (email == '') || (password == '') || (cpassword == '')) {
		tata.error('Error', 'Input fields correctly.')
	} else if(first_name < 3) {
        tata.error('Error', 'Use 3 characters or more for your first name.')
    } else if(last_name < 3) {
        tata.error('Error', 'Use 3 characters or more for your last name.')
    } else if(!email.match(validEmailRegex)) {
		tata.error('Error', 'Email is not valid.')
	} else if(password.length < 8) {
		tata.error('Error', 'Use 8 characters or more for your password.')
	} else if(password != cpassword) {
		tata.error('Error', 'Passwords do not match.')
	} else if(!term_condition) {
		tata.error('Error', 'Please select terms and condition.')
	} else {
		jQuery.ajax({
            type: "POST",
            url: '/register',
            data: {
                csrfmiddlewaretoken: csrf_token,
                email: email,
                password: password,
                cpassword: cpassword,
                f_name: first_name,
                l_name: last_name,
            },
            dataType: 'json',
            async: false,
            success: function (result) {
                if (result.status === 200) {
                    setTimeout(() => {
                        window.location = '/login'
                    }, 5000)
                } else {
                    tata.error('Error', result.msg)
                }
            }
        });
	}
})

$("#signin-btn").on('click', function(e){
	e.preventDefault();
	var email, password;
	email = $("#email").val()
	password = $("#password").val()
	if((email == '') || (password == '')) {
		tata.error('Error', 'Input fields correctly.')
	} else if(!email.match(validEmailRegex)) {
		tata.error('Error', 'Email is not valid.')
	} else if(password.length < 8) {
		tata.error('Error', 'Use 8 characters or more for your password.')
	} else {
		jQuery.ajax({
            type: "POST",
            url: '/login',
            data: {
                csrfmiddlewaretoken: csrf_token,
                email: email,
                password: password
            },
            dataType: 'json',
            async: false,
            success: function (result) {
                if (result.status === 200) {
                    window.location = '/'
                } else {
                    tata.error('Error', result.msg)
                }
            }
        });
	}
})

$("#update-account-btn").on('click', function(e){
    e.preventDefault();
	var first_name, last_name, email;
	first_name = $("#first_name").val()
	last_name = $("#last_name").val()
	email = $("#email").val()

	if((first_name == '') || (last_name == '') || (email == '')) {
		tata.error('Error', 'Input fields correctly.')
	} else if(first_name < 3) {
        tata.error('Error', 'Use 3 characters or more for your first name.')
    } else if(last_name < 3) {
        tata.error('Error', 'Use 3 characters or more for your last name.')
    } else if(!email.match(validEmailRegex)) {
		tata.error('Error', 'Email is not valid.')
	}  else {
		jQuery.ajax({
            type: "POST",
            url: '/account',
            data: {
                email: email,
                f_name: first_name,
                l_name: last_name,
            },
            dataType: 'json',
            async: false,
            success: function (result) {
                if (result.status === 200) {
                    tata.success('Success', result.msg)
                } else {
                    tata.error('Error', result.msg)
                }
            }
        });
	}
})

$(".del-magazine").on('click', function(e){
    var magazine_id = $(this).attr('data-id');
    jQuery.ajax({
        type: "DELETE",
        url: `/magazine/${magazine_id}`,
        data: {
        },
        dataType: 'json',
        async: false,
        success: function (result) {
            if (result.status === 200) {
                tata.success('Success', result.msg)
                $(`button[data-id=${magazine_id}]`).parent().remove();
            } else {
                tata.error('Error', result.msg)
            }
        }
    });
})

})