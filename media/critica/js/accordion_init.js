jQuery().ready(function(){
	jQuery('#subContent .articleList').accordion({
		header: 'div.button',
		autoheight: false,
		alwaysOpen: false, 
		active: '.current'
	});
});