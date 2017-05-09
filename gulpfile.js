var gulp = require('gulp');
var gutil = require('gulp-util');
var del = require('del');
var gulpif = require('gulp-if');
var argv = require('yargs').argv;
var es = require('event-stream')

var stylus = require('gulp-stylus');
var jeet = require('jeet');
var autoprefixer = require('autoprefixer-stylus');

var uglify = require('gulp-uglify');

var changed = require('gulp-changed');
var imagemin = require('gulp-imagemin');
var jpegoptim = require('imagemin-jpegoptim');
var pngquant = require('imagemin-pngquant');


// --------------------------
// VARIABLES
// --------------------------

// Routes
var source = 'website/src/';
var static = 'website/static/';

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
	return del([static]);
});

// Copy assets
gulp.task('assets', clean, function() {
	var assets = gulp.src(source + 'assets/**/*')
		.pipe(gulp.dest(static + 'assets/'));
	var taxes = gulp.src(source + 'taxes/**/*')
		.pipe(gulp.dest(static + 'taxes/'));
	var video = gulp.src(source + 'video/**/*')
		.pipe(gulp.dest(static + 'video/'));
	return es.merge(assets, taxes, video);
});

// Process Stylus and compress CSS
gulp.task('css', clean, function() {
	return gulp.src(source + 'css/styles.styl')
		.pipe(stylus({
			use: [
				jeet(),
				autoprefixer(['iOS >= 7', 'Explorer >= 9', 'Edge >= 12', 'Firefox >= 30', 'Chrome >= 40', 'Safari >= 7', 'Opera >= 40', 'OperaMini >= 22', 'ChromeAndroid >= 40', 'UCAndroid >= 10'])
			]
		}))
		.pipe(gulp.dest(static + 'css/'));
});

// Minify JS
gulp.task('js', clean, function(){
	return gulp.src(source + 'js/**/*.js')
		.pipe(gulpif(production, uglify()))
		.pipe(gulp.dest(static + 'js/'));
});

// Optimize Images
gulp.task('images', clean, function() {
	return gulp.src(source + 'img/**/*.*')
		.pipe(changed(static + 'img/'))
		.pipe(imagemin([
			imagemin.gifsicle(), 
			imagemin.svgo(),
			jpegoptim({
				progressive: true,
				max: 80
			}),
			pngquant({
				quality: 80,
				verbose: true
			})
		],
		{
			verbose: true
		}))
		.pipe(gulp.dest(static + 'img/'));
});


// --------------------------
// DEV/WATCH TASKS
// --------------------------

// WATCH task
gulp.task('watch', ['assets', 'css', 'js', 'images'], function() {
	//Watch changes in styles, js, html and images
	gulp.watch(source + 'css/*.styl', ['css']);
	gulp.watch(source + 'js/**/*.js', ['js']);
	gulp.watch(source + 'img/**/*.*', ['images']);
	gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});

// BUILD task
gulp.task('build', ['assets', 'css', 'js', 'images']);

// DEFAULT task
gulp.task('default', ['watch']);


// --------------------------
// RUN DJANGO MANAGE.PY RUNSERVER
// --------------------------

//var spawn = require('child_process').spawn;

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