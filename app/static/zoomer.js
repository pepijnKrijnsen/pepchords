const el = document.getElementById("song");

window.addEventListener("keydown", function(pressed) {
	var currentSize = getCurrSize(el)
	if (pressed.key === "z") {
		increaseFont(currentSize);
	} else if (pressed.key === "Z") {
		decreaseFont(currentSize);
	};
}, true);

function increaseFont(size) {
	el.style.fontSize = parseFloat(size) + (1/2) + "px";
};

function decreaseFont(size) {
	el.style.fontSize = parseFloat(size) - (1/2) + "px";
};

function getCurrSize(el) {
	let style = window.getComputedStyle(el);
	let sizeWithUnit = style.getPropertyValue("font-size");
	let size = sizeWithUnit.slice(0, -2);
	return parseFloat(size);
};
