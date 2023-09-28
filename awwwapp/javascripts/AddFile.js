$("#adding_file_dropbox").submit(function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    // Get the data from the form
    var name = $("input[name=name]").val();
    var description = $("input[name=description]").val();
    var file = $("#file")[0].files[0];

    // Create a FormData object
    var formData = new FormData();
    formData.append("name", name);
    formData.append("description", description);
    formData.append("file", file);

    // Make an AJAX request to the server
    $.ajax({
        type: "POST",
        url: "/add_file/",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // Handle the response from the server
            console.log(response);
            
        },
        error: function(xhr, status, error) {
            // Handle errors
        }
    });
});

