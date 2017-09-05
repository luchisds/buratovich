var ie = detectIE();

document.onreadystatechange = function() {
	if(ie == 9) {
		if(document.readyState === 'complete') {
			init();
		}
	} else {
		if(document.readyState === 'interactive') {
			init();
		}
	}
}

function init() {

	// MatchesSelector 
	var docEl = document.documentElement;
	var matches = docEl.matches || docEl.webkitMatchesSelector || docEl.mozMatchesSelector || docEl.msMatchesSelector || docEl.oMatchesSelector;
	// usage matches.call(element, selector)


	/// Scroll actions ////////////////////////////////////////////////////////////////////////////////
	var body = document.body;
	var html = document.documentElement;
	var height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
	var viewporth = vh();
	var HEIGHT_FOR_TOP = 1000;

	//Create array from HTMLCollection for manipulation
	var allMods = Array.prototype.slice.call(document.getElementsByClassName('module'));
	var top = document.getElementById('top');

	window.onscroll = function() {
		// Show modules
		showModules();

		// Show top btn
		if(height > HEIGHT_FOR_TOP && height > viewporth) {
			if (visibleEl(top)) {
				if(!hasClass(top, 'top-show')) {
					addClass(top, 'top-show');
				}
			} else {
				if(hasClass(top, 'top-show')) {
					removeClass(top, 'top-show');
				}
			}
		}
	}

	// show visible Modules
	function showModules() {
		for (var i = 0; i < allMods.length; i++) {
			if (visibleEl(allMods[i])) {
				if(ie <= 9 && ie !== false) {
					Velocity(allMods[i], {opacity: 1}, 800);
				} else {
					addClass(allMods[i], 'come-in');
				}
				// delete Module when become visible
				allMods.splice(i,1);
			}
		}
	}

	// ------------- Fade In
	function visibleEl(element) {
		var rect = element.getBoundingClientRect();
		var totalScroll = document.documentElement.clientHeight + document.scrollingElement.scrollTop;
		return (
			totalScroll >= (document.scrollingElement.scrollTop + rect.top)
		);
	}

	// ------------- Go to TOP
	top.addEventListener('click', function(event) {
		event.preventDefault();
		Velocity(html, 'scroll', {offset: '0px', mobileHA: false, duration: 750});
	});

	// To make visible all modules that are visible when page load
	showModules(allMods);


	/// Login Form ////////////////////////////////////////////////////////////////////////////////

	var inputClass = document.getElementsByClassName('input');
	for (var i = 0; i < inputClass.length; i++) {
		inputClass[i].addEventListener('focusin', function() {
			addClass(this.children[0], 'focused');
			this.children[1].style.opacity = 0;
		});
	}
	for (var i = 0; i < inputClass.length; i++) {
		inputClass[i].addEventListener('focusout', function() {
			removeClass(this.children[0], 'focused');
			this.children[1].style.opacity = 1;
		});
	}

	/// Burger Nav ////////////////////////////////////////////////////////////////////////////////

	var navBurger = document.querySelectorAll('.burger .burger-btn')[0];
	var navMain = document.querySelectorAll('nav.main')[0];
	var navBurgerIcon = navBurger.querySelectorAll('i')[0];
	navBurger.addEventListener('click', function(event) {
		event.preventDefault();
		if(hasClass(navMain, 'open')) {
			Velocity(navMain, 'slideUp', {stagger: 40});
			removeClass(navBurgerIcon, 'fa-times');
			addClass(navBurgerIcon, 'fa-bars');
		} else {
			Velocity(navMain, 'transition.bounceDownIn', {stagger: 40});
			removeClass(navBurgerIcon, 'fa-bars');
			addClass(navBurgerIcon, 'fa-times');
		}
		toggleClass(navMain, 'open');
	});


	//## INDEX ##################################################################################
	var home = document.getElementById('home');
	if (home) {

		/// Carousel ////////////////////////////////////////////////////////////////////////////////
		var currentSlide = '';

		// autoplay on left-right arrow click
		var carousel = document.getElementsByClassName('carousel')[0];
		carousel.addEventListener('click', function(event) {
			enableAutoPlay(event);
		});

		// autoplay after drag slide
		flkty.on('dragEnd', function(){
			flkty.playPlayer();
		});

		flkty.on('settle', function() {
			addClass(currentSlide, 'move-in');
		});

		if(ie <= 9 && ie !== false) {
			// change btn on slide autoplay
			flkty.on('cellSelect', function() {
				if (currentSlide) {
					removeClass(currentSlide, 'move-in');
				}
				currentSlide = document.getElementsByClassName('is-selected')[0];
				var selector = currentSlide.className.split(' ')[1];
				changeCurrentBtnSlide('.'+selector);
			});
		} else {
			// change btn on slide autoplay
			flkty.on('select', function() {
				if (currentSlide) {
					removeClass(currentSlide, 'move-in');
				}
				currentSlide = document.getElementsByClassName('is-selected')[0];
				var selector = currentSlide.className.split(' ')[1];
				changeCurrentBtnSlide('.'+selector);
			});
		}

		// change slide on btn click
		var buttonGroup = document.getElementsByClassName('units')[0];
		var buttons = Array.prototype.slice.call(buttonGroup.querySelectorAll('a'));
		buttonGroup.addEventListener('click', function(event) {
			event.preventDefault();
			changeSlide(event, buttons);
		});

		function changeSlide(event, buttons) {
			if (!matches.call(event.target, '.slide')) {
				return;
			}
			selector = event.target.getAttribute('data-selector');
			var index = buttons.indexOf(event.target);
			flkty.select(index);

			changeCurrentBtnSlide(selector);
		}

		function changeCurrentBtnSlide(selector) {
			var current = document.querySelectorAll('a[data-selector="' + selector + '"]')[0];
			var currentUnitName = document.querySelectorAll('li[data-selector="' + selector + '"]')[0];
			var old = buttonGroup.getElementsByClassName('current')[0];
			var oldUnitName = document.querySelectorAll('.unit-names li.current')[0];
			if (old) {
				removeClass(old, 'current');
				removeClass(oldUnitName, 'current');
			}
			addClass(current, 'current');
			addClass(currentUnitName, 'current');
		}

		function enableAutoPlay(event) {
			if(!matches.call(event.target, 'svg') && !matches.call(event.target, 'img')) {
				return;
			}
			flkty.playPlayer();
		}


		/// Rain-Weather /////////////////////////////////////////////////////////////////////////////////////

		var tabTitle = document.getElementsByClassName('tab-title')[0];
		tabTitle.addEventListener('click', function(event){
			event.preventDefault();
			var target = findRwLinks(event.target, 'rwlinks');
			var rwcontent = document.getElementsByClassName('rwcontent');
			for (i = 0; i < rwcontent.length; i++) {
				rwcontent[i].style.display = 'none';
			}
			var rwlinks = document.getElementsByClassName('rwlinks');
			for (i = 0; i < rwlinks.length; i++) {
				rwlinks[i].className = rwlinks[i].className.replace(' active', '');
			}
			document.getElementById(target.className.split(' ')[1]).style.display = 'block';
			addClass(target, 'active');
		});

		function findRwLinks(el, cls) {
			while ((el = el.parentElement) && !el.classList.contains(cls));
			return el;
		}


		/// Weather //////////////////////////////////////////////////////////////////////////////////////////

		var tab = document.getElementsByClassName('tab')[0];
		tab.addEventListener('click', function(event){
			event.preventDefault();
			if (!matches.call(event.target, '.tablinks')) {
				return;
			}
			var tabcontent = document.getElementsByClassName('tabcontent');
			for (i = 0; i < tabcontent.length; i++) {
				tabcontent[i].style.display = 'none';
			}
			var tablinks = document.getElementsByClassName('tablinks');
			for (i = 0; i < tablinks.length; i++) {
				tablinks[i].className = tablinks[i].className.replace(' active', '');
			}
			document.getElementById(event.target.className.split(' ')[1]).style.display = 'block';
			addClass(event.target, 'active');
		});
	}

	/// CONTACT ////////////////////////////////////////////////////////////////////////////////////

	var contact = document.getElementById('contact');
	if (contact) {
		var contactButtons = document.getElementsByClassName('contact-btn');
		var contactUnits = document.getElementsByClassName('unit');
		for (i = 0; i < contactButtons.length; i++) {
			contactButtons[i].addEventListener('click', function(event) {
				event.preventDefault();
				toggleClass(document.querySelectorAll('.contact-btn.active')[0], 'active');
				toggleClass(this, 'active');
				var unitEl = document.getElementById('contact-'+event.target.className.split(' ')[1]);
				for (j = 0; j < contactUnits.length; j++) {
					if (hasClass(contactUnits[j], 'active') && contactUnits[j] != unitEl) {
						Velocity(contactUnits[j], 'slideUp', {stagger: 40});
						removeClass(contactUnits[j], 'active');
					}
				}
				if(!hasClass(unitEl, 'active')) {
					Velocity(unitEl, 'slideDown', {stagger: 40});
					addClass(unitEl, 'active');
				}
			});
		}
	}

	/// Historic Rain ////////////////////////////////////////////////////////////////////////////////////

	var historicRain = document.getElementById('historic-rain');
	if(historicRain) {
		var showDetail = historicRain.getElementsByClassName('show-detail');
		for (i = 0; i < showDetail.length; i++) {
			showDetail[i].addEventListener('click', function(event) {
				event.preventDefault();
				addClass(this.parentElement.parentElement.nextElementSibling, 'show');
				toggleClass(this, 'hide-btn');
				toggleClass(this.nextElementSibling, 'hide-btn');
			});
		}
		var hideDetail = historicRain.getElementsByClassName('hide-detail');
		for (i = 0; i < hideDetail.length; i++) {
			hideDetail[i].addEventListener('click', function(event) {
				event.preventDefault();
				removeClass(this.parentElement.parentElement.nextElementSibling, 'show');
				toggleClass(this, 'hide-btn');
				toggleClass(this.previousElementSibling, 'hide-btn');
			});
		}
	}

	/// EXTRANET Nav //////////////////////////////////////////////////////////////////////////////////////////

	var ctaCte = document.getElementById('ctacte');
	var extranet = document.getElementById('extranet');
	if(extranet || ctaCte) {
		var extranetNav = document.getElementsByClassName('extranet-nav')[0];
		var ctacteBtn = extranetNav.getElementsByClassName('ctacte-btn')[0];
		var ctacteType = extranetNav.getElementsByClassName('ctacte-type')[0];
		if(ctacteBtn) {
			ctacteBtn.addEventListener('click', function(event) {
				event.preventDefault();
				var viewportw = vw();
				if(extranet) {
					var breakPoint = 912;
				} else {
					var breakPoint = 430;
				}
				if(viewportw > breakPoint) {
					moveRow(extranetNav.querySelector('.second'));
				} else {
					moveRow(extranetNav.querySelector('.first'));
				}
				openCtaCteType(ctacteBtn, ctacteType);
			});
		}
	}

	function moveRow(el) {
		toggleClass(el, 'opened');
	}

	function openCtaCteType(btn, bar) {
		toggleClass(btn, 'opened');
		toggleClass(bar, 'opened');
	}

	/// Cta. Cte. Pesos / Cta. Cte. Kilos ////////////////////////////////////////////////////////////////////

	var ctaCteKg = document.getElementById('ctacte');
	if((ctaCte && (hasClass(ctaCte, 'pesos') || hasClass(ctaCte, 'applied'))) || (ctaCteKg && (hasClass(ctaCteKg, 'kilos') || hasClass(ctaCteKg, 'sales')))) {
		var showDetail = ctaCte.getElementsByClassName('show-detail');
		for (i = 0; i < showDetail.length; i++) {
			showDetail[i].addEventListener('click', function(event) {
				event.preventDefault();
				addClass(this.parentElement.parentElement.nextElementSibling, 'show');
				toggleClass(this, 'hide-btn');
				toggleClass(this.nextElementSibling, 'hide-btn');
			});
		}
		var hideDetail = ctaCte.getElementsByClassName('hide-detail');
		for (i = 0; i < hideDetail.length; i++) {
			hideDetail[i].addEventListener('click', function(event) {
				event.preventDefault();
				removeClass(this.parentElement.parentElement.nextElementSibling, 'show');
				toggleClass(this, 'hide-btn');
				toggleClass(this.previousElementSibling, 'hide-btn');
			});
		}
	}


	/// CLASSES Functions ////////////////////////////////////////////////////////////////////////////////

	function hasClass(elem, className) {
		return new RegExp(' ' + className + ' ').test(' ' + elem.className + ' ');
	}

	function addClass(elem, className) {
		if (!hasClass(elem, className)) {
			elem.className += ' ' + className;
		}
	}

	function removeClass(elem, className) {
		var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ') + ' ';
		if (hasClass(elem, className)) {
			while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
				newClass = newClass.replace(' ' + className + ' ', ' ');
			}
			elem.className = newClass.replace(/^\s+|\s+$/g, '');
		}
	}

	function toggleClass(elem, className) {
		var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ' ) + ' ';
		if (hasClass(elem, className)) {
			while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
				newClass = newClass.replace( ' ' + className + ' ' , ' ' );
			}
			elem.className = newClass.replace(/^\s+|\s+$/g, '');
		} else {
			elem.className += ' ' + className;
		}
	}

	// VIEWPORT Functions /////////////////////////////////////////////////////////////////////////////////

	function vh() {
		return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
	}

	function vw() {
		return Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
	}
}