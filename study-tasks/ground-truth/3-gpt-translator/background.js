// Listen for translation requests from the popup
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
    if (request.action === "translateText") {
        fetch(chrome.runtime.getURL('config.json'))
            .then(response => response.json())
            .then(config => {
                const API_KEY = config.OPENAI_API_KEY;
                return fetch("https://api.openai.com/v1/chat/completions", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${API_KEY}`
                    },
                    body: JSON.stringify({
                        model: "gpt-4",
                        messages: [
                            { role: "system", content: `Translate the following text into ${request.language}:` },
                            { role: "user", content: request.text }
                        ],
                        response_format: { type: "text" },
                        temperature: 0.7
                    })
                });
            })
            .then(response => response.json())
            .then(data => sendResponse({ translatedText: data.choices[0].message.content }))
            .catch(error => {
                console.error("Error fetching translation:", error);
                sendResponse({ error: "Translation failed." });
            });
        return true; // Keep the message channel open for async response
    }
});
