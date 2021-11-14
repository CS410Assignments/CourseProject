document.getElementById("searchButton").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  document.getElementById("queryTitle").innerHTML = document.getElementById('searchInput').value;
});
