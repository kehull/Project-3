
var button =d3.select("#enter-btn");

button.on("click", runEnter);
function runEnter(){
d3.event.preventDefault();
var tbody=d3.select("tbody");
//loop through each element of data and add a tr for each element
tableData.forEach((info) => {
    var row =tbody.append("tr");
    //select the key value pairs in each element
    Object.entries(info).forEach(([key,value]) => {
        //add td for each key value pair
        var cell = row.append("td");
        //fill cell with dict value
        cell.text(value);
    });

});

};