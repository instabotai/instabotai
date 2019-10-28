$(document).ready(
function() {
$.ajaxSetup({
cache: false
 });
var username = '{{ username }}';
setInterval(function() {
var min=1; 
var max=1000;  
var random = Math.floor(Math.random() * (+max - +min)) + +min;

    $('#show').load("{{ url_for('static', filename= username + 'info.txt')}}");
    setTimeout(function(){
    $('#show').scrollTop($('#show')[0].scrollHeight);
   
    }, 100);

                }, 7000);
            });
