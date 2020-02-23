// Development for Node json data structure
// Implementation of hash library and development of bitchain structure
// Timestamps formatted as Unix timestamp


function A2U(str) {
    var reserved = '';

    for (var i = 0; i < str.length; i++) {
        reserved += '&#' + str.charCodeAt(i) + ';';
    }

    return reserved;
}


function U2A(str) {
	var reserved = '';
	var code = str.match(/&#(d+);/g);

	if (code === null) {
		return str;
	}

	for (var i = 0; i < code.length; i++) {
		reserved += String.fromCharCode(code[i].replace(/[&#;]/g, ''));
	}

	return reserved;
}

// Develop the Blockchain class

// incoming json object: auxData
// Starting with initial hash and timestamp/content array, compute final hash.
function computeHash(auxData){
	// first convert from utf8 to ascii
	var temparray = Utf8.decode(auxData);
	var temp = JSON.parse(temparray);
	var hash = temp.hi;
	tc = temp.vals;
	var i;
	for (i = 0; i < tc.length; i++) {
		var str = "";
		currNode = tc[i];
		str = str.concat(hash,currNode.t,currNode.c);
		// compute new hash
		var hash = new Hashes.SHA256().hex(str);
	}
	return hash;
}

console.log(A2U("doppelgänger"));
