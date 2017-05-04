var gulp = require('gulp');
var stylus = require('gulp-stylus');
var jeet = require('jeet');
var autoprefixer = require('autoprefixer-stylus');
var uglify = require('gulp-uglify');
var htmlmin = require('gulp-htmlmin');
var changed = require('gulp-changed');
var imagemin = require('gulp-imagemin');
var spawn = require('child_process').spawn;

var argv = require('yargs').argv;

// Routes
var build = 'website/build';


// gulp build --production
var production = !!argv.production;


// Start DJANGO server
gulp.task('serve:backend', function () {
	var devServerPort = process.env.PORT || 8000;
	process.env.PYTHONUNBUFFERED = 1;
	process.env.PYTHONDONTWRITEBITECODE = 1;
	spawn('python', ['manage.py', 'runserver', '0.0.0.0:' + devServerPort], {
		stdio: 'inherit'
	});
});

// Minify JS
gulp.task('js', function(){
	gulp.src('website/static/js/**/*.js')
		.pipe(uglify())
		.pipe(gulp.dest(build + '/js'));
});

// Process Stylus and compress CSS
gulp.task('styles', function() {
	gulp.src('website/static/css/styles.styl')
		.pipe(stylus({
			compress: true,
			use: [jeet(), autoprefixer({browsers:['last 3 versions']})]
		}))
		.pipe(gulp.dest(build + '/css'));
});

// Minify HTML
gulp.task('html', function() {
	gulp.src('website/templates/*.html')
		.pipe(htmlmin({
			collapseWhitespace: true, 
			empty: true
		}))
		.pipe(gulp.dest(build + '/templates'));
});

// Optimize Images
gulp.task('img', function() {
	gulp.src('website/static/img/**/*.*')
		.pipe(changed('./build/img'))
		.pipe(imagemin({
			verbose: true
		}))
		.pipe(gulp.dest(build + '/img'));
});

gulp.task('default', function() {
	gulp.start('serve:backend');
	gulp.watch('website/static/css/*.styl', ['styles']);
	gulp.watch('website/static/js/**/*.js', ['js']);
	gulp.watch('website/templates/*.html', ['html']);
	gulp.watch('website/static/img/**/*.*', ['img']);
});