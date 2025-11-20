function startSymptomChecker() {
    alert("Redirecting to Symptom Checker...");
}

function learnMore() {
    alert("Learn more about Disease Radar.");
}

function searchSymptoms() {
    const searchValue = document.getElementById("symptomSearch").value;
    console.log("Searching for symptoms:", searchValue);
}

function selectSymptom(symptom) {
    alert(`You selected: ${symptom}`);
}
