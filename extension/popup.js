const finalScoreEl = document.getElementById('final-score');
const dishesUlEl = document.getElementById('dish-frequency');
const reviewsUlEl = document.getElementById('sentiment-scores');

const popoverTriggerList = document.querySelectorAll(
  '[data-bs-toggle="popover"]'
);
const popoverList = [...popoverTriggerList].map(
  (popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl)
);

chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
  chrome.tabs.sendMessage(tabs[0].id, { hungryPanda: 'START' }, (res) => {
    fetchData(res.reviews);
  });
});

async function fetchData(reviews) {
  return fetch('http://127.0.0.1:5000', {
    method: 'POST',
    body: JSON.stringify(reviews),
    headers: { 'Content-Type': 'application/json' },
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      // Display final sentiment score
      finalScoreEl.innerText = Number(data['final_score']).toFixed(1);

      // Display sorted dish name + count
      const sortedFood = data['sorted_food'];
      sortedFood.forEach(([dishName, count]) => {
        const li = document.createElement('li');
        li.classList.add(
          'list-group-item',
          'd-flex',
          'justify-content-between',
          'align-items-start'
        );
        li.innerHTML = `<span>${dishName}</span><span class='badge bg-primary rounded-pill'>${count}</span>`;
        dishesUlEl.appendChild(li);
      });

      // Display review + sentiment score
      const sentimentScores = data['sentiment_scores'];
      sentimentScores.forEach(([reviewStr, sentimentScore], idx) => {
        const div = document.createElement('div');
        div.classList.add('carousel-item');
        if (idx === 0) div.classList.add('active');
        div.innerHTML = `
          <div class="card mx-5">
            <div class="card-body">
              <h5 class="card-title">Sentimental score: ${sentimentScore}</h5>
              <p class="card-text review-card fs-6">${reviewStr}</p>
            </div>
          </div>
        `;
        reviewsUlEl.appendChild(div);
      });
    })
    .catch((err) => {
      console.error(err);
    });
}
