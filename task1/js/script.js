/* fill the div (perview) with the content 
 */
function show_perview(name, title, text) {

    var img = document.getElementById("Image");
    img.src = "images/" + name;

    var t = document.getElementById("title");
    t.innerHTML = title;

    var s = document.getElementById("text");
    s.innerHTML = text;

    var test = document.getElementById("preview");

    test.style.display = "block";
};


function hide_perview() {
    var test = document.getElementById("preview");
    test.style.display = "none";
};