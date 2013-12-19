function get_elements(url, format, sdata, selector, attr, attr_value, prefix) {
  $.post(url, sdata, function(data) {
       $(selector).html("");
       $.each(data, function(i, item) {
         var property = item[attr];
         var value = item[attr_value];
         var abs_url = sprintf(format, value);
         var element = "<a id='" + prefix + "element-" + i + "' href='" + abs_url + "'>" + property + "</a>";
         var remove_button = "<button id='" + prefix + "element-remove-" + i + "' class='btn btn-sm btn-danger remove-button' type='button' value='" + value + "'>Remove</button>";
         var element_field = remove_button + "<span name='element-field' class='element-field'>" + element + "</a></span>";
         $(selector).append("<div class='input-large removable'>" + element_field + "</div>");
      });
  });
}


function add_element(url, sdata, error_selector) {
  $.post(url, sdata, function(data){
    initialize_elements();
    clear_errors(error_selector);
    if (!data.success) {
      $(error_selector).html(data.message);
    }
  });
}


function remove_element(url, sdata, error_selector) {
  $.post(url, sdata, function(data){
    initialize_elements();
    clear_errors(error_selector);
    if (!data.success) {
      $(error_selector).html(data.message);
    }
  });
}


function clear_errors(error_selector) {
  $(error_selector).html("");
}
