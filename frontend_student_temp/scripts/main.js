/** 
* Searches for a parameter in the GET request query string.
* @param {string} paramName - A string featuring the GET request parameter name.
* @return {boolean} Returns false when the parameter is not found.
* @return {string} Returns the parameter's value when found.
*/
function findGETParameter(paramName) {
    let searchResult = false;
    let parameters = location.search.substr(1).split("&");
    for (let i = 0; i < parameters.length; i++) {
        let parameter = parameters[i].split("=");
        if (parameter[0] === paramName) {
            searchResult = decodeURIComponent(parameter[1]);
        }
    }
    return searchResult;
}
/** 
* Creates and renders an HTML error element to a specified element.
* @param {string} rootId - The CSS ID of the element which errors are to be rendered to.
* @param {string} msg - The error message to be displayed.
*/
function displayError(rootId, msg) {
    let root = document.getElementById(rootId);
    let errorElm = document.createElement("div")
    errorElm.classList.add("error");
    errorElm.innerHTML = msg;
    root.append(errorElm);
}
/** 
* Fetches question data from the AutoEd backend API using the specified GET question id (qid).
*/
async function fetchQuestion() {
    // Get the qid GET request value from the GET request
    let paramValue = findGETParameter("qid");
    // If qid isn't available, display error and quit
    if (!paramValue) {
        displayError("loader", "Error: No Question ID in GET request");
        return false;
    }

    // Query the API with the qid
    const response = await fetch("/api/question", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            qid: paramValue
        })
    });

    // Check how the request went and display an error/quit
    // if it didn't go well
    if (!response.ok) {
        displayError("loader", "Question Request Error: " + response.statusText);
        return false;
    }

    // TODO: Work with and render the request response data
    console.log(response);
}
