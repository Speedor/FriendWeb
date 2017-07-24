$(function () {

  $("#upload_btn").click(function () {
    
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    start: function (e) {
      
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
          $("#img_obj").attr("src",data.result.url);
          console.log(data.result.url,data.result.name);
      }else{

      }
    }

  });

});
