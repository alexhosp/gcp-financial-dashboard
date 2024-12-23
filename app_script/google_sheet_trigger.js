function handleEdit(e) {
	// Ensure the event object is defined
	if (!e) {
		return
	}

	// Get the active sheet
	var sheet = e.source.getActiveSheet()

	// Check if the edited cell is in the Company Symbol cell
	if (e.range.getColumn() === 1) {
		// Retrieve the new value entered in the edited cell
		var newValue = e.value

		// Define the payload to send in the POST request
		var payload = {
			'Company Symbol': newValue,
		}

		// Construct a POST request
		const options = {
			method: 'post',
			contentType: 'application/json',
			payload: JSON.stringify(payload),
		}

		// Define cloud function URL
		url =
			'https://us-central1-financial-444917.cloudfunctions.net/fetch-alpha-vantaga-data'

		// Send the POST request to the cloud function
		try {
			const response = UrlFetchApp.fetch(url, options)
			// Get the response content as text
			const responseBody = response.getContentText()
			// Write the response to cell C1 for testing
			// sheet.getRange('C1').setValue(responseBody);
		} catch (error) {
			// Log errors that occured in the sheet
			// sheet.getRange('C1').setValue('Error: ' + error.message);
		}
	}
}
