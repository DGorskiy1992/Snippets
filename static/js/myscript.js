window.onload = function(){
var revers = document.getElementById('reverse_button');
function reversed(){
//    var snippets = document.getElementsByClassName('snip_info');


var table = document.getElementById('tbody');
var rows = table.childNodes;
alert(rows);
for (var i=rows.length-1; i>=0; i--){
    table.appendChild(rows[i]);
}




}
revers.onclick = reversed;
}


