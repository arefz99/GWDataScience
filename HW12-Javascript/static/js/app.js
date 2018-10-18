// from data.js
//goodies 
var tableData = data;
var button = d3.select('#filter-btn');
var inputField = d3.select("#datetime");

window.addEventListener('load', () => {displayTable(tableData)});
button.on("click", handleClick);

function handleClick() {
    d3.event.preventDefault();
    var inputValue = inputField.property("value");

    var filteredData = tableData.filter(ufrow => ufrow.datetime === inputValue);
    displayTable(filteredData);
}

/**
 * create table 
 */
function displayTable(anyInput){
    var tbody = d3.select("tbody");
    var rowCount = 0;
    // clear the table, display anyInput
    tbody.html("");
    anyInput.forEach(function(ufrow) {
        var row = tbody.append("tr");
        // rowCount += 1;
        console.log("Added another row");
        Object.entries(ufrow).forEach(function([key, value]) {
            if (key !== 'durationMinutes'){
                var cell = row.append("td");
                cell.text(value);
            }
        });
    });


}


