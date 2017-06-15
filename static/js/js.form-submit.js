function jsFormSubmit (formID, oAction) {
    var oForm = document.getElementById(formID);
    var oAction = (typeof oAction !== 'undefined') ? oAction: oForm.action;
    if (!oAction) {
        alert("Action not found.");
        return false; 
    }
    // Setup callback functions
    var oReq = new XMLHttpRequest();
    oReq.onload = function() { 
        jsFormSubmitDone(oForm, this.responseText); 
    };
    if (oForm.getAttribute('data-onprogress')) {
        oReq.upload.onprogress = function(oEvent) {
            window[oForm.getAttribute('data-onprogress')](oEvent);
        };
    }
    // Send the POST request
    if (oForm.method.toUpperCase() === "POST") {
        oReq.open("POST", oAction);
        oReq.send(new FormData(oForm));
    } else {
        alert("Form method is not POST.");
    }
    return false;
}

function jsFormSubmitDone (oForm, responseText) {
    var response;
    try {
        response = JSON.parse(responseText);
        if (response.success) {
            if (oForm.getAttribute('data-onsuccess')) {
                window[oForm.getAttribute('data-onsuccess')](response);
            }
            return;
        }
    } catch (error) {
        alert("An error occured: " + error);
        console.log(error);
        console.log(responseText);
    }
    if (oForm.getAttribute('data-onerror')) {
        window[oForm.getAttribute('data-onerror')](response);
    }
    return;
}