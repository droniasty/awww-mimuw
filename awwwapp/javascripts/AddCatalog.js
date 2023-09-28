$("#adding_catalog_dropbox").submit(function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    // Get the data from the form
    var name = $("input[name=name]").val();
    var description = $("input[name=description]").val();
    
    // Make an AJAX request to the server
    $.ajax({
        type: "POST",
        url: "/add_catalog/",
        data: {
            name: name,
            description: description
        },
        success: function(response) {
            // Handle the response from the server
            console.log(response);
        },
        error: function(xhr, status, error) {
            // Handle errors
        }
    });
});