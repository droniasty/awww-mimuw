$("#adding_file_dropbox").submit(function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    var name = $("input[name=name]").val();
    var description = $("input[name=description]").val();
    var file = $("#file")[0].files[0];

    var formData = new FormData();
    formData.append("name", name);
    formData.append("description", description);
    formData.append("file", file);

    $.ajax({
        type: "POST",
        url: "/add_file/",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
        },
        error: function(xhr, status, error) {
            console.log(xhr);
        }
    });
});

