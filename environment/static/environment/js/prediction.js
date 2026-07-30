document.addEventListener("DOMContentLoaded", () => {

    const country = document.getElementById("country");
    const year = document.getElementById("year");

    const environmentCard = document.getElementById("environmentCard");
    const loadingBox = document.getElementById("loadingBox");
    const form = document.getElementById("predictionForm");

    if (!country || !year) return;

    async function loadEnvironmentData() {

        if (country.value === "" || year.value === "") {

            environmentCard.style.display = "none";
            return;

        }

        try {

            const response = await fetch(
                `/get-environment-data/?country=${encodeURIComponent(country.value)}&year=${encodeURIComponent(year.value)}`
            );

            const data = await response.json();

            if (data.success) {

                environmentCard.style.display = "block";

                document.getElementById("population").textContent =
                    data.population ?? "--";

                document.getElementById("gdp").textContent =
                    data.gdp ?? "--";

                document.getElementById("forest").textContent =
                    data.forest ?? "--";

                document.getElementById("renewable").textContent =
                    data.renewable ?? "--";

                document.getElementById("pm25").textContent =
                    data.pm25 ?? "--";

                document.getElementById("temperature").textContent =
                    data.temperature ?? "--";

            } else {

                environmentCard.style.display = "none";

            }

        } catch (error) {

            console.error(error);
            environmentCard.style.display = "none";

        }

    }

    country.addEventListener("change", loadEnvironmentData);
    year.addEventListener("change", loadEnvironmentData);

    form.addEventListener("submit", function () {

        if (loadingBox) {

            loadingBox.style.display = "flex";

        }

    });

});
/*=========================
SEARCH
=========================*/

const historySearch = document.getElementById("historySearch");

if(historySearch){

historySearch.addEventListener("keyup",function(){

const filter=this.value.toLowerCase();

document.querySelectorAll(".history-box tbody tr").forEach(row=>{

const country=row.cells[0]?.innerText.toLowerCase()||"";

row.style.display=country.includes(filter)?"":"none";

});

});

}

/*=========================
FILTER
=========================*/

const historyFilter=document.getElementById("historyFilter");

if(historyFilter){

historyFilter.addEventListener("change",function(){

const value=this.value;

document.querySelectorAll(".history-box tbody tr").forEach(row=>{

const badge=row.querySelector(".status-cell");

if(!badge) return;

const text=badge.innerText.toLowerCase();

if(value==="all"){

row.style.display="";

}
else if(text.includes(value)){

row.style.display="";

}
else{

row.style.display="none";

}

});

});

}

/*=========================
EXPORT CSV
=========================*/

const exportBtn=document.getElementById("exportCSV");

if(exportBtn){

exportBtn.onclick=function(){

let csv=[];

document.querySelectorAll(".history-box table tr").forEach(row=>{

let cols=row.querySelectorAll("th,td");

let data=[];

cols.forEach(col=>{

data.push(col.innerText);

});

csv.push(data.join(","));

});

let blob=new Blob([csv.join("\n")],{type:"text/csv"});

let a=document.createElement("a");

a.href=URL.createObjectURL(blob);

a.download="prediction_history.csv";

a.click();

};

}
const trendScript = document.getElementById("trend-data-labels");
const trendValuesScript = document.getElementById("trend-data-values");
const countryScript = document.getElementById("country-data-labels");
const countryValuesScript = document.getElementById("country-data-values");
const riskScript = document.getElementById("risk-data-labels");
const riskValuesScript = document.getElementById("risk-data-values");

if (trendScript && trendValuesScript && countryScript && countryValuesScript && riskScript && riskValuesScript) {
    const trendLabels = JSON.parse(trendScript.textContent);
    const trendValues = JSON.parse(trendValuesScript.textContent);
    const countryLabels = JSON.parse(countryScript.textContent);
    const countryValues = JSON.parse(countryValuesScript.textContent);
    const riskLabels = JSON.parse(riskScript.textContent);
    const riskValues = JSON.parse(riskValuesScript.textContent);

    if (document.getElementById("trendChart")) {
        new Chart(document.getElementById("trendChart"), {
            type: "line",
            data: {
                labels: trendLabels,
                datasets: [{
                    label: "Prediction",
                    data: trendValues,
                    tension: 0.3
                }]
            }
        });
    }

    if (document.getElementById("countryChart")) {
        new Chart(document.getElementById("countryChart"), {
            type: "bar",
            data: {
                labels: countryLabels,
                datasets: [{
                    label: "Prediction",
                    data: countryValues
                }]
            }
        });
    }

    if (document.getElementById("riskChart")) {
        new Chart(document.getElementById("riskChart"), {
            type: "pie",
            data: {
                labels: riskLabels,
                datasets: [{
                    data: riskValues
                }]
            }
        });
    }
}