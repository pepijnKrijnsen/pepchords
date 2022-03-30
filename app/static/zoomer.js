const el = document.getElementById("song");
var change = 0;

window.addEventListener("keydown", function(pressed) {
	if (pressed.key === "z") {
		var currentSize = getCurrSize(el);
		increaseFont(currentSize);
	} else if (pressed.key === "Z") {
		var currentSize = getCurrSize(el);
		decreaseFont(currentSize);
	};
}, true);

function increaseFont(size) {
	el.style.fontSize = size + (1/2) + "px";
	change++
};

function decreaseFont(size) {
	el.style.fontSize = size - (1/2) + "px";
	change--
};

function getCurrSize(el) {
	let style = window.getComputedStyle(el);
	let sizeWithUnit = style.getPropertyValue("font-size");
	let size = sizeWithUnit.slice(0, -2);
	return parseFloat(size);
};

function checkForFontChange() {
    if (change != 0) {
        var anchor = document.getElementById("to_songlist");
        var current_href = anchor.getAttribute("href");
        anchor.setAttribute("href", current_href + "?fontchange=" + change);
    }
};
