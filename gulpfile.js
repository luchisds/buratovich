var gulp = require('gulp');
var gutil = require('gulp-util');
var gulpif = require('gulp-if');
var spawn = require('child_process').spawn;
var argv = require('yargs').argv;

var stylus = require('gulp-stylus');
var jeet = require('jeet');
var autoprefixer = require('autoprefixer-stylus');

var uglify = require('gulp-uglify');

var htmlmin = require('gulp-htmlmin');

var changed = require('gulp-changed');
var imagemin = require('gulp-imagemin');


// --------------------------
// VARIABLES
// --------------------------

// Routes
var source = 'website/static/';
var build = 'website/build/';

// gulp build --production
var production = !!argv.production;
// determine if we're doing a build
var build = argv._.length ? argv._[0] === 'build' : false;
// for production we require the clean method on every individual task
var clean = build ? ['clean'] : [];


// --------------------------
// CUSTOMS TASKS
// --------------------------

// Clean 
gulp.task('clean', function() {
	del([build]);
});

// Copy assets
gulp.task('assets', clean, function() {
	gulp.src(source + 'assets/**/*')
		.pipe(gulp.dest(build + 'assets/'));
	gulp.src(source + 'taxes/**/*')
		.pipe(gulp.dest(build + 'taxes/'));
	gulp.src(source + 'video/**/*')
		.pipe(gulp.dest(build + 'video/'));
});

// Minify HTML
gulp.task('templates', clean, function() {
	gulp.src('website/templates/*.html')
		.pipe(htmlmin({
			collapseWhitespace: true, 
			empty: true
		}))
		.pipe(gulp.dest(build + 'templates/'));
});

// Process Stylus and compress CSS
gulp.task('css', clean, function() {
	gulp.src(source + 'css/styles.styl')
		.pipe(stylus({
			compress: production ? true : false,
			use: [jeet(), autoprefixer({browsers:['last 3 versions']})]
		}))
		.pipe(gulp.dest(build + 'css/'));
});

// Minify JS
gulp.task('js', clean, function(){
	gulp.src(source + 'js/**/*.js')
		.pipe(gulpif(production, uglify()))
		.pipe(gulp.dest(build + 'js/'));
});

// Optimize Images
gulp.task('images', clean, function() {
	gulp.src(source + 'img/**/*.*')
		.pipe(changed(build + 'img/'))
		.pipe(imagemin({
			verbose: true
		}))
		.pipe(gulp.dest(build + 'img/'));
});


// --------------------------
// DEV/WATCH TASKS
// --------------------------

// WATCH task
gulp.task('watch', ['assets', 'templates', 'css', 'js', 'images'], function() {
	//Watch changes in styles, js, html and images
	gulp.watch(source + 'css/*.styl', ['styles']);
	gulp.watch(source + 'js/**/*.js', ['js']);
	gulp.watch(source + 'img/**/*.*', ['img']);
	gulp.watch('website/templates/*.html', ['html']);
	gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});

// BUILD task
gulp.task('build', ['assets', 'templates', 'css', 'js', 'images']);

// DEFAULT task
gulp.task('default', ['watch']);




// gulp.task('default', function() {
// 	// gulp.start('serve:backend');
// });

// Start DJANGO server
// gulp.task('serve:backend', function () {
// 	var devServerPort = process.env.PORT || 8000;
// 	process.env.PYTHONUNBUFFERED = 1;
// 	process.env.PYTHONDONTWRITEBITECODE = 1;
// 	spawn('python', ['manage.py', 'runserver', '0.0.0.0:' + devServerPort], {
// 		stdio: 'inherit'
// 	});
// });