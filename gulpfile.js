var gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    rename = require('gulp-rename');
var autoprefixer = require('gulp-autoprefixer');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sass = require('gulp-sass');
var browserSync = require('browser-sync');

gulp.task('browser-sync', function() {
  browserSync({
    server: {
       baseDir: "./"
    }
  });
});

gulp.task('bs-reload', function () {
  browserSync.reload();
});

gulp.task('styles', function(){
  gulp.src(['src/styles/**/*.scss'])
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(sass())
    .pipe(autoprefixer('last 2 versions'))
    .pipe(gulp.dest('dist/styles/'))
    .pipe(browserSync.reload({stream:true}))
});

gulp.task('scripts', function(){
  return gulp.src('src/scripts/**/*.js')
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(concat('main.js'))
    .pipe(gulp.dest('dist/scripts/'))
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gulp.dest('dist/scripts/'))
    .pipe(browserSync.reload({stream:true}))
});

gulp.task('default', ['browser-sync'], function(){
  gulp.watch("src/styles/**/*.scss", ['styles']);
  gulp.watch("src/scripts/**/*.js", ['scripts']);
  gulp.watch("*.html", ['bs-reload']);
});

gulp.task('copy-semantic-ui-calendar-styles', function() {
  return gulp.src('./node_modules/semantic-ui-calendar/dist/*.min.css')
    .pipe(gulp.dest('./semantic/dist'));
});

gulp.task('copy-semantic-ui-calendar-scripts', function() {
  return gulp.src('./node_modules/semantic-ui-calendar/dist/*.min.js')
    .pipe(gulp.dest('./semantic/dist'));
});

gulp.task('copy-semantic-ui-calendar-styles-2-root', function() {
  return gulp.src('./node_modules/semantic-ui-calendar/dist/*.min.css')
    .pipe(gulp.dest('./'));
});

gulp.task('copy-semantic-ui-calendar-scripts-2-root', function() {
  return gulp.src('./node_modules/semantic-ui-calendar/dist/*.min.js')
    .pipe(gulp.dest('./'));
});

gulp.task('copy-semantic-ui-styles-2-root', function() {
  return gulp.src('./semantic/dist/semantic.min.css')
    .pipe(gulp.dest('./'));
});

gulp.task('copy-semantic-ui-scripts-2-root', function() {
  return gulp.src('./semantic/dist/semantic.min.js')
    .pipe(gulp.dest('./'));
});

gulp.task('copy-semantic-ui-calendar', [
  'copy-semantic-ui-calendar-styles',
  'copy-semantic-ui-calendar-scripts',
]);

gulp.task('copy-everything-to-root', [
  'copy-semantic-ui-styles-2-root',
  'copy-semantic-ui-scripts-2-root',
  'copy-semantic-ui-calendar-styles-2-root',
  'copy-semantic-ui-calendar-scripts-2-root',
]);

