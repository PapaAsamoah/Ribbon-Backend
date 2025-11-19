var apiLink = ""; 
var loadingText = document.getElementById("loadingText");
var sentimentTable = document.getElementById("sentimentTable");
var sentimentBody = document.getElementById("sentimentBody");

function sentimentColor(value) {
    if (value > 0.05) {
        return "green-text";
    }
    if (value < -0.05) {
        return "red-text";
    }
    return "gray-text";
}

function showData(list) {
    loadingText.style.display = "none";
    sentimentTable.style.display = "table";

    for (var i = 0; i < list.length; i++) {
        var item = list[i];
        var row = document.createElement("tr");

        var colorClass = sentimentColor(item.avg_sentiment);

        row.innerHTML =
            "<td class='table-cell'>" + (i + 1) + "</td>" +
            "<td class='table-cell'>" + item.ticker + "</td>" +
            "<td class='table-cell'>" + item.mention_count + "</td>" +
            "<td class='table-cell " + colorClass + "'>" +
                item.avg_sentiment.toFixed(3) +
            "</td>";

        sentimentBody.appendChild(row);
    }
}

showData([]);