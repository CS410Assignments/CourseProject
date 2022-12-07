let reviewSectionEl, reviewUlEl;

window.addEventListener('load', getElements);

function getElements(maxTimes = 5) {
  if (reviewSectionEl && reviewUlEl) return;

  let times = 0;
  while ((!reviewSectionEl || !reviewUlEl) && times < maxTimes) {
    reviewSectionEl = document.querySelector(
      'section[aria-label="Recommended Reviews"]'
    );
    reviewUlEl = reviewSectionEl?.querySelector('ul:not([aria-label="Rating"]');
    times++;
  }
}

function getReviews() {
  let arr = [];

  getElements();
  let list = reviewUlEl.childNodes;
  let len = reviewUlEl.childNodes.length;

  for (let i = 0; i < len; i++) {
    let info = list[i].querySelectorAll('.user-passport-info .css-1m051bw');
    let s = list[i]
      .querySelectorAll('.margin-t1__09f24__w96jn .five-stars__09f24__mBKym')[0]
      .getAttribute('aria-label')
      .split(' ')[0];
    let dateil = list[i].querySelectorAll(
      '.comment__09f24__gu0rG .raw__09f24__T4Ezm'
    )[0].textContent;
    let location = list[i].querySelectorAll(
      '.user-passport-info .responsive-hidden-small__09f24__qQFtj .css-qgunke'
    )[0].textContent;

    let obj = {
      name: info[0].textContent,
      star: s,
      text: dateil,
      location: location,
    };
    arr.push(obj);
  }

  return arr;
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.hungryPanda === 'START') {
    sendResponse({ reviews: getReviews() });
  }
});
