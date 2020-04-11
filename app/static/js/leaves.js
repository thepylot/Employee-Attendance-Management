$.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;


	

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	

	// var chartsheight = $('.flotRealtime2').height();
	// $('.traffic-chart').css('height', chartsheight-122);


	// Counter Number
	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


	 
	 
	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();   		 
		if (windowWidth<1010) { 
			$('body').removeClass('open'); 
			if (windowWidth<760){ 
				$('#left-panel').slideToggle(); 
			} else {
				$('#left-panel').toggleClass('open-menu');  
			} 
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');  
		} 
			 
	}); 

	 
	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>'); 
		});
	});


	// Load Resize 
	$(window).on("load resize", function(event) { 
		var windowWidth = $(window).width();  		 
		if (windowWidth<1010) {
			$('body').addClass('small-device'); 
		} else {
			$('body').removeClass('small-device');  
		} 
		
	});
  
 
});

//DATETIMEPICKER
jQuery(function ($) {
    $('[id="datetimepicker3"]').datetimepicker({
        format: 'LT',
        icons: {
                    time: "fa fa-clock-o",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }
            });
            $('[id="datetimepicker10"]').datetimepicker({
                viewMode: 'days',
                format: 'YYYY-MM-DD',
                icons: {
                    time: "fa fa-clock-o",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }
            });     


});
jQuery(function ($) {
$('.badge').each(function () {
    if ($(this).text() == 'approved') {
        $(this).removeClass('badge-waiting');
        $(this).addClass('badge-complete');
      
    }
    if ($(this).text() == 'declined') {
        $(this).removeClass('badge-waiting');
        $(this).addClass('badge-pending');
      
    }
});
}); 

//DATETIMEPICKER END

//SUMBIT BUTTON

jQuery(function ($) {
	$( "#submit" ).click(function() {
	  $( "#submit" ).addClass( "onclic", 250, validate);
	});
  
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
	//SUBMIT BUTTON END