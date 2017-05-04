var gulp = require('gulp');
var stylus = require('gulp-stylus');
var jeet = require('jeet');
var autoprefixer = require('autoprefixer-stylus');
var uglify = require('gulp-uglify');
var spawn = require('child_process').spawn;

gulp.task('serve:backend', function () {
	var devServerPort = process.env.PORT || 8000;
	process.env.PYTHONUNBUFFERED = 1;
	process.env.PYTHONDONTWRITEBITECODE = 1;
	spawn('python', ['manage.py', 'runserver', '0.0.0.0:' + devServerPort], {
		stdio: 'inherit'
	});
});

gulp.task('js', function(){
	gulp.src('website/static/js/**/*.js')
		.pipe(uglify())
		.pipe(gulp.dest('./build'));
});

gulp.task('styles', function() {
	gulp.src('website/static/css/styles.styl')
		.pipe(stylus({
			use: [jeet(), autoprefixer({browsers:['last 3 versions']})]
		}))
		.pipe(gulp.dest('./build'));
});

gulp.task('default', function() {
	gulp.start('serve:backend');
	gulp.watch('website/static/css/*.styl', ['styles']);
	gulp.watch('website/static/js/**/*.js', ['js']);
});