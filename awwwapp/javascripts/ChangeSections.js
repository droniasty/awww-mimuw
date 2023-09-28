$("#change_section_dropbox").submit(function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    var sections = $("input[name=sections]").val();

    // Make an AJAX request to the server
    $.ajax({
        type: "POST",
        url: "/change_sections/",
        data: {
            sections: sections
        },
        success: function(response) {
            // Handle the response from the server
        },
        error: function(xhr, status, error) {
            // Handle errors
        }
    });
});