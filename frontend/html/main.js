const API_URL = 'http://localhost'

$(document).ready(function (e) {
    let session = $('#session_id').val()
    $.ajax({
            url: `${API_URL}/api/url?session=${session}&format=json`,
            type: "GET",
            dataType: "json",
            success: function (response) {
                var list = $('#list')
                $.each(response.urls, function (index, resp) {
                    list.append(`<li><a href="${resp.full}" target="_blank">${resp.short}</a></li>`)
                })
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });

    $(document).on('submit', '#form', function (e) {
        e.preventDefault();
        $form = $(this)
        let full_link = $form.find('#link')
        $.ajax({
            url: `${API_URL}/api/url/`,
            type: "POST",
            dataType: "json",
            data: {session:session, full: full_link.val()},
            success: function (response) {
                var list = $('#list')
                list.append(`<li><a href="${full_link.val()}" target="_blank">${response.short}</a></li>`)
                full_link.val('')
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    })

})
