$(document).ready(function(){

    var names = []


        var namesList = $('#names-list');
        var downloadBtn = $('#downloadFile');
        var filenameInput = $('#filename');
        var generateNameTags = $('#generateNameTags');
        var downloadBtnFile = $('#downloadBtnFile');


        downloadBtnFile.attr("disabled", "disabled")
        generateNameTags.attr("disabled", "disabled");

    $('#name-tag-form').submit(function(e) {
        e.preventDefault();

         $.ajax({
           type: "POST",
           url: "/name-tag",
           contentType: "application/json",
           data: JSON.stringify({
                "names":names
           }),
           success: function(data) {
                filenameInput.val(data.filename);
                generateNameTags.val("NAME TAGS GENERATED");
                generateNameTags.attr("disabled", "disabled");
                downloadBtnFile.removeAttr("disabled");
           },
           error: function(e){
                console.log(e);
           }
        });

    });

    $( "#addName" ).click(function(e) {
        e.preventDefault();

        var name = $('#name').val();
        var position  = $('#position').val();

        var nameToAdd = {"name": name, "position":position};

        names.push(nameToAdd)
        namesList.append(`
        <div class="name-list-container">
            <p class="name-list" id=${name}>${name} - ${position} <i class="far fa-trash-alt"></i></p>

        </div>
        `);
        name = "";
        position = "";
        generateNameTags.removeAttr("disabled");


    $('.fa-trash-alt').click(function(){
        $(this).parent().remove();
        var removeMe = $(this).parent().prop('id');
        var removeIndex = names.map(function(item) { return item.name; }).indexOf(removeMe);

        // remove object
        names.splice(removeIndex, 1);
        console.log(names);
    });


    });


});

