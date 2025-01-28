// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on("Inn Floor Plan", {
  refresh: function (frm) {
    var wrapper = frm.get_field("html").$wrapper;

    var head =
      "" +
      '<head>\
				<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">\
				<style>\
					#navbar-floor-plan {\
						width: 130px;\
					}\
					#dropdown-floor-plan #dropbtn-floor-plan {\
						border-style: solid;\
  						border-width: 1px;\
						padding: 5px 15px;\
						background-color: inherit;\
					}\
					#navbar-floor-plan a:hover, #dropdown-floor-plan:hover #dropbtn-floor-plan {\
						background-color: #ffa00a;\
					}\
					.dropdown-content {\
						display: none;\
						width: 130px;\
						box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\
						overflow: scroll;\
						max-height: 160px;\
						position: absolute;\
						background-color: white;\
						z-index: 1;\
					}\
					.dropdown-content a {\
						padding: 5px 10px;\
						text-decoration: none;\
						display: block;\
					}\
					#dropdown-floor-plan:hover .dropdown-content {\
						display: block;\
					}\
				</style>\
			</head>';

    var body =
      "" +
      '<body>\
				<div class="navbar" id="navbar-floor-plan">\
					<div class="dropdown" id="dropdown-floor-plan">\
						<button class="dropbtn" id="dropbtn-floor-plan">Choose Floor\
							<i class="fa fa-caret-down"></i>\
						</button>\
						<div class="dropdown-content" id="dropdown-content-floor-plan"></div>\
					</div>\
				</div>\
				<div class="col-xs-12 col-md-8" id="floor-plan-content"></div>\
			</body>';

    var script =
      "" +
      `<script>
			function changeFloor(id) {
					// Hide all SVG elements
					var allSVGs = document.getElementsByTagName("svg");
					for (var i = 0; i < allSVGs.length; i++) {
						allSVGs[i].style.display = "none";
					}
					
					// Show the selected SVG element
					console.log(document.getElementById(id));
					var selectedSVG = document.getElementById(id);
					if (selectedSVG) {
						selectedSVG.style.display = "block";
						} else {
							console.error("SVG element with ID '" + id + "' not found.");
					}

					// Show the information element (if it exists)
					var infoElement = document.getElementById("information");
					if (infoElement) {
						infoElement.style.display = "block";
					} else {
						console.error("Element with ID 'information' not found.");
					}
				}
			</script>`;

    // function changeFloor(id) {
    // 	console.log(id);
    // 	var all = document.getElementsByTagName("svg");
    // 	console.log(all);
    // 	for (var i = 0; i < all.length; i++) {
    // 		all[i].style.display = "none";
    // 	}
    // 	console.log(all);
    // 	document.getElementById(id).style.display = "block";
    // 	document.getElementById("information").style.display = "block";
    // }
    wrapper.html(head + body + script);

    var svg = "";

    var floor_files = [];
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", "/files/floor_files.json", false);
    rawFile.onreadystatechange = function () {
      console.log(rawFile, rawFile.responseText);
      if (rawFile.readyState === 4) {
        if (rawFile.status === 200 || rawFile.status == 0) {
          floor_files = JSON.parse(rawFile.responseText);
        }
      }
    };
    rawFile.send();

    floor_files.forEach((element) => {
      console.log(element, "here");
      var z = document.createElement("a");
      console.log(element);
      z.setAttribute("onclick", 'changeFloor("' + element.id + '")');
      var t = document.createTextNode(element.name);
      z.appendChild(t);
      document.getElementById("dropdown-content-floor-plan").appendChild(z);

      rawFile.open("GET", "/files/" + element.file, false);
      rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
          if (rawFile.status === 200 || rawFile.status == 0) {
            svg = svg + rawFile.responseText;
            console.log(svg);
          }
        }
      };
      rawFile.send();
    });

    var div = document.getElementById("floor-plan-content");
    div.insertAdjacentHTML("afterbegin", svg);

    var all = document.getElementsByTagName("svg");
    for (var i = 0; i < all.length; i++) {
      all[i].style.display = "none";
    }

    frappe.call({
      method:
        "inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_all_room_with_room_booking_status",
      callback: (resp) => {
        console.log(resp);
        resp.message.forEach((element) => {
          if (element.status == "AV") {
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#33a02c;");
          } else if (element.status == "RS") {
            console.log(
              document.getElementById("room-" + element.name),
              element.name
            );
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#1f78b4;");
          } else if (element.status == "RC") {
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#a6cee3;");
          } else if (element.status == "OU") {
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#ff7f00;");
          } else if (element.status == "HU") {
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#fdbf6f;");
          } else if (element.status == "OO") {
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#e31a1c;");
          } else if (element.status == "UC") {
            document
              .getElementById("room-" + element.name)
              .setAttribute("style", "fill:#fb9a99;");
          }
        });
      },
    });

    var information =
      "" +
      '<divc class="col-xs-12 col-md-4">\
				<p><b>Information</b></p>\
				<svg id="information" width="250" height="350">\
					<rect x="0" y="0" width="50" height="25" fill="#33a02c" stroke="black" />\
					<text x="60" y="15" fill="black">AV (Available)</text>\
					<rect x="0" y="50" width="50" height="25" fill="#1f78b4" stroke="black" />\
					<text x="60" y="65" fill="black">RS (Room Sold)</text>\
					<rect x="0" y="100" width="50" height="25" fill="#a6cee3" stroke="black" />\
					<text x="60" y="115" fill="black">RC (Room Compliment)</text>\
					<rect x="0" y="150" width="50" height="25" fill="#ff7f00" stroke="black" />\
					<text x="60" y="165" fill="black">OU (Office Use)</text>\
					<rect x="0" y="200" width="50" height="25" fill="#fdbf6f" stroke="black" />\
					<text x="60" y="215" fill="black">HU (House Use)</text>\
					<rect x="0" y="250" width="50" height="25" fill="#e31a1c" stroke="black" />\
					<text x="60" y="265" fill="black">OO (Out of Order)</text>\
					<rect x="0" y="300" width="50" height="25" fill="#fb9a99" stroke="black" />\
					<text x="60" y="315" fill="black">UC (Under Construction)</text>\
				</svg>\
			</div>';

    wrapper.html(wrapper.html() + information);
  },
});
