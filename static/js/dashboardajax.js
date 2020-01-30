$('.publish').click(function(e){ 
    e.preventDefault();
    var this_ = $(this)
    var story_id = this_.attr("story-id")
    var PublishUrl = this_.attr("data_href")

        $.ajax({
        url: PublishUrl,
        method: "GET",
        data: {
            "story_id":story_id,
        },

        success: function(data){
            console.log(data)
            var published_count = data.published_stories;
            var unpublished = data.unpublished_stories;
            var denied = data.denied_stories;

            $(".row_" + story_id).text("");
            $(".published_stories").text(published_count);
            $(".unpublished_stories").text(unpublished);
            $(".denied_stories").text(denied);
        }
    })
})

$('.deny').click(function(e){ 
    e.preventDefault();
    var this_ = $(this)
    var story_id = this_.attr("story-id")
    var DenyUrl = this_.attr("data_href")
    console.log(story_id)

    $.ajax({
        url: DenyUrl,
        method: "GET",
        data: {
            "story_id":story_id,
        },

        success: function(data){
            console.log(data)
            var pk = data.story_pk;
            var published_count = data.published_stories;
            var unpublished = data.unpublished_stories;
            var denied = data.denied_stories;

            $(".row_" + pk).text("");
            $(".published_stories").text(published_count);
            $(".unpublished_stories").text(unpublished);
            $(".denied_stories").text(denied);
        }
    })
})

$(document).ready(function() {
    $('.activate').click(function(e){
        e.preventDefault();
        var this_ = $(this)
        var id = this_.attr('id').split('_')[1];
        var user_primarykey = this_.attr("user_primarykey")
        var ActivateUrl = this_.attr("data_href")
        // var id = $('btn-activate').attr("id")
        // console.log(id)
        
        console.log(user_primarykey)

        $.ajax({
            url: ActivateUrl,
            method: "GET",
            data: {
                "user_primarykey":user_primarykey,
            },

            success: function(data){
                console.log(data)
                var pk = data.user_pk;
                console.log

                $(".activate_btn_" + pk).text("activated");
            }
        });
    });
});

$('.deactivate').click(function(e){ 
    e.preventDefault();
    var this_ = $(this)
    var id = this_.attr('id').split('_')[1];
    var user_primarykey = this_.attr("user_primarykey")
    var DeactivateUrl = this_.attr("data_href")

    $.ajax({
        url: DeactivateUrl,
        method: "GET",
        data: {
            "user_primarykey":user_primarykey,
        },

        success: function(data){
            console.log(data)
            var pk = data.user_pk;

            $(".deactivate_btn_" + pk).text("deactivated");
           
        }
    })
})
