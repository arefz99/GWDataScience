//Initialize leaflet (html canvas)
var map = L.map('map').setView([0.0, 0.0], 2);

//Let's draw the map. 
var basemap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', { maxZoom: 17, attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)' }).addTo( map );

//Let's define the points on the map
earthquakes.features.forEach(earthquake => {
    var latitude = +earthquake.geometry.coordinates[1];
    var longitude = +earthquake.geometry.coordinates[0];
    var magnitude = +earthquake.properties.mag;

    L.circle([latitude, longitude], {
        // color: "red",
        stroke: false,
        fillColor: "black",
        fillOpacity: magnitude/10,
        radius: 50000 * magnitude // in meters
    }).bindTooltip(earthquake.properties.title, {
        permenant:false
    }).addTo(map);

});

//-------------------------------------------------
// Putting the legend on the map
var legend = L.control({position: 'bottomright'});

  legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
              magnitude = [0, 2, 4, 6, 8],
              labels = [];

  // loop through our density intervals and generate a label with a colored square for each interval
    div.innerHTML +=
        'Earthquake <br> Magnitude <br>'
    for (var i = 0; i < magnitude.length; i++) {
        div.innerHTML +=
            '<span style="background: black; width: 20px; opacity:' + getOpacity(magnitude[i]) + '">&nbsp;&nbsp;&nbsp;&nbsp;</span> ' +
            magnitude[i] + (magnitude[i + 1] ? '&ndash;' + magnitude[i + 1] + '<br>' : '+');
    }
    return div;
  };

  legend.addTo(map);

// here x is the variable corresponding to the value of the magnitude. 
function getOpacity(x) {
    return  x/10;
}

function getRadius(value){
  return value*40000
}


  


