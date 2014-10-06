
        var tag_list = [];
        var TYPING_BOX ;
        var RESULT_BOX ;
        var SAVE_TAG_LIST_BUTTON;

         // set vietnamese text for input






      function user_remove_tag(tag_info ){
            tag_list = jQuery.grep(tag_list, function(value) {
            return value != tag_info;
            });
      }

      function user_select_tag_handler(tag_info, suggestion_box_id){
         $("#" + TYPING_BOX).val(tag_info);
         alert(suggestion_box_id);
         $("#" + suggestion_box_id).remove();

         current_tag = $("#" + RESULT_BOX).html();
         //$('#target').html(current_tag+' ' + tag_info);
         //alert(tag_info + tag_list);

         if ($.inArray(tag_info, tag_list) == -1)
        {
            tag_list[tag_list.length] = tag_info;
            var txt1 = "<span class = post-tag>" + tag_info + "<span id = delete_tag value = "+ tag_info + " class = delete-tag title = remove this tag>x</span></span>";
            $("#" + RESULT_BOX).append(txt1);
         }

         $('#tag_list').val(tag_list);
         $("#" + SAVE_TAG_LIST_BUTTON).show();


      }
