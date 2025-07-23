document.getElementById("languageSelect").addEventListener("change", () => {
    const customLanguageInput = document.getElementById("customLanguageInput");
    if (document.getElementById("languageSelect").value === "custom") {
        customLanguageInput.style.display = "block";
    } else {
        customLanguageInput.style.display = "none";
    }
});

document.getElementById("translateButton").addEventListener("click", () => {
    const text = document.getElementById("textInput").value.trim();
    const languageSelect = document.getElementById("languageSelect");
    let language = languageSelect.options[languageSelect.selectedIndex].text;
    if (language.toLowerCase() === "custom language") {
        language = document.getElementById("customLanguageInput").value.trim();
    }
    const output = document.getElementById("translatedText");
    if (text) {
        output.innerText = "Translating your text, please wait...";
        chrome.runtime.sendMessage({ action: "translateText", text }, (response) => {
            output.innerText = response.translatedText || response.error || "Sorry, translation failed. Please try again.";
        });
    } else {
        output.innerText = "Please enter some text to translate.";
    }
});

document.getElementById("copyButton").addEventListener("click", () => {
    const translatedText = document.getElementById("translatedText").innerText;
    if (translatedText && translatedText !== "Your translation will appear here...") {
        navigator.clipboard.writeText(translatedText)
            .catch(err => {
                console.error("Could not copy text: ", err);
            });
    }
});
