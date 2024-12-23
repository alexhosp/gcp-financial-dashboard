function handleEdit(e) {
    // Ensure the event object is defined
    if (!e) {
        return;
    }

    // Get the active sheet
    var sheet = e.source.getActiveSheet();

    // Check if the edited cell is in the Company Symbol column
    if (e.range.getColumn() === 1) {
        // Retrieve the new value entered in the edited cell
        var newValue = e.value;

        // Define the payload to send in the POST request
        var payload = {
            'Company Symbol': newValue,
        };

        // Construct a POST request
        const options = {
            method: 'post',
            contentType: 'application/json',
            payload: JSON.stringify(payload),
        };

        // Define the Cloud Function URL (replace with your deployed function's URL)
        const url = 'https://your-region-your-project-id.cloudfunctions.net/your-function-name';

        // Send the POST request to the Cloud Function
        try {
            const response = UrlFetchApp.fetch(url, options);
            // Optional: Get the response content as text for testing/debugging
            // const responseBody = response.getContentText();
            // sheet.getRange('C1').setValue(responseBody); // Example of writing response to the sheet
        } catch (error) {
            // Log errors that occurred in the sheet (optional for debugging)
            // sheet.getRange('C1').setValue('Error: ' + error.message);
        }
    }
}
