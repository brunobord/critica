// shows the slickbox DIV on clicking the link with an ID of "slick-show"
$('a.slick-show').click(
function() {
	$('.slickbox').slideDown('slow');
	$('a.slick-show').hide('');
	return false;
});
function my_kwicks(){
    $('.kwicks').kwicks({
		duration: 300,   
        max: 113,  
        spacing:  0  
    });
}  

$(document).ready(function() {
	// hides the slickbox as soon as the DOM is ready
	// (a little sooner than page load)
	$('.slickbox').hide();
	// shows the slickbox on clicking the noted link 
	$('p.slick-show a').click(function() {
		$('.slickbox').slideDown('slow');
		$('p.slick-show').css("display","none");
		 return false;
	});
	// hides the slickbox on clicking the noted link 
	$('p.slick-hide a').click(function() {
		$('.slickbox').slideUp('slow');
		$('p.slick-show').css("display","block");
		return false;
	 });
	$('a.slick-toggle').click(function() {
		$('.slickbox').toggle(400);
		return false;
	 });
});


$(document).ready(function(){					
	my_kwicks();
});

// Fancy Zoom initialisation
$(document).ready(function() { 
	$("div.illustration a").fancybox({'hideOnContentClick': true });
	
}); 





