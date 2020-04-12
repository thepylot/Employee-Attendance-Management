 // Submit post on submit
 jQuery(function ($) {
    

    jQuery(document).on('submit', '#attend-form',function(e){
        e.preventDefault();
   
        jQuery.ajax({
            type:'POST',
            url:'/base/create-leave/',
            data:{
                leave_type:$('#leave_type').val(),
                leave_start_date:$('#leave_start_date').val(),
                leave_end_date:$('#leave_end_date').val(),
                leave_start_time:$('#leave_start_time').val(),
                leave_end_time:$('#leave_end_time').val(),
                leave_reason:$('#leave_reason').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
   
            },
            success:function(){
               document.getElementById("attend-form").reset();
               jQuery(function ($) {
                   $( "#submit" ).addClass( "onclic", 250, validate);
                   validate();
               
                 function validate() {
                   setTimeout(function() {
                     $( "#submit" ).removeClass( "onclic" );
                     $( "#submit" ).addClass( "validate", 450, callback );
                   }, 2250 );
                 }
                   function callback() {
                     setTimeout(function() {
                       $( "#submit" ).removeClass( "validate" );
                     }, 1250 );
                   }
                 }); 
               
               // Simulate an HTTP redirect:
               window.location.replace("/base/leaves");
               // $('#new-attend').prepend(
               //   '<td> <span class="name">' + json.leave_type + '</span> </td><td> <span class="product">' + json.leave_start_date + ' ' + '<span>-</span>' + ' ' + json.leave_end_date +'</span></td><td><span>' + json.leave_start_time + '<span>-</span>' + json.leave_end_time + '</span></td><td><span class="badge badge-waiting">Waiting</span></td><td><i class="fas fa-ellipsis-h"></i></td>') 
            },
   
            error : function(xhr,errmsg,err) {
             $( "#submit" ).removeClass( "onclic");
           jQuery('#form-error').html('<div class="alert alert-danger" role="alert">' +
           'Please provide proper information and complete all fields. </div>'); // add the error to the dom
           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
       }
        });
    });
    jQuery(document).on('submit', '#profile-form',function(e){
     e.preventDefault();
   
     jQuery.ajax({
         type:'POST',
         url:'/auth/settings/',
         data:{
             username:$('#username').val(),
             email:$('#email').val(),
             first_name:$('#first_name').val(),
             last_name:$('#last_name').val(),
             address:$('#address').val(),
             city:$('#city').val(),
             country:$('#country').val(),
             postal_code:$('#postal_code').val(),
             about:$('#about').val(),
             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
   
         },
         success:function(){
            document.getElementById("profile-form").reset();
            console.log('Sent!')
            
         },
   
         error : function(xhr,errmsg,err) {
        jQuery('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
     });
   });
   });