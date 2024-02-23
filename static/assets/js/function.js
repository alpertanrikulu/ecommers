console.log("Working Fine!!!!!!!!");

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("Comment saved to DB")

            if(response.bool == true){
                $("#review-res").html("Review added successfully.")
            }
        }
    })
})