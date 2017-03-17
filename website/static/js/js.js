document.onreadystatechange = function () {
	if(document.readyState === 'interactive') {

		var top = document.getElementById('top');
		top.addEventListener('click', function(event) {
			console.log('click');
			event.preventDefault();
			var html = document.getElementsByTagName('html')[0];
			Velocity(html, 'scroll', {offset: '0px', mobileHA: false, duration: 750});
		});


		/// Login Form ////////////////////////////////////////////////////////////////////////////////

		var nav = document.getElementsByTagName('nav')[0];
		login = nav.getElementsByClassName('login-btn')[0];
		if(login) {
			login.addEventListener('click', function(event) {
				event.preventDefault();
				toggleClass(this, 'active');
				if(hasClass(this, 'active')) {
					Velocity(document.getElementsByClassName('customer')[0], 'slideDown', { duration: 500 });
				} else {
					Velocity(document.getElementsByClassName('customer')[0], 'slideUp', { duration: 500 });
				}
			});
		}

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

		var eye = document.getElementsByClassName('eye');
		for (var i = 0; i < eye.length; i++) {
			eye[i].addEventListener('mousedown', function() {
				var target = findParent(this, 'input');
				for (var i = 0; i < target.childNodes.length; i++) {
					if (hasClass(target.childNodes[i], 'password')) {
						// Change password input type
						pwd = target.childNodes[i];
					}
				}
				pwd.setAttribute('type', 'text');
				addClass(this, 'selected');
			});

			eye[i].addEventListener('mouseup', function() {
				pwd.setAttribute('type', 'password');
				removeClass(this, 'selected');
			});
		}

		function findParent(el, cls) {
			while ((el = el.parentElement) && !el.classList.contains(cls));
			return el;
		}


		//## INDEX ##################################################################################
		var home = document.getElementById('home');
		if (home) {

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
				if (!matchesSelector(event.target, '.tablinks')) {
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


		/// Cta. Cte. Kilos ////////////////////////////////////////////////////////////////////////////////////

		var ctaCteKg = document.getElementById('ctacte');
		if(ctaCteKg && hasClass(ctaCteKg, 'kilos')) {
			var showAnalysis = ctaCteKg.getElementsByClassName('show-analysis');
			for (i = 0; i < showAnalysis.length; i++) {
				showAnalysis[i].addEventListener('click', function(event) {
					event.preventDefault();
					addClass(this.parentElement.parentElement.nextElementSibling, 'show');
					toggleClass(this, 'hide-btn');
					toggleClass(this.nextElementSibling, 'hide-btn');
				});
			}
			var hideAnalysis = ctaCteKg.getElementsByClassName('hide-analysis');
			for (i = 0; i < hideAnalysis.length; i++) {
				hideAnalysis[i].addEventListener('click', function(event) {
					event.preventDefault();
					removeClass(this.parentElement.parentElement.nextElementSibling, 'show');
					toggleClass(this, 'hide-btn');
					toggleClass(this.previousElementSibling, 'hide-btn');
				});
			}
		}


		/// Scroll FadeIn ////////////////////////////////////////////////////////////////////////////////////

		function visibleEl(element) {
			var rect = element.getBoundingClientRect();
			var totalScroll = document.documentElement.clientHeight + document.scrollingElement.scrollTop;
			return (
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