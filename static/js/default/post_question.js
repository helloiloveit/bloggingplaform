
        var tag_list = [];
        var TYPING_BOX ;
        var TAG_TYPING_BOX;
        var RESULT_BOX ;
        var SAVE_TAG_LIST_BUTTON;

      function capitaliseFirstLetter(string)
        {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }


      function user_remove_tag(tag_info ){
            tag_list = jQuery.grep(tag_list, function(value) {
            return value != tag_info;
            });

      }

      function user_select_tag_handler(tag_info, suggestion_box_id){
         tag_info =  capitaliseFirstLetter(tag_info);
         $("#" + TYPING_BOX).val(tag_info);
         $("#" + suggestion_box_id).remove();

         current_tag = $("#" + RESULT_BOX).html();

         if ($.inArray(tag_info, tag_list) == -1)
        {
            tag_list[tag_list.length] = tag_info;
            var txt1 = "<span class = post-tag>" + tag_info + "<span id = delete_tag value = "+ tag_info + " class = delete-tag title = remove this tag>x</span></span>";
            $("#" + RESULT_BOX).append(txt1);
         }

         $('#tag_list').val(tag_list);
         $("#" + SAVE_TAG_LIST_BUTTON).show();


      }


      function user_select_tag_handler_new(tag_info ){
         tag_info =  capitaliseFirstLetter(tag_info);
         $("#" + TYPING_BOX).val(tag_info);

         current_tag = $("#" + RESULT_BOX).html();

         if ($.inArray(tag_info, tag_list) == -1)
        {
            tag_list[tag_list.length] = tag_info;
            var txt1 = "<span class = post-tag>" + tag_info + "<span id = delete_tag value = "+ tag_info + " class = delete-tag title = remove this tag>x</span></span>";
            $("#" + RESULT_BOX).append(txt1);
         }

         $('#tag_list').val(tag_list);
         $("#" + SAVE_TAG_LIST_BUTTON).show();


      }
