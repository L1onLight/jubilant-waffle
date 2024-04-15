const API_URL = "http://localhost:8000/"

function getCookie(name) {
    const cookieValue = document.cookie.match(
        "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
    );
    return cookieValue ? cookieValue.pop() : "";
}

function getCSRF() {
    return getCookie("csrftoken")
}

async function fetchUrl(endpoint, data, method = "POST") {
    const url = API_URL + endpoint;
    const csrftoken = getCookie("csrftoken");

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            return responseData; // Return the parsed JSON data
        } else {
            throw new Error("Form error");
        }
    } catch (error) {
        // Handle any errors that occur during submission
        console.error(error);
        throw error; // Rethrow the error for the caller to handle if needed
    }
}


export {fetchUrl, getCSRF};