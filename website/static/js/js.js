document.onreadystatechange = function () {
	if(document.readyState === 'interactive') {

		/// Login Form ////////////////////////////////////////////////////////////////////////////////

		var nav = document.getElementsByTagName('nav')[0];
		login = nav.getElementsByClassName('login')[0];
		login.addEventListener('click', function(event) {
			event.preventDefault();
			toggleClass(this, 'active');
			if(hasClass(this, 'active')) {
				Velocity(document.getElementsByClassName('customer')[0], 'slideDown', { duration: 500 });
			} else {
				Velocity(document.getElementsByClassName('customer')[0], 'slideUp', { duration: 500 });
			}
		});

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

		/// Carousel ////////////////////////////////////////////////////////////////////////////////

		var currentSlide = '';

		flkty.on('settle', function() {
			addClass(currentSlide, 'move-in');
		});

		// autoplay on left-right arrow click
		var carousel = document.getElementsByClassName('carousel')[0];
		carousel.addEventListener('click', function(event) {
			enableAutoPlay(event);
		});

		// autoplay after drag slide
		flkty.on('dragEnd', function(){
			flkty.playPlayer();
		});

		// change btn on slide autoplay
		flkty.on('select', function() {
			if (currentSlide) {
				removeClass(currentSlide, 'move-in');
			}
			currentSlide = document.getElementsByClassName('is-selected')[0];
			var selector = currentSlide.className.split(' ')[1];
			changeCurrentBtnSlide('.'+selector);
		});

		// change slide on btn click
		var buttonGroup = document.getElementsByClassName('units')[0];
		buttonGroup.addEventListener('click', function(event) {
			event.preventDefault();
			changeSlide(event);
		});

		function changeSlide(event) {
			// filter for button clicks
			if (!matchesSelector(event.target, '.slide')) {
				return;
			}
			var selector = event.target.getAttribute('data-selector');
			flkty.selectCell(selector);

			changeCurrentBtnSlide(selector);
		}

		function changeCurrentBtnSlide(selector) {
			var current = document.querySelectorAll('[data-selector="' + selector + '"]')[0];
			var old = buttonGroup.getElementsByClassName('current')[0];
			if (old) {
				removeClass(old, 'current');
			}
			addClass(current, 'current');
		}

		function enableAutoPlay(event) {
			if(!matchesSelector(event.target, 'svg') && !matchesSelector(event.target, 'img')) {
				return;
			}
			flkty.playPlayer();
		}


		/// Weather //////////////////////////////////////////////////////////////////////////////////////////

		var tab = document.getElementsByClassName('tab')[0];
		tab.addEventListener('click', function(event){
			event.preventDefault();
			if (!matchesSelector(event.target, '.tablinks')) {
				return;
			}
			var tabcontent = document.getElementsByClassName("tabcontent");
			//console.log(tabcontent);
			for (i = 0; i < tabcontent.length; i++) {
				tabcontent[i].style.display = "none";
			}
			var tablinks = document.getElementsByClassName("tablinks");
			for (i = 0; i < tablinks.length; i++) {
				tablinks[i].className = tablinks[i].className.replace(' active', '');
			}
			document.getElementById(event.target.className.split(' ')[1]).style.display = 'block';
			addClass(event.target, 'active');
		});


		/// Scroll FadeIn ////////////////////////////////////////////////////////////////////////////////////

		function visibleEl(element) {
			var rect = element.getBoundingClientRect();
			console.log(rect);
			var totalScroll = document.documentElement.clientHeight + document.scrollingElement.scrollTop;
			console.log(document.scrollingElement.scrollTop + rect.top);
			console.log(totalScroll);
			return (
				//rect.top >= 0 &&
				//rect.left >= 0 &&
				totalScroll >= (document.scrollingElement.scrollTop + rect.top)
			);
		}

		var allMods = document.getElementsByClassName('module');
		for (var i = 0; i < allMods.length; i++) {
			if (visibleEl(allMods[i])) {
				addClass(allMods[i], 'come-in');
				// addClass(allMods[i], 'already-visible');
			}
		}

		window.onscroll = function() {
			var el = document.getElementsByClassName('module');
			for (var i = 0; i < el.length; i++) {
				if (visibleEl(el[i])) {
					addClass(el[i], 'come-in');
					// addClass(el[i], 'already-visible');
				}
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
	}
}