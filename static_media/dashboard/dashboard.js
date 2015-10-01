
var AJAX_OK = 'OK'


$(document).ready(function(){
    $('.load-section').on('click', function(){
        var $this = $(this);
        var url = $this.attr('ajax');
        var target = $this.attr('target');

        var xhr = $.ajax({
                url: url,
                type: 'POST',
                dataType: 'json',
                this_this: $this,
                success: function(response) {
                    var text = this.text;
                    this.this_this.html(text);

                    if (response['status'] == AJAX_OK) {
                            var target_attr = 'target';
                            var target_id = $this.attr(target_attr);
                            var target = $('#'+target_id);

                            target.html(response['response']);
                    }
                },
                statusCode: {
                    404: function() {
                        alert("There was some error in accessing the resource, re-loading the page.");
                    },
                    403: function() {
                        alert("There was some error in accessing the resource, re-loading the page.");
                    }
                }
        });
    });
});
