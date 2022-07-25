var validEmailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
$(document).ready(function () {

$(".main-wrapper").on('click', '#add-magazine-btn, #edit-recipe-btn', function(e){
	e.preventDefault();
	var title, description;
	title = $("#magazine_title").val()
	description = $("#magazine_description").val()

	if(title.length < 3) {
		tata.error('Error', 'Input title must greater than 3.')
	} else if(description.length < 11) {
		tata.error('Error', 'Input description must greater than 10.')
	} else {
		var magazineData = new FormData();
		magazineData.append('title', title);
		magazineData.append('description', description)
		jQuery.ajax({
            type: "POST",
            url: '/new-magazine',
            data: magazineData,
            contentType: false,
            processData: false,
            success: function (result) {
                if (result.status === 200) {
                    window.location = '/magazine/' + result.id
                } else {
                    tata.error('Error', result.msg)
                }
            }
        });
	}
})

})