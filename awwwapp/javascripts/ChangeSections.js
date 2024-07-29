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
            console.log(response);
        },
        error: function(xhr, status, error) {
            console.log(xhr);
        }
    });
});